# File: cofensevision_on_poll.py
#
# Copyright (c) 2023-2026 Cofense
#
# This unpublished material is proprietary to Cofense.
# All rights reserved. The methods and
# techniques described herein are considered trade secrets
# and/or confidential. Reproduction or distribution, in whole
# or in part, is forbidden except by express written permission
# of Cofense.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions
# and limitations under the License.

from datetime import datetime, timedelta, timezone

import phantom.app as phantom

import cofensevision_consts as consts
from actions import BaseAction


class OnPollAction(BaseAction):
    """Class to handle the on poll action.

    Every AI cluster returned by the '/api/v6/aiClusters' endpoint is ingested as a container and
    every email of that cluster is ingested as an artifact of the respective container.
    """

    def _discard_state_entry(self, key):
        """Drop a state entry that can no longer be used, so that the poll falls back to the start time.

        A corrupt entry would otherwise fail every following cycle the same way and stop the
        ingestion until the state file is deleted by hand.

        :param key: state key to drop
        """
        self._connector.debug_print(f"Discarding the unusable '{key}' state entry: {self._connector.state.get(key)!r}")
        self._connector.state.pop(key, None)
        self._connector.is_state_updated = True

    def _get_window(self):
        """Determine the polling window.

        :return: phantom.APP_SUCCESS/phantom.APP_ERROR, start date and end date
        """
        lag = self._connector.config.get(consts.VISION_CONFIG_INGESTION_LAG, consts.VISION_ON_POLL_DEFAULT_INGESTION_LAG)
        ret_val, lag = self._connector.util.validate_integer(self._action_result, lag, consts.VISION_CONFIG_INGESTION_LAG, allow_zero=True)
        if phantom.is_fail(ret_val):
            return self._action_result.get_status(), None, None

        now = datetime.now(timezone.utc).replace(tzinfo=None)
        end_time = self._connector.util.format_datetime(now - timedelta(minutes=lag))

        # Splunk SOAR passes its own start_time and end_time to every POLL NOW run (the last few days
        # up to the current time), which would override the configured start time, so both are
        # ignored: POLL NOW always starts at 'start_time_poll_now'.
        if self._connector.is_poll_now():
            key = consts.VISION_CONFIG_START_TIME_POLL_NOW
        else:
            last_ingested_date = self._connector.state.get(consts.VISION_STATE_LAST_INGESTED_DATE)
            if last_ingested_date is not None and not self._connector.util.parse_utc_datetime(last_ingested_date):
                self._discard_state_entry(consts.VISION_STATE_LAST_INGESTED_DATE)
                last_ingested_date = None

            if last_ingested_date:
                self._connector.debug_print(f"Fetching the clusters ingested after the last polled date: {last_ingested_date}")
                return phantom.APP_SUCCESS, last_ingested_date, end_time

            key = consts.VISION_CONFIG_START_TIME

        value = self._connector.config.get(key) or consts.VISION_ON_POLL_DEFAULT_START_TIME
        ret_val, start_time = self._connector.util.parse_start_time(value)
        if phantom.is_fail(ret_val):
            return (
                self._action_result.set_status(
                    phantom.APP_ERROR,
                    consts.VISION_ERROR_INVALID_START_TIME.format(key=key),
                ),
                None,
                None,
            )

        return phantom.APP_SUCCESS, start_time, end_time

    def _get_poll_now_count(self, key):
        """Fetch a POLL NOW count limit, None for a scheduled poll or when it was not given.

        :param key: action parameter key
        :return: phantom.APP_SUCCESS/phantom.APP_ERROR and the limit
        """
        value = self._param.get(key)
        if not self._connector.is_poll_now() or value is None:
            return phantom.APP_SUCCESS, None
        return self._connector.util.validate_integer(self._action_result, value, key)

    def _get_limits(self):
        """Determine the ingestion limits of the current polling cycle.

        :return: phantom.APP_SUCCESS/phantom.APP_ERROR, maximum artifacts per container,
            maximum containers and maximum artifacts of a POLL NOW run
        """
        failed = (None, None, None)
        max_artifacts = self._connector.config.get(consts.VISION_CONFIG_MAX_ARTIFACTS, consts.VISION_ON_POLL_DEFAULT_MAX_ARTIFACTS)
        ret_val, max_artifacts = self._connector.util.validate_integer(self._action_result, max_artifacts, consts.VISION_CONFIG_MAX_ARTIFACTS)
        if phantom.is_fail(ret_val):
            return self._action_result.get_status(), *failed

        ret_val, max_containers = self._get_poll_now_count(consts.VISION_PARAM_CONTAINER_COUNT)
        if phantom.is_fail(ret_val):
            return self._action_result.get_status(), *failed

        ret_val, max_poll_artifacts = self._get_poll_now_count(consts.VISION_PARAM_ARTIFACT_COUNT)
        if phantom.is_fail(ret_val):
            return self._action_result.get_status(), *failed

        return phantom.APP_SUCCESS, max_artifacts, max_containers, max_poll_artifacts

    @staticmethod
    def _get_clusters(response):
        """Fetch the clusters from the API response.

        The v6 aiClusters endpoint returns a bare JSON array of clusters.

        :param response: response returned by the API
        :return: list of clusters
        """
        return response if isinstance(response, list) else []

    def _get_window_emails(self, cluster, window_start, window_end):
        """Select the emails of the cluster that were ingested in the polling window.

        The endpoint returns a cluster whenever at least one of its emails was ingested in the
        requested range, but it carries every email of that cluster, including the ones ingested
        long before the window. Only the emails of the window are ingested, so that a cluster
        which keeps growing produces one container per window instead of re-ingesting its whole
        history into every new container.

        :param cluster: cluster dictionary
        :param window_start: start of the polling window, as a naive UTC datetime object
        :param window_end: end of the polling window, as a naive UTC datetime object
        :return: list of emails ingested in the polling window
        """
        emails = []
        for email in cluster.get(consts.VISION_CLUSTER_EMAIL_KEY) or []:
            # combinedMessageId identifies the email across clusters. Without it the artifact
            # cannot be deduplicated, so the email is skipped here, before chunking, so that a
            # cluster made only of such emails never produces an empty container.
            if not email.get("combinedMessageId"):
                self._connector.debug_print(f"Skipping an email without an identifier in the cluster {cluster.get('id')}")
                continue

            processed_on = self._connector.util.parse_utc_datetime(email.get("processedOn"))
            if not processed_on:
                self._connector.debug_print(f"Skipping an email without a valid ingestion timestamp in the cluster {cluster.get('id')}")
                continue

            if window_start <= processed_on < window_end:
                emails.append((processed_on, email))

        # The chunk an email lands in must not depend on the order the API returns it in,
        # otherwise a re-polled window would slice the emails differently and duplicate them
        # across containers. Oldest first, so the last email of a chunk is its newest.
        emails.sort(key=lambda entry: (entry[0], entry[1]["combinedMessageId"]))
        return [email for _, email in emails]

    def _prepare_artifact(self, cluster, container_id, email):
        """Prepare an artifact for an email of the cluster.

        :param cluster: cluster dictionary the email belongs to
        :param container_id: ID of the container of the cluster
        :param email: email dictionary
        :return: artifact dictionary
        """
        email_id = email["combinedMessageId"]
        signature = email.get("signature") or {}

        cef = {
            "clusterId": cluster.get("id"),
            "clusterTitle": cluster.get("title"),
            "combinedMessageId": email_id,
            "internetMessageId": email.get("messageId"),
            "emailSubject": email.get("subject"),
            "fromEmail": email.get("sender"),
            "recipientCount": email.get("recipientCount"),
            "receivedOn": email.get("processedOn"),
            "normalizedContentHash": signature.get("normalizedContentHash"),
            "quarantineJobId": email.get("quarantineJobId"),
            "iocIds": email.get("iocIds"),
        }
        cef = {key: value for key, value in cef.items() if value not in (None, "", [])}

        return {
            "name": email.get("subject") or consts.VISION_ARTIFACT_NAME,
            "label": consts.VISION_ARTIFACT_LABEL,
            "container_id": container_id,
            "source_data_identifier": consts.VISION_ARTIFACT_SDI.format(email_id=email_id),
            "cef": cef,
            "cef_types": consts.VISION_ON_POLL_CEF_TYPES,
            "data": email,
            "run_automation": False,
        }

    def _save_cluster(self, cluster, emails, from_date, to_date, chunk, chunks):
        """Save one chunk of the cluster emails as a container along with its emails as artifacts.

        :param cluster: cluster dictionary
        :param emails: emails of the chunk to ingest, oldest first
        :param from_date: start of the polling window
        :param to_date: end of the polling window
        :param chunk: index of the chunk within the polling window
        :param chunks: number of chunks the cluster emails of the polling window are split into
        :return: phantom.APP_SUCCESS/phantom.APP_ERROR and the number of artifacts saved
        """
        cluster_id = cluster.get("id")
        # The ingestion timestamp of the newest email of the chunk, not the clock, identifies the
        # container: re-polling the same emails rebuilds the same identifier and the platform
        # deduplicates, while emails ingested later form a chunk of their own instead of being
        # added to a container an earlier cycle created.
        newest = emails[-1].get("processedOn")
        # The name shows where the container starts: every email it holds was ingested at or after
        # its oldest email. The identifier keeps the newest one, which the deduplication relies on.
        oldest = emails[0].get("processedOn")
        name = consts.VISION_CONTAINER_NAME.format(
            title=cluster.get("title") or consts.VISION_CONTAINER_DEFAULT_TITLE, cluster_id=cluster_id, oldest=oldest
        )
        if chunks > 1:
            name = consts.VISION_CONTAINER_NAME_PART.format(name=name, part=chunk + 1, parts=chunks)
        container = {
            "name": name,
            "source_data_identifier": consts.VISION_CONTAINER_SDI.format(cluster_id=cluster_id, newest=newest, chunk=chunk),
            "description": " ".join(
                filter(
                    None,
                    [
                        cluster.get("userNote"),
                        consts.VISION_CONTAINER_DESCRIPTION.format(cluster_id=cluster_id, from_date=from_date, to_date=to_date),
                    ],
                )
            ),
            "data": {key: value for key, value in cluster.items() if key != consts.VISION_CLUSTER_EMAIL_KEY},
        }

        container_label = self._connector.config.get("ingest", {}).get("container_label")
        if container_label:
            container["label"] = container_label

        ret_val, message, container_id = self._connector.save_container(container)
        if phantom.is_fail(ret_val) or not container_id:
            return (
                self._action_result.set_status(
                    phantom.APP_ERROR,
                    consts.VISION_ERROR_SAVE_CONTAINER.format(cluster_id=cluster_id, error=message),
                ),
                0,
            )

        artifacts = [self._prepare_artifact(cluster, container_id, email) for email in emails]

        # Run the active playbooks only once, after the last artifact of the container is created
        artifacts[-1]["run_automation"] = True

        ret_val, message, _ = self._connector.save_artifacts(artifacts)
        if phantom.is_fail(ret_val):
            return (
                self._action_result.set_status(
                    phantom.APP_ERROR,
                    consts.VISION_ERROR_SAVE_ARTIFACTS.format(cluster_id=cluster_id, error=message),
                ),
                0,
            )

        return phantom.APP_SUCCESS, len(artifacts)

    def _update_state(self, to_date):
        """Store the polling cursor for the next cycle.

        :param to_date: end date of the polling window
        """
        # Earlier builds retained a truncated window here. Its start is the stored cursor, so the
        # window that follows the cursor already covers the emails that entry was holding back.
        self._connector.state.pop(consts.VISION_STATE_PENDING_POLL, None)
        self._connector.state[consts.VISION_STATE_LAST_INGESTED_DATE] = to_date
        self._connector.is_state_updated = True

    def execute(self):
        """Execute the on poll action."""
        ret_val, from_date, to_date = self._get_window()
        if phantom.is_fail(ret_val):
            return self._action_result.get_status()

        ret_val, max_artifacts, max_containers, max_poll_artifacts = self._get_limits()
        if phantom.is_fail(ret_val):
            return self._action_result.get_status()

        params = {
            "fromDateTime": from_date,
            "toDateTime": to_date,
            "excludeEmails": False,
            "size": consts.VISION_ON_POLL_PAGE_SIZE,
            "page": consts.VISION_DEFAULT_PAGE_NUMBER,
            "sort": consts.VISION_ON_POLL_SORT,
        }
        window_start = self._connector.util.parse_utc_datetime(from_date)
        window_end = self._connector.util.parse_utc_datetime(to_date)

        # The window ends 'ingestion_lag' minutes ago, so a start time or a polling
        # interval shorter than the lag produces a window the API rejects with a 422
        # ("fromDateTime must be before toDateTime"). Nothing is due yet, so the cycle is a no-op
        # and the cursor is left untouched for the next one.
        if window_start >= window_end:
            self._connector.debug_print(f"Nothing to poll yet, the window {from_date} - {to_date} is empty")
            summary = consts.VISION_SUCCESS_ON_POLL.format(emails=0, clusters=0, containers=0)
            self._connector.save_progress(summary)
            return self._action_result.set_status(phantom.APP_SUCCESS, summary)

        total_containers = 0
        total_clusters = 0
        total_emails = 0
        limit_reached = False

        while not limit_reached:
            ret_val, response = self._connector.util.make_rest_call_helper(
                consts.VISION_ENDPOINT_AI_CLUSTERS,
                self._action_result,
                method="get",
                params=params,
            )
            if phantom.is_fail(ret_val):
                return self._action_result.get_status()

            clusters = self._get_clusters(response)
            if not clusters:
                break

            for cluster in clusters:
                cluster_id = cluster.get("id")
                # Without an ID the cluster cannot be identified in the container
                if cluster_id is None:
                    self._connector.debug_print("Skipping a cluster without an ID")
                    continue

                emails = self._get_window_emails(cluster, window_start, window_end)
                # Every returned cluster has at least one email in the window, so an empty list
                # means the cluster only carries emails this cycle must not ingest
                if not emails:
                    self._connector.debug_print(f"Skipping the cluster {cluster_id} without emails ingested in the polling window")
                    continue

                # POLL NOW keeps no state to resume from, so its container_count and artifact_count
                # are exact and may cut a cluster short. A scheduled poll has no such limit: it
                # ingests every email of the window, split into containers of 'max_artifacts'.
                if max_containers and total_containers >= max_containers:
                    limit_reached = True
                    break

                if max_poll_artifacts:
                    emails = emails[: max_poll_artifacts - total_emails]

                chunk_starts = range(0, len(emails), max_artifacts)
                for chunk, start in enumerate(chunk_starts):
                    if max_containers and total_containers >= max_containers:
                        break
                    ret_val, ingested_emails = self._save_cluster(
                        cluster, emails[start : start + max_artifacts], from_date, to_date, chunk, len(chunk_starts)
                    )
                    if phantom.is_fail(ret_val):
                        return self._action_result.get_status()

                    total_containers += 1
                    total_emails += ingested_emails

                total_clusters += 1

                if (max_containers and total_containers >= max_containers) or (max_poll_artifacts and total_emails >= max_poll_artifacts):
                    limit_reached = True
                    break

            if len(clusters) < consts.VISION_ON_POLL_PAGE_SIZE:
                break

            params["page"] += 1

        if not self._connector.is_poll_now():
            self._update_state(to_date)

        summary = consts.VISION_SUCCESS_ON_POLL.format(emails=total_emails, clusters=total_clusters, containers=total_containers)
        self._connector.save_progress(summary)

        return self._action_result.set_status(phantom.APP_SUCCESS, summary)

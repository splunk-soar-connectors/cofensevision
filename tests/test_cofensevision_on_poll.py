# File: test_cofensevision_on_poll.py
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

import json
import unittest
from unittest.mock import Mock, patch

from freezegun import freeze_time

import cofensevision_consts as consts
from cofensevision_connector import CofenseVisionConnector
from tests import cofensevision_config


# Splunk SOAR passes the maximum count for the scheduled and interval polls
MAX_COUNT_VALUE = 4294967295
FROZEN_TIME = "2024-05-31T12:00:00.000000"
# The polling window stops the default ingestion lag (5 minutes) short of the current time
FROZEN_DATE = "2024-05-31T11:55:00.000Z"
# IOC IDs are MD5 digests; the live API returns normalizedContentHash as a signed 64-bit integer string
IOC_ID = "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6"  # pragma: allowlist secret
CONTENT_HASH = "5547099433710119834"


def get_email(email_id, processed_on="2024-05-31T10:00:00Z"):
    """Prepare an email of a cluster, shaped as the v6 aiClusters API returns it."""
    return {
        "combinedMessageId": f"abc{email_id}-net{email_id}",
        "messageId": f"<{email_id}@mail.phishing-domain.com>",
        "subject": f"Invoice {email_id}",
        "recipientCount": 3,
        "sender": "attacker@phishing-domain.com",
        "processedOn": processed_on,
        "signature": {
            "normalizedContentHash": CONTENT_HASH,
            "normalizedTokenCount": 142,
        },
        "iocIds": [IOC_ID],
        "quarantineJobId": 42,
    }


def get_cluster(cluster_id, email_count, processed_on="2024-05-31T10:00:00Z"):
    """Prepare a cluster along with its emails, shaped as the v6 aiClusters API returns it."""
    return {
        "id": cluster_id,
        "title": f"Cluster {cluster_id}",
        "userNote": "malicious campaign",
        "emailCount": email_count,
        "emails": [get_email(cluster_id * 10 + index, processed_on) for index in range(email_count)],
    }


class TestOnPollAction(unittest.TestCase):
    """Class to test the On Poll action."""

    def setUp(self):
        """Set up method for the tests."""
        self.connector = CofenseVisionConnector()
        self.test_json = dict(cofensevision_config.TEST_JSON)
        self.test_json.update({"action": "on poll", "identifier": "on_poll"})
        self.test_json["config"] = dict(cofensevision_config.TEST_JSON["config"])
        self.test_json["parameters"] = [{"container_count": MAX_COUNT_VALUE}]

        cofensevision_config.set_state_file(client_id=True, access_token=True)

        container_patcher = patch.object(CofenseVisionConnector, "save_container")
        artifact_patcher = patch.object(CofenseVisionConnector, "save_artifacts")
        self.mock_save_container = container_patcher.start()
        self.mock_save_artifacts = artifact_patcher.start()
        self.addCleanup(container_patcher.stop)
        self.addCleanup(artifact_patcher.stop)

        self.mock_save_container.side_effect = lambda container: (True, "Added Container", 100 + container["data"]["id"])
        self.mock_save_artifacts.return_value = (True, "Added artifacts", [1])

        return super().setUp()

    def run_action(self, mock_get, pages):
        """Execute the on poll action against the provided pages of clusters."""
        self.request_params = []
        responses = []
        for page in pages:
            response = Mock()
            response.status_code = 200
            response.headers = cofensevision_config.DEFAULT_HEADERS
            response.json.return_value = page
            responses.append(response)

        def request(_url, **kwargs):
            # The action reuses a single params dict for every page, snapshot it at call time
            self.request_params.append(dict(kwargs["params"]))
            return responses[len(self.request_params) - 1]

        mock_get.side_effect = request

        ret_val = self.connector._handle_action(json.dumps(self.test_json), None)
        return json.loads(ret_val)

    @staticmethod
    def get_state_file():
        """Read the state file saved by the connector."""
        with open(cofensevision_config.STATE_FILE_PATH) as state_file:
            return json.load(state_file)

    @classmethod
    def update_state_file(cls, **entries):
        """Add the provided entries to the state file created by the setUp method."""
        state_file = cls.get_state_file()
        state_file.update(entries)
        cofensevision_config.set_state_file(raw=json.dumps(state_file))

    @freeze_time(FROZEN_TIME)
    @patch("cofensevision_utils.requests.get")
    def test_on_poll_first_cycle_pass(self, mock_get):
        """Test the first scheduled poll, the window starts at the 'start_time' configuration parameter."""
        self.test_json["config"]["start_time"] = "1d"

        ret_val = self.run_action(mock_get, [[get_cluster(1, 2), get_cluster(2, 1)]])

        self.assertEqual(ret_val["status"], "success")
        self.assertEqual(
            self.request_params,
            [
                {
                    "fromDateTime": "2024-05-30T12:00:00.000Z",
                    "toDateTime": FROZEN_DATE,
                    "excludeEmails": False,
                    "size": consts.VISION_ON_POLL_PAGE_SIZE,
                    "page": 0,
                    "sort": consts.VISION_ON_POLL_SORT,
                }
            ],
        )

        containers = [call.args[0] for call in self.mock_save_container.call_args_list]
        self.assertEqual(
            [container["name"] for container in containers],
            ["1 : Cluster 1 - 2024-05-31T10:00:00Z", "2 : Cluster 2 - 2024-05-31T10:00:00Z"],
        )
        self.assertEqual(
            [container["source_data_identifier"] for container in containers],
            ["cofense-vision-cluster-1-2024-05-31T10:00:00Z-0", "cofense-vision-cluster-2-2024-05-31T10:00:00Z-0"],
        )

        artifacts = [artifact for call in self.mock_save_artifacts.call_args_list for artifact in call.args[0]]
        self.assertEqual(
            [artifact["source_data_identifier"] for artifact in artifacts],
            ["cofense-vision-email-abc10-net10", "cofense-vision-email-abc11-net11", "cofense-vision-email-abc20-net20"],
        )
        self.assertEqual([artifact["container_id"] for artifact in artifacts], [101, 101, 102])
        # The playbooks must run only once, after the last artifact of a container is created
        self.assertEqual([artifact["run_automation"] for artifact in artifacts], [False, True, True])
        self.assertEqual(
            artifacts[0]["cef"],
            {
                "clusterId": 1,
                "clusterTitle": "Cluster 1",
                "combinedMessageId": "abc10-net10",
                "internetMessageId": "<10@mail.phishing-domain.com>",
                "emailSubject": "Invoice 10",
                "fromEmail": "attacker@phishing-domain.com",
                "recipientCount": 3,
                "receivedOn": "2024-05-31T10:00:00Z",
                "normalizedContentHash": CONTENT_HASH,
                "quarantineJobId": 42,
                "iocIds": [IOC_ID],
            },
        )
        # The IOC and quarantine job identifiers must be actionable from the artifact
        self.assertEqual(
            artifacts[0]["cef_types"]["iocIds"] + artifacts[0]["cef_types"]["quarantineJobId"],
            ["cofense vision ioc id", "cofense vision quarantine job id"],
        )

        state_file = self.get_state_file()
        self.assertEqual(state_file[consts.VISION_STATE_LAST_INGESTED_DATE], FROZEN_DATE)
        self.assertNotIn(consts.VISION_STATE_PENDING_POLL, state_file)

    @freeze_time(FROZEN_TIME)
    @patch("cofensevision_utils.requests.get")
    def test_on_poll_next_cycle_pass(self, mock_get):
        """Test the scheduled poll which continues from the date of the previous cycle."""
        self.update_state_file(**{consts.VISION_STATE_LAST_INGESTED_DATE: "2024-05-31T06:00:00.000Z"})

        ret_val = self.run_action(mock_get, [[get_cluster(3, 1)]])

        self.assertEqual(ret_val["status"], "success")
        self.assertEqual(self.request_params[0]["fromDateTime"], "2024-05-31T06:00:00.000Z")
        self.assertEqual(self.get_state_file()[consts.VISION_STATE_LAST_INGESTED_DATE], FROZEN_DATE)

    @freeze_time(FROZEN_TIME)
    @patch("cofensevision_utils.requests.get")
    def test_on_poll_drops_window_retained_by_earlier_build(self, mock_get):
        """Test that a window retained by the removed 'max_emails' limit is dropped and the poll follows the cursor.

        That entry never advanced the cursor, so the window following the cursor still covers its emails.
        """
        self.update_state_file(
            **{
                consts.VISION_STATE_LAST_INGESTED_DATE: "2024-05-30T12:00:00.000Z",
                consts.VISION_STATE_PENDING_POLL: {
                    "from_date": "2024-05-30T12:00:00.000Z",
                    "to_date": "2024-05-31T06:00:00.000Z",
                    "cluster_ids": [1],
                },
            }
        )

        ret_val = self.run_action(mock_get, [[get_cluster(1, 2), get_cluster(2, 1, "2024-05-31T05:00:00Z")]])

        self.assertEqual(ret_val["status"], "success")
        self.assertEqual(self.request_params[0]["fromDateTime"], "2024-05-30T12:00:00.000Z")
        self.assertEqual(self.request_params[0]["toDateTime"], FROZEN_DATE)
        self.assertEqual(self.mock_save_container.call_count, 2)

        state_file = self.get_state_file()
        self.assertEqual(state_file[consts.VISION_STATE_LAST_INGESTED_DATE], FROZEN_DATE)
        self.assertNotIn(consts.VISION_STATE_PENDING_POLL, state_file)

    @freeze_time(FROZEN_TIME)
    @patch("cofensevision_utils.requests.get")
    def test_on_poll_now_pass(self, mock_get):
        """Test the POLL NOW run, it uses its own start time, honors the container count and does not update the state."""
        self.test_json["config"]["start_time_poll_now"] = "6h"
        self.test_json["parameters"] = [{"container_count": 1}]

        ret_val = self.run_action(mock_get, [[get_cluster(1, 1), get_cluster(2, 1)]])

        self.assertEqual(ret_val["status"], "success")
        self.assertEqual(self.request_params[0]["fromDateTime"], "2024-05-31T06:00:00.000Z")
        self.assertEqual(self.mock_save_container.call_count, 1)

        state_file = self.get_state_file()
        self.assertNotIn(consts.VISION_STATE_LAST_INGESTED_DATE, state_file)
        self.assertNotIn(consts.VISION_STATE_PENDING_POLL, state_file)

    @freeze_time(FROZEN_TIME)
    @patch("cofensevision_utils.requests.get")
    def test_on_poll_pagination_pass(self, mock_get):
        """Test that a full page is followed by the next one and the clusters without an ID are skipped."""
        full_page = [get_cluster(cluster_id, 1) for cluster_id in range(consts.VISION_ON_POLL_PAGE_SIZE)]
        last_page = [{"title": "Cluster without an ID", "emails": [get_email(1)]}, get_cluster(999, 1)]

        ret_val = self.run_action(mock_get, [full_page, last_page])

        self.assertEqual(ret_val["status"], "success")
        self.assertEqual([params["page"] for params in self.request_params], [0, 1])

        containers = [call.args[0] for call in self.mock_save_container.call_args_list]
        self.assertEqual(len(containers), consts.VISION_ON_POLL_PAGE_SIZE + 1)
        self.assertEqual(containers[-1]["source_data_identifier"], "cofense-vision-cluster-999-2024-05-31T10:00:00Z-0")
        self.assertEqual(self.get_state_file()[consts.VISION_STATE_LAST_INGESTED_DATE], FROZEN_DATE)

    @patch("cofensevision_utils.requests.get")
    def test_on_poll_invalid_start_time_fail(self, mock_get):
        """Test the on poll action with an invalid 'start_time' configuration parameter."""
        self.test_json["config"]["start_time"] = "1 month"

        ret_val = self.run_action(mock_get, [[]])

        self.assertEqual(ret_val["status"], "failed")
        self.assertEqual(
            ret_val["result_data"][0]["message"],
            consts.VISION_ERROR_INVALID_START_TIME.format(key=consts.VISION_CONFIG_START_TIME),
        )
        mock_get.assert_not_called()

    @patch("cofensevision_utils.requests.get")
    def test_on_poll_out_of_range_start_time_fail(self, mock_get):
        """Test that a relative start time too large to represent is rejected instead of raising."""
        self.test_json["config"]["start_time"] = "99999999999d"

        ret_val = self.run_action(mock_get, [[]])

        self.assertEqual(ret_val["status"], "failed")
        self.assertEqual(
            ret_val["result_data"][0]["message"],
            consts.VISION_ERROR_INVALID_START_TIME.format(key=consts.VISION_CONFIG_START_TIME),
        )
        mock_get.assert_not_called()

    @freeze_time(FROZEN_TIME)
    @patch("cofensevision_utils.requests.get")
    def test_on_poll_recovers_from_corrupt_state(self, mock_get):
        """Test that a corrupt cursor or retained window is discarded and the poll falls back to 'start_time'.

        Kept as is, a corrupt entry would fail every following cycle the same way.
        """
        self.test_json["config"]["start_time"] = "1d"
        corrupt_states = [
            {consts.VISION_STATE_LAST_INGESTED_DATE: "not-a-date"},
            {consts.VISION_STATE_PENDING_POLL: {"from_date": "xx", "to_date": "yy"}},
            {consts.VISION_STATE_PENDING_POLL: "corrupt"},
            {consts.VISION_STATE_PENDING_POLL: {"from_date": FROZEN_DATE, "to_date": FROZEN_DATE}},
        ]
        for corrupt_state in corrupt_states:
            with self.subTest(state=corrupt_state):
                cofensevision_config.set_state_file(client_id=True, access_token=True)
                self.update_state_file(**corrupt_state)

                ret_val = self.run_action(mock_get, [[get_cluster(1, 1)]])

                self.assertEqual(ret_val["status"], "success")
                self.assertEqual(self.request_params[0]["fromDateTime"], "2024-05-30T12:00:00.000Z")
                state_file = self.get_state_file()
                self.assertNotIn(consts.VISION_STATE_PENDING_POLL, state_file)
                self.assertEqual(state_file[consts.VISION_STATE_LAST_INGESTED_DATE], FROZEN_DATE)

    @freeze_time(FROZEN_TIME)
    @patch("cofensevision_utils.requests.get")
    def test_on_poll_skips_emails_without_identifier(self, mock_get):
        """Test that a null emails list and an email without an identifier do not produce artifacts."""
        no_emails = get_cluster(1, 0)
        no_emails["emails"] = None
        unidentified = get_cluster(2, 1)
        del unidentified["emails"][0]["combinedMessageId"]

        ret_val = self.run_action(mock_get, [[no_emails, unidentified, get_cluster(3, 1)]])

        self.assertEqual(ret_val["status"], "success")
        # Neither the cluster without emails nor the one whose only email has no identifier
        # produces a container, so no container is ever created empty
        self.assertEqual(self.mock_save_container.call_count, 1)
        # Only the identifiable email of the third cluster becomes an artifact
        artifacts = [artifact for call in self.mock_save_artifacts.call_args_list for artifact in call.args[0]]
        self.assertEqual([artifact["source_data_identifier"] for artifact in artifacts], ["cofense-vision-email-abc30-net30"])
        self.assertIn("1 email(s) from 1 cluster(s) into 1 container(s)", ret_val["result_data"][0]["message"])

    @freeze_time(FROZEN_TIME)
    @patch("cofensevision_utils.requests.get")
    def test_on_poll_recurring_cluster_creates_new_container(self, mock_get):
        """Test that a cluster polled again only ingests its new emails, into a container of its own.

        The API returns a cluster whenever one of its emails was ingested in the window, together
        with every email it ever held, so a later cycle must neither backfill the container of an
        earlier cycle nor re-ingest the emails that cycle already took.
        """
        self.update_state_file(**{consts.VISION_STATE_LAST_INGESTED_DATE: "2024-05-31T06:00:00.000Z"})

        cluster = get_cluster(1, 1, "2024-05-30T09:00:00Z")
        cluster["emails"].append(get_email(11, "2024-05-31T10:00:00Z"))

        ret_val = self.run_action(mock_get, [[cluster]])

        self.assertEqual(ret_val["status"], "success")
        container = self.mock_save_container.call_args_list[0].args[0]
        # The newest email of the chunk, not only the cluster ID, identifies the container
        self.assertEqual(container["source_data_identifier"], "cofense-vision-cluster-1-2024-05-31T10:00:00Z-0")

        artifacts = [artifact for call in self.mock_save_artifacts.call_args_list for artifact in call.args[0]]
        self.assertEqual([artifact["source_data_identifier"] for artifact in artifacts], ["cofense-vision-email-abc11-net11"])
        self.assertIn("1 email(s) from 1 cluster(s) into 1 container(s)", ret_val["result_data"][0]["message"])

    @freeze_time(FROZEN_TIME)
    @patch("cofensevision_utils.requests.get")
    def test_on_poll_splits_cluster_into_capped_containers(self, mock_get):
        """Test that a cluster larger than 'max_artifacts' is split into deterministic containers."""
        self.test_json["config"]["max_artifacts"] = 100
        cluster = get_cluster(1, 200)
        # The API returns the emails in an arbitrary order, the split must not depend on it
        cluster["emails"].reverse()

        ret_val = self.run_action(mock_get, [[cluster]])

        self.assertEqual(ret_val["status"], "success")
        containers = [call.args[0] for call in self.mock_save_container.call_args_list]
        self.assertEqual(
            [container["source_data_identifier"] for container in containers],
            ["cofense-vision-cluster-1-2024-05-31T10:00:00Z-0", "cofense-vision-cluster-1-2024-05-31T10:00:00Z-1"],
        )
        self.assertEqual([len(call.args[0]) for call in self.mock_save_artifacts.call_args_list], [100, 100])

        # Every email is ingested exactly once and lands in a chunk decided by its sort order
        artifacts = [artifact for call in self.mock_save_artifacts.call_args_list for artifact in call.args[0]]
        sdis = [artifact["source_data_identifier"] for artifact in artifacts]
        self.assertEqual(len(set(sdis)), 200)
        self.assertEqual(sdis, sorted(sdis, key=lambda sdi: sdi.split("-")[3]))
        self.assertIn("200 email(s) from 1 cluster(s) into 2 container(s)", ret_val["result_data"][0]["message"])

    @freeze_time(FROZEN_TIME)
    @patch("cofensevision_utils.requests.get")
    def test_on_poll_repeated_poll_now_reuses_the_same_containers(self, mock_get):
        """Test that polling the same emails twice rebuilds the same container identifiers.

        Two POLL NOW runs a few minutes apart cover different windows, so a clock-derived
        identifier would ingest every email again into a second set of containers.
        """
        self.test_json["parameters"] = [{"container_count": 5}]
        page = [get_cluster(1, 2), get_cluster(2, 1)]

        first = self.run_action(mock_get, [page])
        first_sdis = [call.args[0]["source_data_identifier"] for call in self.mock_save_container.call_args_list]
        self.mock_save_container.reset_mock()

        with freeze_time("2024-05-31T12:05:00.000000"):
            second = self.run_action(mock_get, [page])
        second_sdis = [call.args[0]["source_data_identifier"] for call in self.mock_save_container.call_args_list]

        self.assertEqual(first["status"], "success")
        self.assertEqual(second["status"], "success")
        self.assertEqual(first_sdis, second_sdis)

    @freeze_time(FROZEN_TIME)
    @patch("cofensevision_utils.requests.get")
    def test_on_poll_ingests_every_email_in_one_cycle(self, mock_get):
        """Test that a scheduled poll ingests every email of the window in one cycle, split by 'max_artifacts'."""
        self.test_json["config"]["max_artifacts"] = 50
        page = []
        for cluster_id in (1, 2, 3):
            cluster = get_cluster(cluster_id, 0)
            cluster["emails"] = [get_email(f"{cluster_id}x{index}") for index in range(120)]
            cluster["emailCount"] = 120
            page.append(cluster)

        ret_val = self.run_action(mock_get, [page])

        self.assertEqual(ret_val["status"], "success")
        self.assertIn("360 email(s) from 3 cluster(s) into 9 container(s)", ret_val["result_data"][0]["message"])
        state_file = self.get_state_file()
        self.assertEqual(state_file[consts.VISION_STATE_LAST_INGESTED_DATE], FROZEN_DATE)
        self.assertNotIn(consts.VISION_STATE_PENDING_POLL, state_file)

        # 3 clusters of 120 emails, split into containers of 50, 50 and 20
        containers = [call.args[0]["source_data_identifier"] for call in self.mock_save_container.call_args_list]
        self.assertEqual(len(set(containers)), 9)
        # Emails sharing one ingestion timestamp land in several containers, told apart by the part
        names = [call.args[0]["name"] for call in self.mock_save_container.call_args_list]
        self.assertEqual(len(set(names)), 9)
        self.assertEqual(names[:3], [f"1 : Cluster 1 - 2024-05-31T10:00:00Z - Part {part} of 3" for part in (1, 2, 3)])
        chunk_sizes = [len(call.args[0]) for call in self.mock_save_artifacts.call_args_list]
        self.assertEqual(chunk_sizes, [50, 50, 20] * 3)
        sdis = [artifact["source_data_identifier"] for call in self.mock_save_artifacts.call_args_list for artifact in call.args[0]]
        self.assertEqual(len(set(sdis)), 360)

    @freeze_time(FROZEN_TIME)
    @patch("cofensevision_utils.requests.get")
    def test_on_poll_container_named_after_oldest_email(self, mock_get):
        """Test that each container is named after its oldest email and identified by its newest one."""
        self.test_json["config"]["max_artifacts"] = 2
        cluster = get_cluster(7, 0)
        # Returned out of order, the emails are sorted by their ingestion timestamp before chunking
        cluster["emails"] = [
            get_email(3, "2024-05-31T11:00:00Z"),
            get_email(1, "2024-05-31T09:00:00Z"),
            get_email(2, "2024-05-31T10:00:00Z"),
        ]

        ret_val = self.run_action(mock_get, [[cluster]])

        self.assertEqual(ret_val["status"], "success")
        containers = [call.args[0] for call in self.mock_save_container.call_args_list]
        self.assertEqual(
            [container["name"] for container in containers],
            ["7 : Cluster 7 - 2024-05-31T09:00:00Z - Part 1 of 2", "7 : Cluster 7 - 2024-05-31T11:00:00Z - Part 2 of 2"],
        )
        self.assertEqual(
            [container["source_data_identifier"] for container in containers],
            ["cofense-vision-cluster-7-2024-05-31T10:00:00Z-0", "cofense-vision-cluster-7-2024-05-31T11:00:00Z-1"],
        )

    @freeze_time(FROZEN_TIME)
    @patch("cofensevision_utils.requests.get")
    def test_on_poll_shorter_than_ingestion_lag_is_a_no_op(self, mock_get):
        """Test that a start time shorter than the ingestion lag polls nothing instead of failing.

        The API rejects a window whose start is not before its end with a 422, so the window is
        never sent and the cursor is left for the next cycle.
        """
        self.test_json["config"]["start_time"] = "1m"

        ret_val = self.run_action(mock_get, [[]])

        self.assertEqual(ret_val["status"], "success")
        self.assertIn("0 email(s) from 0 cluster(s) into 0 container(s)", ret_val["result_data"][0]["message"])
        mock_get.assert_not_called()
        self.assertNotIn(consts.VISION_STATE_LAST_INGESTED_DATE, self.get_state_file())

    def saved_artifacts(self):
        """Return every artifact the action saved, in order."""
        return [artifact for call in self.mock_save_artifacts.call_args_list for artifact in call.args[0]]

    @freeze_time(FROZEN_TIME)
    @patch("cofensevision_utils.requests.get")
    def test_poll_now_artifact_count_is_exact_pass(self, mock_get):
        """Test that POLL NOW stops at artifact_count even within a cluster (COF-N1)."""
        self.test_json["parameters"] = [{"container_count": 1, "artifact_count": 3}]

        ret_val = self.run_action(mock_get, [[get_cluster(1, 48), get_cluster(2, 5)]])

        self.assertEqual(ret_val["status"], "success")
        self.assertEqual(self.mock_save_container.call_count, 1)
        self.assertEqual(len(self.saved_artifacts()), 3)
        self.assertIn("3 email(s) from 1 cluster(s) into 1 container(s)", ret_val["result_data"][0]["message"])

    @freeze_time(FROZEN_TIME)
    @patch("cofensevision_utils.requests.get")
    def test_poll_now_container_count_is_exact_pass(self, mock_get):
        """Test that POLL NOW stops at container_count even when one cluster spans several containers."""
        self.test_json["config"]["max_artifacts"] = 100
        self.test_json["parameters"] = [{"container_count": 1}]

        ret_val = self.run_action(mock_get, [[get_cluster(1, 250)]])

        self.assertEqual(ret_val["status"], "success")
        self.assertEqual(self.mock_save_container.call_count, 1)
        self.assertEqual(len(self.saved_artifacts()), 100)

    @freeze_time(FROZEN_TIME)
    @patch("cofensevision_utils.requests.get")
    def test_scheduled_poll_ignores_poll_now_parameters_pass(self, mock_get):
        """Test that a scheduled poll ignores artifact_count and the POLL NOW time range and follows its cursor."""
        self.test_json["config"]["max_artifacts"] = 100
        self.test_json["parameters"] = [
            {"container_count": MAX_COUNT_VALUE, "artifact_count": 3, "start_time": 1577836800000, "end_time": 1577923200000}
        ]

        ret_val = self.run_action(mock_get, [[get_cluster(1, 250)]])

        self.assertEqual(ret_val["status"], "success")
        self.assertEqual(len(self.saved_artifacts()), 250)
        self.assertEqual(self.request_params[0]["fromDateTime"], "2024-05-30T12:00:00.000Z")
        self.assertEqual(self.request_params[0]["toDateTime"], FROZEN_DATE)

    @freeze_time(FROZEN_TIME)
    @patch("cofensevision_utils.requests.get")
    def test_poll_now_uses_configured_start_time_pass(self, mock_get):
        """Test that POLL NOW starts at 'start_time_poll_now' and ignores the time range Splunk SOAR passes to it.

        The platform passes start_time and end_time to every POLL NOW run; honoring them made the
        configured start time ineffective.
        """
        self.test_json["config"]["start_time_poll_now"] = "100d"
        self.test_json["parameters"] = [{"container_count": 5, "start_time": 1716681600000, "end_time": 1717156800000}]

        ret_val = self.run_action(mock_get, [[]])

        self.assertEqual(ret_val["status"], "success")
        self.assertEqual(self.request_params[0]["fromDateTime"], "2024-02-21T12:00:00.000Z")
        self.assertEqual(self.request_params[0]["toDateTime"], FROZEN_DATE)

    @freeze_time(FROZEN_TIME)
    @patch("cofensevision_utils.requests.get")
    def test_ingestion_lag_is_configurable_pass(self, mock_get):
        """Test that the 'ingestion_lag' asset parameter sets how far behind now the window ends (COF-N2)."""
        for lag, to_date in ((30, "2024-05-31T11:30:00.000Z"), (0, "2024-05-31T12:00:00.000Z")):
            with self.subTest(lag=lag):
                cofensevision_config.set_state_file(client_id=True, access_token=True)
                self.test_json["config"]["ingestion_lag"] = lag
                ret_val = self.run_action(mock_get, [[]])
                self.assertEqual(ret_val["status"], "success")
                self.assertEqual(self.request_params[0]["toDateTime"], to_date)

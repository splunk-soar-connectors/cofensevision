# File: cofensevision_list_clusters.py
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


class ListClustersAction(BaseAction):
    """Class to handle list clusters action."""

    def _prepare_query_parameters(self):
        """Prepare the query parameters to list the clusters.

        :return: phantom.APP_ERROR/phantom.APP_SUCCESS and query parameter dictionary
        """
        page = self._param.get("page", consts.VISION_DEFAULT_PAGE_NUMBER)
        ret_val, page = self._connector.util.validate_integer(self._action_result, page, "page", True)
        if phantom.is_fail(ret_val):
            return self._action_result.get_status(), None

        size = self._param.get("size", consts.VISION_DEFAULT_PAGE_SIZE)
        ret_val, size = self._connector.util.validate_integer(self._action_result, size, "size", max_value=consts.VISION_MAX_PAGE_SIZE)
        if phantom.is_fail(ret_val):
            return self._action_result.get_status(), None

        params = {"page": page, "size": size, "excludeEmails": self._param.get("exclude_emails", False)}

        sort_field = self._param.get("sort_field")
        order = self._param.get("order")
        if sort_field and sort_field not in consts.VISION_CLUSTER_SORT_FIELDS:
            return self._action_result.set_status(
                phantom.APP_ERROR, consts.VISION_ERROR_VALUE_LIST.format("sort_field", ", ".join(consts.VISION_CLUSTER_SORT_FIELDS))
            ), None
        if order and order not in consts.VISION_VALID_SORT_ORDER:
            return self._action_result.set_status(
                phantom.APP_ERROR, consts.VISION_ERROR_VALUE_LIST.format("order", ", ".join(consts.VISION_VALID_SORT_ORDER))
            ), None
        if sort_field:
            params["sort"] = f"{sort_field},{order}" if order else sort_field
        elif order:
            # The 'order' parameter has no effect unless 'sort_field' is also supplied. Note this instead of failing.
            self._connector.save_progress("The 'order' parameter was ignored because 'sort_field' was not provided")

        from_date = self._param.get("from_date", "")
        if not from_date:
            # The vendor API requires 'fromDateTime' to be present, so default it to the last 24 hours when not supplied.
            from_date = (datetime.now(timezone.utc) - timedelta(hours=24)).strftime(consts.VISION_ISO8601_UTC_DATE_FORMAT)

        ret_val, date_range = self._connector.util.validate_date_range(
            self._action_result, from_date, "from_date", self._param.get("to_date", ""), "to_date"
        )
        if phantom.is_fail(ret_val):
            return self._action_result.get_status(), None
        from_date, to_date = date_range

        if from_date:
            params["fromDateTime"] = from_date
        if to_date:
            params["toDateTime"] = to_date

        return phantom.APP_SUCCESS, params

    def execute(self):
        """Execute the list clusters action."""
        ret_val, params = self._prepare_query_parameters()
        if phantom.is_fail(ret_val):
            return self._action_result.get_status()

        ret_val, response = self._connector.util.make_rest_call_helper(consts.VISION_ENDPOINT_AI_CLUSTERS, self._action_result, params=params)
        if phantom.is_fail(ret_val):
            return self._action_result.get_status()

        if response is None or (isinstance(response, dict) and not response):
            return self._action_result.set_status(phantom.APP_ERROR, consts.VISION_ERROR_ACTION_EMPTY_RESPONSE)

        if not isinstance(response, (list, dict)):
            return self._action_result.set_status(phantom.APP_ERROR, consts.VISION_ERROR_UNEXPECTED_RESPONSE_FORMAT)

        clusters = response if isinstance(response, list) else response.get("clusters", [])
        for data in clusters:
            self._action_result.add_data(data)

        total_clusters = self._action_result.get_data_size()
        self._action_result.update_summary({"total_clusters": total_clusters})

        return self._action_result.set_status(phantom.APP_SUCCESS, consts.VISION_SUCCESS_LIST_CLUSTERS_ACTION.format(total_clusters))

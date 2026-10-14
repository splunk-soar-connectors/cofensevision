# File: cofensevision_update_cluster.py
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

import phantom.app as phantom

import cofensevision_consts as consts
from actions import BaseAction


class UpdateClusterAction(BaseAction):
    """Class to handle update cluster action."""

    def execute(self):
        """Execute the update cluster action."""
        ret_val, cluster_id = self._connector.util.validate_integer(
            self._action_result, self._param[consts.VISION_PARAM_CLUSTER_ID], consts.VISION_PARAM_CLUSTER_ID
        )
        if phantom.is_fail(ret_val):
            return self._action_result.get_status()

        body = {}
        if self._param.get("title"):
            body["title"] = self._param["title"]
        if self._param.get("note"):
            body["userNote"] = self._param["note"]

        if not body:
            return self._action_result.set_status(phantom.APP_ERROR, consts.VISION_ERROR_MISSING_UPDATE_PARAMETER)

        endpoint = consts.VISION_ENDPOINT_AI_CLUSTER.format(cluster_id=cluster_id)
        ret_val, response = self._connector.util.make_rest_call_helper(endpoint, self._action_result, method="patch", data=json.dumps(body))
        if phantom.is_fail(ret_val):
            return self._action_result.get_status()

        if response:
            self._action_result.add_data(response)

        return self._action_result.set_status(phantom.APP_SUCCESS, consts.VISION_SUCCESS_UPDATE_CLUSTER_ACTION)

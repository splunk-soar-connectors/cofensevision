# File: cofensevision_update_vision_ai_config.py
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


class UpdateVisionAiConfigAction(BaseAction):
    """Class to handle update vision ai config action."""

    def _prepare_request_body(self):
        """Prepare a request body to update the vision ai config with only the supplied parameters.

        :return: phantom.APP_ERROR/phantom.APP_SUCCESS and request body dictionary
        """
        body = {}

        if "enable" in self._param:
            ret_val, value = self._connector.util.validate_boolean(self._action_result, self._param["enable"], "enable")
            if phantom.is_fail(ret_val):
                return self._action_result.get_status(), None
            body["enabled"] = value

        if "auto_quarantine" in self._param:
            ret_val, value = self._connector.util.validate_boolean(self._action_result, self._param["auto_quarantine"], "auto_quarantine")
            if phantom.is_fail(ret_val):
                return self._action_result.get_status(), None
            body["autoQuarantine"] = value

        if "operator_approval" in self._param:
            ret_val, value = self._connector.util.validate_boolean(self._action_result, self._param["operator_approval"], "operator_approval")
            if phantom.is_fail(ret_val):
                return self._action_result.get_status(), None
            body["operatorApproval"] = value

        if "tos_accepted" in self._param:
            ret_val, value = self._connector.util.validate_boolean(self._action_result, self._param["tos_accepted"], "tos_accepted")
            if phantom.is_fail(ret_val):
                return self._action_result.get_status(), None
            body["tosAccepted"] = value

        if "cluster_match_time" in self._param:
            ret_val, value = self._connector.util.validate_ranged_integer(
                self._action_result,
                self._param["cluster_match_time"],
                "cluster_match_time",
                min_value=consts.VISION_MIN_CLUSTER_MATCH_TIME,
                max_value=consts.VISION_MAX_CLUSTER_MATCH_TIME,
            )
            if phantom.is_fail(ret_val):
                return self._action_result.get_status(), None
            body["clusterTimeToMatchMs"] = value

        if "min_cluster_size" in self._param:
            ret_val, value = self._connector.util.validate_ranged_integer(
                self._action_result, self._param["min_cluster_size"], "min_cluster_size", min_value=consts.VISION_MIN_CLUSTER_SIZE
            )
            if phantom.is_fail(ret_val):
                return self._action_result.get_status(), None
            body["minClusterSize"] = value

        if "cluster_rapid_growth_time" in self._param:
            ret_val, value = self._connector.util.validate_ranged_integer(
                self._action_result,
                self._param["cluster_rapid_growth_time"],
                "cluster_rapid_growth_time",
                min_value=consts.VISION_MIN_CLUSTER_RAPID_GROWTH_TIME,
                max_value=consts.VISION_MAX_CLUSTER_RAPID_GROWTH_TIME,
            )
            if phantom.is_fail(ret_val):
                return self._action_result.get_status(), None
            body["rapidlyTimeMs"] = value

        if "similarity_level" in self._param:
            ret_val, value = self._connector.util.validate_ranged_integer(
                self._action_result,
                self._param["similarity_level"],
                "similarity_level",
                min_value=consts.VISION_MIN_SIMILARITY_LEVEL,
                max_value=consts.VISION_MAX_SIMILARITY_LEVEL,
            )
            if phantom.is_fail(ret_val):
                return self._action_result.get_status(), None
            body["similarityLevel"] = value

        if not body:
            return self._action_result.set_status(phantom.APP_ERROR, consts.VISION_ERROR_MISSING_UPDATE_PARAMETER), None

        return phantom.APP_SUCCESS, body

    def execute(self):
        """Execute the update vision ai config action."""
        ret_val, body = self._prepare_request_body()
        if phantom.is_fail(ret_val):
            return self._action_result.get_status()

        ret_val, response = self._connector.util.make_rest_call_helper(
            consts.VISION_ENDPOINT_AI_CLUSTER_CONFIG, self._action_result, method="patch", data=json.dumps(body)
        )
        if phantom.is_fail(ret_val):
            return self._action_result.get_status()

        if response:
            self._action_result.add_data(response)

        return self._action_result.set_status(phantom.APP_SUCCESS, consts.VISION_SUCCESS_UPDATE_AI_CONFIG_ACTION)

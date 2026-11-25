# File: test_cofensevision_update_vision_ai_config.py
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
from unittest.mock import patch

import cofensevision_consts as consts
from cofensevision_connector import CofenseVisionConnector
from tests import cofensevision_config


class TestUpdateVisionAiConfigAction(unittest.TestCase):
    """Class to test the update vision ai config action."""

    def setUp(self):
        """Set up method for the tests."""
        self.connector = CofenseVisionConnector()
        self.test_json = dict(cofensevision_config.TEST_JSON)
        self.test_json.update({"action": "update vision ai config", "identifier": "update_vision_ai_config"})

        return super().setUp()

    @patch("cofensevision_utils.requests.patch")
    def test_update_vision_ai_config_pass(self, mock_patch):
        """Test the valid case for the update vision ai config action.

        Token is available in the state file.
        Patch the patch() to return the valid response.
        """
        cofensevision_config.set_state_file(client_id=True, access_token=True)

        self.test_json["parameters"] = [
            {
                "min_cluster_size": 100,
                "similarity_level": 5,
                "cluster_rapid_growth_time": 14400000,
            }
        ]

        mock_patch.return_value.status_code = 200
        mock_patch.return_value.headers = cofensevision_config.DEFAULT_HEADERS
        mock_patch.return_value.json.return_value = {"minClusterSize": 100, "similarityLevel": 5, "rapidlyTimeMs": 14400000}

        ret_val = self.connector._handle_action(json.dumps(self.test_json), None)
        ret_val = json.loads(ret_val)
        self.assertEqual(ret_val["result_summary"]["total_objects"], 1)
        self.assertEqual(ret_val["result_summary"]["total_objects_successful"], 1)
        self.assertEqual(ret_val["status"], "success")
        self.assertEqual(ret_val["result_data"][0]["message"], consts.VISION_SUCCESS_UPDATE_AI_CONFIG_ACTION)

        expected_body = {"minClusterSize": 100, "similarityLevel": 5, "rapidlyTimeMs": 14400000}
        mock_patch.assert_called_once()
        call_args, call_kwargs = mock_patch.call_args
        self.assertEqual(call_args[0], f"{self.test_json['config']['base_url']}{consts.VISION_ENDPOINT_AI_CLUSTER_CONFIG}")
        self.assertEqual(call_kwargs["headers"], cofensevision_config.ACTION_HEADER)
        self.assertEqual(call_kwargs["timeout"], consts.VISION_REQUEST_TIMEOUT)
        self.assertEqual(call_kwargs["verify"], False)
        self.assertEqual(json.loads(call_kwargs["data"]), expected_body)

    def test_update_vision_ai_config_no_parameters_fail(self):
        """Test the update vision ai config action with no update parameters supplied."""
        self.test_json["parameters"] = [{}]

        ret_val = self.connector._handle_action(json.dumps(self.test_json), None)
        ret_val = json.loads(ret_val)
        self.assertEqual(ret_val["result_summary"]["total_objects"], 1)
        self.assertEqual(ret_val["result_summary"]["total_objects_successful"], 0)
        self.assertEqual(ret_val["status"], "failed")
        self.assertEqual(ret_val["result_data"][0]["message"], consts.VISION_ERROR_MISSING_UPDATE_PARAMETER)

    def test_update_vision_ai_config_invalid_similarity_level_fail(self):
        """Test the update vision ai config action with an out-of-range 'similarity_level' parameter."""
        self.test_json["parameters"] = [{"similarity_level": 11}]

        ret_val = self.connector._handle_action(json.dumps(self.test_json), None)
        ret_val = json.loads(ret_val)
        self.assertEqual(ret_val["result_summary"]["total_objects"], 1)
        self.assertEqual(ret_val["result_summary"]["total_objects_successful"], 0)
        self.assertEqual(ret_val["status"], "failed")
        self.assertEqual(
            ret_val["result_data"][0]["message"],
            consts.VISION_ERROR_INVALID_RANGE_PARAM.format(
                key="similarity_level", min=consts.VISION_MIN_SIMILARITY_LEVEL, max=consts.VISION_MAX_SIMILARITY_LEVEL
            ),
        )

    def test_update_vision_ai_config_invalid_min_cluster_size_fail(self):
        """Test the update vision ai config action with a 'min_cluster_size' below the allowed minimum."""
        self.test_json["parameters"] = [{"min_cluster_size": 5}]

        ret_val = self.connector._handle_action(json.dumps(self.test_json), None)
        ret_val = json.loads(ret_val)
        self.assertEqual(ret_val["result_summary"]["total_objects"], 1)
        self.assertEqual(ret_val["result_summary"]["total_objects_successful"], 0)
        self.assertEqual(ret_val["status"], "failed")
        self.assertEqual(
            ret_val["result_data"][0]["message"],
            consts.VISION_ERROR_INVALID_MIN_VALUE_PARAM.format(key="min_cluster_size", min=consts.VISION_MIN_CLUSTER_SIZE),
        )

    def test_update_vision_ai_config_invalid_enable_fail(self):
        """Test the update vision ai config action with an invalid 'enable' value list selection."""
        self.test_json["parameters"] = [{"enable": "yes"}]

        ret_val = self.connector._handle_action(json.dumps(self.test_json), None)
        ret_val = json.loads(ret_val)
        self.assertEqual(ret_val["result_summary"]["total_objects"], 1)
        self.assertEqual(ret_val["result_summary"]["total_objects_successful"], 0)
        self.assertEqual(ret_val["status"], "failed")
        self.assertEqual(
            ret_val["result_data"][0]["message"],
            consts.VISION_ERROR_VALUE_LIST.format("enable", ", ".join(consts.VISION_VALID_BOOLEAN_VALUES)),
        )

    def test_update_vision_ai_config_invalid_cluster_match_time_fail(self):
        """Test the update vision ai config action with an out-of-range 'cluster_match_time' parameter."""
        self.test_json["parameters"] = [{"cluster_match_time": 1}]

        ret_val = self.connector._handle_action(json.dumps(self.test_json), None)
        ret_val = json.loads(ret_val)
        self.assertEqual(ret_val["result_summary"]["total_objects"], 1)
        self.assertEqual(ret_val["result_summary"]["total_objects_successful"], 0)
        self.assertEqual(ret_val["status"], "failed")
        self.assertEqual(
            ret_val["result_data"][0]["message"],
            consts.VISION_ERROR_INVALID_RANGE_PARAM.format(
                key="cluster_match_time", min=consts.VISION_MIN_CLUSTER_MATCH_TIME, max=consts.VISION_MAX_CLUSTER_MATCH_TIME
            ),
        )

    def test_update_vision_ai_config_invalid_cluster_rapid_growth_time_fail(self):
        """Test the update vision ai config action with an out-of-range 'cluster_rapid_growth_time' parameter."""
        self.test_json["parameters"] = [{"cluster_rapid_growth_time": 1}]

        ret_val = self.connector._handle_action(json.dumps(self.test_json), None)
        ret_val = json.loads(ret_val)
        self.assertEqual(ret_val["result_summary"]["total_objects"], 1)
        self.assertEqual(ret_val["result_summary"]["total_objects_successful"], 0)
        self.assertEqual(ret_val["status"], "failed")
        self.assertEqual(
            ret_val["result_data"][0]["message"],
            consts.VISION_ERROR_INVALID_RANGE_PARAM.format(
                key="cluster_rapid_growth_time",
                min=consts.VISION_MIN_CLUSTER_RAPID_GROWTH_TIME,
                max=consts.VISION_MAX_CLUSTER_RAPID_GROWTH_TIME,
            ),
        )

    @patch("cofensevision_utils.requests.patch")
    def test_update_vision_ai_config_server_fail(self, mock_patch):
        """Test the update vision ai config action with a server error."""
        cofensevision_config.set_state_file(client_id=True, access_token=True)
        self.test_json["parameters"] = [{"enable": "True"}]

        mock_patch.return_value.status_code = 500
        mock_patch.return_value.headers = cofensevision_config.DEFAULT_HEADERS
        mock_patch.return_value.json.return_value = {"error": "Internal server error"}

        ret_val = self.connector._handle_action(json.dumps(self.test_json), None)
        ret_val = json.loads(ret_val)
        self.assertEqual(ret_val["result_summary"]["total_objects"], 1)
        self.assertEqual(ret_val["result_summary"]["total_objects_successful"], 0)
        self.assertEqual(ret_val["status"], "failed")
        self.assertIn("Error from server. Status code: 500", ret_val["result_data"][0]["message"])

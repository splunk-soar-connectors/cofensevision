# File: test_cofensevision_get_cluster.py
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


class TestGetClusterAction(unittest.TestCase):
    """Class to test the get cluster action."""

    def setUp(self):
        """Set up method for the tests."""
        self.connector = CofenseVisionConnector()
        self.test_json = dict(cofensevision_config.TEST_JSON)
        self.test_json.update({"action": "get cluster", "identifier": "get_cluster"})

        return super().setUp()

    @patch("cofensevision_utils.requests.get")
    def test_get_cluster_pass(self, mock_get):
        """Test the valid case for the get cluster action.

        Token is available in the state file.
        Patch the get() to return the valid response.
        """
        cofensevision_config.set_state_file(client_id=True, access_token=True)
        cluster_id = 2

        self.test_json["parameters"] = [
            {
                consts.VISION_PARAM_CLUSTER_ID: cluster_id,
                "exclude_emails": True,
            }
        ]

        mock_get.return_value.status_code = 200
        mock_get.return_value.headers = cofensevision_config.DEFAULT_HEADERS
        mock_get.return_value.json.return_value = {"id": cluster_id, "title": "Splunk SOAR Test"}

        ret_val = self.connector._handle_action(json.dumps(self.test_json), None)
        ret_val = json.loads(ret_val)
        self.assertEqual(ret_val["result_summary"]["total_objects"], 1)
        self.assertEqual(ret_val["result_summary"]["total_objects_successful"], 1)
        self.assertEqual(ret_val["status"], "success")
        self.assertEqual(ret_val["result_data"][0]["message"], consts.VISION_SUCCESS_GET_CLUSTER_ACTION)

        mock_get.assert_called_with(
            f"{self.test_json['config']['base_url']}{consts.VISION_ENDPOINT_AI_CLUSTER.format(cluster_id=cluster_id)}",
            headers=cofensevision_config.ACTION_HEADER,
            timeout=consts.VISION_REQUEST_TIMEOUT,
            verify=False,
            params={"excludeEmails": True},
        )

    def test_get_cluster_invalid_id_fail(self):
        """Test the get cluster action with invalid 'id' parameter."""
        self.test_json["parameters"] = [{consts.VISION_PARAM_CLUSTER_ID: "non_numeric"}]

        ret_val = self.connector._handle_action(json.dumps(self.test_json), None)
        ret_val = json.loads(ret_val)
        self.assertEqual(ret_val["result_summary"]["total_objects"], 1)
        self.assertEqual(ret_val["result_summary"]["total_objects_successful"], 0)
        self.assertEqual(ret_val["status"], "failed")
        self.assertEqual(ret_val["result_data"][0]["message"], consts.VISION_ERROR_INVALID_INT_PARAM.format(key=consts.VISION_PARAM_CLUSTER_ID))

    @patch("cofensevision_utils.requests.get")
    def test_get_cluster_non_existing_fail(self, mock_get):
        """Test the get cluster action with a valid id, but the cluster does not exist."""
        cofensevision_config.set_state_file(client_id=True, access_token=True)
        cluster_id = 2

        self.test_json["parameters"] = [{consts.VISION_PARAM_CLUSTER_ID: cluster_id}]

        response_json = {"status": "NOT_FOUND", "message": "Object not found", "details": ["Unable to find the requested object"]}

        mock_get.return_value.status_code = 404
        mock_get.return_value.headers = cofensevision_config.DEFAULT_HEADERS
        mock_get.return_value.json.return_value = response_json
        mock_get.return_value.text = json.dumps(response_json)

        ret_val = self.connector._handle_action(json.dumps(self.test_json), None)
        ret_val = json.loads(ret_val)
        self.assertEqual(ret_val["result_summary"]["total_objects"], 1)
        self.assertEqual(ret_val["result_summary"]["total_objects_successful"], 0)
        self.assertEqual(ret_val["status"], "failed")
        self.assertIn("Status code: 404", ret_val["result_data"][0]["message"])

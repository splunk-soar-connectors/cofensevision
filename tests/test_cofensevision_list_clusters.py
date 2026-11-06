# File: test_cofensevision_list_clusters.py
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


class TestListClustersAction(unittest.TestCase):
    """Class to test the list clusters action."""

    def setUp(self):
        """Set up method for the tests."""
        self.connector = CofenseVisionConnector()
        self.test_json = dict(cofensevision_config.TEST_JSON)
        self.test_json.update({"action": "list clusters", "identifier": "list_clusters"})

        return super().setUp()

    @patch("cofensevision_utils.requests.get")
    def test_list_clusters_pass(self, mock_get):
        """Test the valid case for the list clusters action.

        Token is available in the state file.
        Patch the get() to return the valid response.
        """
        cofensevision_config.set_state_file(client_id=True, access_token=True)

        self.test_json["parameters"] = [
            {
                "page": 1,
                "size": 100,
                "sort_field": "createdDate",
                "order": "desc",
                "exclude_emails": False,
                "from_date": "2024-05-31T00:00:00.000Z",
                "to_date": "2024-06-07T00:00:00.000Z",
            }
        ]

        mock_get.return_value.status_code = 200
        mock_get.return_value.headers = cofensevision_config.DEFAULT_HEADERS
        mock_get.return_value.json.return_value = {"clusters": [{"id": 1}, {"id": 2}]}

        ret_val = self.connector._handle_action(json.dumps(self.test_json), None)
        ret_val = json.loads(ret_val)
        self.assertEqual(ret_val["result_summary"]["total_objects"], 1)
        self.assertEqual(ret_val["result_summary"]["total_objects_successful"], 1)
        self.assertEqual(ret_val["status"], "success")
        self.assertEqual(ret_val["result_data"][0]["message"], "Total clusters: 2")

        expected_params = {
            "page": 1,
            "size": 100,
            "excludeEmails": False,
            "sort": "createdDate,desc",
            "fromDateTime": "2024-05-31T00:00:00.000Z",
            "toDateTime": "2024-06-07T00:00:00.000Z",
        }
        mock_get.assert_called_with(
            f"{self.test_json['config']['base_url']}{consts.VISION_ENDPOINT_AI_CLUSTERS}",
            headers=cofensevision_config.ACTION_HEADER,
            timeout=consts.VISION_REQUEST_TIMEOUT,
            verify=False,
            params=expected_params,
        )

    def test_list_clusters_invalid_page_fail(self):
        """Test the list clusters action with invalid 'page' parameter."""
        self.test_json["parameters"] = [{"page": "non_numeric"}]

        ret_val = self.connector._handle_action(json.dumps(self.test_json), None)
        ret_val = json.loads(ret_val)
        self.assertEqual(ret_val["result_summary"]["total_objects"], 1)
        self.assertEqual(ret_val["result_summary"]["total_objects_successful"], 0)
        self.assertEqual(ret_val["status"], "failed")
        self.assertEqual(ret_val["result_data"][0]["message"], "Please provide a valid integer value in the 'page' parameter")

    def test_list_clusters_invalid_sort_field_fail(self):
        """Test the list clusters action with an invalid 'sort_field' parameter."""
        self.test_json["parameters"] = [{"sort_field": "invalidField"}]

        ret_val = self.connector._handle_action(json.dumps(self.test_json), None)
        ret_val = json.loads(ret_val)
        self.assertEqual(ret_val["result_summary"]["total_objects"], 1)
        self.assertEqual(ret_val["result_summary"]["total_objects_successful"], 0)
        self.assertEqual(ret_val["status"], "failed")
        self.assertEqual(
            ret_val["result_data"][0]["message"],
            consts.VISION_ERROR_VALUE_LIST.format("sort_field", ", ".join(consts.VISION_CLUSTER_SORT_FIELDS)),
        )

    def test_list_clusters_invalid_order_fail(self):
        """Test the list clusters action with an invalid 'order' parameter."""
        self.test_json["parameters"] = [{"order": "invalid"}]

        ret_val = self.connector._handle_action(json.dumps(self.test_json), None)
        ret_val = json.loads(ret_val)
        self.assertEqual(ret_val["result_summary"]["total_objects"], 1)
        self.assertEqual(ret_val["result_summary"]["total_objects_successful"], 0)
        self.assertEqual(ret_val["status"], "failed")
        self.assertEqual(
            ret_val["result_data"][0]["message"],
            consts.VISION_ERROR_VALUE_LIST.format("order", ", ".join(consts.VISION_VALID_SORT_ORDER)),
        )

    def test_list_clusters_invalid_from_date_fail(self):
        """Test the list clusters action with an invalid 'from_date' parameter."""
        self.test_json["parameters"] = [{"from_date": "2024-05-31"}]

        ret_val = self.connector._handle_action(json.dumps(self.test_json), None)
        ret_val = json.loads(ret_val)
        self.assertEqual(ret_val["result_summary"]["total_objects"], 1)
        self.assertEqual(ret_val["result_summary"]["total_objects_successful"], 0)
        self.assertEqual(ret_val["status"], "failed")
        self.assertEqual(ret_val["result_data"][0]["message"], consts.VISION_ERROR_INVALID_ISO8601_UTC_DATE.format("from_date"))

    def test_list_clusters_invalid_to_date_fail(self):
        """Test the list clusters action with an invalid 'to_date' parameter."""
        self.test_json["parameters"] = [{"to_date": "invalid_date"}]

        ret_val = self.connector._handle_action(json.dumps(self.test_json), None)
        ret_val = json.loads(ret_val)
        self.assertEqual(ret_val["result_summary"]["total_objects"], 1)
        self.assertEqual(ret_val["result_summary"]["total_objects_successful"], 0)
        self.assertEqual(ret_val["status"], "failed")
        self.assertEqual(ret_val["result_data"][0]["message"], consts.VISION_ERROR_INVALID_ISO8601_UTC_DATE.format("to_date"))

    def test_list_clusters_from_date_after_to_date_fail(self):
        """Test the list clusters action when 'from_date' is later than 'to_date'."""
        self.test_json["parameters"] = [{"from_date": "2024-06-07T00:00:00.000Z", "to_date": "2024-05-31T00:00:00.000Z"}]

        ret_val = self.connector._handle_action(json.dumps(self.test_json), None)
        ret_val = json.loads(ret_val)
        self.assertEqual(ret_val["result_summary"]["total_objects"], 1)
        self.assertEqual(ret_val["result_summary"]["total_objects_successful"], 0)
        self.assertEqual(ret_val["status"], "failed")
        self.assertEqual(ret_val["result_data"][0]["message"], consts.VISION_ERROR_FROM_DATE_AFTER_TO_DATE.format("from_date", "to_date"))

    @patch("cofensevision_utils.requests.get")
    def test_list_clusters_no_clusters_pass(self, mock_get):
        """Test the list clusters action when the API returns a valid but empty list of clusters (200 [])."""
        cofensevision_config.set_state_file(client_id=True, access_token=True)
        self.test_json["parameters"] = [{}]

        mock_get.return_value.status_code = 200
        mock_get.return_value.headers = cofensevision_config.DEFAULT_HEADERS
        mock_get.return_value.json.return_value = []

        ret_val = self.connector._handle_action(json.dumps(self.test_json), None)
        ret_val = json.loads(ret_val)
        self.assertEqual(ret_val["result_summary"]["total_objects"], 1)
        self.assertEqual(ret_val["result_summary"]["total_objects_successful"], 1)
        self.assertEqual(ret_val["status"], "success")
        self.assertEqual(ret_val["result_data"][0]["message"], consts.VISION_SUCCESS_LIST_CLUSTERS_ACTION.format(0))

    @patch("cofensevision_utils.requests.get")
    def test_list_clusters_empty_response_fail(self, mock_get):
        """Test the list clusters action with an empty response."""
        cofensevision_config.set_state_file(client_id=True, access_token=True)
        self.test_json["parameters"] = [{}]

        mock_get.return_value.status_code = 200
        mock_get.return_value.headers = {}
        mock_get.return_value.text = ""

        ret_val = self.connector._handle_action(json.dumps(self.test_json), None)
        ret_val = json.loads(ret_val)
        self.assertEqual(ret_val["result_summary"]["total_objects"], 1)
        self.assertEqual(ret_val["result_summary"]["total_objects_successful"], 0)
        self.assertEqual(ret_val["status"], "failed")
        self.assertEqual(ret_val["result_data"][0]["message"], consts.VISION_ERROR_ACTION_EMPTY_RESPONSE)

    @patch("cofensevision_utils.requests.get")
    def test_list_clusters_server_fail(self, mock_get):
        """Test the list clusters action with a server error."""
        cofensevision_config.set_state_file(client_id=True, access_token=True)
        self.test_json["parameters"] = [{}]

        mock_get.return_value.status_code = 500
        mock_get.return_value.headers = cofensevision_config.DEFAULT_HEADERS
        mock_get.return_value.json.return_value = {"error": "Internal server error"}

        ret_val = self.connector._handle_action(json.dumps(self.test_json), None)
        ret_val = json.loads(ret_val)
        self.assertEqual(ret_val["result_summary"]["total_objects"], 1)
        self.assertEqual(ret_val["result_summary"]["total_objects_successful"], 0)
        self.assertEqual(ret_val["status"], "failed")
        self.assertIn("Error from server. Status code: 500", ret_val["result_data"][0]["message"])

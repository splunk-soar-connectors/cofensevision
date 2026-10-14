# File: cofensevision_utils.py
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


import os
import re
import time
import urllib.parse
import uuid
from collections import OrderedDict
from datetime import datetime, timedelta, timezone

import encryption_helper
import phantom.app as phantom
import phantom.rules as phantom_rules
import requests
from bs4 import BeautifulSoup
from dateutil.parser import parse
from phantom.vault import Vault

import cofensevision_consts as consts


class RetVal(tuple):
    """This class returns the tuple of two elements."""

    def __new__(cls, val1, val2=None):
        """Create a new tuple object."""
        return tuple.__new__(RetVal, (val1, val2))


class CofenseVisionUtils:
    """This class holds all the util methods."""

    def __init__(self, connector=None):
        """Util constructor method."""
        self._connector = connector
        self._access_token = None
        self.filename = None

        # The response from the 'get message' action comes as plain text with an application/json header.
        # These variables are used to process a response for this peculiar API behavior.
        self._get_token = False
        self._is_generate_token = False

        if connector:
            # Decrypt the state file
            connector.state = self._decrypt_state(connector.state)
            self._access_token = connector.state.get(consts.VISION_STATE_TOKEN, {}).get(consts.VISION_STATE_ACCESS_TOKEN)

    def _get_error_message_from_exception(self, e):
        """Get an appropriate error message from the exception.

        :param e: Exception object
        :return: error message
        """
        error_code = None
        error_msg = consts.VISION_ERROR_MESSAGE_UNAVAILABLE

        self._connector.error_print("Error occurred.", e)
        try:
            if hasattr(e, "args"):
                if len(e.args) > 1:
                    error_code = e.args[0]
                    error_msg = e.args[1]
                elif len(e.args) == 1:
                    error_msg = e.args[0]
        except Exception as e:
            self._connector.error_print(f"Error occurred while fetching exception information. Details: {e!s}")

        if not error_code:
            error_text = f"Error message: {error_msg}"
        else:
            error_text = f"Error code: {error_code}. Error message: {error_msg}"

        return error_text

    # Validations
    @staticmethod
    def is_valid_ioc_id(value):
        """Return whether a value is a 32-character hexadecimal IOC identifier."""
        return isinstance(value, str) and re.fullmatch(r"[0-9a-fA-F]{32}", value) is not None

    def validate_integer(self, action_result, parameter, key, allow_zero=False, max_value=None):
        """Check if the provided input parameter value is valid.

        :param action_result: Action result or BaseConnector object
        :param parameter: Input parameter value
        :param key: Input parameter key
        :param allow_zero: Zero is allowed or not (default False)
        :param max_value: Maximum allowed value
        :returns: phantom.APP_SUCCESS/phantom.APP_ERROR and parameter value itself.
        """
        try:
            if not float(parameter).is_integer():
                return action_result.set_status(phantom.APP_ERROR, consts.VISION_ERROR_INVALID_INT_PARAM.format(key=key)), None

            parameter = int(parameter)
        except Exception:
            return action_result.set_status(phantom.APP_ERROR, consts.VISION_ERROR_INVALID_INT_PARAM.format(key=key)), None

        if parameter < 0:
            return action_result.set_status(phantom.APP_ERROR, consts.VISION_ERROR_NEGATIVE_INT_PARAM.format(key=key)), None
        if not allow_zero and parameter == 0:
            return action_result.set_status(phantom.APP_ERROR, consts.VISION_ERROR_ZERO_INT_PARAM.format(key=key)), None
        if max_value and parameter > max_value:
            return action_result.set_status(phantom.APP_ERROR, consts.VISION_ERROR_MAX_ALLOWED_INT_PARAM.format(max=max_value, key=key)), None

        return phantom.APP_SUCCESS, parameter

    def validate_ranged_integer(self, action_result, parameter, key, min_value=None, max_value=None):
        """Check if the provided input parameter value is a valid integer within an inclusive range.

        :param action_result: Action result or BaseConnector object
        :param parameter: Input parameter value
        :param key: Input parameter key
        :param min_value: Minimum allowed value (inclusive), may be negative
        :param max_value: Maximum allowed value (inclusive)
        :returns: phantom.APP_SUCCESS/phantom.APP_ERROR and parameter value itself.
        """
        try:
            if not float(parameter).is_integer():
                return action_result.set_status(phantom.APP_ERROR, consts.VISION_ERROR_INVALID_INT_PARAM.format(key=key)), None

            parameter = int(parameter)
        except Exception:
            return action_result.set_status(phantom.APP_ERROR, consts.VISION_ERROR_INVALID_INT_PARAM.format(key=key)), None

        if max_value is not None and (parameter < (min_value if min_value is not None else parameter) or parameter > max_value):
            return action_result.set_status(
                phantom.APP_ERROR, consts.VISION_ERROR_INVALID_RANGE_PARAM.format(key=key, min=min_value, max=max_value)
            ), None

        if max_value is None and min_value is not None and parameter < min_value:
            return action_result.set_status(phantom.APP_ERROR, consts.VISION_ERROR_INVALID_MIN_VALUE_PARAM.format(key=key, min=min_value)), None

        return phantom.APP_SUCCESS, parameter

    def validate_boolean(self, action_result, parameter, key):
        """Check if the provided input parameter is a valid 'True'/'False' value list selection.

        :param action_result: Action result or BaseConnector object
        :param parameter: Input parameter value
        :param key: Input parameter key
        :returns: phantom.APP_SUCCESS/phantom.APP_ERROR and the parameter converted to a boolean.
        """
        if parameter not in consts.VISION_VALID_BOOLEAN_VALUES:
            return action_result.set_status(
                phantom.APP_ERROR, consts.VISION_ERROR_VALUE_LIST.format(key, ", ".join(consts.VISION_VALID_BOOLEAN_VALUES))
            ), None

        return phantom.APP_SUCCESS, parameter == "True"

    # Parsing
    def _process_empty_response(self, response, action_result):
        """Process the empty response returned from the server.

        :param response: requests.Response object
        :param action_result: Action result or BaseConnector object
        :returns: phantom.APP_SUCCESS/phantom.APP_ERROR and an empty dictionary
        """
        if response.status_code in [200, 204]:
            return RetVal(phantom.APP_SUCCESS, {})

        return RetVal(action_result.set_status(phantom.APP_ERROR, consts.VISION_ERROR_EMPTY_RESPONSE.format(response.status_code)))

    def _process_html_response(self, response, action_result):
        """Process the html response returned from the server.

        :param response: requests.Response object
        :param action_result: Action result or BaseConnector object
        :returns: phantom.APP_ERROR and the None value
        """
        # An html response, treat it like an error
        status_code = response.status_code

        try:
            soup = BeautifulSoup(response.text, "html.parser")
            # Remove the script, style, footer and navigation part from the HTML message
            for element in soup(["script", "style", "footer", "nav"]):
                element.extract()
            error_text = soup.text
            split_lines = error_text.split("\n")
            split_lines = [x.strip() for x in split_lines if x.strip()]
            error_text = "\n".join(split_lines)
        except Exception:
            error_text = "Cannot parse error details"

        message = consts.VISION_ERROR_GENERAL_MESSAGE.format(status_code, error_text)
        message = message.replace("{", "{{").replace("}", "}}")

        # Large HTML pages may be returned by the wrong URLs.
        # Use default error message in place of large HTML page.
        if len(message) > 500:
            return RetVal(action_result.set_status(phantom.APP_ERROR, consts.VISION_ERROR_HTML_RESPONSE))

        return RetVal(action_result.set_status(phantom.APP_ERROR, message))

    def _process_json_response(self, response, action_result):
        """Process the json response returned from the server.

        :param response: requests.Response object
        :param action_result: Action result or BaseConnector object
        :returns: phantom.APP_SUCCESS/phantom.APP_ERROR and the response dictionary
        """
        try:
            # Token endpoint doesn't return json response
            if self._get_token and not self._is_generate_token:
                resp_json = {"token": response.text}
            else:
                resp_json = response.json()
        except Exception as e:
            error_message = self._get_error_message_from_exception(e)
            return RetVal(action_result.set_status(phantom.APP_ERROR, consts.VISION_ERROR_JSON_RESPONSE.format(error_message)))

        # Please specify the status codes here
        if 200 <= response.status_code < 399:
            return RetVal(phantom.APP_SUCCESS, resp_json)

        # You should process the error returned in the json
        message = consts.VISION_ERROR_GENERAL_MESSAGE.format(response.status_code, response.text.replace("{", "{{").replace("}", "}}"))
        message = f"Error from server. {message}"

        return RetVal(action_result.set_status(phantom.APP_ERROR, message))

    def _add_file_to_vault(self, action_result, local_dir, long_filename=None):
        """Add the file to the Vault.

        :param action_result: Action result or BaseConnector object
        :param local_dir: Directory where the file to be saved is stored
        param long_filename: Long filename of the file
        :returns: phantom.APP_SUCCESS/phantom.APP_ERROR and the vault information
        """
        container_id = self._connector.get_container_id()
        file_name = long_filename or self.filename
        vault_file = None

        # Add file to the vault
        self._connector.debug_print("Adding file to the Vault")
        success, message, vault_id = phantom_rules.vault_add(
            container=container_id, file_location=f"{local_dir}/{self.filename}", file_name=file_name
        )

        if not success:
            return RetVal(action_result.set_status(phantom.APP_ERROR, f"Could not add file to the Vault: {message}"))

        self._connector.debug_print("Added file to the Vault")

        # Retrieve stored file information
        success, message, vault_info = phantom_rules.vault_info(vault_id, container_id=container_id)

        if not (success or vault_info):
            return RetVal(action_result.set_status(phantom.APP_ERROR, f"Could not find the file in the Vault: {message}"))

        # Find the file with the current filename from the list of files having the same ID
        for file in vault_info:
            if file.get("name") == file_name:
                vault_file = file
                break

        # Cleanup temp dir
        try:
            self._connector.debug_print("Deleting temporary directory")
            if os.path.exists(local_dir):
                os.rmdir(local_dir)
        except Exception as e:
            self._connector.debug_print(f"Unable to delete the temporary directory: {self._get_error_message_from_exception(e)}")

        if vault_file:
            return RetVal(phantom.APP_SUCCESS, vault_file)

        return RetVal(action_result.set_status(phantom.APP_ERROR, "Could not find the file in the Vault"))

    def _process_stream_response(self, response, action_result):
        """Process the stream response returned from the server, saves it to a file and adds it to the vault.

        :param response: requests.Response object
        :param action_result: Action result or BaseConnector object
        :returns: phantom.APP_SUCCESS/phantom.APP_ERROR and vault info
        """
        long_filename = None
        if not (200 <= response.status_code < 399):
            message = consts.VISION_ERROR_GENERAL_MESSAGE.format(response.status_code, response.text.replace("{", "{{").replace("}", "}}"))
            message = f"Error from server. {message}"

            return RetVal(action_result.set_status(phantom.APP_ERROR, message))

        guid = uuid.uuid4()

        if hasattr(Vault, "get_vault_tmp_dir"):
            vault_tmp_dir = Vault.get_vault_tmp_dir().rstrip("/")
            local_dir = f"{vault_tmp_dir}/{guid}"
        else:
            local_dir = f"/opt/phantom/vault/tmp/{guid}"

        self._connector.debug_print("Creating temporary vault directory")

        try:
            os.makedirs(local_dir)
        except Exception as e:
            return RetVal(
                action_result.set_status(
                    phantom.APP_ERROR, f"Unable to create temporary Vault folder {self._get_error_message_from_exception(e)}"
                )
            )

        if len(self.filename) >= 255:
            long_filename, ext = os.path.splitext(self.filename)
            self.filename = f"{uuid.uuid4()}{ext}"

        file_path = f"{local_dir}/{self.filename}"

        # Save the stream response to the file
        try:
            with open(file_path, "wb") as f:
                self._connector.debug_print("Writing data to the file")
                for chunk in response.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        f.write(chunk)
        except Exception as e:
            return RetVal(
                action_result.set_status(phantom.APP_ERROR, f"Unable to write file to disk. Error: {self._get_error_message_from_exception(e)}"),
                None,
            )

        return self._add_file_to_vault(action_result, local_dir, long_filename)

    def _process_response(self, response, action_result):
        """Process the response returned from the server.

        :param response: requests.Response object
        :param action_result: Action result or BaseConnector object
        :returns: phantom.APP_SUCCESS/phantom.APP_ERROR and the response dictionary
        """
        # store the r_text in debug data, it will get dumped in the logs if the action fails
        if hasattr(action_result, "add_debug_data"):
            action_result.add_debug_data({"r_status_code": response.status_code})
            action_result.add_debug_data({"r_headers": response.headers})
            if "stream" not in response.headers.get("Content-Type", ""):
                action_result.add_debug_data({"r_text": response.text})

        # Process each 'Content-Type' of response separately
        # Process a json response
        if "json" in response.headers.get("Content-Type", ""):
            return self._process_json_response(response, action_result)

        # Process an HTML response, Do this no matter what the api talks.
        # There is a high chance of a PROXY in between phantom and the rest of
        # world, in case of errors, PROXY's return HTML, this function parses
        # the error and adds it to the action_result.
        if "html" in response.headers.get("Content-Type", ""):
            return self._process_html_response(response, action_result)

        # Process file response
        if "stream" in response.headers.get("Content-Type", ""):
            return self._process_stream_response(response, action_result)

        # it's not content-type that is to be parsed, handle an empty response
        if not response.text:
            return self._process_empty_response(response, action_result)

        # everything else is actually an error at this point
        message = consts.VISION_ERROR_GENERAL_MESSAGE.format(response.status_code, response.text.replace("{", "{{").replace("}", "}}"))
        message = f"Can't process response from server. {message}"

        return RetVal(action_result.set_status(phantom.APP_ERROR, message))

    def make_rest_call(self, endpoint, action_result, method="get", **kwargs):
        """Make an REST API call and passes the response to the process method.

        :param endpoint: The endpoint string to make the REST API request
        :param action_result: Action result or BaseConnector object
        :param method: The HTTP method for API request
        :returns: phantom.APP_SUCCESS/phantom.APP_ERROR and the response dictionary returned by the process response method
        """
        try:
            request_func = getattr(requests, method)
        except AttributeError:
            return RetVal(action_result.set_status(phantom.APP_ERROR, f"Invalid method: {method}"))

        # Create a URL to connect to
        url = f"{self._connector.config['base_url'].rstrip('/')}{endpoint}"

        response = None
        max_retries = consts.VISION_DEFAULT_MAX_RETRIES
        for attempt in range(max_retries + 1):
            try:
                response = request_func(
                    url, timeout=consts.VISION_REQUEST_TIMEOUT, verify=self._connector.config.get("verify_server_cert", True), **kwargs
                )
            except Exception as e:
                error_message = self._get_error_message_from_exception(e)
                return RetVal(action_result.set_status(phantom.APP_ERROR, consts.VISION_ERROR_REST_CALL.format(error_message)))

            retryable = response.status_code in consts.VISION_RETRYABLE_STATUS_CODES
            if not retryable or attempt == max_retries:
                break

            wait_time = consts.VISION_DEFAULT_RETRY_WAIT_TIME * (2**attempt)
            if response.status_code == 429:
                retry_after = response.headers.get("Retry-After")
                if retry_after:
                    try:
                        wait_time = float(retry_after)
                    except (TypeError, ValueError):
                        pass
                wait_time = min(wait_time, consts.VISION_MAX_RETRY_WAIT_TIME)

            self._connector.debug_print(
                f"Received status code {response.status_code} from the server. "
                f"Retrying in {wait_time} seconds (attempt {attempt + 1} of {max_retries})"
            )
            time.sleep(wait_time)

        return self._process_response(response, action_result)

    def _set_is_generate_token(func):
        """Set the flags for the generate token method."""

        def inner_func(self, action_result):
            self._is_generate_token = True
            self._connector.is_state_updated = True
            ret_val = func(self, action_result)
            self._is_generate_token = False
            return ret_val

        return inner_func

    @_set_is_generate_token
    def generate_token(self, action_result):
        """Generate a new access token using the provided credentials and stores it to the state file.

        :param action_result: Action result or BaseConnector object
        :returns: phantom.APP_SUCCESS/phantom.APP_ERROR
        """
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        data = {
            "client_id": self._connector.config["client_id"],
            "client_secret": self._connector.config["client_secret"],
            "grant_type": "client_credentials",
        }

        ret_val, resp_json = self.make_rest_call(consts.VISION_ENDPOINT_TOKEN, action_result, data=data, method="post", headers=headers)
        if phantom.is_fail(ret_val):
            self._connector.state.pop(consts.VISION_STATE_TOKEN, None)
            return action_result.get_status()

        # Reset the header with authorization key
        try:
            self._access_token = resp_json[consts.VISION_STATE_ACCESS_TOKEN]
        except KeyError:
            self._connector.debug_print("Unable to find the access token from the returned response")
            self._connector.state.pop(consts.VISION_STATE_TOKEN, None)
            return action_result.set_status(phantom.APP_ERROR, "Token generation failed")

        self._connector.state[consts.VISION_STATE_TOKEN] = resp_json
        self._connector.state[consts.VISION_STATE_TOKEN][consts.VISION_STATE_TOKEN_GENERATED_AT] = time.time()

        self._connector.debug_print("Token generated successfully")
        return action_result.set_status(phantom.APP_SUCCESS)

    def _is_token_expired(self):
        """Check whether the stored access token has expired (or is about to), using the state file's expiry metadata.

        This is used as a proactive, independent check in addition to `_is_token_error_message`, so that a token
        can be refreshed ahead of time even if a future error format isn't recognized as a token error.

        :return: True if the token is expired or near expiry, False if it is still valid or the metadata is missing
        """
        token_state = self._connector.state.get(consts.VISION_STATE_TOKEN, {})
        generated_at = token_state.get(consts.VISION_STATE_TOKEN_GENERATED_AT)
        expires_in = token_state.get(consts.VISION_STATE_EXPIRES_IN)

        if generated_at is None or expires_in is None:
            return False

        try:
            expires_in = float(expires_in)
        except (TypeError, ValueError):
            return False

        return time.time() >= (generated_at + expires_in - consts.VISION_TOKEN_EXPIRY_BUFFER_SECONDS)

    @staticmethod
    def _is_token_error_message(message):
        """Check whether an error message indicates an authentication/token problem.

        Cofense Vision has been observed to report an expired/invalid token using different error formats
        (e.g. 'invalid_token', or {"error": "invalid_client", "error_description": "Bad credentials"}), so this
        checks for any of several known keywords instead of a single exact string.

        :param message: error message string to check
        :return: True if the message indicates a token/auth error, False otherwise
        """
        if not message:
            return False

        message = message.lower()
        return any(keyword in message for keyword in consts.VISION_TOKEN_ERROR_KEYWORDS)

    def make_rest_call_helper(self, endpoint, action_result, method="get", headers=None, **kwargs):
        """Make the REST API call and generates new token if required.

        :param endpoint: The endpoint string to make the REST API request
        :param action_result: Action result or BaseConnector object
        :param method: The HTTP method for API request
        :returns: phantom.APP_SUCCESS/phantom.APP_ERROR and the response dictionary
        """
        if not headers or not isinstance(headers, dict):
            headers = dict(consts.VISION_DEFAULT_HEADERS)
        else:
            headers.update(consts.VISION_DEFAULT_HEADERS)

        if kwargs.get("stream"):
            headers.pop("Accept", None)

        if self._access_token and self._is_token_expired():
            self._connector.debug_print("Token has expired based on the state file's expiry information. Hence, generating a new token.")
            self._access_token = None

        if self._access_token:
            headers.update({"Authorization": f"Bearer {self._access_token}"})
            ret_val, resp_json = self.make_rest_call(endpoint, action_result, method, headers=headers, **kwargs)
            if phantom.is_success(ret_val):
                return RetVal(phantom.APP_SUCCESS, resp_json)
            if not self._is_token_error_message(action_result.get_message()):
                return RetVal(action_result.get_status())
            self._connector.debug_print("Token is invalid/expired. Hence, generating a new token.")
        else:
            self._connector.debug_print("Token is not available. Hence, generating a new token.")

        # The token is either expired or not present in the state file, generate a new token.
        ret_val = self.generate_token(action_result)
        if phantom.is_fail(ret_val):
            return RetVal(action_result.get_status())

        headers.update({"Authorization": f"Bearer {self._access_token}"})
        ret_val, resp_json = self.make_rest_call(endpoint, action_result, method, headers=headers, **kwargs)
        if phantom.is_fail(ret_val):
            return RetVal(action_result.get_status())

        return RetVal(phantom.APP_SUCCESS, resp_json)

    def encrypt_state(self, state):
        """Encrypt the state file.

        :param state: state dictionary to be encrypted
        :return: state dictionary with encrypted token
        """
        try:
            if state.get(consts.VISION_STATE_TOKEN, {}).get(consts.VISION_STATE_ACCESS_TOKEN):
                state[consts.VISION_STATE_TOKEN][consts.VISION_STATE_ACCESS_TOKEN] = encryption_helper.encrypt(
                    state[consts.VISION_STATE_TOKEN][consts.VISION_STATE_ACCESS_TOKEN], self._connector.get_asset_id()
                )
        except Exception as e:
            self._connector.debug_print("Error occurred while encrypting the state file.", e)
            state.pop(consts.VISION_STATE_TOKEN, None)
        return state

    def _decrypt_state(self, state):
        """Decrypt the state file.

        :param state: state dictionary to be decrypted
        :return: state dictionary with decrypted token
        """
        try:
            if state.get(consts.VISION_STATE_TOKEN, {}).get(consts.VISION_STATE_ACCESS_TOKEN):
                state[consts.VISION_STATE_TOKEN][consts.VISION_STATE_ACCESS_TOKEN] = encryption_helper.decrypt(
                    state[consts.VISION_STATE_TOKEN][consts.VISION_STATE_ACCESS_TOKEN], self._connector.get_asset_id()
                )
        except Exception as e:
            self._connector.debug_print("Error occurred while decrypting the state file.", e)
            state.pop(consts.VISION_STATE_TOKEN, None)
        return state

    def split_value_list(self, values, delimiter=","):
        """Separate values with the provided delimiter.

        :param values: string value to split
        :param delimiter: delimiter to split with
        :return: list of separated values
        """
        values = [value.strip() for value in values.split(delimiter)]
        values = list(filter(None, values))
        # Remove duplicates by preserving the order
        values = list(OrderedDict.fromkeys(values))
        return values

    def parse_date_string(self, value, default_value=False):
        """Parse the date and converts it to the specified format.

        :param values: string value to parse
        :param default_value: Boolean to return the default value if not provided
        :return: phantom.APP_SUCCESS/phantom.APP_ERROR and parsed date
        """
        if not value:
            if default_value:
                return phantom.APP_SUCCESS, datetime.now(timezone.utc).strftime(consts.VISION_DATE_FORMAT)
            return phantom.APP_SUCCESS, None
        try:
            date = parse(value)
            return phantom.APP_SUCCESS, date.strftime(consts.VISION_DATE_FORMAT)
        except Exception:
            return phantom.APP_ERROR, None

    def validate_iso8601_utc_date(self, action_result, value, key):
        """Validate that the value is a UTC date/time string in ISO 8601 format (YYYY-MM-DDTHH:MM:SS.sssZ).

        :param action_result: Action result or BaseConnector object
        :param value: date string to validate
        :param key: input parameter key, used in the error message
        :return: phantom.APP_SUCCESS/phantom.APP_ERROR and the parsed datetime object (None if value is empty)
        """
        if not value:
            return phantom.APP_SUCCESS, None

        if not re.fullmatch(consts.VISION_ISO8601_UTC_DATE_REGEX, value):
            return action_result.set_status(phantom.APP_ERROR, consts.VISION_ERROR_INVALID_ISO8601_UTC_DATE.format(key)), None

        try:
            parsed_date = datetime.strptime(value, consts.VISION_ISO8601_UTC_DATE_FORMAT)
        except ValueError:
            return action_result.set_status(phantom.APP_ERROR, consts.VISION_ERROR_INVALID_ISO8601_UTC_DATE.format(key)), None

        return phantom.APP_SUCCESS, parsed_date

    def validate_date_range(self, action_result, from_date, from_key, to_date, to_key):
        """Validate the from/to date parameters are valid UTC ISO 8601 dates and that from_date is not after to_date.

        :param action_result: Action result or BaseConnector object
        :param from_date: from date string (may be empty)
        :param from_key: input parameter key for from_date, used in error messages
        :param to_date: to date string (may be empty)
        :param to_key: input parameter key for to_date, used in error messages
        :return: phantom.APP_SUCCESS/phantom.APP_ERROR and a (from_date, to_date) tuple of the original values
        """
        ret_val, parsed_from_date = self.validate_iso8601_utc_date(action_result, from_date, from_key)
        if phantom.is_fail(ret_val):
            return action_result.get_status(), None

        ret_val, parsed_to_date = self.validate_iso8601_utc_date(action_result, to_date, to_key)
        if phantom.is_fail(ret_val):
            return action_result.get_status(), None

        if parsed_from_date and parsed_to_date and parsed_from_date > parsed_to_date:
            return action_result.set_status(phantom.APP_ERROR, consts.VISION_ERROR_FROM_DATE_AFTER_TO_DATE.format(from_key, to_key)), None

        return phantom.APP_SUCCESS, (from_date or None, to_date or None)

    def validate_sort_param(self, values):
        """Parse the sort parameter and converts it to the required format.

        :param values: string value to parse
        :return: phantom.APP_SUCCESS/phantom.APP_ERROR and list of sort order
        """
        if not values:
            return phantom.APP_SUCCESS, None

        sort_fields = consts.VISION_SUPPORTED_SORT_FIELDS.get(self._connector.get_action_identifier(), [])
        final_list = []
        value_list = self.split_value_list(values)
        for value in value_list:
            sort_property = self.split_value_list(value, ":")
            if len(sort_property) == 1:
                if sort_property[0] not in sort_fields:
                    return phantom.APP_ERROR, None
            elif len(sort_property) == 2:
                if sort_property[0] not in sort_fields:
                    return phantom.APP_ERROR, None
                if sort_property[1] not in consts.VISION_VALID_SORT_ORDER:
                    return phantom.APP_ERROR, None
            else:
                return phantom.APP_ERROR, None
            final_list.append(",".join(sort_property))

        return phantom.APP_SUCCESS, final_list

    def extract_list_field(self, action_result, response, key):
        """Extract a list field from a response dictionary.

        A missing or non-list field indicates the response is not in the expected shape, and is
        treated as an error instead of being silently reported as a successful, empty result.

        :param action_result: Action result or BaseConnector object
        :param response: response dictionary
        :param key: key expected to hold a list of items
        :return: phantom.APP_SUCCESS/phantom.APP_ERROR and the list value
        """
        if not isinstance(response, dict) or not isinstance(response.get(key), list):
            return action_result.set_status(phantom.APP_ERROR, consts.VISION_ERROR_UNEXPECTED_RESPONSE_FORMAT), None

        return phantom.APP_SUCCESS, response[key]

    @staticmethod
    def quote_path_segment(value):
        """Encode an untrusted value as one URL path segment."""
        return urllib.parse.quote(str(value), safe="")

    @staticmethod
    def format_datetime(value):
        """Convert a datetime object into the millisecond precision UTC string expected by the Vision APIs.

        :param value: naive UTC datetime object
        :return: formatted date string
        """
        return f"{value.strftime(consts.VISION_ON_POLL_DATE_FORMAT)[:-3]}Z"

    def parse_start_time(self, value):
        """Parse a relative (1d, 6h) or an absolute date value into the Vision API date string.

        :param value: relative or absolute date value
        :return: phantom.APP_SUCCESS/phantom.APP_ERROR and the formatted date
        """
        value = str(value).strip()
        relative_time = re.fullmatch(consts.VISION_RELATIVE_TIME_REGEX, value, re.IGNORECASE)
        if relative_time:
            count = int(relative_time.group(1))
            if not count:
                return phantom.APP_ERROR, None
            unit = consts.VISION_RELATIVE_TIME_UNITS[relative_time.group(2).lower()]
            now = datetime.now(timezone.utc).replace(tzinfo=None)
            try:
                return phantom.APP_SUCCESS, self.format_datetime(now - timedelta(**{unit: count}))
            except OverflowError:
                # A count beyond what a timedelta holds, or a start before year 1
                return phantom.APP_ERROR, None

        date = self.parse_utc_datetime(value)
        if not date:
            return phantom.APP_ERROR, None

        return phantom.APP_SUCCESS, self.format_datetime(date)

    @staticmethod
    def parse_utc_datetime(value):
        """Parse an API date string into a naive UTC datetime object.

        :param value: date string, with or without a timezone offset
        :return: naive UTC datetime object, or None if the value cannot be parsed
        """
        try:
            date = parse(str(value))
        except Exception:
            return None

        if date.tzinfo:
            date = date.astimezone(timezone.utc).replace(tzinfo=None)

        return date

# File: cofensevision_consts.py
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


# Endpoints
BASE_ENDPOINT = "/api/v6"
VISION_ENDPOINT_TOKEN = "/uaa/oauth/token"
VISION_ENDPOINT_TEST_CONNECTIVITY = "/actuator/health"
VISION_ENDPOINT_MESSAGE_SEARCH = f"{BASE_ENDPOINT}/searches"
VISION_ENDPOINT_QUARANTINE_JOBS = f"{BASE_ENDPOINT}/quarantineJobs"
VISION_ENDPOINT_FILTER_JOBS = f"{BASE_ENDPOINT}/quarantineJobs/filter"
VISION_ENDPOINT_QUARANTINE_JOB = f"{BASE_ENDPOINT}/quarantineJobs/{{job_id}}"
VISION_ENDPOINT_APPROVE_QUARANTINE_JOBS = f"{BASE_ENDPOINT}/quarantineJobs/{{job_id}}/approve"
VISION_ENDPOINT_RESTORE_QUARANTINE_JOBS = f"{BASE_ENDPOINT}/quarantineJobs/{{job_id}}/restore"
VISION_ENDPOINT_STOP_QUARANTINE_JOBS = f"{BASE_ENDPOINT}/quarantineJobs/{{job_id}}/stop"
VISION_ENDPOINT_MESSAGE = f"{BASE_ENDPOINT}/messages"
VISION_ENDPOINT_ATTACHMENT = f"{BASE_ENDPOINT}/attachment"
VISION_ENDPOINT_IOC = "/iocrepository/v1/iocs"
VISION_ENDPOINT_MESSAGE_METADATA = f"{BASE_ENDPOINT}/messages/metadata"
VISION_ENDPOINT_SEARCHABLE_HEADER = f"{BASE_ENDPOINT}/config/searchableHeaders"
VISION_ENDPOINT_IOC_LAST = f"{VISION_ENDPOINT_IOC}/last"
VISION_ENDPOINT_DOWNLOAD_LOGS = f"{BASE_ENDPOINT}/download/logs"
VISION_ENDPOINT_AI_CLUSTERS = f"{BASE_ENDPOINT}/aiClusters"
VISION_ENDPOINT_AI_CLUSTER = f"{BASE_ENDPOINT}/aiClusters/{{cluster_id}}"
VISION_ENDPOINT_QUARANTINE_CLUSTER = f"{BASE_ENDPOINT}/quarantineJobs/cluster/{{cluster_id}}"
VISION_ENDPOINT_REJECT_QUARANTINE_JOBS = f"{BASE_ENDPOINT}/quarantineJobs/{{job_id}}/reject"
VISION_ENDPOINT_RETRY_QUARANTINE_JOBS = f"{BASE_ENDPOINT}/quarantineJobs/{{job_id}}/retry"
VISION_ENDPOINT_AI_CLUSTER_CONFIG = f"{BASE_ENDPOINT}/config/aicluster"

# JSON keys
VISION_STATE_TOKEN = "token"
VISION_STATE_ACCESS_TOKEN = "access_token"
VISION_STATE_EXPIRES_IN = "expires_in"
VISION_STATE_TOKEN_GENERATED_AT = "generated_at"
VISION_TOKEN_EXPIRY_BUFFER_SECONDS = 60

VISION_MESSAGE_EXPIRED_TOKEN = "invalid_token"
# Keywords observed across different Cofense Vision error formats for an expired/invalid access token,
# e.g. {"error": "invalid_token", ...}, {"error": "invalid_client", "error_description": "Bad credentials"},
# or {"error": "unauthorized", "error_description": "Full authentication is required..."}.
VISION_TOKEN_ERROR_KEYWORDS = (
    "invalid_token",
    "invalid_client",
    "unauthorized",
    "unauthenticated",
    "not authenticated",
    "bad credentials",
)
VISION_IOC_SOURCE_HEADER = "X-Cofense-IOC-Source"

# Status and Error messages
VISION_ERROR_MESSAGE_UNAVAILABLE = "Error message unavailable. Please check the asset configuration and|or action parameters"
VISION_ERROR_INVALID_INT_PARAM = "Please provide a valid integer value in the '{key}' parameter"
VISION_ERROR_NEGATIVE_INT_PARAM = "Please provide a valid non-negative integer value in the '{key}' parameter"
VISION_ERROR_ZERO_INT_PARAM = "Please provide a non-zero positive integer value in the '{key}' parameter"
VISION_ERROR_MAX_ALLOWED_INT_PARAM = "Please provide a non-zero positive integer value upto {max} in the '{key}' parameter"
VISION_ERROR_EMPTY_RESPONSE = "Status code: {}. Empty response and no information in the header"
VISION_ERROR_HTML_RESPONSE = "Error parsing html response"
VISION_ERROR_JSON_RESPONSE = "Unable to parse JSON response. Error: {0}"
VISION_ERROR_GENERAL_MESSAGE = "Status code: {0}, Data from server: {1}"
VISION_ERROR_REST_CALL = "Error connecting to server. Details: {0}"
VISION_ERROR_STATE_FILE_CORRUPT = "Error occurred while loading the state file. Resetting the state file with the default format."
VISION_SUCCESS_TEST_CONNECTIVITY = "Test Connectivity Passed"
VISION_ERROR_TEST_CONNECTIVITY = "Test Connectivity Failed"
VISION_ERROR_SYSTEM_HEALTH = "Failed to get the system health status"
VISION_SUCCESS_SYSTEM_HEALTH = "Cofense Vision is up and running"
VISION_ERROR_ACTION_EMPTY_RESPONSE = "The server returned an unexpected empty response"
VISION_ERROR_UNEXPECTED_RESPONSE_FORMAT = "The server returned a response in an unexpected format"
VISION_ERROR_TEST_CONNECTIVITY_INVALID_STATUS = "Error message: Server status is {}"
VISION_ERROR_EXTRA_VALUES = "The {0} parameter has more than {1} values. Please enter max {1} values to create a search."
VISION_ERROR_INVALID_MD5_VALUE = "Please provide a valid value for MD5 Hash in the attachment_hashes parameter"
VISION_ERROR_INVALID_SHA256_VALUE = "Please provide a valid value for SHA256 Hash in the attachment_hashes parameter"
VISION_ERROR_INVALID_HASH_TYPE_VALUE = "Please provide a valid hashType in attachment_hashes parameter. Allowed values are : SHA256, MD5 "
VISION_ERROR_INVALID_HASH_VALUE = "Please provide a valid value for attachment_hashes parameter. "
VISION_ERROR_INVALID_IOC_ID = "Please provide a 32-character hexadecimal IOC ID"
VISION_ERROR_INVALID_DATE_FORMAT = "Please provide a value of {} parameter in valid date format"
VISION_ERROR_INVALID_HEADER = "Please provide a valid value of headers parameter"
VISION_ERROR_VALUE_LIST = "Please provide a valid value for '{}' parameter. Valid values are: {}"
VISION_ERROR_INVALID_FILENAME = "Please provide a valid file name including the extension in the 'filename' parameter"
VISION_SUCCESS_GET_MESSAGE_SEARCH_ACTION = "Fetched message search successfully"
VISION_SUCCESS_SEARCHABLE_HEADERS_ACTION = "Fetched searchable headers successfully"
VISION_SUCCESS_GET_IOC_ACTION = "Fetched IOC successfully"
VISION_SUCCESS_DELETE_IOC_ACTION = "Delete IOC action ran successfully and IOC with MD5 ID {} is deleted"
VISION_SUCCESS_CREATE_QUARANTINE_JOB = "Created a quarantine job successfully"
VISION_SUCCESS_DELETE_QUARANTINE_JOB = "Deleted the quarantine job successfully"
VISION_ERROR_INVALID_PARAMETER_VALUE = "Please provide valid value in the '{}' parameter"
VISION_GET_METADATA_SUCCESS = "Retrieved message metadata successfully"
VISION_UPDATE_IOC_SUCCESS = "Updated the IOC successfully"
VISION_SUCCESS_GET_LAST_IOC_ACTION = "Get Last IOC Action succeeded, MD5 ID of fetched IOC : {}"
VISION_NO_HASH_PARAMETER = "Please provide a value for at least one of the hash parameters"
VISION_ERROR_BOTH_HASH_PARAMETERS = "Please provide only one of the 'md5' or 'sha256' parameters, not both"
VISION_ERROR_INVALID_MD5_PARAMETER = "Please provide a valid MD5 value in the 'md5' parameter"
VISION_ERROR_INVALID_SHA256_PARAMETER = "Please provide a valid SHA256 value in the 'sha256' parameter"
VISION_SUCCESS_APPROVE_JOB_ACTION = "The quarantine job has been approved successfully"
VISION_SUCCESS_RESTORE_JOB_ACTION = "Successfully initiated the restore process"
VISION_SUCCESS_GET_JOB_ACTION = "Successfully retrieved the quarantine job information"
VISION_SUCCESS_STOP_JOB_ACTION = "Successfully stopped the quarantine job"
VISION_SUCCESS_REJECT_JOB_ACTION = "Successfully rejected the quarantine job"
VISION_SUCCESS_RETRY_JOB_ACTION = "Successfully retried the quarantine job"
VISION_SUCCESS_LIST_CLUSTERS_ACTION = "Total clusters: {}"
VISION_SUCCESS_GET_CLUSTER_ACTION = "Successfully retrieved the cluster information"
VISION_SUCCESS_UPDATE_CLUSTER_ACTION = "Successfully updated the cluster"
VISION_SUCCESS_QUARANTINE_CLUSTER_ACTION = "Successfully created a quarantine job for the cluster"
VISION_SUCCESS_GET_AI_CONFIG_ACTION = "Successfully retrieved the Vision AI configuration"
VISION_SUCCESS_UPDATE_AI_CONFIG_ACTION = "Successfully updated the Vision AI configuration"
VISION_ERROR_MISSING_UPDATE_PARAMETER = "Please provide at least one parameter to update"
VISION_ERROR_MISSING_SEARCH_FILTER = "Please provide at least one filter parameter to create a search"
VISION_ERROR_INVALID_RANGE_PARAM = "Please provide a valid integer value in the '{key}' parameter between {min} and {max}"
VISION_ERROR_INVALID_MIN_VALUE_PARAM = "Please provide a valid integer value in the '{key}' parameter greater than or equal to {min}"
VISION_ERROR_INVALID_ISO8601_UTC_DATE = (
    "Please provide a valid value in the '{}' parameter. The date and time must be in UTC in ISO 8601 format "
    "(YYYY-MM-DDTHH:MM:SS.sssZ), for example: 2024-05-31T00:00:00.000Z"
)
VISION_ERROR_FROM_DATE_AFTER_TO_DATE = "The '{}' parameter value must not be greater than the '{}' parameter value"

# Consts
VISION_REQUEST_TIMEOUT = 120
VISION_DEFAULT_MAX_RETRIES = 3
VISION_DEFAULT_RETRY_WAIT_TIME = 2
VISION_RETRYABLE_STATUS_CODES = [429, 500, 502, 503, 504]
VISION_MAX_RETRY_WAIT_TIME = 60
VISION_DEFAULT_PAGE_SIZE = 50
VISION_DEFAULT_PAGE_NUMBER = 0
VISION_MAX_PAGE_SIZE = 2000
VISION_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
VISION_ISO8601_UTC_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
VISION_ISO8601_UTC_DATE_REGEX = r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{1,6}Z"
VISION_DEFAULT_HEADERS = {"Accept": "application/json", "Content-Type": "application/json"}
VISION_HASH_TYPE_MD5 = "MD5"
VISION_HASH_TYPE_SHA256 = "SHA256"
VISION_MAX_ALLOWED_VALUES = 3
VISION_VALID_SORT_PROPERTY = ["id", "createdBy", "createdDate", "modifiedBy", "modifiedDate", "receivedAfterDate", "receivedBeforeDate"]
VISION_VALID_SORT_ORDER = ["asc", "desc"]
VISION_THREAT_TYPES = ["domain", "md5", "sender", "sha256", "subject", "url"]
VISION_SUPPORTED_SORT_FIELDS = {
    "list_quarantine_jobs": ["id", "createdBy", "createdDate", "modifiedBy", "modifiedDate", "stopRequested"],
    "list_message_searches": ["id", "createdBy", "createdDate", "modifiedBy", "modifiedDate", "receivedAfterDate", "receivedBeforeDate"],
    "get_message_search_results": ["id", "subject", "createdOn", "sentOn", "processedOn", "htmlBody", "md5", "sha1", "sha256"],
    "list_iocs": ["updatedAt"],
}
VISION_JOB_STATUS = ["NEW", "PENDING_APPROVAL", "QUEUED", "RUNNING", "COMPLETED", "FAILED"]
VISION_SUPPORTED_CRITERIA = ["ANY", "ALL"]
VISION_CLUSTER_SORT_FIELDS = [
    "id",
    "fromDate",
    "toDate",
    "emailCount",
    "recipientCount",
    "similarityLevel",
    "title",
    "createdDate",
    "modifiedDate",
    "avgCharacterCount",
]
VISION_MIN_SIMILARITY_LEVEL = -10
VISION_MAX_SIMILARITY_LEVEL = 10
VISION_MIN_CLUSTER_SIZE = 10
VISION_MIN_CLUSTER_MATCH_TIME = 86400000
VISION_MAX_CLUSTER_MATCH_TIME = 604800000
VISION_MIN_CLUSTER_RAPID_GROWTH_TIME = 900000
VISION_MAX_CLUSTER_RAPID_GROWTH_TIME = 86400000
VISION_VALID_BOOLEAN_VALUES = ["True", "False"]

# Action Parameters
VISION_UPDATE_IOCS_REQUIRED_PARAMS = ["threat_type", "threat_value", "threat_level", "created_at", "source_id"]
VISION_PARAM_SENDERS = "senders"
VISION_PARAM_SUBJECTS = "subjects"
VISION_PARAM_ATTACHMENT_NAMES = "attachment_names"
VISION_PARAM_ATTACHMENT_HASH_MATCH_CRITERIA = "attachment_hash_match_criteria"
VISION_PARAM_ATTACHMENT_HASHES = "attachment_hashes"
VISION_PARAM_ATTACHMENT_MIME_TYPES = "attachment_mime_types"
VISION_PARAM_ATTACHMENT_EXCLUDE_MIME_TYPES = "attachment_exclude_mime_types"
VISION_PARAM_DOMAIN_MATCH_CRITERIA = "domain_match_criteria"
VISION_PARAM_DOMAINS = "domains"
VISION_PARAM_HEADERS = "headers"
VISION_PARAM_INTERNET_MESSAGE_ID = "internet_message_id"
VISION_PARAM_PARTIAL_INGEST = "partial_ingest"
VISION_PARAM_RECEIVED_AFTER_DATE = "received_after_date"
VISION_PARAM_RECEIVED_BEFORE_DATE = "received_before_date"
VISION_PARAM_RECIPIENT = "recipient"
VISION_PARAM_URL = "url"
VISION_PARAM_IOC_MD5_ID = "id"
VISION_PARAM_IOC_SOURCE = "source"
VISION_PARAM_JOB_ID = "id"
VISION_PARAM_CLUSTER_ID = "id"

# On Poll
VISION_STATE_LAST_INGESTED_DATE = "last_ingested_date"
# Written only by earlier builds, which retained a window truncated by the removed 'max_emails'
# limit; the poll now drops it when it stores the cursor
VISION_STATE_PENDING_POLL = "pending_poll"
VISION_ERROR_INVALID_START_TIME = (
    "Please provide a valid value in the '{key}' parameter. Supported formats are relative time, for example 1d, 6h, "
    "or a UTC date, for example 2024-05-31T00:00:00Z"
)
VISION_ERROR_SAVE_CONTAINER = "Error occurred while saving the container for the cluster ID {cluster_id}. Error: {error}"
VISION_ERROR_SAVE_ARTIFACTS = "Error occurred while saving the artifacts for the cluster ID {cluster_id}. Error: {error}"
VISION_SUCCESS_ON_POLL = "Ingested {emails} email(s) from {clusters} cluster(s) into {containers} container(s) successfully"
VISION_ON_POLL_PAGE_SIZE = 50
VISION_ON_POLL_DEFAULT_START_TIME = "1d"
VISION_ON_POLL_DEFAULT_MAX_ARTIFACTS = 100
# An email becomes visible to the API when its row is committed, which can be slightly later
# than the processedOn timestamp it carries. Polling only up to this many minutes ago keeps the
# windows contiguous and non-overlapping, so a late commit is still picked up by the next cycle
# instead of falling into a window that has already closed. An email committed later than this
# is never ingested; deployments that see slower commits raise the 'ingestion_lag' asset parameter.
VISION_ON_POLL_DEFAULT_INGESTION_LAG = 5
# Default order is fromDate,desc which re-sorts as new emails arrive; a stable key
# keeps the page walk consistent for the duration of a polling cycle.
VISION_ON_POLL_SORT = "id,asc"
VISION_ON_POLL_CEF_TYPES = {
    "internetMessageId": ["cofense vision internet message id"],
    "fromEmail": ["email"],
    "clusterId": ["cofense vision cluster id"],
    "iocIds": ["cofense vision ioc id"],
    "quarantineJobId": ["cofense vision quarantine job id"],
}
VISION_ON_POLL_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"
VISION_RELATIVE_TIME_REGEX = r"(\d+)\s*([smhdw])"
VISION_RELATIVE_TIME_UNITS = {"s": "seconds", "m": "minutes", "h": "hours", "d": "days", "w": "weeks"}
# The v6 aiClusters endpoint returns a bare JSON array of clusters; the emails of a
# cluster are carried in its "emails" key, which may be null.
VISION_CLUSTER_EMAIL_KEY = "emails"
# A cluster grows as new emails join it, so it is returned again by every polling window that
# ingests one of its emails. The container is identified by the ingestion timestamp of the newest
# email it holds plus its chunk index, never by the polling clock: a re-polled cycle rebuilds the
# same identifiers and the platform deduplicates, while emails ingested later form containers of
# their own instead of backfilling one an earlier cycle created.
VISION_CONTAINER_SDI = "cofense-vision-cluster-{cluster_id}-{newest}-{chunk}"
VISION_ARTIFACT_SDI = "cofense-vision-email-{email_id}"
# The container name carries the cluster ID and the ingestion timestamp of the oldest email it holds,
# so every email of the container was ingested at or after the timestamp in its name
VISION_CONTAINER_NAME = "{cluster_id} : {title} - {oldest}"
VISION_CONTAINER_NAME_PART = "{name} - Part {part} of {parts}"
VISION_CONTAINER_DEFAULT_TITLE = "Cofense Vision"
VISION_ARTIFACT_NAME = "Cofense Vision Email"
VISION_ARTIFACT_LABEL = "email"
VISION_CONTAINER_DESCRIPTION = "Emails of the Cofense Vision AI cluster with ID {cluster_id} ingested between {from_date} and {to_date}"
VISION_CONFIG_START_TIME = "start_time"
VISION_CONFIG_START_TIME_POLL_NOW = "start_time_poll_now"
VISION_CONFIG_MAX_ARTIFACTS = "max_artifacts"
VISION_PARAM_CONTAINER_COUNT = "container_count"
VISION_CONFIG_INGESTION_LAG = "ingestion_lag"
VISION_PARAM_ARTIFACT_COUNT = "artifact_count"

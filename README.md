# Cofense Vision

Publisher: Cofense <br>
Connector Version: 3.0.0 <br>
Product Vendor: Cofense <br>
Product Name: Cofense Vision <br>
Minimum Product Version: 5.5.0

This app implements investigative and generic actions to quarantine emails, manage IOCs, search messages, download messages and their attachments

<!--  File: manual_readme_content.md

 Copyright (c) 2023-2026 Cofense

 This unpublished material is proprietary to Cofense.
 All rights reserved. The methods and
 techniques described herein are considered trade secrets
 and/or confidential. Reproduction or distribution, in whole
 or in part, is forbidden except by express written permission
 of Cofense.

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software distributed under
 the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
 either express or implied. See the License for the specific language governing permissions
 and limitations under the License. -->

## Asset Configuration

| Parameter | Description |
|-----------------------|------------------------------------------------------------------------------|
| Cofense Vision URL | The base URL of the Cofense Vision instance, for example `https://vision.example.com` |
| Verify Server Certificate | Whether to verify the SSL certificate of the Cofense Vision server (enabled by default) |
| Client ID | The client ID of an OAuth 2.0 client credentials application registered in Cofense Vision |
| Client Secret | The client secret associated with the Client ID |

## Authentication

This app authenticates using the OAuth 2.0 client credentials grant. On **test connectivity**, and automatically before
any action if no token is cached or the cached token has expired, the app exchanges the configured Client ID and Client
Secret for an access token and stores it in the encrypted state file. Actions reuse this cached token until it expires
or the server rejects it, at which point a new token is generated automatically.

### Configuration variables

This table lists the configuration variables required to operate Cofense Vision. These variables are specified when configuring a Cofense Vision asset in Splunk SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**base_url** | required | string | Cofense Vision URL |
**verify_server_cert** | optional | boolean | Verify Server Certificate |
**client_id** | required | string | Client ID |
**client_secret** | required | password | Client Secret |
**start_time** | optional | string | Start Time (Default: 1d). The date from which the cluster emails must be fetched |
**start_time_poll_now** | optional | string | Start Time for Poll Now (Default: 1d). The date from which the cluster emails must be fetched |
**max_artifacts** | optional | numeric | Maximum number of artifacts in a single container (Default: 100) |
**ingestion_lag** | optional | numeric | Minutes the polling window stays behind the current time, so emails committed late are still ingested (Default: 5). An email committed later than this is not ingested |

### Supported Actions

[test connectivity](#action-test-connectivity) - Validate the asset configuration for connectivity using supplied configuration <br>
[get message metadata](#action-get-message-metadata) - Retrieves the metadata of the message that matches the specified internet message ID and recipient email address <br>
[get message](#action-get-message) - Fetches full content of an email and saves it as a zip file to the Vault <br>
[get message attachment](#action-get-message-attachment) - Fetches an attachment by using its MD5 or SHA256 hash and saves it to the Vault <br>
[list quarantine jobs](#action-list-quarantine-jobs) - Fetches a list of matching quarantine jobs <br>
[create quarantine job](#action-create-quarantine-job) - Creates a new quarantine job <br>
[restore quarantine job](#action-restore-quarantine-job) - Restores emails quarantined by the job identified by the ID <br>
[list message searches](#action-list-message-searches) - Retrieves the list of searches <br>
[get message search](#action-get-message-search) - Retrieves the search identified by an ID <br>
[get quarantine job](#action-get-quarantine-job) - Retrieves quarantine job identified by the ID <br>
[approve quarantine job](#action-approve-quarantine-job) - Approves the quarantine job identified by the ID. When the Auto Quarantine feature is configured to require manual approvals, this endpoint can approve the pending quarantine jobs <br>
[delete quarantine job](#action-delete-quarantine-job) - Deletes the quarantine job identified by the ID <br>
[get messagesearch results](#action-get-messagesearch-results) - Retrieves the results for the search identified by the search ID <br>
[delete ioc](#action-delete-ioc) - Deletes a single active or expired IOC from the local IOC Repository <br>
[stop quarantine job](#action-stop-quarantine-job) - Issues a request to stop the quarantine job identified by ID <br>
[create message search](#action-create-message-search) - Creates a new search based on the user-specified filters <br>
[get last ioc](#action-get-last-ioc) - Retrieves the last updated IOC from the local IOC Repository. It may return an active or an expired IOC <br>
[update iocs](#action-update-iocs) - Updates one or more IOCs stored in the local IOC repository <br>
[update ioc](#action-update-ioc) - Updates the IOC identified by its unique MD5 ID <br>
[list iocs](#action-list-iocs) - Lists the IOCs stored in the local IOC Repository <br>
[get ioc](#action-get-ioc) - Retrieves the IOC identified by its unique MD5 ID <br>
[list searchable headers](#action-list-searchable-headers) - Retrieves a list of configured header keys that can be used to create a message search <br>
[download logs](#action-download-logs) - Downloads the log files for all Cofense Vision components <br>
[list clusters](#action-list-clusters) - Retrieves clusters that contain at least one email with an ingestion timestamp that falls in the requested date and time range <br>
[get cluster](#action-get-cluster) - Retrieves a single cluster identified by the ID, including the emails in the cluster <br>
[update cluster](#action-update-cluster) - Updates the cluster identified by the ID <br>
[quarantine cluster](#action-quarantine-cluster) - Manually creates a quarantine job for all emails in a cluster that are not already associated with an existing quarantine job for this cluster <br>
[reject quarantine job](#action-reject-quarantine-job) - Rejects the quarantine job identified by the ID. When the Auto Quarantine feature is configured to require manual approvals, this endpoint can reject pending quarantine jobs <br>
[retry quarantine job](#action-retry-quarantine-job) - Issues a request to retry the quarantine job identified by the ID <br>
[get vision ai config](#action-get-vision-ai-config) - Retrieves the current Vision AI configuration settings, including whether the feature is enabled, whether the Terms of Service have been accepted, and all tunable cluster parameters <br>
[update vision ai config](#action-update-vision-ai-config) - Performs a partial update of the Vision AI configuration, updating only those parameters included in the request <br>
[on poll](#action-on-poll) - Callback action for the on poll ingest functionality

## action: 'test connectivity'

Validate the asset configuration for connectivity using supplied configuration

Type: **test** <br>
Read only: **True**

The test connectivity action will first check if the Cofense Vision server is up. If the server is up and running, it will use the credentials to generate the access token. Once the token is received, it will be stored in the state file.

#### Action Parameters

No parameters are required for this action

#### Action Output

No Output

## action: 'get message metadata'

Retrieves the metadata of the message that matches the specified internet message ID and recipient email address

Type: **investigate** <br>
Read only: **True**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**internet_message_id** | required | Unique identifier of the email, enclosed in angle brackets | string | `cofense vision internet message id` |
**recipient_address** | required | Recipient address of the email | string | `email` |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.parameter.internet_message_id | string | `cofense vision internet message id` | <154949148.36247.1665620111111@edf45488dd9c> |
action_result.parameter.recipient_address | string | `email` | testuser@test.com |
action_result.data.\*.attachments.\*.contentType | string | | application/zip |
action_result.data.\*.attachments.\*.detectedContentType | string | | application/zip |
action_result.data.\*.attachments.\*.filename | string | | fileNum-Thread[mailer-006,5,main]-text-file-36247.txt.zip |
action_result.data.\*.attachments.\*.id | numeric | | 6619844 |
action_result.data.\*.attachments.\*.md5 | string | `md5` | 940f1f22d39a17feadebcda817139376 |
action_result.data.\*.attachments.\*.sha256 | string | `sha256` | 092edcf103124a00342194f7489e22430434b516ed4e27eb1ab5e8472ec36cae |
action_result.data.\*.attachments.\*.size | numeric | | 1206 |
action_result.data.\*.deliveredOn | string | | |
action_result.data.\*.from.\*.address | string | | testuser@test.com |
action_result.data.\*.from.\*.id | numeric | | 2616086 |
action_result.data.\*.from.\*.personal | string | | testuser |
action_result.data.\*.headers.\*.name | string | | From |
action_result.data.\*.headers.\*.value | string | | testuser@test.com |
action_result.data.\*.htmlBody | string | | |
action_result.data.\*.id | numeric | | 2616086 |
action_result.data.\*.internetMessageId | string | `cofense vision internet message id` | <154949148.36247.1665620111111@edf45488dd9c> |
action_result.data.\*.md5 | string | `md5` | 2c05a12e6b87e2f5046cf88633868f07 |
action_result.data.\*.processedOn | string | | 2022-10-13T00:19:24.776+00:00 |
action_result.data.\*.receivedOn | string | | 2022-10-13T00:19:21.000+00:00 |
action_result.data.\*.recipients.\*.address | string | | testuser@test.com |
action_result.data.\*.recipients.\*.id | numeric | | 19039468 |
action_result.data.\*.recipients.\*.personal | string | | testuser |
action_result.data.\*.recipients.\*.recipientType | string | | to |
action_result.data.\*.sentOn | string | | 2022-10-13T00:19:20.000+00:00 |
action_result.data.\*.sha1 | string | `sha1` | f792cae1723c381e55d4786232c71304eb1364c0 |
action_result.data.\*.sha256 | string | `sha256` | c82f3b550efcce43996b85b86ef1c0a48a4953f7d317996644111d2b8afdaaed |
action_result.data.\*.subject | string | | Just a test |
action_result.data.\*.textBody | string | | |
action_result.data.\*.messageIdHeader | string | | <852266475.122.1788931518336@vision.cofenseselab.cofense-vision.com> |
action_result.data.\*.emailEnvironmentId | numeric | | 1 |
action_result.data.\*.networkMessageIdHeader | string | | face5fe2-79da-4d75-a9f0-08df0e32bcdc |
action_result.summary | string | | |
action_result.message | string | | Retrieved message metadata successfully |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'get message'

Fetches full content of an email and saves it as a zip file to the Vault

Type: **investigate** <br>
Read only: **True**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**internet_message_id** | required | Unique identifier of the email, enclosed in angle brackets | string | `cofense vision internet message id` |
**recipient_address** | required | Recipient address of the email | string | `email` |
**password** | optional | Password to protect the zip file | string | |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.parameter.internet_message_id | string | `cofense vision internet message id` | <154949148.36247.1665620111111@edf45488dd9c> |
action_result.parameter.password | string | | test |
action_result.parameter.recipient_address | string | `email` | testuser@test.com |
action_result.data.\*.aka.\* | string | | message_2023-01-06_06:49:00.536505.zip |
action_result.data.\*.container | string | | Get message |
action_result.data.\*.container_id | numeric | | 2 |
action_result.data.\*.create_time | string | | 0 minutes ago |
action_result.data.\*.created_via | string | | automation |
action_result.data.\*.hash | string | `vault id` | daf4cd5ede7cda3398434bbb22cfb791c2b43310 |
action_result.data.\*.id | numeric | | 1 |
action_result.data.\*.metadata.sha1 | string | `sha1` | daf4cd5ede7cda3398434bbb22cfb791c2b43310 |
action_result.data.\*.metadata.sha256 | string | `sha256` | 10e14b2a20340fe9b352bc05ccf09bd3ae24e1d1bac5b7aa92b1cf6c8838f5e4 |
action_result.data.\*.mime_type | string | | application/zip |
action_result.data.\*.name | string | | message_2023-01-06_06:49:00.536505.zip |
action_result.data.\*.path | string | | /opt/phantom/vault/da/f4/daf4cd5ede7cda3398434bbb22cfb791c2b43310 |
action_result.data.\*.size | numeric | | 1642149 |
action_result.data.\*.task | string | | |
action_result.data.\*.user | string | | admin |
action_result.data.\*.vault_document | numeric | | 1 |
action_result.data.\*.vault_id | string | `sha1` `vault id` | daf4cd5ede7cda3398434bbb22cfb791c2b43310 |
action_result.data.\*.es_attachment_id | string | | |
action_result.summary.vault_id | string | `vault id` | daf4cd5ede7cda3398434bbb22cfb791c2b43310 |
action_result.message | string | | Vault id: daf4cd5ede7cda3398434bbb22cfb791c2b43310 |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'get message attachment'

Fetches an attachment by using its MD5 or SHA256 hash and saves it to the Vault

Type: **investigate** <br>
Read only: **True**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**md5** | optional | Hex-encoded string that represents an attachment's MD5 hash | string | `md5` |
**sha256** | optional | Hex-encoded string that represents an attachment's SHA256 hash | string | `sha256` |
**filename** | required | File name including the extension to give to the file | string | |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.parameter.filename | string | | test.txt |
action_result.parameter.md5 | string | `md5` | 21b6b32fb4e526d594afe70ea56a0e0c |
action_result.parameter.sha256 | string | `sha256` | ef7247f075e010e7a9f4af6fa8f8dd4436b1cc12355226bbdc270a0fb1c885d0 |
action_result.data.\*.aka.\* | string | | test.txt |
action_result.data.\*.container | string | | Test |
action_result.data.\*.container_id | numeric | | 5 |
action_result.data.\*.create_time | string | | 0 minutes ago |
action_result.data.\*.created_via | string | | automation |
action_result.data.\*.hash | string | `vault id` | 31c194010afedb76694517e6250b5339d72ed518 |
action_result.data.\*.id | numeric | | 29 |
action_result.data.\*.metadata.sha1 | string | `sha1` | 31c194010afedb76694517e6250b5339d72ed518 |
action_result.data.\*.metadata.sha256 | string | `sha256` | ef7247f075e010e7a9f4af6fa8f8dd4436b1cc12355226bbdc270a0fb1c885d0 |
action_result.data.\*.mime_type | string | | text/plain |
action_result.data.\*.name | string | | test.txt |
action_result.data.\*.path | string | | /opt/phantom/vault/31/c1/31c194010afedb76694517e6250b5339d72ed518 |
action_result.data.\*.size | numeric | | 3079266 |
action_result.data.\*.task | string | | |
action_result.data.\*.user | string | | admin |
action_result.data.\*.vault_document | numeric | | 29 |
action_result.data.\*.vault_id | string | `vault id` | 31c194010afedb76694517e6250b5339d72ed518 |
action_result.data.\*.es_attachment_id | string | | |
action_result.summary.vault_id | string | `vault id` | 31c194010afedb76694517e6250b5339d72ed518 |
action_result.message | string | | Vault id: 31c194010afedb76694517e6250b5339d72ed518 |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'list quarantine jobs'

Fetches a list of matching quarantine jobs

Type: **investigate** <br>
Read only: **True**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**page** | optional | Start page of the results. The value must be a positive integer or 0 | numeric | |
**size** | optional | Number of results per page. The value must be a positive integer up to 2000 | numeric | |
**sort** | optional | The name-value pair defining the order of the response. Comma separated values are supported | string | |
**exclude_quarantine_emails** | optional | Whether to remove (true) or not remove (false) quarantined emails from the response | boolean | |
**include_status** | optional | Filters quarantine jobs by including emails with the specified status. Supports comma-separated values | string | |
**exclude_status** | optional | Filters quarantine jobs by excluding emails with the specified status. Supports comma-separated values | string | |
**iocs** | optional | Unique MD5 hash identifier of one or more IOCs. Comma separated values are supported | string | `md5` `cofense vision ioc id` |
**sources** | optional | One or more configured IOC sources. Comma separated values are supported | string | `cofense vision source` |
**modified_date_after** | optional | Emails modified after this date and time. The date and time must be in UTC | string | |
**auto_quarantine** | optional | Whether to list only auto quarantine jobs (true) or both (false) | boolean | |
**cluster_id** | optional | One or more IDs of the cluster to filter on. Comma-separated values are supported | string | `cofense vision cluster id` |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.parameter.auto_quarantine | boolean | | True False |
action_result.parameter.exclude_quarantine_emails | boolean | | True False |
action_result.parameter.exclude_status | string | | NEW,FAILED,COMPLETED |
action_result.parameter.include_status | string | | NEW,FAILED,COMPLETED |
action_result.parameter.iocs | string | `md5` `cofense vision ioc id` | b93cba4829a00dabef96036bb6765d20 |
action_result.parameter.modified_date_after | string | | 01 Mar 2021 01 Feb 2021 04:45:33 2022-04-17T14:05:44Z 15/09/2022 |
action_result.parameter.page | numeric | | 1 |
action_result.parameter.size | numeric | | 50 |
action_result.parameter.sort | string | | createdBy:desc,id:asc |
action_result.parameter.sources | string | `cofense vision source` | Vision-UI |
action_result.parameter.cluster_id | string | `cofense vision cluster id` | 45,78,99 |
action_result.data.\*.autoQuarantine | boolean | | True False |
action_result.data.\*.createdBy | string | | system |
action_result.data.\*.createdDate | string | | 2022-07-15T05:43:39.136018 |
action_result.data.\*.emailCount | numeric | | |
action_result.data.\*.id | numeric | `cofense vision quarantine job id` | 239 |
action_result.data.\*.aiClusterId | string | `cofense vision cluster id` | 45 |
action_result.data.\*.context | string | | |
action_result.data.\*.detection | string | | |
action_result.data.\*.isClusterInitiated | boolean | | True False |
action_result.data.\*.matchingIOCs | string | | |
action_result.data.\*.matchingSources | string | | |
action_result.data.\*.quarantineEmailReadStatusCounts | string | | |
action_result.data.\*.statusCounts | string | | |
action_result.data.\*.whoClickedPending | boolean | | True False |
action_result.data.\*.whoDeletedPending | boolean | | True False |
action_result.data.\*.willRetry | boolean | | True False |
action_result.data.\*.matchingIocInfo.\*.attributes.threat_type | string | | SUBJECT |
action_result.data.\*.matchingIocInfo.\*.attributes.threat_value | string | | essentially wolfish3 time 1657392753323 |
action_result.data.\*.matchingIocInfo.\*.id | string | | b93cba4829a00dabef96036bb6765d20 |
action_result.data.\*.matchingIocInfo.\*.metadata.quarantine.created_at | string | | 2022-07-15T05:43:38.912+00:00 |
action_result.data.\*.matchingIocInfo.\*.metadata.quarantine.expired | boolean | | True False |
action_result.data.\*.matchingIocInfo.\*.metadata.quarantine.expires_at | string | | 2022-07-29T18:29:59.999+00:00 |
action_result.data.\*.matchingIocInfo.\*.metadata.quarantine.first_quarantined_at | string | | 2022-07-15T05:43:39.096+00:00 |
action_result.data.\*.matchingIocInfo.\*.metadata.quarantine.last_quarantined_at | string | | 2022-07-15T05:43:39.096+00:00 |
action_result.data.\*.matchingIocInfo.\*.metadata.quarantine.match_count | numeric | | 1 |
action_result.data.\*.matchingIocInfo.\*.metadata.quarantine.quarantine_count | numeric | | 10 |
action_result.data.\*.matchingIocInfo.\*.metadata.source | string | | |
action_result.data.\*.matchingIocInfo.\*.type | string | | ioc |
action_result.data.\*.modifiedBy | string | | system |
action_result.data.\*.modifiedDate | string | | 2022-07-19T05:51:33.949938 |
action_result.data.\*.quarantineEmails.\*.createdDate | string | | 2022-07-15T05:43:39.091849 |
action_result.data.\*.quarantineEmails.\*.errorMessage | string | | |
action_result.data.\*.quarantineEmails.\*.ewsMessageId | string | | AAMkADAwNjYyZmI2LWYxYzgtNDJlZS05NWJmLTM3YjNlN2IzNzM5OABGAAAAAAAO1fllLjAOSLm9MgsUozfxBwCRXmjDwC9US6/LTV+t6MQIAABhh9RXAACRXmjDwC9US6/LTV+t6MQIAABtcrLJAAA= |
action_result.data.\*.quarantineEmails.\*.id | numeric | | 5207 |
action_result.data.\*.quarantineEmails.\*.internetMessageId | string | | <1270149500.1722827.1657392753324@af226d4cfbab> |
action_result.data.\*.quarantineEmails.\*.originalFolderId | string | | AAMkADAwNjYyZmI2LWYxYzgtNDJlZS05NWJmLTM3YjNlN2IzNzM5OAAuAAAAAAAO1fllLjAOSLm9MgsUozfxAQCRXmjDwC9US6/LTV+t6MQIAAAAAAEkAAA= |
action_result.data.\*.quarantineEmails.\*.quarantinedDate | string | | 2022-08-03T05:58:51.939468 |
action_result.data.\*.quarantineEmails.\*.recipientAddress | string | | testuser@test.com |
action_result.data.\*.quarantineEmails.\*.status | string | | EXPUNGED |
action_result.data.\*.quarantineJobRuns.\*.completedDate | string | | 2022-07-19T05:51:33.96021 |
action_result.data.\*.quarantineJobRuns.\*.error | numeric | | |
action_result.data.\*.quarantineJobRuns.\*.id | numeric | `cofense vision quarantine job id` | 379 |
action_result.data.\*.quarantineJobRuns.\*.jobRunType | string | | QUARANTINE |
action_result.data.\*.quarantineJobRuns.\*.startedDate | string | | 2022-07-19T05:51:33.950313 |
action_result.data.\*.quarantineJobRuns.\*.status | string | | COMPLETED |
action_result.data.\*.quarantineJobRuns.\*.total | numeric | | 1 |
action_result.data.\*.searchId | numeric | | |
action_result.data.\*.stopRequested | boolean | | True False |
action_result.data.\*.statusCounts.\*.count | numeric | | 1 |
action_result.data.\*.statusCounts.\*.status | string | | QUARANTINE_ERROR |
action_result.data.\*.quarantineEmails.\*.isRead | string | | |
action_result.data.\*.quarantineEmails.\*.already | string | | |
action_result.data.\*.quarantineEmails.\*.foundEnvId | string | | |
action_result.data.\*.quarantineEmails.\*.ingestEnvId | string | | |
action_result.data.\*.quarantineEmails.\*.clickDetails | string | | |
action_result.data.\*.quarantineEmails.\*.isClickedAny | string | | |
action_result.data.\*.quarantineEmails.\*.isClickedIOC | string | | |
action_result.data.\*.quarantineEmails.\*.deleteDetails | string | | |
action_result.data.\*.quarantineEmails.\*.deletedByUser | string | | |
action_result.data.\*.quarantineEmails.\*.foundFolderType | string | | |
action_result.data.\*.quarantineEmails.\*.hasCalendarEvent | boolean | | True False |
action_result.data.\*.quarantineJobRuns.\*.createdBy | string | | crestdatauser |
action_result.data.\*.quarantineEmailReadStatusCounts.read | numeric | | |
action_result.data.\*.quarantineEmailReadStatusCounts.unRead | numeric | | |
action_result.data.\*.quarantineEmailReadStatusCounts.deleted | numeric | | |
action_result.data.\*.quarantineEmailReadStatusCounts.clickedAny | numeric | | |
action_result.data.\*.quarantineEmailReadStatusCounts.clickedIoc | numeric | | |
action_result.data.\*.quarantineEmailReadStatusCounts.notAvailable | numeric | | 1 |
action_result.data.\*.quarantineEmailReadStatusCounts.calendarEvents | numeric | | |
action_result.data.\*.quarantineEmailReadStatusCounts.whoDeletedStatus | string | | DONE_NO_DELETER |
action_result.data.\*.quarantineEmailReadStatusCounts.whoClickedRetries | string | | |
action_result.data.\*.quarantineEmailReadStatusCounts.whoDeletedRetries | numeric | | 1 |
action_result.data.\*.quarantineEmailReadStatusCounts.clickedNotAvailable | numeric | | 1 |
action_result.data.\*.matchingIocInfo.\*.metadata.quarantine.wildcard | boolean | | True False |
action_result.data.\*.matchingIocInfo.\*.metadata.quarantine.false_positive | boolean | | True False |
action_result.data.\*.matchingIocInfo.\*.metadata.quarantine.email_restore_count | numeric | | |
action_result.data.\*.matchingIocInfo.\*.metadata.quarantine.recipient_restore_count | numeric | | |
action_result.data.\*.matchingIocInfo.\*.metadata.quarantine.email_quarantine_success | numeric | | 2 |
action_result.data.\*.matchingIocInfo.\*.metadata.quarantine.recipient_quarantine_success | numeric | | 2 |
action_result.summary.total_quarantine_jobs | numeric | | 28 |
action_result.message | string | | Total quarantine jobs: 28 |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'create quarantine job'

Creates a new quarantine job

Type: **generic** <br>
Read only: **False**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**quarantine_emails** | required | A comma-separated string of quarantine emails, specifying the recipient address and internet message ID of the email | string | |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.parameter.quarantine_emails | string | | test@test.com:\<CAFRPxWuOFW@test.com&>:<WCuib9wCsz@test.com>,testuser@test.com:<YCuib9wCs1@test.com> |
action_result.data.\*.autoQuarantine | boolean | | True False |
action_result.data.\*.createdBy | string | | cds |
action_result.data.\*.createdDate | string | | 2023-01-11T07:10:32.715663869 |
action_result.data.\*.emailCount | numeric | | 1 |
action_result.data.\*.id | numeric | `cofense vision quarantine job id` | 1458 |
action_result.data.\*.modifiedBy | string | | cds |
action_result.data.\*.modifiedDate | string | | 2023-01-11T07:10:32.715663869 |
action_result.data.\*.quarantineEmails.\*.createdDate | string | | 2023-01-11T07:10:32.712651423 |
action_result.data.\*.quarantineEmails.\*.errorMessage | string | | |
action_result.data.\*.quarantineEmails.\*.ewsMessageId | string | | |
action_result.data.\*.quarantineEmails.\*.id | numeric | | 6965 |
action_result.data.\*.quarantineEmails.\*.internetMessageId | string | | <CAFRPxWtRtkkfV892gtZ+CsjtSECOZmA@test.com> |
action_result.data.\*.quarantineEmails.\*.originalFolderId | string | | |
action_result.data.\*.quarantineEmails.\*.quarantinedDate | string | | |
action_result.data.\*.quarantineEmails.\*.recipientAddress | string | | testuser@test.com |
action_result.data.\*.quarantineEmails.\*.status | string | | NEW |
action_result.data.\*.quarantineJobRuns.\*.completedDate | string | | |
action_result.data.\*.quarantineJobRuns.\*.error | numeric | | |
action_result.data.\*.quarantineJobRuns.\*.id | numeric | | 2812 |
action_result.data.\*.quarantineJobRuns.\*.jobRunType | string | | QUARANTINE |
action_result.data.\*.quarantineJobRuns.\*.startedDate | string | | |
action_result.data.\*.quarantineJobRuns.\*.status | string | | NEW |
action_result.data.\*.quarantineJobRuns.\*.total | numeric | | 1 |
action_result.data.\*.searchId | string | | |
action_result.data.\*.stopRequested | boolean | | True False |
action_result.data.\*.context | string | | |
action_result.data.\*.detection | string | | |
action_result.data.\*.willRetry | boolean | | True False |
action_result.data.\*.aiClusterId | string | | |
action_result.data.\*.statusCounts.\*.count | numeric | | 1 |
action_result.data.\*.statusCounts.\*.status | string | | NEW |
action_result.data.\*.quarantineEmails.\*.isRead | string | | |
action_result.data.\*.quarantineEmails.\*.already | string | | |
action_result.data.\*.quarantineEmails.\*.foundEnvId | string | | |
action_result.data.\*.quarantineEmails.\*.ingestEnvId | string | | |
action_result.data.\*.quarantineEmails.\*.clickDetails | string | | |
action_result.data.\*.quarantineEmails.\*.isClickedAny | string | | |
action_result.data.\*.quarantineEmails.\*.isClickedIOC | string | | |
action_result.data.\*.quarantineEmails.\*.deleteDetails | string | | |
action_result.data.\*.quarantineEmails.\*.deletedByUser | string | | |
action_result.data.\*.quarantineEmails.\*.foundFolderType | string | | |
action_result.data.\*.quarantineEmails.\*.hasCalendarEvent | boolean | | True False |
action_result.data.\*.quarantineJobRuns.\*.createdBy | string | | crestdatauser |
action_result.data.\*.whoClickedPending | boolean | | True False |
action_result.data.\*.whoDeletedPending | boolean | | True False |
action_result.data.\*.isClusterInitiated | boolean | | True False |
action_result.data.\*.quarantineEmailReadStatusCounts.read | numeric | | |
action_result.data.\*.quarantineEmailReadStatusCounts.unRead | numeric | | |
action_result.data.\*.quarantineEmailReadStatusCounts.deleted | numeric | | |
action_result.data.\*.quarantineEmailReadStatusCounts.clickedAny | numeric | | |
action_result.data.\*.quarantineEmailReadStatusCounts.clickedIoc | numeric | | |
action_result.data.\*.quarantineEmailReadStatusCounts.notAvailable | numeric | | 1 |
action_result.data.\*.quarantineEmailReadStatusCounts.calendarEvents | numeric | | |
action_result.data.\*.quarantineEmailReadStatusCounts.whoDeletedStatus | string | | |
action_result.data.\*.quarantineEmailReadStatusCounts.whoClickedRetries | string | | |
action_result.data.\*.quarantineEmailReadStatusCounts.whoDeletedRetries | string | | |
action_result.data.\*.quarantineEmailReadStatusCounts.clickedNotAvailable | numeric | | 1 |
action_result.summary | string | | |
action_result.message | string | | Created a quarantine job successfully |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'restore quarantine job'

Restores emails quarantined by the job identified by the ID

Type: **generic** <br>
Read only: **False**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**id** | required | ID of the quarantine job in cofense vision to be restored | numeric | `cofense vision quarantine job id` |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.parameter.id | numeric | `cofense vision quarantine job id` | 1234 |
action_result.data | string | | |
action_result.summary | string | | |
action_result.message | string | | Successfully initiated the restore process |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'list message searches'

Retrieves the list of searches

Type: **investigate** <br>
Read only: **True**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**page** | optional | The start page of the results. The value must be a positive integer or 0 | numeric | |
**size** | optional | The number of results to retrieve per page. The value must be a positive integer up to 2000 | numeric | |
**sort** | optional | The name-value pair defining the order of the response. Comma separated values are supported | string | |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.parameter.page | numeric | | 0 |
action_result.parameter.size | numeric | | 50 |
action_result.parameter.sort | string | | createdBy:desc,id:asc |
action_result.data.\*.attachmentHashCriteria.attachmentHashes.\*.hashString | string | | a855dc7659e527bf2C1a5bdFc43519c6 |
action_result.data.\*.attachmentHashCriteria.attachmentHashes.\*.hashType | string | | MD5 |
action_result.data.\*.attachmentHashCriteria.type | string | | ANY |
action_result.data.\*.createdBy | string | | visionAdmin |
action_result.data.\*.createdDate | string | | 2022-12-09T20:16:42.868693 |
action_result.data.\*.domainCriteria.type | string | | ANY |
action_result.data.\*.headers.\*.key | string | | X-MS-Exchange-Organization-AuthSource |
action_result.data.\*.id | numeric | `cofense vision search id` | 2146 |
action_result.data.\*.internetMessageId | string | | |
action_result.data.\*.modifiedBy | string | | visionAdmin |
action_result.data.\*.modifiedDate | string | | 2022-12-09T20:16:42.868693 |
action_result.data.\*.partialIngest | string | | |
action_result.data.\*.receivedAfterDate | string | | |
action_result.data.\*.receivedBeforeDate | string | | |
action_result.data.\*.recipient | string | | |
action_result.data.\*.url | string | | |
action_result.summary.total_message_searches | numeric | | 50 |
action_result.message | string | | Total message searches: 50 |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'get message search'

Retrieves the search identified by an ID

Type: **investigate** <br>
Read only: **True**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**id** | required | The unique ID that cofense vision has assigned to a search | numeric | `cofense vision search id` |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.parameter.id | numeric | `cofense vision search id` | 1234 |
action_result.data.\*.attachmentHashCriteria.type | string | | ANY |
action_result.data.\*.createdBy | string | | CofenseTAP |
action_result.data.\*.createdDate | string | | 2022-12-09T20:31:12.605426 |
action_result.data.\*.domainCriteria.type | string | | ANY |
action_result.data.\*.id | numeric | `cofense vision search id` | 2147 |
action_result.data.\*.internetMessageId | string | | |
action_result.data.\*.modifiedBy | string | | CofenseTAP |
action_result.data.\*.modifiedDate | string | | 2022-12-09T20:31:12.605426 |
action_result.data.\*.partialIngest | string | | |
action_result.data.\*.receivedAfterDate | string | | |
action_result.data.\*.receivedBeforeDate | string | | |
action_result.data.\*.recipient | string | | |
action_result.data.\*.url | string | | |
action_result.summary | string | | |
action_result.message | string | | Fetched message search successfully |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'get quarantine job'

Retrieves quarantine job identified by the ID

Type: **investigate** <br>
Read only: **True**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**id** | required | ID of the quarantine job in cofense vision to be retrieved | numeric | `cofense vision quarantine job id` |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.parameter.id | numeric | `cofense vision quarantine job id` | 1234 |
action_result.data.\*.autoQuarantine | boolean | | True False |
action_result.data.\*.createdBy | string | | cds |
action_result.data.\*.createdDate | string | | 2022-07-07T11:47:47.831045 |
action_result.data.\*.emailCount | numeric | | 2 |
action_result.data.\*.id | numeric | `cofense vision quarantine job id` | 1234 |
action_result.data.\*.matchingIocInfo.\*.attributes.threat_type | string | | URL |
action_result.data.\*.matchingIocInfo.\*.attributes.threat_value | string | | https://test.com |
action_result.data.\*.matchingIocInfo.\*.id | string | | 4c620dda186fce3f088bd0c58b30dfaf |
action_result.data.\*.matchingIocInfo.\*.metadata.quarantine.created_at | string | | 2023-01-10T12:07:29.564+00:00 |
action_result.data.\*.matchingIocInfo.\*.metadata.quarantine.expired | boolean | | True False |
action_result.data.\*.matchingIocInfo.\*.metadata.quarantine.expires_at | string | | 2021-12-28T06:38:13.405+00:00 |
action_result.data.\*.matchingIocInfo.\*.metadata.quarantine.first_quarantined_at | string | | 2023-01-10T12:08:34.638+00:00 |
action_result.data.\*.matchingIocInfo.\*.metadata.quarantine.last_quarantined_at | string | | 2023-01-10T12:11:08.705+00:00 |
action_result.data.\*.matchingIocInfo.\*.metadata.quarantine.match_count | numeric | | 2 |
action_result.data.\*.matchingIocInfo.\*.metadata.quarantine.quarantine_count | numeric | | 2 |
action_result.data.\*.matchingIocInfo.\*.metadata.source | string | | |
action_result.data.\*.matchingIocInfo.\*.type | string | | ioc |
action_result.data.\*.modifiedBy | string | | system |
action_result.data.\*.modifiedDate | string | | 2022-07-07T12:39:26.128664 |
action_result.data.\*.quarantineEmails.\*.createdDate | string | | 2022-07-07T11:19:18.498196 |
action_result.data.\*.quarantineEmails.\*.errorMessage | string | | No primary addresses were found for 34/xxxxx@cofense.com |
action_result.data.\*.quarantineEmails.\*.ewsMessageId | string | | |
action_result.data.\*.quarantineEmails.\*.id | numeric | | 34 |
action_result.data.\*.quarantineEmails.\*.internetMessageId | string | | <BYAPR11MB2824EF099FE06D3740572200DC8D0@BYAPR11MB2824.namprd11.prod.outlook.com> |
action_result.data.\*.quarantineEmails.\*.originalFolderId | string | | |
action_result.data.\*.quarantineEmails.\*.quarantinedDate | string | | |
action_result.data.\*.quarantineEmails.\*.recipientAddress | string | | svc-nextgen-sw-2@cofense.com |
action_result.data.\*.quarantineEmails.\*.status | string | | UNKNOWN_MAILBOX |
action_result.data.\*.quarantineJobRuns.\*.completedDate | string | | 2022-07-07T11:47:54.77392 |
action_result.data.\*.quarantineJobRuns.\*.error | numeric | | 2 |
action_result.data.\*.quarantineJobRuns.\*.id | numeric | | 106 |
action_result.data.\*.quarantineJobRuns.\*.jobRunType | string | | QUARANTINE |
action_result.data.\*.quarantineJobRuns.\*.startedDate | string | | 2022-07-07T11:47:54.270013 |
action_result.data.\*.quarantineJobRuns.\*.status | string | | COMPLETED |
action_result.data.\*.quarantineJobRuns.\*.total | numeric | | 2 |
action_result.data.\*.searchId | string | | |
action_result.data.\*.stopRequested | boolean | | True False |
action_result.data.\*.context | string | | |
action_result.data.\*.detection | string | | |
action_result.data.\*.willRetry | boolean | | True False |
action_result.data.\*.aiClusterId | string | | |
action_result.data.\*.statusCounts.\*.count | numeric | | 2 |
action_result.data.\*.statusCounts.\*.status | string | | NEW |
action_result.data.\*.quarantineEmails.\*.isRead | string | | |
action_result.data.\*.quarantineEmails.\*.already | string | | |
action_result.data.\*.quarantineEmails.\*.foundEnvId | string | | |
action_result.data.\*.quarantineEmails.\*.ingestEnvId | string | | |
action_result.data.\*.quarantineEmails.\*.clickDetails | string | | |
action_result.data.\*.quarantineEmails.\*.isClickedAny | string | | |
action_result.data.\*.quarantineEmails.\*.isClickedIOC | string | | |
action_result.data.\*.quarantineEmails.\*.deleteDetails | string | | |
action_result.data.\*.quarantineEmails.\*.deletedByUser | string | | |
action_result.data.\*.quarantineEmails.\*.foundFolderType | string | | |
action_result.data.\*.quarantineEmails.\*.hasCalendarEvent | boolean | | True False |
action_result.data.\*.quarantineJobRuns.\*.createdBy | string | | crestdatauser |
action_result.data.\*.whoClickedPending | boolean | | True False |
action_result.data.\*.whoDeletedPending | boolean | | True False |
action_result.data.\*.isClusterInitiated | boolean | | True False |
action_result.data.\*.quarantineEmailReadStatusCounts.read | numeric | | |
action_result.data.\*.quarantineEmailReadStatusCounts.unRead | numeric | | |
action_result.data.\*.quarantineEmailReadStatusCounts.deleted | numeric | | |
action_result.data.\*.quarantineEmailReadStatusCounts.clickedAny | numeric | | |
action_result.data.\*.quarantineEmailReadStatusCounts.clickedIoc | numeric | | |
action_result.data.\*.quarantineEmailReadStatusCounts.notAvailable | numeric | | 2 |
action_result.data.\*.quarantineEmailReadStatusCounts.calendarEvents | numeric | | |
action_result.data.\*.quarantineEmailReadStatusCounts.whoDeletedStatus | string | | |
action_result.data.\*.quarantineEmailReadStatusCounts.whoClickedRetries | string | | |
action_result.data.\*.quarantineEmailReadStatusCounts.whoDeletedRetries | string | | |
action_result.data.\*.quarantineEmailReadStatusCounts.clickedNotAvailable | numeric | | 2 |
action_result.summary | string | | |
action_result.message | string | | Successfully retrieved the quarantine job information |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'approve quarantine job'

Approves the quarantine job identified by the ID. When the Auto Quarantine feature is configured to require manual approvals, this endpoint can approve the pending quarantine jobs

Type: **generic** <br>
Read only: **False**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**id** | required | ID of the quarantine job in cofense vision to be approved | numeric | `cofense vision quarantine job id` |
**message_count** | optional | Number of emails containing IOC matches to be quarantined | numeric | |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.parameter.id | numeric | `cofense vision quarantine job id` | 1234 |
action_result.parameter.message_count | numeric | | 3 |
action_result.data | string | | |
action_result.summary | string | | |
action_result.message | string | | The quarantine job has been approved successfully |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'delete quarantine job'

Deletes the quarantine job identified by the ID

Type: **generic** <br>
Read only: **False**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**id** | required | ID of the quarantine job in cofense vision to be deleted | numeric | `cofense vision quarantine job id` |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.parameter.id | numeric | `cofense vision quarantine job id` | 1422 |
action_result.data | string | | |
action_result.summary | string | | |
action_result.message | string | | Deleted the quarantine job successfully |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'get messagesearch results'

Retrieves the results for the search identified by the search ID

Type: **investigate** <br>
Read only: **True**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**id** | required | The unique ID that cofense vision has assigned to a search | numeric | `cofense vision search id` |
**page** | optional | Start page of the results. The value must be a positive integer or 0 | numeric | |
**size** | optional | Number of results to fetch per page. The value must be a positive integer up to 2000 | numeric | |
**sort** | optional | The name-value pair defining the order of the response. Comma separated values are supported | string | |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.parameter.id | numeric | `cofense vision search id` | 4825 |
action_result.parameter.page | numeric | | 0 |
action_result.parameter.size | numeric | | 50 |
action_result.parameter.sort | string | | createdBy:desc,id:asc |
action_result.data.\*.attachments.\*.contentType | string | | text/plain |
action_result.data.\*.attachments.\*.detectedContentType | string | | text/plain |
action_result.data.\*.attachments.\*.filename | string | | test_file.txt |
action_result.data.\*.attachments.\*.id | numeric | | 13933890 |
action_result.data.\*.attachments.\*.md5 | string | | d5d5ae3069669b4e08071e992f98f081 |
action_result.data.\*.attachments.\*.sha256 | string | | ef7247f075e010e7a9f4af6fa8f8dd4436b1cc12355226bbdc270a0fb1c885d0 |
action_result.data.\*.attachments.\*.size | numeric | | 3079266 |
action_result.data.\*.deliveredOn | string | | |
action_result.data.\*.from.\*.address | string | | testuser@test.com |
action_result.data.\*.from.\*.id | numeric | | 4406179 |
action_result.data.\*.from.\*.personal | string | | Test user |
action_result.data.\*.headers.\*.name | string | | X-MS-Exchange-Organization-InternalOrgSender |
action_result.data.\*.headers.\*.value | string | | False |
action_result.data.\*.htmlBody | string | | |
action_result.data.\*.id | numeric | | 4406179 |
action_result.data.\*.internetMessageId | string | `cofense vision internet message id` | <CAFRPxWtRtkkfV892gtZ+CsjtSECOZmA@test.com> |
action_result.data.\*.md5 | string | `md5` | ac208a9b84646dd7913c20520e2f9c6f |
action_result.data.\*.processedOn | string | | 2022-12-15T13:11:11.287+00:00 |
action_result.data.\*.receivedOn | string | | 2022-12-15T13:11:07.000+00:00 |
action_result.data.\*.recipients.\*.address | string | | testuser@test.com |
action_result.data.\*.recipients.\*.id | numeric | | 36939637 |
action_result.data.\*.recipients.\*.personal | string | | |
action_result.data.\*.recipients.\*.recipientType | string | | to |
action_result.data.\*.sentOn | string | | 2022-12-15T13:10:53.000+00:00 |
action_result.data.\*.sha1 | string | `sha1` | 31bc336427b2426c1480221b1ff1f1648adc4388 |
action_result.data.\*.sha256 | string | `sha256` | 48c13b22e3d6ffb9ad5f85b6c2a32b5c80bffcd563d8c04bb7befd01b803fc20 |
action_result.data.\*.subject | string | | A test mail |
action_result.data.\*.textBody | string | | |
action_result.data.\*.messageIdHeader | string | | <852266475.122.1788931518336@vision.cofenseselab.cofense-vision.com> |
action_result.data.\*.emailEnvironmentId | numeric | | 1 |
action_result.data.\*.networkMessageIdHeader | string | | face5fe2-79da-4d75-a9f0-08df0e32bcdc |
action_result.summary.total_results | numeric | | 4 |
action_result.message | string | | Total results: 4 |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'delete ioc'

Deletes a single active or expired IOC from the local IOC Repository

Type: **generic** <br>
Read only: **False**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**id** | required | The MD5 ID of the IOC to be deleted | string | `md5` `cofense vision ioc id` |
**source** | required | A single IOC source value, to fetch the IOCs added or modified by that particular source | string | `cofense vision source` |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.parameter.id | string | `md5` `cofense vision ioc id` | 27b609152ff01a84e0a7e421d7fd0fc7 |
action_result.parameter.source | string | `cofense vision source` | Triage-1 |
action_result.data.\*.attributes.threat_type | string | | URL |
action_result.data.\*.attributes.threat_value | string | `cofense vision threat value` `domain` `md5` `sha256` `url` | http://test.com/demo |
action_result.data.\*.id | string | `md5` `cofense vision ioc id` | 41ecc26bd356dd706cc1a0cd839cad2c |
action_result.data.\*.metadata.quarantine.created_at | string | | 2022-07-07T09:58:57.170+00:00 |
action_result.data.\*.metadata.quarantine.expired | boolean | | True False |
action_result.data.\*.metadata.quarantine.expires_at | string | | 2030-10-30T00:00:00.000+00:00 |
action_result.data.\*.metadata.quarantine.first_quarantined_at | string | | |
action_result.data.\*.metadata.quarantine.last_quarantined_at | string | | |
action_result.data.\*.metadata.quarantine.match_count | numeric | | |
action_result.data.\*.metadata.quarantine.quarantine_count | numeric | | |
action_result.data.\*.metadata.quarantine.wildcard | boolean | | True False |
action_result.data.\*.metadata.source.created_at | string | | 2020-01-30T00:00:00.000+00:00 |
action_result.data.\*.metadata.source.id | string | | arbitrary source identifier |
action_result.data.\*.metadata.source.requested_expiration | string | | 2030-10-30T00:00:00.000+00:00 |
action_result.data.\*.metadata.source.threat_level | string | | Malicious |
action_result.data.\*.metadata.source.updated_at | string | | 2020-03-30T00:00:00.000+00:00 |
action_result.data.\*.type | string | | ioc |
action_result.summary | string | | |
action_result.message | string | | Delete IOC action ran successfully |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'stop quarantine job'

Issues a request to stop the quarantine job identified by ID

Type: **generic** <br>
Read only: **False**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**id** | required | ID of the quarantine job in cofense vision to be stopped | numeric | `cofense vision quarantine job id` |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.parameter.id | numeric | `cofense vision quarantine job id` | 1234 |
action_result.data.\*.autoQuarantine | boolean | | True False |
action_result.data.\*.createdBy | string | | cds |
action_result.data.\*.createdDate | string | | 2022-07-07T11:47:47.831045 |
action_result.data.\*.emailCount | numeric | | 2 |
action_result.data.\*.id | numeric | `cofense vision quarantine job id` | 1234 |
action_result.data.\*.modifiedBy | string | | cds |
action_result.data.\*.modifiedDate | string | | 2023-01-16T07:08:42.068037 |
action_result.data.\*.quarantineEmails.\*.createdDate | string | | 2022-07-07T11:19:18.498196 |
action_result.data.\*.quarantineEmails.\*.errorMessage | string | | No primary addresses were found for 34/xxxxx@cofense.com |
action_result.data.\*.quarantineEmails.\*.ewsMessageId | string | | |
action_result.data.\*.quarantineEmails.\*.id | numeric | | 34 |
action_result.data.\*.quarantineEmails.\*.internetMessageId | string | | <BYAPR11MB2824EF099FE06D3740572200DC8D0@BYAPR11MB2824.namprd11.prod.outlook.com> |
action_result.data.\*.quarantineEmails.\*.originalFolderId | string | | |
action_result.data.\*.quarantineEmails.\*.quarantinedDate | string | | |
action_result.data.\*.quarantineEmails.\*.recipientAddress | string | | svc-nextgen-sw-2@cofense.com |
action_result.data.\*.quarantineEmails.\*.status | string | | UNKNOWN_MAILBOX |
action_result.data.\*.quarantineJobRuns.\*.completedDate | string | | 2022-07-07T11:47:54.77392 |
action_result.data.\*.quarantineJobRuns.\*.error | numeric | | 2 |
action_result.data.\*.quarantineJobRuns.\*.id | numeric | | 106 |
action_result.data.\*.quarantineJobRuns.\*.jobRunType | string | | QUARANTINE |
action_result.data.\*.quarantineJobRuns.\*.startedDate | string | | 2022-07-07T11:47:54.270013 |
action_result.data.\*.quarantineJobRuns.\*.status | string | | COMPLETED |
action_result.data.\*.quarantineJobRuns.\*.total | numeric | | 2 |
action_result.data.\*.searchId | string | | |
action_result.data.\*.stopRequested | boolean | | True False |
action_result.data.\*.context | string | | |
action_result.data.\*.detection | string | | |
action_result.data.\*.willRetry | boolean | | True False |
action_result.data.\*.aiClusterId | string | | |
action_result.data.\*.statusCounts.\*.count | numeric | | 2 |
action_result.data.\*.statusCounts.\*.status | string | | QUARANTINE_ERROR |
action_result.data.\*.quarantineEmails.\*.isRead | string | | |
action_result.data.\*.quarantineEmails.\*.already | string | | |
action_result.data.\*.quarantineEmails.\*.foundEnvId | string | | |
action_result.data.\*.quarantineEmails.\*.ingestEnvId | string | | |
action_result.data.\*.quarantineEmails.\*.clickDetails | string | | |
action_result.data.\*.quarantineEmails.\*.isClickedAny | string | | |
action_result.data.\*.quarantineEmails.\*.isClickedIOC | string | | |
action_result.data.\*.quarantineEmails.\*.deleteDetails | string | | |
action_result.data.\*.quarantineEmails.\*.deletedByUser | string | | |
action_result.data.\*.quarantineEmails.\*.foundFolderType | string | | |
action_result.data.\*.quarantineEmails.\*.hasCalendarEvent | boolean | | True False |
action_result.data.\*.quarantineJobRuns.\*.createdBy | string | | crestdatauser |
action_result.data.\*.whoClickedPending | boolean | | True False |
action_result.data.\*.whoDeletedPending | boolean | | True False |
action_result.data.\*.isClusterInitiated | boolean | | True False |
action_result.data.\*.quarantineEmailReadStatusCounts.read | numeric | | |
action_result.data.\*.quarantineEmailReadStatusCounts.unRead | numeric | | |
action_result.data.\*.quarantineEmailReadStatusCounts.deleted | numeric | | |
action_result.data.\*.quarantineEmailReadStatusCounts.clickedAny | numeric | | |
action_result.data.\*.quarantineEmailReadStatusCounts.clickedIoc | numeric | | |
action_result.data.\*.quarantineEmailReadStatusCounts.notAvailable | numeric | | 2 |
action_result.data.\*.quarantineEmailReadStatusCounts.calendarEvents | numeric | | |
action_result.data.\*.quarantineEmailReadStatusCounts.whoDeletedStatus | string | | DONE_NO_DELETER |
action_result.data.\*.quarantineEmailReadStatusCounts.whoClickedRetries | string | | |
action_result.data.\*.quarantineEmailReadStatusCounts.whoDeletedRetries | numeric | | 1 |
action_result.data.\*.quarantineEmailReadStatusCounts.clickedNotAvailable | numeric | | 2 |
action_result.summary | string | | |
action_result.message | string | | Successfully stopped the quarantine job |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'create message search'

Creates a new search based on the user-specified filters

Type: **generic** <br>
Read only: **False**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**subjects** | optional | A comma-separated string of subjects to create a search for an email's subject. Max 3 values are allowed | string | |
**senders** | optional | A comma-separated string of senders to create a search for an email's sender. Max 3 values are allowed | string | |
**attachment_names** | optional | A comma-separated string of attachment names to create a search for an email's attachments. Max 3 values are allowed | string | |
**attachment_hash_match_criteria** | optional | The type of matching performed on the hashes specified in the attachment_hashes argument. Allowed values are ANY and ALL | string | |
**attachment_hashes** | optional | A comma-separated string of attachment hashes to create a search for an email's attachment hashes. Supported format: hashtype1:hashvalue1. Example : md5:938c2cc0dcc05f2b68c4287040cfcf71. Max 3 values are allowed | string | |
**attachment_mime_types** | optional | A comma-separated string of MIME types to create a search for an email's attachment MIME type. Max 3 values are allowed | string | |
**attachment_exclude_mime_types** | optional | A comma-separated string of MIME types to create a search for excluding an email's attachment MIME type. Max 3 values are allowed | string | |
**domain_match_criteria** | optional | The type of matching to perform on the domains specified in the domains argument. Allowed values ANY and ALL | string | |
**domains** | optional | A comma-separated string of domains to create a search for domains in an email's body or its attachment. Max 3 values are allowed | string | |
**headers** | optional | A comma-separated string of key-value pairs, defining the additional criteria to search for in the email header. Max 3 values are allowed | string | |
**internet_message_id** | optional | The unique identifier of the email, enclosed in angle brackets. This argument is case-sensitive | string | `cofense vision internet message id` |
**partial_ingest** | optional | Whether to create a search with partially ingested emails (true) or without partially ingested emails (false) | boolean | |
**received_after_date** | optional | Date and time to create a search for emails which are received on or after the specified UTC date and time | string | |
**received_before_date** | optional | Date and time to create a search for emails which are received before or on the specified UTC date and time | string | |
**recipient** | optional | Create a search with the specified recipient. Supports one or more wildcard characters (\*) in any position of a recipient's email address | string | |
**url** | optional | Create a search with the specified url. Supports one or more wildcard characters (\*) in any position of the URL | string | |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.parameter.attachment_exclude_mime_types | string | | image/png |
action_result.parameter.attachment_hash_match_criteria | string | | ANY |
action_result.parameter.attachment_hashes | string | | md5:938c2cc0dcc05f2b68c4287040cfcf71 |
action_result.parameter.attachment_mime_types | string | | image/png |
action_result.parameter.attachment_names | string | | test.png |
action_result.parameter.domain_match_criteria | string | | ANY |
action_result.parameter.domains | string | | test.com |
action_result.parameter.headers | string | | X-MS-Exchange-Organization-AuthSource:DM6PR19MB3772.namprd19.prod.test.com |
action_result.parameter.internet_message_id | string | `cofense vision internet message id` | <1C626FCE-6749-4DE9-884C-C025173F80BB@phishme.com> |
action_result.parameter.partial_ingest | boolean | | True False |
action_result.parameter.received_after_date | string | | 2022-12-22T12:27:29.768 |
action_result.parameter.received_before_date | string | | 2022-12-22T12:27:29.768 |
action_result.parameter.recipient | string | | fname.lname@phishme.com |
action_result.parameter.senders | string | | fname.lname@phishme.com |
action_result.parameter.subjects | string | | This is a test subject |
action_result.parameter.url | string | | https://test.com |
action_result.data.\*.attachmentHashCriteria.attachmentHashes.\*.hashString | string | | 938c2cc0dcc05f2b68c4287040cfcf71 |
action_result.data.\*.attachmentHashCriteria.attachmentHashes.\*.hashType | string | | MD5 |
action_result.data.\*.attachmentHashCriteria.type | string | | ANY |
action_result.data.\*.createdBy | string | | cds |
action_result.data.\*.createdDate | string | | 2022-12-22T12:27:29.768 |
action_result.data.\*.domainCriteria.type | string | | ANY |
action_result.data.\*.headers.\*.key | string | | X-MS-Exchange-Organization-AuthSource |
action_result.data.\*.id | numeric | `cofense vision search id` | 3972 |
action_result.data.\*.internetMessageId | string | | <1C626FCE-6749-4DE9-884C-C025173F80BB@phishme.com> |
action_result.data.\*.modifiedBy | string | | cds |
action_result.data.\*.modifiedDate | string | | 2022-12-22T12:27:29.768 |
action_result.data.\*.partialIngest | boolean | | True False |
action_result.data.\*.receivedAfterDate | string | | 2023-01-01T12:27:29.768 |
action_result.data.\*.receivedBeforeDate | string | | 2023-01-03T12:27:29.768 |
action_result.data.\*.recipient | string | | test@test.com |
action_result.data.\*.url | string | | https://test.com |
action_result.summary | string | | |
action_result.summary.search_id | numeric | | 3646 |
action_result.message | string | | Search id: 3482 |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'get last ioc'

Retrieves the last updated IOC from the local IOC Repository. It may return an active or an expired IOC

Type: **investigate** <br>
Read only: **True**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**source** | required | A single IOC source value, to fetch the IOCs added or modified by that particular source | string | `cofense vision source` |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.parameter.source | string | `cofense vision source` | Triage-1 |
action_result.data.\*.attributes.threat_type | string | | URL |
action_result.data.\*.attributes.threat_value | string | `cofense vision threat value` `domain` `md5` `sha256` `url` | http://test.com/demo |
action_result.data.\*.id | string | `md5` `cofense vision ioc id` | 41ecc26bd356dd706cc1a0cd839cad2c |
action_result.data.\*.metadata.quarantine.created_at | string | | 2022-07-07T09:58:57.170+00:00 |
action_result.data.\*.metadata.quarantine.expired | boolean | | True False |
action_result.data.\*.metadata.quarantine.expires_at | string | | 2030-10-30T00:00:00.000+00:00 |
action_result.data.\*.metadata.quarantine.first_quarantined_at | string | | |
action_result.data.\*.metadata.quarantine.last_quarantined_at | string | | |
action_result.data.\*.metadata.quarantine.match_count | numeric | | |
action_result.data.\*.metadata.quarantine.quarantine_count | numeric | | |
action_result.data.\*.metadata.quarantine.wildcard | boolean | | True False |
action_result.data.\*.metadata.source.created_at | string | | 2020-01-30T00:00:00.000+00:00 |
action_result.data.\*.metadata.source.id | string | | arbitrary source identifier |
action_result.data.\*.metadata.source.requested_expiration | string | | 2030-10-30T00:00:00.000+00:00 |
action_result.data.\*.metadata.source.threat_level | string | | Malicious |
action_result.data.\*.metadata.source.updated_at | string | | 2020-03-30T00:00:00.000+00:00 |
action_result.data.\*.type | string | | ioc |
action_result.data.\*.metadata.source.created_by | string | | Devon@GJBData.com |
action_result.data.\*.metadata.quarantine.false_positive | boolean | | True False |
action_result.data.\*.metadata.quarantine.email_restore_count | numeric | | |
action_result.data.\*.metadata.quarantine.recipient_restore_count | numeric | | |
action_result.data.\*.metadata.quarantine.email_quarantine_success | numeric | | 3466 |
action_result.data.\*.metadata.quarantine.recipient_quarantine_success | numeric | | 10674 |
action_result.summary | string | | |
action_result.summary.ioc_id | string | | d1c54c37fd53d37094ef1dc7530ca949 |
action_result.message | string | | Get Last IOC Action succeeded |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'update iocs'

Updates one or more IOCs stored in the local IOC repository

Type: **generic** <br>
Read only: **False**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**source** | required | Single IOC source | string | `cofense vision source` |
**iocs_json** | optional | List of JSON data containing IOC detail to be updated in the IOC local repository | string | |
**threat_type** | optional | Type of IOC | string | |
**threat_value** | optional | Actual value of the IOC to match in the email | string | `cofense vision threat value` `domain` `md5` `sha256` `url` |
**threat_level** | optional | The severity of the IOC | string | |
**source_id** | optional | Unique identifier assigned by the IOC source | string | |
**created_at** | optional | The UTC date and time the IOC source included the IOC for the first time | string | |
**updated_at** | optional | The UTC date and time the IOC source last updated the IOC | string | |
**requested_expiration** | optional | Expiration date and time for this IOC in UTC | string | |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.parameter.created_at | string | | 4/10/2022 |
action_result.parameter.iocs_json | string | | [{"threat_type": "Domain","threat_value": "test1.com","threat_level": "Malicious","created_at": "20/08/2032","source_id": "test_source_1","updated_at": "20/08/2032","requested_expiration": "30/08/2032"},{"threat_type": "Domain","threat_value": "test2.com","threat_level": "Malicious","created_at": "20/08/2032","source_id": "test_source_2","updated_at": "20/08/2032","requested_expiration": "30/08/2032"}] |
action_result.parameter.requested_expiration | string | | 4/12/2022 |
action_result.parameter.source | string | `cofense vision source` | Vision-UI |
action_result.parameter.source_id | string | | test_source_id |
action_result.parameter.threat_level | string | | Malicious |
action_result.parameter.threat_type | string | | URL |
action_result.parameter.threat_value | string | `cofense vision threat value` `domain` `md5` `sha256` `url` | https://domain.com |
action_result.parameter.updated_at | string | | 4/11/2022 |
action_result.data.\*.attributes.threat_type | string | | URL |
action_result.data.\*.attributes.threat_value | string | `cofense vision threat value` `domain` `md5` `sha256` `url` | https://domain.com |
action_result.data.\*.id | string | `md5` `cofense vision ioc id` | 7a89dc65140fdd10a71bf4c4721df6f4 |
action_result.data.\*.metadata.quarantine.created_at | string | | 2022-12-28T08:53:19.112+00:00 |
action_result.data.\*.metadata.quarantine.expired | boolean | | True False |
action_result.data.\*.metadata.quarantine.expires_at | string | | 2025-04-17T14:05:00.000+00:00 |
action_result.data.\*.metadata.quarantine.first_quarantined_at | string | | |
action_result.data.\*.metadata.quarantine.last_quarantined_at | string | | |
action_result.data.\*.metadata.quarantine.match_count | numeric | | |
action_result.data.\*.metadata.quarantine.quarantine_count | numeric | | |
action_result.data.\*.metadata.quarantine.wildcard | boolean | | True False |
action_result.data.\*.metadata.source.created_at | string | | 2022-04-10T00:00:00.000+00:00 |
action_result.data.\*.metadata.source.id | string | | test_source_id |
action_result.data.\*.metadata.source.requested_expiration | string | | 2022-04-12T00:00:00.000+00:00 |
action_result.data.\*.metadata.source.threat_level | string | | Malicious |
action_result.data.\*.metadata.source.updated_at | string | | 2022-04-11T00:00:00.000+00:00 |
action_result.data.\*.type | string | | ioc |
action_result.summary.total_iocs_updated | numeric | | 1 |
action_result.message | string | | Total iocs updated: 1 |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'update ioc'

Updates the IOC identified by its unique MD5 ID

Type: **generic** <br>
Read only: **False**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**id** | required | The ID of the IOC to be updated | string | `md5` `cofense vision ioc id` |
**expires_at** | required | Expiration date and time of the IOC in UTC | string | |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.parameter.expires_at | string | | 2080-05-15 |
action_result.parameter.id | string | `md5` `cofense vision ioc id` | 7a785c76033e6e2f1464ba3f41ffb23a |
action_result.data.\*.attributes.threat_type | string | | URL |
action_result.data.\*.attributes.threat_value | string | `cofense vision threat value` `domain` `md5` `sha256` `url` | https://test.com |
action_result.data.\*.id | string | `md5` `cofense vision ioc id` | 7a785c76033e6e2f1464ba3f41ffb23a |
action_result.data.\*.metadata.quarantine.created_at | string | | 2023-01-02T09:43:38.392+00:00 |
action_result.data.\*.metadata.quarantine.expired | boolean | | True False |
action_result.data.\*.metadata.quarantine.expires_at | string | | 2080-05-15T00:00:00.000+00:00 |
action_result.data.\*.metadata.quarantine.first_quarantined_at | string | | |
action_result.data.\*.metadata.quarantine.last_quarantined_at | string | | |
action_result.data.\*.metadata.quarantine.match_count | numeric | | |
action_result.data.\*.metadata.quarantine.quarantine_count | numeric | | |
action_result.data.\*.metadata.quarantine.wildcard | boolean | | True False |
action_result.data.\*.metadata.source | string | | |
action_result.data.\*.type | string | | ioc |
action_result.summary | string | | |
action_result.message | string | | |
summary.total_objects | numeric | | |
summary.total_objects_successful | numeric | | |

## action: 'list iocs'

Lists the IOCs stored in the local IOC Repository

Type: **investigate** <br>
Read only: **True**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**source** | required | A single IOC source value | string | `cofense vision source` |
**since** | optional | Include only IOCs that were added to the repository after the given UTC date | string | |
**page** | optional | Start page of the results. The value must be a positive integer or 0 | numeric | |
**size** | optional | Number of results to fetch per page. The value must be a positive integer up to 2000 | numeric | |
**sort** | optional | The name-value pair defining the order of the response. Comma separated values are supported | string | |
**include_expired** | optional | Whether to include expired IOCs (true) or not include expired IOCs (false) | boolean | |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.parameter.include_expired | boolean | | True False |
action_result.parameter.page | numeric | | 0 |
action_result.parameter.since | string | | 4/10/2022 |
action_result.parameter.size | numeric | | 50 |
action_result.parameter.sort | string | | UpdatedAt:asc |
action_result.parameter.source | string | `cofense vision source` | Vision-UI |
action_result.data.\*.attributes.threat_type | string | | URL |
action_result.data.\*.attributes.threat_value | string | `cofense vision threat value` `domain` `md5` `sha256` `url` | http://test.com/demo |
action_result.data.\*.id | string | `md5` `cofense vision ioc id` | e2c28ae167b51ad9e2eb8c656ab88ccb |
action_result.data.\*.metadata.quarantine.created_at | string | | 2022-12-28T09:35:32.011+00:00 |
action_result.data.\*.metadata.quarantine.expired | boolean | | True False |
action_result.data.\*.metadata.quarantine.expires_at | string | | 2030-10-30T00:00:00.000+00:00 |
action_result.data.\*.metadata.quarantine.first_quarantined_at | string | | |
action_result.data.\*.metadata.quarantine.last_quarantined_at | string | | |
action_result.data.\*.metadata.quarantine.match_count | numeric | | 1 |
action_result.data.\*.metadata.quarantine.quarantine_count | numeric | | 1 |
action_result.data.\*.metadata.quarantine.wildcard | boolean | | True False |
action_result.data.\*.metadata.source.created_at | string | | 2021-02-03T00:00:00.000+00:00 |
action_result.data.\*.metadata.source.id | string | | sid_12345 |
action_result.data.\*.metadata.source.requested_expiration | string | | 2030-10-30T00:00:00.000+00:00 |
action_result.data.\*.metadata.source.threat_level | string | | Malicious |
action_result.data.\*.metadata.source.updated_at | string | | 2020-03-28T00:00:00.000+00:00 |
action_result.data.\*.type | string | | ioc |
action_result.data.\*.metadata.source.created_by | string | | Devon@GJBData.com |
action_result.data.\*.metadata.quarantine.false_positive | boolean | | True False |
action_result.data.\*.metadata.quarantine.email_restore_count | numeric | | |
action_result.data.\*.metadata.quarantine.recipient_restore_count | numeric | | |
action_result.data.\*.metadata.quarantine.email_quarantine_success | numeric | | 3466 |
action_result.data.\*.metadata.quarantine.recipient_quarantine_success | numeric | | 10674 |
action_result.summary.total_iocs | numeric | | 5 |
action_result.message | string | | Total iocs: 10 |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'get ioc'

Retrieves the IOC identified by its unique MD5 ID

Type: **investigate** <br>
Read only: **True**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**id** | required | The MD5 ID of the IOC | string | `md5` `cofense vision ioc id` |
**source** | required | A single IOC source value, to fetch the IOCs added or modified by that particular source | string | `cofense vision source` |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.parameter.id | string | `md5` `cofense vision ioc id` | 27b609152ff01a84e0a7e421d7fd0fc7 |
action_result.parameter.source | string | `cofense vision source` | Triage-1 |
action_result.data.\*.attributes.threat_type | string | | URL |
action_result.data.\*.attributes.threat_value | string | `cofense vision threat value` `domain` `md5` `sha256` `url` | http://test.com/demo |
action_result.data.\*.id | string | `md5` | 41ecc26bd356dd706cc1a0cd839cad2c |
action_result.data.\*.metadata.quarantine.created_at | string | | 2022-07-07T09:58:57.170+00:00 |
action_result.data.\*.metadata.quarantine.expired | boolean | | True False |
action_result.data.\*.metadata.quarantine.expires_at | string | | 2030-10-30T00:00:00.000+00:00 |
action_result.data.\*.metadata.quarantine.first_quarantined_at | string | | |
action_result.data.\*.metadata.quarantine.last_quarantined_at | string | | |
action_result.data.\*.metadata.quarantine.match_count | numeric | | |
action_result.data.\*.metadata.quarantine.quarantine_count | numeric | | |
action_result.data.\*.metadata.quarantine.wildcard | boolean | | True False |
action_result.data.\*.metadata.source.created_at | string | | 2020-01-30T00:00:00.000+00:00 |
action_result.data.\*.metadata.source.id | string | | arbitrary source identifier |
action_result.data.\*.metadata.source.requested_expiration | string | | 2030-10-30T00:00:00.000+00:00 |
action_result.data.\*.metadata.source.threat_level | string | | Malicious |
action_result.data.\*.metadata.source.updated_at | string | | 2020-03-30T00:00:00.000+00:00 |
action_result.data.\*.type | string | | ioc |
action_result.summary | string | | |
action_result.message | string | | Get IOC action passed |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'list searchable headers'

Retrieves a list of configured header keys that can be used to create a message search

Type: **investigate** <br>
Read only: **True**

#### Action Parameters

No parameters are required for this action

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.data.\*.header | string | | |
action_result.summary | string | | |
action_result.message | string | | Total searchable headers: 25 |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'download logs'

Downloads the log files for all Cofense Vision components

Type: **investigate** <br>
Read only: **True**

#### Action Parameters

No parameters are required for this action

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.data.\*.aka.\* | string | | test.txt |
action_result.data.\*.container | string | | Test |
action_result.data.\*.container_id | numeric | | 5 |
action_result.data.\*.create_time | string | | 0 minutes ago |
action_result.data.\*.created_via | string | | automation |
action_result.data.\*.hash | string | `vault id` | 31c194010afedb76694517e6250b5339d72ed518 |
action_result.data.\*.id | numeric | | 29 |
action_result.data.\*.metadata.sha1 | string | `sha1` | 31c194010afedb76694517e6250b5339d72ed518 |
action_result.data.\*.metadata.sha256 | string | `sha256` | ef7247f075e010e7a9f4af6fa8f8dd4436b1cc12355226bbdc270a0fb1c885d0 |
action_result.data.\*.mime_type | string | | text/plain |
action_result.data.\*.name | string | | logfiles_2023-01-06_06:49:00.536505.zip |
action_result.data.\*.path | string | | /opt/phantom/vault/31/c1/31c194010afedb76694517e6250b5339d72ed518 |
action_result.data.\*.size | numeric | | 3079266 |
action_result.data.\*.task | string | | |
action_result.data.\*.user | string | | admin |
action_result.data.\*.vault_document | numeric | | 29 |
action_result.data.\*.vault_id | string | `vault id` | 31c194010afedb76694517e6250b5339d72ed518 |
action_result.data.\*.es_attachment_id | string | | |
action_result.summary.vault_id | string | `vault id` | 31c194010afedb76694517e6250b5339d72ed518 |
action_result.message | string | | Vault id: 31c194010afedb76694517e6250b5339d72ed518 |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'list clusters'

Retrieves clusters that contain at least one email with an ingestion timestamp that falls in the requested date and time range

Type: **investigate** <br>
Read only: **True**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**page** | optional | Start page of the results. The value must be a positive integer or 0 | numeric | |
**size** | optional | Number of results per page. The value must be a positive integer up to 2000 | numeric | |
**sort_field** | optional | Sort results based on this field | string | |
**order** | optional | Order for the sorted field | string | |
**from_date** | optional | Emails ingested on or after this date and time. The date and time must be in UTC in ISO 8601 format, for example: 2024-05-31T00:00:00.000Z | string | |
**to_date** | optional | Emails ingested before this date and time. The date and time must be in UTC in ISO 8601 format, for example: 2024-05-31T00:00:00.000Z | string | |
**exclude_emails** | optional | Whether to remove the email details from the response | boolean | |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.parameter.page | numeric | | 0 |
action_result.parameter.size | numeric | | 50 |
action_result.parameter.sort_field | string | | createdDate |
action_result.parameter.order | string | | desc |
action_result.parameter.from_date | string | | 2024-05-31T00:00:00.000Z |
action_result.parameter.to_date | string | | 2024-06-07T00:00:00.000Z |
action_result.parameter.exclude_emails | boolean | | True False |
action_result.data.\*.id | numeric | `cofense vision cluster id` | 2 |
action_result.data.\*.title | string | | Credential phishing campaign targeting finance |
action_result.data.\*.fromDate | string | | 2025-06-01T08:00:00Z |
action_result.data.\*.toDate | string | | 2025-06-01T12:30:00Z |
action_result.data.\*.similarityLevel | numeric | | 5 |
action_result.data.\*.emailCount | numeric | | 47 |
action_result.data.\*.recipientCount | numeric | | 287 |
action_result.data.\*.userNote | string | | Escalated to SOC for immediate review. |
action_result.data.\*.signals | string | | VARIED_URLS VARIED_SENDER |
action_result.data.\*.iocIds | string | | a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6 |
action_result.data.\*.iocInfo | string | | |
action_result.data.\*.avgCharacterCount | numeric | | 1145 |
action_result.data.\*.centroids | string | | |
action_result.data.\*.disabledAQ | boolean | | True False |
action_result.data.\*.envIds | string | | |
action_result.data.\*.similarityLevelCalculated | numeric | | |
action_result.data.\*.uniqueSenderCount | numeric | | |
action_result.data.\*.emails.\*.subject | string | | Urgent: Verify your account |
action_result.data.\*.createdDate | string | | 2025-06-01T07:55:00Z |
action_result.data.\*.modifiedDate | string | | 2025-06-01T13:00:00Z |
action_result.data.\*.quarantineJobIds | string | `cofense vision quarantine job id` | 42 |
action_result.data.\*.emails | string | | |
action_result.data.\*.centroids.centroid1 | numeric | | -3233901077497987035 |
action_result.data.\*.centroids.centroid3 | string | | |
action_result.data.\*.emails.\*.envId | numeric | | 1 |
action_result.data.\*.emails.\*.iocIds | string | | |
action_result.data.\*.emails.\*.sender | string | | vision@vision.cofenseselab.cofense-vision.com |
action_result.data.\*.emails.\*.messageId | string | | <1234679914.1121.1791784062046@vision.cofenseselab.cofense-vision.com> |
action_result.data.\*.emails.\*.signature.hash1 | numeric | | -3234041814986375131 |
action_result.data.\*.emails.\*.signature.hash2 | string | | |
action_result.data.\*.emails.\*.signature.hash3 | string | | |
action_result.data.\*.emails.\*.signature.normalizedTokenCount | string | | |
action_result.data.\*.emails.\*.signature.normalizedContentHash | string | | -6032669796344245314 |
action_result.data.\*.emails.\*.signature.normalizedCharacterCount | numeric | | 462 |
action_result.data.\*.emails.\*.processedOn | string | | 2026-10-12T05:48:07.182Z |
action_result.data.\*.emails.\*.recipientCount | numeric | | 1 |
action_result.data.\*.emails.\*.quarantineJobId | string | | |
action_result.data.\*.emails.\*.similarityLevel | numeric | | 10 |
action_result.data.\*.emails.\*.combinedMessageId | string | | d67c9fec-1f6d-4937-68f3-08df2824558a / <1234679914.1121.1791784062046@vision.cofenseselab.cofense-vision.com> |
action_result.summary.total_clusters | numeric | | 1 |
action_result.message | string | | Total clusters: 1 |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'get cluster'

Retrieves a single cluster identified by the ID, including the emails in the cluster

Type: **investigate** <br>
Read only: **True**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**id** | required | ID of the cluster to retrieve | numeric | `cofense vision cluster id` |
**exclude_emails** | optional | Whether to remove the email details from the response | boolean | |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.parameter.id | numeric | `cofense vision cluster id` | 2 |
action_result.parameter.exclude_emails | boolean | | True False |
action_result.data.\*.id | numeric | `cofense vision cluster id` | 2 |
action_result.data.\*.title | string | | Splunk SOAR Test |
action_result.data.\*.userNote | string | | |
action_result.data.\*.signals | string | | VARIED_URLS VARIED_SENDER |
action_result.data.\*.iocIds | string | | a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6 |
action_result.data.\*.iocInfo | string | | |
action_result.data.\*.avgCharacterCount | numeric | | 1145 |
action_result.data.\*.centroids | string | | |
action_result.data.\*.disabledAQ | string | | |
action_result.data.\*.envIds | string | | |
action_result.data.\*.similarityLevel | numeric | | 5 |
action_result.data.\*.similarityLevelCalculated | string | | |
action_result.data.\*.uniqueSenderCount | numeric | | |
action_result.data.\*.emailCount | numeric | | 47 |
action_result.data.\*.recipientCount | numeric | | 287 |
action_result.data.\*.fromDate | string | | 2025-06-01T08:00:00Z |
action_result.data.\*.toDate | string | | 2025-06-01T12:30:00Z |
action_result.data.\*.emails.\*.subject | string | | Urgent: Verify your account |
action_result.data.\*.createdDate | string | | 2025-06-01T07:55:00Z |
action_result.data.\*.modifiedDate | string | | 2025-06-01T13:00:00Z |
action_result.data.\*.quarantineJobIds | string | `cofense vision quarantine job id` | |
action_result.data.\*.emails | string | | |
action_result.data.\*.centroids.centroid1 | numeric | | -3309326476157132231 |
action_result.data.\*.centroids.centroid3 | string | | |
action_result.data.\*.emails.\*.envId | numeric | | 1 |
action_result.data.\*.emails.\*.iocIds | string | | |
action_result.data.\*.emails.\*.sender | string | | vision@vision.cofenseselab.cofense-vision.com |
action_result.data.\*.emails.\*.messageId | string | | <1085709641.289.1789027601150@vision.cofenseselab.cofense-vision.com> |
action_result.data.\*.emails.\*.signature.hash1 | numeric | | -1003483466943248855 |
action_result.data.\*.emails.\*.signature.hash2 | string | | |
action_result.data.\*.emails.\*.signature.hash3 | string | | |
action_result.data.\*.emails.\*.signature.normalizedTokenCount | string | | |
action_result.data.\*.emails.\*.signature.normalizedContentHash | string | | -6457353019152139510 |
action_result.data.\*.emails.\*.signature.normalizedCharacterCount | numeric | | 446 |
action_result.data.\*.emails.\*.processedOn | string | | 2026-09-10T08:06:59.275Z |
action_result.data.\*.emails.\*.recipientCount | numeric | | 1 |
action_result.data.\*.emails.\*.quarantineJobId | string | | |
action_result.data.\*.emails.\*.similarityLevel | numeric | | 8 |
action_result.data.\*.emails.\*.combinedMessageId | string | | 05bf32c4-3f14-4741-c0db-08df0f1272f4 / <1085709641.289.1789027601150@vision.cofenseselab.cofense-vision.com> |
action_result.message | string | | Successfully retrieved the cluster information |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'update cluster'

Updates the cluster identified by the ID

Type: **generic** <br>
Read only: **False**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**id** | required | ID of the cluster to update | numeric | `cofense vision cluster id` |
**title** | optional | Title to be assigned to the cluster | string | |
**note** | optional | Note to be added to the cluster | string | |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.parameter.id | numeric | `cofense vision cluster id` | 2 |
action_result.parameter.title | string | | Splunk SOAR Test |
action_result.parameter.note | string | | Updating for testing |
action_result.data.\*.id | numeric | `cofense vision cluster id` | 2 |
action_result.data.\*.title | string | | Credential phishing campaign targeting finance dept |
action_result.data.\*.userNote | string | | Escalated to SOC for immediate review. |
action_result.data.\*.signals | string | | VARIED_URLS VARIED_SENDER |
action_result.data.\*.iocIds | string | | a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6 |
action_result.data.\*.avgCharacterCount | numeric | | 1145 |
action_result.data.\*.createdDate | string | | 2025-06-01T07:55:00Z |
action_result.data.\*.modifiedDate | string | | 2025-06-05T16:42:00Z |
action_result.data.\*.quarantineJobIds | string | `cofense vision quarantine job id` | |
action_result.data.\*.emails | string | | |
action_result.data.\*.toDate | string | | 2026-09-10T08:06:59.275Z |
action_result.data.\*.fromDate | string | | 2026-05-14T17:37:40.479Z |
action_result.data.\*.centroids.centroid1 | numeric | | -3309326476157132231 |
action_result.data.\*.centroids.centroid3 | string | | |
action_result.data.\*.disabledAQ | string | | |
action_result.data.\*.emailCount | numeric | | 4949 |
action_result.data.\*.recipientCount | numeric | | 4949 |
action_result.data.\*.similarityLevel | numeric | | 3 |
action_result.data.\*.uniqueSenderCount | numeric | | 1 |
action_result.data.\*.similarityLevelCalculated | string | | |
action_result.data.\*.envIds | string | | |
action_result.message | string | | Successfully updated the cluster |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'quarantine cluster'

Manually creates a quarantine job for all emails in a cluster that are not already associated with an existing quarantine job for this cluster

Type: **contain** <br>
Read only: **False**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**id** | required | ID of the cluster to quarantine | numeric | `cofense vision cluster id` |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.parameter.id | numeric | `cofense vision cluster id` | 2 |
action_result.data.\*.id | numeric | `cofense vision quarantine job id` | 1458 |
action_result.data.\*.aiClusterId | numeric | `cofense vision cluster id` | 1 |
action_result.data.\*.autoQuarantine | boolean | | True False |
action_result.data.\*.status | string | | COMPLETED |
action_result.data.\*.stopRequested | boolean | | True False |
action_result.data.\*.createdBy | string | | system |
action_result.data.\*.createdDate | string | | 2026-03-25T14:00:00Z |
action_result.data.\*.modifiedDate | string | | 2026-03-25T14:00:00Z |
action_result.data.\*.emailCount | string | | |
action_result.data.\*.matchingIOCs | string | | |
action_result.data.\*.quarantineEmails.\*.internetMessageId | string | | <1270149500.1722827.1657392753324@af226d4cfbab> |
action_result.data.\*.quarantineEmails.\*.recipientAddress | string | | testuser@test.com |
action_result.data.\*.quarantineEmails.\*.status | string | | EXPUNGED |
action_result.data.\*.context | string | | |
action_result.data.\*.searchId | string | | |
action_result.data.\*.detection | string | | cluster |
action_result.data.\*.willRetry | boolean | | True False |
action_result.data.\*.modifiedBy | string | | crestdatauser |
action_result.data.\*.quarantineJobRuns.\*.id | numeric | | 17161 |
action_result.data.\*.quarantineJobRuns.\*.error | numeric | | |
action_result.data.\*.quarantineJobRuns.\*.total | numeric | | 708 |
action_result.data.\*.quarantineJobRuns.\*.status | string | | NEW |
action_result.data.\*.quarantineJobRuns.\*.createdBy | string | | crestdatauser |
action_result.data.\*.quarantineJobRuns.\*.jobRunType | string | | QUARANTINE |
action_result.data.\*.quarantineJobRuns.\*.startedDate | string | | |
action_result.data.\*.quarantineJobRuns.\*.completedDate | string | | |
action_result.data.\*.whoClickedPending | boolean | | True False |
action_result.data.\*.whoDeletedPending | boolean | | True False |
action_result.data.\*.isClusterInitiated | boolean | | True False |
action_result.data.\*.quarantineEmailReadStatusCounts | string | | |
action_result.message | string | | Successfully created a quarantine job for the cluster |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'reject quarantine job'

Rejects the quarantine job identified by the ID. When the Auto Quarantine feature is configured to require manual approvals, this endpoint can reject pending quarantine jobs

Type: **generic** <br>
Read only: **False**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**id** | required | ID of the quarantine job in cofense vision to be rejected | numeric | `cofense vision quarantine job id` |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.parameter.id | numeric | `cofense vision quarantine job id` | 1234 |
action_result.data | string | | |
action_result.message | string | | Successfully rejected the quarantine job |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'retry quarantine job'

Issues a request to retry the quarantine job identified by the ID

Type: **generic** <br>
Read only: **False**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**id** | required | ID of the quarantine job in cofense vision to be retried | numeric | `cofense vision quarantine job id` |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.parameter.id | numeric | `cofense vision quarantine job id` | 1234 |
action_result.data | string | | |
action_result.message | string | | Successfully retried the quarantine job |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'get vision ai config'

Retrieves the current Vision AI configuration settings, including whether the feature is enabled, whether the Terms of Service have been accepted, and all tunable cluster parameters

Type: **investigate** <br>
Read only: **True**

#### Action Parameters

No parameters are required for this action

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.data.\*.enabled | boolean | | True False |
action_result.data.\*.tosAccepted | boolean | | True False |
action_result.data.\*.tosAcceptedBy | string | | |
action_result.data.\*.tosAcceptedFromIp | string | | |
action_result.data.\*.autoQuarantine | boolean | | True False |
action_result.data.\*.operatorApproval | boolean | | True False |
action_result.data.\*.minClusterSize | numeric | | 100 |
action_result.data.\*.clusterTimeToMatchMs | numeric | | 259200000 |
action_result.data.\*.similarityLevel | numeric | | 5 |
action_result.data.\*.rapidlyTimeMs | numeric | | 28800000 |
action_result.message | string | | Successfully retrieved the Vision AI configuration |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'update vision ai config'

Performs a partial update of the Vision AI configuration, updating only those parameters included in the request

Type: **generic** <br>
Read only: **False**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**enable** | optional | Whether the Vision AI feature is turned on | string | |
**auto_quarantine** | optional | Vision auto quarantines clusters | string | |
**operator_approval** | optional | Whether Vision requires operator approval to auto quarantine clusters | string | |
**cluster_match_time** | optional | Time window in milliseconds when emails are eligible for clustering. The value must be from 86400000 (24 hours) to 604800000 (7 days) | numeric | |
**min_cluster_size** | optional | Minimum number of emails required to form a cluster. The minimum value is 10 | numeric | |
**cluster_rapid_growth_time** | optional | Time window in milliseconds used to determine if a cluster is growing rapidly. The value must be from 900000 (15 minutes) to 86400000 (24 hours) | numeric | |
**similarity_level** | optional | How strictly emails must match to be clustered, an integer from -10 to 10, with 10 indicating the closest matching | numeric | |
**tos_accepted** | optional | Whether the Terms of Service have been accepted | string | |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.parameter.enable | string | | True False |
action_result.parameter.auto_quarantine | string | | True False |
action_result.parameter.operator_approval | string | | True False |
action_result.parameter.cluster_match_time | numeric | | 86400000 |
action_result.parameter.min_cluster_size | numeric | | 100 |
action_result.parameter.cluster_rapid_growth_time | numeric | | 14400000 |
action_result.parameter.similarity_level | numeric | | 5 |
action_result.parameter.tos_accepted | string | | True False |
action_result.data.\*.enabled | boolean | | True False |
action_result.data.\*.tosAccepted | boolean | | True False |
action_result.data.\*.autoQuarantine | boolean | | True False |
action_result.data.\*.operatorApproval | boolean | | True False |
action_result.data.\*.minClusterSize | numeric | | 100 |
action_result.data.\*.clusterTimeToMatchMs | numeric | | 259200000 |
action_result.data.\*.similarityLevel | numeric | | 5 |
action_result.data.\*.rapidlyTimeMs | numeric | | 14400000 |
action_result.data.\*.tosAcceptedBy | string | | Devon.Sullivan@cofense.com |
action_result.data.\*.tosAcceptedFromIp | string | | 40.121.106.7, 172.31.3.26 |
action_result.message | string | | Successfully updated the Vision AI configuration |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'on poll'

Callback action for the on poll ingest functionality

Type: **ingest** <br>
Read only: **True**

Retrieves the emails of the Cofense Vision AI clusters ingested in the polling window and creates a container for every cluster along with an artifact for every email of that cluster. A cluster keeps growing as new emails join it, so it is returned again by every polling window that ingests one of its emails. Only the emails of the window are ingested, into containers identified by the ingestion timestamp of the newest email they hold. Scheduled polling windows never overlap, so every email is ingested once and a scheduled poll never adds artifacts to a container created by an earlier scheduled poll. POLL NOW is meant for sampling: it neither reads nor updates the polling checkpoint, so its window can overlap the windows of other polls. A poll whose window overlaps an earlier POLL NOW, whether another POLL NOW or a scheduled poll, can add older emails to a container that POLL NOW created, and repeating POLL NOW over a cluster that is still receiving emails ingests those emails again into new containers. No email is lost in either case. To avoid both, delete the containers created by POLL NOW before scheduled polling covers the same period. Every container is named after its cluster ID, the cluster title and the ingestion timestamp of the oldest email it holds, so every email of the container was ingested at or after that time, for example '291 : Invoice campaign - 2024-05-31T10:00:00Z'; the polling window is stated in the container description. The emails of a cluster are split across containers of at most 'Maximum number of artifacts in a single container' artifacts each, so a cluster of 200 emails with the default limit of 100 produces 2 containers. Those containers are named with their part, for example '... - Part 1 of 2'. The polling window ends 'Ingestion lag' minutes (5 by default) before the current time, so that an email whose row is committed after its ingestion timestamp is still picked up by the next cycle; an email committed later than the lag is never ingested. The polling window starts at the 'Start Time' asset configuration parameter for the first scheduled or interval poll and at the end of the previous polling window for the subsequent ones. The 'Start Time for Poll Now' asset configuration parameter is used for the manual POLL NOW runs; the start_time and end_time that Splunk SOAR passes to the action are ignored. POLL NOW stops exactly at its container_count and artifact_count, even within a cluster. Both parameters accept a relative time, for example 1d, 6h, 30m, or an absolute UTC date, for example 2024-05-31T00:00:00Z. A scheduled poll ingests every email of every cluster returned for its window; there is no limit on the number of emails in a cycle.

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**container_count** | optional | Maximum number of containers to create during POLL NOW | numeric | |
**artifact_count** | optional | Maximum number of artifacts to create during POLL NOW | numeric | |
**start_time** | optional | Parameter ignored in this app | numeric | |
**end_time** | optional | Parameter ignored in this app | numeric | |
**container_id** | optional | Parameter ignored in this app | numeric | |

#### Action Output

No Output

______________________________________________________________________

Auto-generated Splunk SOAR Connector documentation.

Copyright 2026 Splunk Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.

[comment]: # "Auto-generated SOAR connector documentation"
# Cofense Vision

Publisher: Cofense  
Connector Version: 1\.0\.1  
Product Vendor: Cofense  
Product Name: Cofense Vision  
Product Version Supported (regex): "\.\*"  
Minimum Product Version: 5\.5\.0  

This app implements investigative and generic actions to quarantine emails, manage IOCs, search messages, download messages and their attachments

[comment]: # "File: README.md"
[comment]: # ""
[comment]: # "Copyright (c) 2023 Cofense"
[comment]: # ""
[comment]: # "This unpublished material is proprietary to Cofense."
[comment]: # "All rights reserved. The methods and"
[comment]: # "techniques described herein are considered trade secrets"
[comment]: # "and/or confidential. Reproduction or distribution, in whole"
[comment]: # "or in part, is forbidden except by express written permission"
[comment]: # "of Cofense."
[comment]: # ""
[comment]: # "Licensed under the Apache License, Version 2.0 (the 'License');"
[comment]: # "you may not use this file except in compliance with the License."
[comment]: # "You may obtain a copy of the License at"
[comment]: # ""
[comment]: # "    http://www.apache.org/licenses/LICENSE-2.0"
[comment]: # ""
[comment]: # "Unless required by applicable law or agreed to in writing, software distributed under"
[comment]: # "the License is distributed on an 'AS IS' BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,"
[comment]: # "either express or implied. See the License for the specific language governing permissions"
[comment]: # "and limitations under the License."
[comment]: # ""
## Explanation of the Asset Configuration Parameters

The asset configuration parameters affect 'test connectivity' and some other actions of the
application. The parameters related to test connectivity action are Cofense Vision URL, Verify
server certificate, Client ID and Client Secret.

-   **Cofense Vision URL:** The URL used to connect with the Cofense Vision server.
-   **Verify server certificate:** Validate server certificate.
-   **Client ID:** Client ID.
-   **Client Secret:** Client Secret.

## Explanation of the Actions' Parameters

-   ### Test Connectivity

    This action will check the status of the Cofense Vision Server and test connectivity of Splunk
    SOAR to the Cofense Vision instance. It can be used to generate a new token.  
    The action validates the provided asset configuration parameters. Based on the response from the
    API call, appropriate success and failure message will be displayed when the action gets
    executed.

-   ### Get Message

    Fetches full content of an email and saves it as a zip file to the Vault. The file added to the
    vault will be named as "message\_\<UTC_date>.zip".

    -   **Action Parameter: Internet Message ID**

          

        -   This parameter accepts a unique identifier of the email, enclosed in angle brackets.
        -   Users can get the internet message ID by executing the "get messagesearch results"
            action.
        -   Example: \<AC6CAE11-779E-4044-BB25-110171AB0301@example.com>

    -   **Action Parameter: Recipient Address**

          

        -   This parameter accepts recipient address of the email.
        -   The email address can be a carbon copy (Cc) or blind carbon copy (Bcc) recipient but
            cannot be a shared mailbox or a distribution list.
        -   Users can get the recipient address by executing the "get messagesearch results" action.
        -   Example: test@domain.com

    -   **Action Parameter: Password**

          

        -   This parameter accepts a password string used to protect the zip file. Leading and
            trailing spaces will be stripped from the provided value.

-   ### Get Message Metadata

    Retrieves the metadata of a message that matches the specified internet message ID and recipient
    email address.

    -   **Action Parameter: Internet Message ID**

          

        -   This parameter accepts a unique identifier of the email, enclosed in angle brackets.
        -   Users can get the internet message ID by executing the "get messagesearch results"
            action.
        -   Example: \<AC6CAE11-779E-4044-BB25-110171AB0301@example.com>

    -   **Action Parameter: Recipient Address**

          

        -   This parameter accepts recipient address of the email.
        -   The email address can be a carbon copy (Cc) or blind carbon copy (Bcc) recipient but
            cannot be a shared mailbox or a distribution list.
        -   Users can get the recipient address by executing the "get messagesearch results" action.
        -   Example: test@domain.com

-   ### Get Message Attachment

    Fetches an attachment by using its MD5 or SHA256 hash and saves it to the Vault.

    -   **Action Parameter: MD5**

          

        -   It is a hex-encoded string that represents an attachment's MD5 hash.
        -   Users can get the MD5 hash by executing the "get messagesearch results" action.
        -   Example: 21b6b32fb4e526d594afe70ea56a0e0c

    -   **Action Parameter: SHA256**

          

        -   It is a hex-encoded string that represents an attachment's SHA256 hash.
        -   Users can get the SHA256 hash by executing the "get messagesearch results" action.
        -   Example: 9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08

    -   **Action Parameter: File name**

          

        -   It is a file name including the extension to be given to the file.
        -   Example: test.txt

-   ### Create Message Search

    Creates a new search based on the user-specified filters.

    -   **Action Parameter: Subjects**

          

        -   It is a comma-separated string of subjects to create a search for an email's subject. It
            supports the use of one or more wildcard characters (\*) in any position of a subject.
            Maximum 3 values are allowed.
        -   Example: Check this out,News of the day

    -   **Action Parameter: Senders**

          

        -   It is a comma-separated string of senders to create a search for an email's sender. It
            supports the use of one or more wildcard characters (\*) in any position of a sender
            email address. Maximum 3 values are allowed.
        -   Example: testuser@test.com

    -   **Action Parameter: Attachment names**

          

        -   It is a comma-separated string of attachment names to create a search for an email's
            attachment. The email must include at least one attachment matching one of the specified
            file names. It supports the use of one or more wildcard characters (\*) in any position
            of a an attachment file name. Maximum 3 values are allowed.
        -   Example: foo.jpg,bar.jpg

    -   **Action Parameter: Attachment hashes**

          

        -   It is a comma-separated string of attachment hashes to create a search for an email's
            attachment hashes. Maximum 3 values are allowed.
        -   Supported format: hashtype1:hashvalue1:hashvalue2,hashtype2:hashvalue3
        -   Possible values for hash type are: md5 and sha256
        -   Example: sha256:f814c32d07400260cda1c3dd8479c843bfa6062e1221bd85c04c5eee570ac413

    -   **Action Parameter: Attachment hash match criteria**

          

        -   The type of matching to perform on the hashes specified in the "attachment hashes"
            parameter. Possible values are:
            -   ALL: Emails must include all listed attachment hashes.
            -   ANY: Emails must contain at least one of the listed attachment hash.
        -   Default is ANY.

    -   **Action Parameter: Attachment mime types**

          

        -   It is a comma-separated string of MIME types to create a search for an email's
            attachment MIME type. This property returns emails with at least one attachment of one
            of the listed mime types. Maximum 3 values are allowed.
        -   Example: image/png

    -   **Action Parameter: Attachment exclude mime types**

          

        -   It is a comma-separated string of MIME types to create a search for excluding an email's
            attachment MIME type. This property excludes attachments that have one of these mime
            types from the matching process. Maximum 3 values are allowed.
        -   Example: image/jpg

    -   **Action Parameter: Domains**

          

        -   It is a comma-separated string of domains to create a search for domains in an email's
            attachment body or its attachment. Maximum 3 values are allowed.
        -   Example: test.com

    -   **Action Parameter: Domain match criteria**

          

        -   It is the type of matching to perform on the domains specified in the "domains"
            parameter. Possible values are:
            -   ALL: Emails must include all listed domains.
            -   ANY: Emails must contain at least one of the listed domains.
        -   Default is ANY.

    -   **Action Parameter: Headers**

          

        -   It is a comma-separated string of key-value pairs, defining the additional criteria to
            search for in the email header. Maximum 3 values are allowed.
        -   Supported format: key1:value1,key2:value2:value3
        -   List of available headers to create a search can be retrieved by executing 'list
            searchable headers' action.
        -   Example: X-MS-Exchange-Organization-AuthSource:DM6PR19MB3772.namprd19.prod.test.com

    -   **Action Parameter: Internet Message ID**

          

        -   It is a unique identifier of the email, enclosed in angle brackets. It is
            case-sensitive.
        -   Example: \<AC6CAE11-779E-4044-BB25-110171AB0301@example.com>

    -   **Action Parameter: Partial ingest**

          

        -   It indicates whether to create a search with partially ingested emails (true) or without
            partially ingested emails (false).

    -   **Action Parameter: Received after date**

          

        -   Date and time to create a search for emails which are received on or after the specified
            UTC date and time. The timestamp is in UTC.
        -   Supported formats: yyyy-mm-dd, yyyy-mm-ddTHH:MM:SSZ.
        -   Example: "01 Mar 2021", "01 Feb 2021 04:45:33", "2022-04-17T14:05:44Z"

    -   **Action Parameter: Received before date**

          

        -   Date and time to create a search for emails which are received before or on the
            specified UTC date and time.
        -   Supported formats: yyyy-mm-dd, yyyy-mm-ddTHH:MM:SSZ.
        -   Example: "01 Mar 2021", "01 Feb 2021 04:45:33", "2022-04-17T14:05:44Z"

    -   **Action Parameter: Recipient**

          

        -   To create a search with the specified recipient. Supports one or more wildcard
            characters (\*) in any position of a recipient's email address.
        -   The email address can be a carbon copy (Cc) or blind carbon copy (Bcc) recipient but
            cannot be a shared mailbox or a distribution list.
        -   Users can get the recipient address by executing the "get messagesearch results" action.
        -   Example: testuser@test.com

    -   **Action Parameter: URL**

          

        -   To create a search with the specified url. Supports one or more wildcard characters (\*)
            in any position of the URL.
        -   Example: https://test.com

-   ### List Message Searches

    Retrieves the list of searches.

    -   **Action Parameter: Page**

          

        -   Start page of the results. The value must be a positive integer or 0.
        -   Default: 0

    <!-- -->

    -   **Action Parameter: Size**

          

        -   Number of results per page. The value must be a positive integer up to 2000.
        -   Default: 50

    <!-- -->

    -   **Action Parameter: Sort**

          

        -   The name-value pair defining the order of the response. Comma separated values are
            supported.
        -   Supported format: **propertyName1:sortOrder1,propertyName2** .
        -   As indicated in the supported format, the SortOrder can be omitted from the parameter.
            API will use ascending order if no order is specified.
        -   Supported values for propertyName are: **id, createdBy, createdDate, modifiedBy,
            modifiedDate, receivedAfterDate, receivedBeforeDate** .
        -   Supported values for sortOrder are: **asc, desc** .
        -   Default value from API end: " **id,asc** ".

-   ### Get Message Search

    Retrieves the search identified by an ID.

    -   **Action Parameter: ID**

          

        -   The unique ID that cofense vision has assigned to a search.
        -   The ID can be retrieved by using the "list message searches" action.

-   ### Get Message Search Results

    Retrieves the results for the search identified by the search ID.

    -   **Action Parameter: ID**

          

        -   The unique ID that cofense vision has assigned to a search.
        -   The ID can be retrieved by using the "list message searches" action.

    <!-- -->

    -   **Action Parameter: Page**

          

        -   Start page of the results. The value must be a positive integer or 0.
        -   Default: 0

    <!-- -->

    -   **Action Parameter: Size**

          

        -   Number of results per page. The value must be a positive integer up to 2000.
        -   Default: 50

    <!-- -->

    -   **Action Parameter: Sort**

          

        -   The name-value pair defining the order of the response. Comma separated values are
            supported.
        -   Supported format: **propertyName1,propertyName2:sortOrder2** .
        -   As indicated in the supported format, the SortOrder can be omitted from the parameter.
            API will use ascending order if no order is specified.
        -   Supported values for propertyName are: **id, subject, createdOn, sentOn, processedOn,
            htmlBody, md5, sha1, sha256** . In the response, the attribute name for "createdOn" is
            "receivedOn".
        -   Supported values for sortOrder are: **asc, desc** .
        -   Default value from API end: " **id,asc** ".

-   ### List Searchable Headers

    Retrieves a list of configured header keys that can be used to create a message search.  
    The action has no parameters.

-   ### List IOCs

    Lists the IOCs stored in the local IOC Repository.

    -   **Action Parameter: Source**

          

        -   Single IOC source.
        -   The value can contain uppercase letters, lowercase letters, numbers, and certain special
            characters (. - \_ \~).
        -   Example: "Triage-1", "Vision-UI"

    <!-- -->

    -   **Action Parameter: Page**

          

        -   Start page of the results. The value must be a positive integer or 0.
        -   Default: 0

    <!-- -->

    -   **Action Parameter: Size**

          

        -   Number of results per page. The value must be a positive integer up to 2000.
        -   Default: 50

    <!-- -->

    -   **Action Parameter: Sort**

          

        -   The name-value pair defining the order of the response.
        -   Supported format: **propertyName1:sortOrder1** OR **propertyName1** .
        -   The SortOrder can be omitted from the parameter. API will use ascending order if no
            order is specified.
        -   The only accepted value for propertyName is **updatedAt** .
        -   Supported values for sortOrder are: **asc, desc** .

    <!-- -->

    -   **Action Parameter: Include expired**

          

        -   Whether to include expired IOCs (true) or not include expired IOCs (false).
        -   Default: False

    <!-- -->

    -   **Action Parameter: Since**

          

        -   Include only IOCs that were added to the repository after the given UTC date.
        -   Supported formats: yyyy-mm-dd, yyyy-mm-ddTHH:MM:SSZ.
        -   Example: "01 Mar 2021", "01 Feb 2021 04:45:33", "2022-04-17T14:05:44Z"

-   ### Get IOC

    Retrieves the IOC identified by its unique MD5 ID.

    -   **Action Parameter: ID**

          

        -   The ID of the IOC.
        -   Users can get the list of IDs by executing the 'list iocs' action.

    <!-- -->

    -   **Action Parameter: Source**

          

        -   Single IOC source.
        -   The value can contain uppercase letters, lowercase letters, numbers, and certain special
            characters (. - \_ \~).
        -   Example: "Triage-1", "Vision-UI"

-   ### Update IOC

    Updates the IOC identified by its unique MD5 ID.

    -   **Action Parameter: ID**

          

        -   The ID of the IOC to be updated.
        -   Users can get the list of IDs by executing the 'list iocs' action.

    <!-- -->

    -   **Action Parameter: Expires at**

          

        -   Expiration date and time of the IOC. The timestamp is in UTC.
        -   Supported formats: yyyy-mm-dd, yyyy-mm-ddTHH:MM:SSZ.
        -   Example: "01 Mar 2021", "01 Feb 2021 04:45:33", "2022-04-17T14:05:44Z"

-   ### Update IOCs

    Updates one or more IOCs stored in the local IOC repository. It creates new IOC(s) if the
    corresponding IOC does not exist.

    -   **Action Parameter: Source**

          

        -   Single IOC source.
        -   The value can contain uppercase letters, lowercase letters, numbers, and certain special
            characters (. - \_ \~).
        -   Examples: "Triage-1", "Vision-UI"

    <!-- -->

    -   **Action Parameter: IOCs JSON**

          

        -   To update multiple IOCs use 'iocs json' parameter.

        -   List of JSON data containing IOC detail to be updated in the IOC local repository.

        -   Supported Format:
                [
                {
                    "threat_type": "Domain",
                    "threat_value": "test1.com",
                    "threat_level": "Malicious",
                    "created_at": "20/08/2022",
                    "source_id": "test_source_1",
                    "updated_at": "20/08/2022",
                    "requested_expiration": "30/08/2022"
                },
                {
                    "threat_type": "Domain",
                    "threat_value": "test2.com",
                    "threat_level": "Malicious",
                    "created_at": "20/08/2022",
                    "source_id": "test_source_2",
                    "updated_at": "20/08/2022",
                    "requested_expiration": "30/08/2022"
                }
                ]

    <!-- -->

    -   **Action Parameter: Threat type**

          

        -   Type of IOC
        -   Values can be from one of the following: Domain, MD5, Sender, SHA256, Subject or URL.

    <!-- -->

    -   **Action Parameter: Threat value**

          

        -   Actual value of the IOC match in the email.

    <!-- -->

    -   **Action Parameter: Threat level**

          

        -   The severity of the IOC.
        -   Example: "Malicious"

    <!-- -->

    -   **Action Parameter: Source ID**

          

        -   Unique identifier assigned by the IOC source.
        -   Example: source1_id_00001

    <!-- -->

    -   **Action Parameter: Created at**

          

        -   The UTC date and time the IOC source included the IOC for the first time.
        -   Supported formats: yyyy-mm-dd, yyyy-mm-ddTHH:MM:SSZ.
        -   Example: "01 Mar 2021", "01 Feb 2021 04:45:33", "2022-04-17T14:05:44Z"

    <!-- -->

    -   **Action Parameter: Updated at**

          

        -   The UTC date and time the IOC source last updated the IOC. If it is not provided, app
            will consider current UTC time for the field.
        -   Supported formats: yyyy-mm-dd, yyyy-mm-ddTHH:MM:SSZ.
        -   Example: "01 Mar 2021", "01 Feb 2021 04:45:33", "2022-04-17T14:05:44Z"

    <!-- -->

    -   **Action Parameter: Requested expiration**

          

        -   Expiration date and time for this IOC in UTC.
        -   The IOC repository calculates an expiration date and time 14 days after the IOC is sent
            to the IOC repository.
        -   Supported formats: yyyy-mm-dd, yyyy-mm-ddTHH:MM:SSZ.
        -   Example: "01 Mar 2021", "01 Feb 2021 04:45:33", "2022-04-17T14:05:44Z"

      
    **Notes:**

    -   The 'iocs json' parameter will take precedence over other parameters.
    -   The threat_type, threat_value, threat_level, created_at and source_id parameters are
        required to update a single IOC.

-   ### Get Last IOC

    Retrieves the last updated IOC from the local IOC Repository. It may return an active or an
    expired IOC.

    -   **Action Parameter: Source**

          

        -   Single IOC source.
        -   The value can contain uppercase letters, lowercase letters, numbers, and certain special
            characters (. - \_ \~).
        -   Example: "Triage-1", "Vision-UI"

-   ### Delete IOC

    Deletes a single active or expired IOC from the local IOC Repository.

    -   **Action Parameter: ID**

          

        -   The ID of the IOC to be deleted.
        -   Users can get the list of IDs by executing the 'list iocs' action.

    <!-- -->

    -   **Action Parameter: Source**

          

        -   Single IOC source.
        -   The value can contain uppercase letters, lowercase letters, numbers, and certain special
            characters (. - \_ \~).
        -   Example: "Triage-1", "Vision-UI"

-   ### List Quarantine Jobs

    Fetches a list of matching quarantine jobs.

    -   **Action Parameter: Exclude quarantine emails**

          

        -   Whether to remove (true) or not remove (false) quarantined emails from the response.
        -   Default: False

    <!-- -->

    -   **Action Parameter: Page**

          

        -   Start page of the results. The value must be a positive integer or 0.
        -   Default: 0

    <!-- -->

    -   **Action Parameter: Size**

          

        -   Number of results per page. The value must be a positive integer up to 2000.
        -   Default: 50

    <!-- -->

    -   **Action Parameter: Sort**

          

        -   The name-value pair defining the order of the response. Comma separated values are
            supported.
        -   Supported format: **propertyName1,propertyName2:sortOrder2** .
        -   As indicated in the supported format, the SortOrder can be omitted from the parameter.
            API will use ascending order if no order is specified.
        -   Supported values for propertyName are: **id, createdBy, createdDate, modifiedBy,
            modifiedDate, stopRequested** .
        -   Supported values for sortOrder are: **asc, desc** .
        -   Default value from API end: " **id,asc** ".

    <!-- -->

    -   **Action Parameter: Auto quarantine**

          

        -   Whether to list only auto quarantine jobs (true) or both (false).
        -   Default: False

    <!-- -->

    -   **Action Parameter: Include status and Exclude status**

          
        Include status: Filters quarantine jobs by including emails with the specified status.
        Supports comma-separated values.  
        Exclude status: Filters quarantine jobs by excluding emails with the specified status.
        Supports comma-separated values.  

        -   Supported values are: **NEW, PENDING_APPROVAL, QUEUED, RUNNING, COMPLETED, FAILED.**

              

            -   NEW: Job was created but is not yet queued.
            -   PENDING_APPROVAL: Job was created from an auto quarantine action and is waiting for
                approval to run.
            -   QUEUED: Job is queued but has not yet run.
            -   RUNNING: Job is currently running.
            -   COMPLETED: Job run finished and emails were quarantined or restored.
            -   FAILED: Job run finished but some emails to be quarantined or restored are in an
                error state. Cofense Vision retries failed jobs until the retry limit is reached.

    <!-- -->

    -   **Action Parameter: IOCs**

          

        -   Unique MD5 hash identifier of one or more IOCs. Comma separated values are supported.
        -   Example: 07fa1e91f99050521a87edc784e83fd5

    <!-- -->

    -   **Action Parameter: Modified date after**

          

        -   Emails modified after this date and time. The date and time must be in UTC.
        -   Supported formats are: yyyy-mm-dd, yyyy-mm-ddTHH:MM:SSZ, dd/mm/yyyy
        -   Example: "01 Mar 2021", "01 Feb 2021 04:45:33", "2022-04-17T14:05:44Z", "15/09/2022"

    <!-- -->

    -   **Action Parameter: Source**

          

        -   One or more configured IOC sources. Comma separated values are supported.
        -   Example: Intelligence, Triage-1

-   ### Create Quarantine Job

    Creates a new quarantine job.

    -   **Action Parameter: Quarantine emails**

          

        -   A comma-separated string of quarantine emails, specifying the recipient address and
            internet message ID of the email.
        -   Example:
            test@test.com:\<CAFRPxWuOFW@test.com>:\<WCuib9wCsz@test.com>,testuser@test.com:\<YCuib9wCs1@test.com>

-   ### Get Quarantine Job

    Retrieves quarantine job identified by the ID.

    -   **Action Parameter: ID**

          

        -   ID of the quarantine job in cofense vision to be retrieved.
        -   Users can get the list of ID by executing the 'list quarantine jobs' action.
        -   Example: 1422

-   ### Approve Quarantine Job

    Approves the quarantine job identified by the ID. When the Auto Quarantine feature is configured
    to require manual approvals, this action can approve the pending quarantine jobs.

    -   **Action Parameter: ID**

          

        -   ID of the quarantine job in cofense vision to be approved.
        -   Users can get the list of ID by executing the 'list quarantine jobs' action.

    -   **Action Parameter: Message Count**

          

        -   Number of emails containing IOC matches to be quarantined. When 'message count' is
            present, Cofense Vision quarantines a subset of the total number of emails containing
            IOC matches.
        -   The value must be a positive integer.
        -   If 'message count' is not present, all messages will be approved.

-   ### Restore Quarantine Job

    Restores emails quarantined by the job identified by the ID.

    -   **Action Parameter: ID**

          

        -   ID of the quarantine job in cofense vision to be restored.
        -   Users can get the list of ID by executing the 'list quarantine jobs' action.

-   ### Stop Quarantine Job

    Issues a request to stop the quarantine job identified by ID.

    -   **Action Parameter: ID**

          

        -   ID of the quarantine job in cofense vision to be stopped.
        -   Users can get the list of ID by executing the 'list quarantine jobs' action.
        -   Example: 1422

-   ### Delete Quarantine Job

    Deletes the quarantine job identified by the ID.

    -   **Action Parameter: ID**

          

        -   ID of the quarantine job in cofense vision to be deleted.
        -   Example: 1422

-   ### Download Logs

    Downloads the log files for all Cofense Vision components. This action will work as expected
    only for on-prem Vision instances and not for Saas instances.  
    The action has no parameters.


### Configuration Variables
The below configuration variables are required for this Connector to operate.  These variables are specified when configuring a Cofense Vision asset in SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**base\_url** |  required  | string | Cofense Vision URL
**verify\_server\_cert** |  optional  | boolean | Verify Server Certificate
**client\_id** |  required  | string | Client ID
**client\_secret** |  required  | password | Client Secret

### Supported Actions  
[test connectivity](#action-test-connectivity) - Validate the asset configuration for connectivity using supplied configuration  
[get message metadata](#action-get-message-metadata) - Retrieves the metadata of the message that matches the specified internet message ID and recipient email address  
[get message](#action-get-message) - Fetches full content of an email and saves it as a zip file to the Vault  
[get message attachment](#action-get-message-attachment) - Fetches an attachment by using its MD5 or SHA256 hash and saves it to the Vault  
[list quarantine jobs](#action-list-quarantine-jobs) - Fetches a list of matching quarantine jobs  
[create quarantine job](#action-create-quarantine-job) - Creates a new quarantine job  
[restore quarantine job](#action-restore-quarantine-job) - Restores emails quarantined by the job identified by the ID  
[list message searches](#action-list-message-searches) - Retrieves the list of searches  
[get message search](#action-get-message-search) - Retrieves the search identified by an ID  
[get quarantine job](#action-get-quarantine-job) - Retrieves quarantine job identified by the ID  
[approve quarantine job](#action-approve-quarantine-job) - Approves the quarantine job identified by the ID\. When the Auto Quarantine feature is configured to require manual approvals, this endpoint can approve the pending quarantine jobs  
[delete quarantine job](#action-delete-quarantine-job) - Deletes the quarantine job identified by the ID  
[get messagesearch results](#action-get-messagesearch-results) - Retrieves the results for the search identified by the search ID  
[delete ioc](#action-delete-ioc) - Deletes a single active or expired IOC from the local IOC Repository  
[stop quarantine job](#action-stop-quarantine-job) - Issues a request to stop the quarantine job identified by ID  
[create message search](#action-create-message-search) - Creates a new search based on the user\-specified filters  
[get last ioc](#action-get-last-ioc) - Retrieves the last updated IOC from the local IOC Repository\. It may return an active or an expired IOC  
[update iocs](#action-update-iocs) - Updates one or more IOCs stored in the local IOC repository  
[update ioc](#action-update-ioc) - Updates the IOC identified by its unique MD5 ID  
[list iocs](#action-list-iocs) - Lists the IOCs stored in the local IOC Repository  
[get ioc](#action-get-ioc) - Retrieves the IOC identified by its unique MD5 ID  
[list searchable headers](#action-list-searchable-headers) - Retrieves a list of configured header keys that can be used to create a message search  
[download logs](#action-download-logs) - Downloads the log files for all Cofense Vision components  

## action: 'test connectivity'
Validate the asset configuration for connectivity using supplied configuration

Type: **test**  
Read only: **True**

The test connectivity action will first check if the Cofense Vision server is up\. If the server is up and running, it will use the credentials to generate the access token\. Once the token is received, it will be stored in the state file\.

#### Action Parameters
No parameters are required for this action

#### Action Output
No Output  

## action: 'get message metadata'
Retrieves the metadata of the message that matches the specified internet message ID and recipient email address

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**internet\_message\_id** |  required  | Unique identifier of the email, enclosed in angle brackets | string |  `cofense vision internet message id` 
**recipient\_address** |  required  | Recipient address of the email | string |  `email` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action\_result\.status | string |  |   success  failed 
action\_result\.parameter\.internet\_message\_id | string |  `cofense vision internet message id`  |   <154949148\.36247\.1665620111111\@edf45488dd9c> 
action\_result\.parameter\.recipient\_address | string |  `email`  |   testuser\@test\.com 
action\_result\.data\.\*\.attachments\.\*\.contentType | string |  |   application/zip 
action\_result\.data\.\*\.attachments\.\*\.detectedContentType | string |  |   application/zip 
action\_result\.data\.\*\.attachments\.\*\.filename | string |  |   fileNum\-Thread\[mailer\-006,5,main\]\-text\-file\-36247\.txt\.zip 
action\_result\.data\.\*\.attachments\.\*\.id | numeric |  |   6619844 
action\_result\.data\.\*\.attachments\.\*\.md5 | string |  `md5`  |   940f1f22d39a17feadebcda817139376 
action\_result\.data\.\*\.attachments\.\*\.sha256 | string |  `sha256`  |   092edcf103124a00342194f7489e22430434b516ed4e27eb1ab5e8472ec36cae 
action\_result\.data\.\*\.attachments\.\*\.size | numeric |  |   1206 
action\_result\.data\.\*\.deliveredOn | string |  |  
action\_result\.data\.\*\.from\.\*\.address | string |  |   testuser\@test\.com 
action\_result\.data\.\*\.from\.\*\.id | numeric |  |   2616086 
action\_result\.data\.\*\.from\.\*\.personal | string |  |   testuser 
action\_result\.data\.\*\.headers\.\*\.name | string |  |   From 
action\_result\.data\.\*\.headers\.\*\.value | string |  |   testuser\@test\.com 
action\_result\.data\.\*\.htmlBody | string |  |  
action\_result\.data\.\*\.id | numeric |  |   2616086 
action\_result\.data\.\*\.internetMessageId | string |  `cofense vision internet message id`  |   <154949148\.36247\.1665620111111\@edf45488dd9c> 
action\_result\.data\.\*\.md5 | string |  `md5`  |   2c05a12e6b87e2f5046cf88633868f07 
action\_result\.data\.\*\.processedOn | string |  |   2022\-10\-13T00\:19\:24\.776\+00\:00 
action\_result\.data\.\*\.receivedOn | string |  |   2022\-10\-13T00\:19\:21\.000\+00\:00 
action\_result\.data\.\*\.recipients\.\*\.address | string |  |   testuser\@test\.com 
action\_result\.data\.\*\.recipients\.\*\.id | numeric |  |   19039468 
action\_result\.data\.\*\.recipients\.\*\.personal | string |  |   testuser 
action\_result\.data\.\*\.recipients\.\*\.recipientType | string |  |   to 
action\_result\.data\.\*\.sentOn | string |  |   2022\-10\-13T00\:19\:20\.000\+00\:00 
action\_result\.data\.\*\.sha1 | string |  `sha1`  |   f792cae1723c381e55d4786232c71304eb1364c0 
action\_result\.data\.\*\.sha256 | string |  `sha256`  |   c82f3b550efcce43996b85b86ef1c0a48a4953f7d317996644111d2b8afdaaed 
action\_result\.data\.\*\.subject | string |  |   Just a test 
action\_result\.data\.\*\.textBody | string |  |  
action\_result\.summary | string |  |  
action\_result\.message | string |  |   Retrieved message metadata successfully 
summary\.total\_objects | numeric |  |   1 
summary\.total\_objects\_successful | numeric |  |   1   

## action: 'get message'
Fetches full content of an email and saves it as a zip file to the Vault

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**internet\_message\_id** |  required  | Unique identifier of the email, enclosed in angle brackets | string |  `cofense vision internet message id` 
**recipient\_address** |  required  | Recipient address of the email | string |  `email` 
**password** |  optional  | Password to protect the zip file | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action\_result\.status | string |  |   success  failed 
action\_result\.parameter\.internet\_message\_id | string |  `cofense vision internet message id`  |   <154949148\.36247\.1665620111111\@edf45488dd9c> 
action\_result\.parameter\.password | string |  |   test 
action\_result\.parameter\.recipient\_address | string |  `email`  |   testuser\@test\.com 
action\_result\.data\.\*\.aka\.\* | string |  |   message\_2023\-01\-06\_06\:49\:00\.536505\.zip 
action\_result\.data\.\*\.container | string |  |   Get message 
action\_result\.data\.\*\.container\_id | numeric |  |   2 
action\_result\.data\.\*\.create\_time | string |  |   0 minutes ago 
action\_result\.data\.\*\.created\_via | string |  |   automation 
action\_result\.data\.\*\.hash | string |  `vault id`  |   daf4cd5ede7cda3398434bbb22cfb791c2b43310 
action\_result\.data\.\*\.id | numeric |  |   1 
action\_result\.data\.\*\.metadata\.sha1 | string |  `sha1`  |   daf4cd5ede7cda3398434bbb22cfb791c2b43310 
action\_result\.data\.\*\.metadata\.sha256 | string |  `sha256`  |   10e14b2a20340fe9b352bc05ccf09bd3ae24e1d1bac5b7aa92b1cf6c8838f5e4 
action\_result\.data\.\*\.mime\_type | string |  |   application/zip 
action\_result\.data\.\*\.name | string |  |   message\_2023\-01\-06\_06\:49\:00\.536505\.zip 
action\_result\.data\.\*\.path | string |  |   /opt/phantom/vault/da/f4/daf4cd5ede7cda3398434bbb22cfb791c2b43310 
action\_result\.data\.\*\.size | numeric |  |   1642149 
action\_result\.data\.\*\.task | string |  |  
action\_result\.data\.\*\.user | string |  |   admin 
action\_result\.data\.\*\.vault\_document | numeric |  |   1 
action\_result\.data\.\*\.vault\_id | string |  `sha1`  `vault id`  |   daf4cd5ede7cda3398434bbb22cfb791c2b43310 
action\_result\.summary\.vault\_id | string |  `vault id`  |   daf4cd5ede7cda3398434bbb22cfb791c2b43310 
action\_result\.message | string |  |   Vault id\: daf4cd5ede7cda3398434bbb22cfb791c2b43310 
summary\.total\_objects | numeric |  |   1 
summary\.total\_objects\_successful | numeric |  |   1   

## action: 'get message attachment'
Fetches an attachment by using its MD5 or SHA256 hash and saves it to the Vault

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**md5** |  optional  | Hex\-encoded string that represents an attachment's MD5 hash | string |  `md5` 
**sha256** |  optional  | Hex\-encoded string that represents an attachment's SHA256 hash | string |  `sha256` 
**filename** |  required  | File name including the extension to give to the file | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action\_result\.status | string |  |   success  failed 
action\_result\.parameter\.filename | string |  |   test\.txt 
action\_result\.parameter\.md5 | string |  `md5`  |   21b6b32fb4e526d594afe70ea56a0e0c 
action\_result\.parameter\.sha256 | string |  `sha256`  |   ef7247f075e010e7a9f4af6fa8f8dd4436b1cc12355226bbdc270a0fb1c885d0 
action\_result\.data\.\*\.aka\.\* | string |  |   test\.txt 
action\_result\.data\.\*\.container | string |  |   Test 
action\_result\.data\.\*\.container\_id | numeric |  |   5 
action\_result\.data\.\*\.create\_time | string |  |   0 minutes ago 
action\_result\.data\.\*\.created\_via | string |  |   automation 
action\_result\.data\.\*\.hash | string |  `vault id`  |   31c194010afedb76694517e6250b5339d72ed518 
action\_result\.data\.\*\.id | numeric |  |   29 
action\_result\.data\.\*\.metadata\.sha1 | string |  `sha1`  |   31c194010afedb76694517e6250b5339d72ed518 
action\_result\.data\.\*\.metadata\.sha256 | string |  `sha256`  |   ef7247f075e010e7a9f4af6fa8f8dd4436b1cc12355226bbdc270a0fb1c885d0 
action\_result\.data\.\*\.mime\_type | string |  |   text/plain 
action\_result\.data\.\*\.name | string |  |   test\.txt 
action\_result\.data\.\*\.path | string |  |   /opt/phantom/vault/31/c1/31c194010afedb76694517e6250b5339d72ed518 
action\_result\.data\.\*\.size | numeric |  |   3079266 
action\_result\.data\.\*\.task | string |  |  
action\_result\.data\.\*\.user | string |  |   admin 
action\_result\.data\.\*\.vault\_document | numeric |  |   29 
action\_result\.data\.\*\.vault\_id | string |  `vault id`  |   31c194010afedb76694517e6250b5339d72ed518 
action\_result\.summary\.vault\_id | string |  `vault id`  |   31c194010afedb76694517e6250b5339d72ed518 
action\_result\.message | string |  |   Vault id\: 31c194010afedb76694517e6250b5339d72ed518 
summary\.total\_objects | numeric |  |   1 
summary\.total\_objects\_successful | numeric |  |   1   

## action: 'list quarantine jobs'
Fetches a list of matching quarantine jobs

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**page** |  optional  | Start page of the results\. The value must be a positive integer or 0 | numeric | 
**size** |  optional  | Number of results per page\. The value must be a positive integer up to 2000 | numeric | 
**sort** |  optional  | The name\-value pair defining the order of the response\. Comma separated values are supported | string | 
**exclude\_quarantine\_emails** |  optional  | Whether to remove \(true\) or not remove \(false\) quarantined emails from the response | boolean | 
**include\_status** |  optional  | Filters quarantine jobs by including emails with the specified status\. Supports comma\-separated values | string | 
**exclude\_status** |  optional  | Filters quarantine jobs by excluding emails with the specified status\. Supports comma\-separated values | string | 
**iocs** |  optional  | Unique MD5 hash identifier of one or more IOCs\. Comma separated values are supported | string |  `md5`  `cofense vision ioc id` 
**sources** |  optional  | One or more configured IOC sources\. Comma separated values are supported | string |  `cofense vision source` 
**modified\_date\_after** |  optional  | Emails modified after this date and time\. The date and time must be in UTC | string | 
**auto\_quarantine** |  optional  | Whether to list only auto quarantine jobs \(true\) or both \(false\) | boolean | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action\_result\.status | string |  |   success  failed 
action\_result\.parameter\.auto\_quarantine | boolean |  |   True  False 
action\_result\.parameter\.exclude\_quarantine\_emails | boolean |  |   True  False 
action\_result\.parameter\.exclude\_status | string |  |   NEW,FAILED,COMPLETED 
action\_result\.parameter\.include\_status | string |  |   NEW,FAILED,COMPLETED 
action\_result\.parameter\.iocs | string |  `md5`  `cofense vision ioc id`  |   b93cba4829a00dabef96036bb6765d20 
action\_result\.parameter\.modified\_date\_after | string |  |   01 Mar 2021  01 Feb 2021 04\:45\:33  2022\-04\-17T14\:05\:44Z  15/09/2022 
action\_result\.parameter\.page | numeric |  |   1 
action\_result\.parameter\.size | numeric |  |   50 
action\_result\.parameter\.sort | string |  |   createdBy\:desc,id\:asc 
action\_result\.parameter\.sources | string |  `cofense vision source`  |   Vision\-UI 
action\_result\.data\.\*\.autoQuarantine | boolean |  |   True  False 
action\_result\.data\.\*\.createdBy | string |  |   system 
action\_result\.data\.\*\.createdDate | string |  |   2022\-07\-15T05\:43\:39\.136018 
action\_result\.data\.\*\.emailCount | numeric |  |  
action\_result\.data\.\*\.id | numeric |  `cofense vision quarantine job id`  |   239 
action\_result\.data\.\*\.matchingIocInfo\.\*\.attributes\.threat\_type | string |  |   SUBJECT 
action\_result\.data\.\*\.matchingIocInfo\.\*\.attributes\.threat\_value | string |  |   essentially wolfish3 time 1657392753323 
action\_result\.data\.\*\.matchingIocInfo\.\*\.id | string |  |   b93cba4829a00dabef96036bb6765d20 
action\_result\.data\.\*\.matchingIocInfo\.\*\.metadata\.quarantine\.created\_at | string |  |   2022\-07\-15T05\:43\:38\.912\+00\:00 
action\_result\.data\.\*\.matchingIocInfo\.\*\.metadata\.quarantine\.expired | boolean |  |   True  False 
action\_result\.data\.\*\.matchingIocInfo\.\*\.metadata\.quarantine\.expires\_at | string |  |   2022\-07\-29T18\:29\:59\.999\+00\:00 
action\_result\.data\.\*\.matchingIocInfo\.\*\.metadata\.quarantine\.first\_quarantined\_at | string |  |   2022\-07\-15T05\:43\:39\.096\+00\:00 
action\_result\.data\.\*\.matchingIocInfo\.\*\.metadata\.quarantine\.last\_quarantined\_at | string |  |   2022\-07\-15T05\:43\:39\.096\+00\:00 
action\_result\.data\.\*\.matchingIocInfo\.\*\.metadata\.quarantine\.match\_count | numeric |  |   1 
action\_result\.data\.\*\.matchingIocInfo\.\*\.metadata\.quarantine\.quarantine\_count | numeric |  |   10 
action\_result\.data\.\*\.matchingIocInfo\.\*\.metadata\.source | string |  |  
action\_result\.data\.\*\.matchingIocInfo\.\*\.type | string |  |   ioc 
action\_result\.data\.\*\.modifiedBy | string |  |   system 
action\_result\.data\.\*\.modifiedDate | string |  |   2022\-07\-19T05\:51\:33\.949938 
action\_result\.data\.\*\.quarantineEmails\.\*\.createdDate | string |  |   2022\-07\-15T05\:43\:39\.091849 
action\_result\.data\.\*\.quarantineEmails\.\*\.errorMessage | string |  |  
action\_result\.data\.\*\.quarantineEmails\.\*\.ewsMessageId | string |  |   AAMkADAwNjYyZmI2LWYxYzgtNDJlZS05NWJmLTM3YjNlN2IzNzM5OABGAAAAAAAO1fllLjAOSLm9MgsUozfxBwCRXmjDwC9US6/LTV\+t6MQIAABhh9RXAACRXmjDwC9US6/LTV\+t6MQIAABtcrLJAAA= 
action\_result\.data\.\*\.quarantineEmails\.\*\.id | numeric |  |   5207 
action\_result\.data\.\*\.quarantineEmails\.\*\.internetMessageId | string |  |   <1270149500\.1722827\.1657392753324\@af226d4cfbab> 
action\_result\.data\.\*\.quarantineEmails\.\*\.originalFolderId | string |  |   AAMkADAwNjYyZmI2LWYxYzgtNDJlZS05NWJmLTM3YjNlN2IzNzM5OAAuAAAAAAAO1fllLjAOSLm9MgsUozfxAQCRXmjDwC9US6/LTV\+t6MQIAAAAAAEkAAA= 
action\_result\.data\.\*\.quarantineEmails\.\*\.quarantinedDate | string |  |   2022\-08\-03T05\:58\:51\.939468 
action\_result\.data\.\*\.quarantineEmails\.\*\.recipientAddress | string |  |   testuser\@test\.com 
action\_result\.data\.\*\.quarantineEmails\.\*\.status | string |  |   EXPUNGED 
action\_result\.data\.\*\.quarantineJobRuns\.\*\.completedDate | string |  |   2022\-07\-19T05\:51\:33\.96021 
action\_result\.data\.\*\.quarantineJobRuns\.\*\.error | numeric |  |  
action\_result\.data\.\*\.quarantineJobRuns\.\*\.id | numeric |  `cofense vision quarantine job id`  |   379 
action\_result\.data\.\*\.quarantineJobRuns\.\*\.jobRunType | string |  |   QUARANTINE 
action\_result\.data\.\*\.quarantineJobRuns\.\*\.startedDate | string |  |   2022\-07\-19T05\:51\:33\.950313 
action\_result\.data\.\*\.quarantineJobRuns\.\*\.status | string |  |   COMPLETED 
action\_result\.data\.\*\.quarantineJobRuns\.\*\.total | numeric |  |   1 
action\_result\.data\.\*\.searchId | string |  |  
action\_result\.data\.\*\.stopRequested | boolean |  |   True  False 
action\_result\.summary\.total\_quarantine\_jobs | numeric |  |   28 
action\_result\.message | string |  |   Total quarantine jobs\: 28 
summary\.total\_objects | numeric |  |   1 
summary\.total\_objects\_successful | numeric |  |   1   

## action: 'create quarantine job'
Creates a new quarantine job

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**quarantine\_emails** |  required  | A comma\-separated string of quarantine emails, specifying the recipient address and internet message ID of the email | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action\_result\.status | string |  |   success  failed 
action\_result\.parameter\.quarantine\_emails | string |  |   test\@test\.com\:<CAFRPxWuOFW\@test\.com&>\:<WCuib9wCsz\@test\.com>,testuser\@test\.com\:<YCuib9wCs1\@test\.com> 
action\_result\.data\.\*\.autoQuarantine | boolean |  |   True  False 
action\_result\.data\.\*\.createdBy | string |  |   cds 
action\_result\.data\.\*\.createdDate | string |  |   2023\-01\-11T07\:10\:32\.715663869 
action\_result\.data\.\*\.emailCount | numeric |  |   1 
action\_result\.data\.\*\.id | numeric |  `cofense vision quarantine job id`  |   1458 
action\_result\.data\.\*\.modifiedBy | string |  |   cds 
action\_result\.data\.\*\.modifiedDate | string |  |   2023\-01\-11T07\:10\:32\.715663869 
action\_result\.data\.\*\.quarantineEmails\.\*\.createdDate | string |  |   2023\-01\-11T07\:10\:32\.712651423 
action\_result\.data\.\*\.quarantineEmails\.\*\.errorMessage | string |  |  
action\_result\.data\.\*\.quarantineEmails\.\*\.ewsMessageId | string |  |  
action\_result\.data\.\*\.quarantineEmails\.\*\.id | numeric |  |   6965 
action\_result\.data\.\*\.quarantineEmails\.\*\.internetMessageId | string |  |   <CAFRPxWtRtkkfV892gtZ\+CsjtSECOZmA\@test\.com> 
action\_result\.data\.\*\.quarantineEmails\.\*\.originalFolderId | string |  |  
action\_result\.data\.\*\.quarantineEmails\.\*\.quarantinedDate | string |  |  
action\_result\.data\.\*\.quarantineEmails\.\*\.recipientAddress | string |  |   testuser\@test\.com 
action\_result\.data\.\*\.quarantineEmails\.\*\.status | string |  |   NEW 
action\_result\.data\.\*\.quarantineJobRuns\.\*\.completedDate | string |  |  
action\_result\.data\.\*\.quarantineJobRuns\.\*\.error | numeric |  |  
action\_result\.data\.\*\.quarantineJobRuns\.\*\.id | numeric |  |   2812 
action\_result\.data\.\*\.quarantineJobRuns\.\*\.jobRunType | string |  |   QUARANTINE 
action\_result\.data\.\*\.quarantineJobRuns\.\*\.startedDate | string |  |  
action\_result\.data\.\*\.quarantineJobRuns\.\*\.status | string |  |   NEW 
action\_result\.data\.\*\.quarantineJobRuns\.\*\.total | numeric |  |   1 
action\_result\.data\.\*\.searchId | string |  |  
action\_result\.data\.\*\.stopRequested | boolean |  |   True  False 
action\_result\.summary | string |  |  
action\_result\.message | string |  |   Created a quarantine job successfully 
summary\.total\_objects | numeric |  |   1 
summary\.total\_objects\_successful | numeric |  |   1   

## action: 'restore quarantine job'
Restores emails quarantined by the job identified by the ID

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**id** |  required  | ID of the quarantine job in cofense vision to be restored | numeric |  `cofense vision quarantine job id` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action\_result\.status | string |  |   success  failed 
action\_result\.parameter\.id | numeric |  `cofense vision quarantine job id`  |   1234 
action\_result\.data | string |  |  
action\_result\.summary | string |  |  
action\_result\.message | string |  |   Successfully initiated the restore process 
summary\.total\_objects | numeric |  |   1 
summary\.total\_objects\_successful | numeric |  |   1   

## action: 'list message searches'
Retrieves the list of searches

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**page** |  optional  | The start page of the results\. The value must be a positive integer or 0 | numeric | 
**size** |  optional  | The number of results to retrieve per page\. The value must be a positive integer up to 2000 | numeric | 
**sort** |  optional  | The name\-value pair defining the order of the response\. Comma separated values are supported | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action\_result\.status | string |  |   success  failed 
action\_result\.parameter\.page | numeric |  |   0 
action\_result\.parameter\.size | numeric |  |   50 
action\_result\.parameter\.sort | string |  |   createdBy\:desc,id\:asc 
action\_result\.data\.\*\.attachmentHashCriteria\.attachmentHashes\.\*\.hashString | string |  |   a855dc7659e527bf2C1a5bdFc43519c6 
action\_result\.data\.\*\.attachmentHashCriteria\.attachmentHashes\.\*\.hashType | string |  |   MD5 
action\_result\.data\.\*\.attachmentHashCriteria\.type | string |  |   ANY 
action\_result\.data\.\*\.createdBy | string |  |   visionAdmin 
action\_result\.data\.\*\.createdDate | string |  |   2022\-12\-09T20\:16\:42\.868693 
action\_result\.data\.\*\.domainCriteria\.type | string |  |   ANY 
action\_result\.data\.\*\.headers\.\*\.key | string |  |   X\-MS\-Exchange\-Organization\-AuthSource 
action\_result\.data\.\*\.id | numeric |  `cofense vision search id`  |   2146 
action\_result\.data\.\*\.internetMessageId | string |  |  
action\_result\.data\.\*\.modifiedBy | string |  |   visionAdmin 
action\_result\.data\.\*\.modifiedDate | string |  |   2022\-12\-09T20\:16\:42\.868693 
action\_result\.data\.\*\.partialIngest | boolean |  |   True  False 
action\_result\.data\.\*\.receivedAfterDate | string |  |  
action\_result\.data\.\*\.receivedBeforeDate | string |  |  
action\_result\.data\.\*\.recipient | string |  |  
action\_result\.data\.\*\.url | string |  |  
action\_result\.summary\.total\_message\_searches | numeric |  |   50 
action\_result\.message | string |  |   Total message searches\: 50 
summary\.total\_objects | numeric |  |   1 
summary\.total\_objects\_successful | numeric |  |   1   

## action: 'get message search'
Retrieves the search identified by an ID

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**id** |  required  | The unique ID that cofense vision has assigned to a search | numeric |  `cofense vision search id` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action\_result\.status | string |  |   success  failed 
action\_result\.parameter\.id | numeric |  `cofense vision search id`  |   1234 
action\_result\.data\.\*\.attachmentHashCriteria\.type | string |  |   ANY 
action\_result\.data\.\*\.createdBy | string |  |   CofenseTAP 
action\_result\.data\.\*\.createdDate | string |  |   2022\-12\-09T20\:31\:12\.605426 
action\_result\.data\.\*\.domainCriteria\.type | string |  |   ANY 
action\_result\.data\.\*\.id | numeric |  `cofense vision search id`  |   2147 
action\_result\.data\.\*\.internetMessageId | string |  |  
action\_result\.data\.\*\.modifiedBy | string |  |   CofenseTAP 
action\_result\.data\.\*\.modifiedDate | string |  |   2022\-12\-09T20\:31\:12\.605426 
action\_result\.data\.\*\.partialIngest | boolean |  |   True  False 
action\_result\.data\.\*\.receivedAfterDate | string |  |  
action\_result\.data\.\*\.receivedBeforeDate | string |  |  
action\_result\.data\.\*\.recipient | string |  |  
action\_result\.data\.\*\.url | string |  |  
action\_result\.summary | string |  |  
action\_result\.message | string |  |   Fetched message search successfully 
summary\.total\_objects | numeric |  |   1 
summary\.total\_objects\_successful | numeric |  |   1   

## action: 'get quarantine job'
Retrieves quarantine job identified by the ID

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**id** |  required  | ID of the quarantine job in cofense vision to be retrieved | numeric |  `cofense vision quarantine job id` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action\_result\.status | string |  |   success  failed 
action\_result\.parameter\.id | numeric |  `cofense vision quarantine job id`  |   1234 
action\_result\.data\.\*\.autoQuarantine | boolean |  |   True  False 
action\_result\.data\.\*\.createdBy | string |  |   cds 
action\_result\.data\.\*\.createdDate | string |  |   2022\-07\-07T11\:47\:47\.831045 
action\_result\.data\.\*\.emailCount | numeric |  |   2 
action\_result\.data\.\*\.id | numeric |  `cofense vision quarantine job id`  |   1234 
action\_result\.data\.\*\.matchingIocInfo\.\*\.attributes\.threat\_type | string |  |   URL 
action\_result\.data\.\*\.matchingIocInfo\.\*\.attributes\.threat\_value | string |  |   https\://test\.com 
action\_result\.data\.\*\.matchingIocInfo\.\*\.id | string |  |   4c620dda186fce3f088bd0c58b30dfaf 
action\_result\.data\.\*\.matchingIocInfo\.\*\.metadata\.quarantine\.created\_at | string |  |   2023\-01\-10T12\:07\:29\.564\+00\:00 
action\_result\.data\.\*\.matchingIocInfo\.\*\.metadata\.quarantine\.expired | boolean |  |   True  False 
action\_result\.data\.\*\.matchingIocInfo\.\*\.metadata\.quarantine\.expires\_at | string |  |   2021\-12\-28T06\:38\:13\.405\+00\:00 
action\_result\.data\.\*\.matchingIocInfo\.\*\.metadata\.quarantine\.first\_quarantined\_at | string |  |   2023\-01\-10T12\:08\:34\.638\+00\:00 
action\_result\.data\.\*\.matchingIocInfo\.\*\.metadata\.quarantine\.last\_quarantined\_at | string |  |   2023\-01\-10T12\:11\:08\.705\+00\:00 
action\_result\.data\.\*\.matchingIocInfo\.\*\.metadata\.quarantine\.match\_count | numeric |  |   2 
action\_result\.data\.\*\.matchingIocInfo\.\*\.metadata\.quarantine\.quarantine\_count | numeric |  |   2 
action\_result\.data\.\*\.matchingIocInfo\.\*\.metadata\.source | string |  |  
action\_result\.data\.\*\.matchingIocInfo\.\*\.type | string |  |   ioc 
action\_result\.data\.\*\.modifiedBy | string |  |   system 
action\_result\.data\.\*\.modifiedDate | string |  |   2022\-07\-07T12\:39\:26\.128664 
action\_result\.data\.\*\.quarantineEmails\.\*\.createdDate | string |  |   2022\-07\-07T11\:19\:18\.498196 
action\_result\.data\.\*\.quarantineEmails\.\*\.errorMessage | string |  |   No primary addresses were found for 34/xxxxx\@cofense\.com 
action\_result\.data\.\*\.quarantineEmails\.\*\.ewsMessageId | string |  |  
action\_result\.data\.\*\.quarantineEmails\.\*\.id | numeric |  |   34 
action\_result\.data\.\*\.quarantineEmails\.\*\.internetMessageId | string |  |   <BYAPR11MB2824EF099FE06D3740572200DC8D0\@BYAPR11MB2824\.namprd11\.prod\.outlook\.com> 
action\_result\.data\.\*\.quarantineEmails\.\*\.originalFolderId | string |  |  
action\_result\.data\.\*\.quarantineEmails\.\*\.quarantinedDate | string |  |  
action\_result\.data\.\*\.quarantineEmails\.\*\.recipientAddress | string |  |   svc\-nextgen\-sw\-2\@cofense\.com 
action\_result\.data\.\*\.quarantineEmails\.\*\.status | string |  |   UNKNOWN\_MAILBOX 
action\_result\.data\.\*\.quarantineJobRuns\.\*\.completedDate | string |  |   2022\-07\-07T11\:47\:54\.77392 
action\_result\.data\.\*\.quarantineJobRuns\.\*\.error | numeric |  |   2 
action\_result\.data\.\*\.quarantineJobRuns\.\*\.id | numeric |  |   106 
action\_result\.data\.\*\.quarantineJobRuns\.\*\.jobRunType | string |  |   QUARANTINE 
action\_result\.data\.\*\.quarantineJobRuns\.\*\.startedDate | string |  |   2022\-07\-07T11\:47\:54\.270013 
action\_result\.data\.\*\.quarantineJobRuns\.\*\.status | string |  |   COMPLETED 
action\_result\.data\.\*\.quarantineJobRuns\.\*\.total | numeric |  |   2 
action\_result\.data\.\*\.searchId | string |  |  
action\_result\.data\.\*\.stopRequested | boolean |  |   True  False 
action\_result\.summary | string |  |  
action\_result\.message | string |  |   Successfully retrieved the quarantine job information 
summary\.total\_objects | numeric |  |   1 
summary\.total\_objects\_successful | numeric |  |   1   

## action: 'approve quarantine job'
Approves the quarantine job identified by the ID\. When the Auto Quarantine feature is configured to require manual approvals, this endpoint can approve the pending quarantine jobs

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**id** |  required  | ID of the quarantine job in cofense vision to be approved | numeric |  `cofense vision quarantine job id` 
**message\_count** |  optional  | Number of emails containing IOC matches to be quarantined | numeric | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action\_result\.status | string |  |   success  failed 
action\_result\.parameter\.id | numeric |  `cofense vision quarantine job id`  |   1234 
action\_result\.parameter\.message\_count | numeric |  |   3 
action\_result\.data | string |  |  
action\_result\.summary | string |  |  
action\_result\.message | string |  |   The quarantine job has been approved successfully 
summary\.total\_objects | numeric |  |   1 
summary\.total\_objects\_successful | numeric |  |   1   

## action: 'delete quarantine job'
Deletes the quarantine job identified by the ID

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**id** |  required  | ID of the quarantine job in cofense vision to be deleted | numeric |  `cofense vision quarantine job id` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action\_result\.status | string |  |   success  failed 
action\_result\.parameter\.id | numeric |  `cofense vision quarantine job id`  |   1422 
action\_result\.data | string |  |  
action\_result\.summary | string |  |  
action\_result\.message | string |  |   Deleted the quarantine job successfully 
summary\.total\_objects | numeric |  |   1 
summary\.total\_objects\_successful | numeric |  |   1   

## action: 'get messagesearch results'
Retrieves the results for the search identified by the search ID

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**id** |  required  | The unique ID that cofense vision has assigned to a search | numeric |  `cofense vision search id` 
**page** |  optional  | Start page of the results\. The value must be a positive integer or 0 | numeric | 
**size** |  optional  | Number of results to fetch per page\. The value must be a positive integer up to 2000 | numeric | 
**sort** |  optional  | The name\-value pair defining the order of the response\. Comma separated values are supported | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action\_result\.status | string |  |   success  failed 
action\_result\.parameter\.id | numeric |  `cofense vision search id`  |   4825 
action\_result\.parameter\.page | numeric |  |   0 
action\_result\.parameter\.size | numeric |  |   50 
action\_result\.parameter\.sort | string |  |  
action\_result\.data\.\*\.attachments\.\*\.contentType | string |  |   text/plain 
action\_result\.data\.\*\.attachments\.\*\.detectedContentType | string |  |   text/plain 
action\_result\.data\.\*\.attachments\.\*\.filename | string |  |   test\_file\.txt 
action\_result\.data\.\*\.attachments\.\*\.id | numeric |  |   13933890 
action\_result\.data\.\*\.attachments\.\*\.md5 | string |  |   d5d5ae3069669b4e08071e992f98f081 
action\_result\.data\.\*\.attachments\.\*\.sha256 | string |  |   ef7247f075e010e7a9f4af6fa8f8dd4436b1cc12355226bbdc270a0fb1c885d0 
action\_result\.data\.\*\.attachments\.\*\.size | numeric |  |   3079266 
action\_result\.data\.\*\.deliveredOn | string |  |  
action\_result\.data\.\*\.from\.\*\.address | string |  |   testuser\@test\.com 
action\_result\.data\.\*\.from\.\*\.id | numeric |  |   4406179 
action\_result\.data\.\*\.from\.\*\.personal | string |  |   Test user 
action\_result\.data\.\*\.headers\.\*\.name | string |  |   X\-MS\-Exchange\-Organization\-InternalOrgSender 
action\_result\.data\.\*\.headers\.\*\.value | string |  |   False 
action\_result\.data\.\*\.htmlBody | string |  |  
action\_result\.data\.\*\.id | numeric |  |   4406179 
action\_result\.data\.\*\.internetMessageId | string |  `cofense vision internet message id`  |   <CAFRPxWtRtkkfV892gtZ\+CsjtSECOZmA\@test\.com> 
action\_result\.data\.\*\.md5 | string |  `md5`  |   ac208a9b84646dd7913c20520e2f9c6f 
action\_result\.data\.\*\.processedOn | string |  |   2022\-12\-15T13\:11\:11\.287\+00\:00 
action\_result\.data\.\*\.receivedOn | string |  |   2022\-12\-15T13\:11\:07\.000\+00\:00 
action\_result\.data\.\*\.recipients\.\*\.address | string |  |   testuser\@test\.com 
action\_result\.data\.\*\.recipients\.\*\.id | numeric |  |   36939637 
action\_result\.data\.\*\.recipients\.\*\.personal | string |  |  
action\_result\.data\.\*\.recipients\.\*\.recipientType | string |  |   to 
action\_result\.data\.\*\.sentOn | string |  |   2022\-12\-15T13\:10\:53\.000\+00\:00 
action\_result\.data\.\*\.sha1 | string |  `sha1`  |   31bc336427b2426c1480221b1ff1f1648adc4388 
action\_result\.data\.\*\.sha256 | string |  `sha256`  |   48c13b22e3d6ffb9ad5f85b6c2a32b5c80bffcd563d8c04bb7befd01b803fc20 
action\_result\.data\.\*\.subject | string |  |   A test mail 
action\_result\.data\.\*\.textBody | string |  |  
action\_result\.summary\.total\_results | numeric |  |   4 
action\_result\.message | string |  |   Total results\: 4 
summary\.total\_objects | numeric |  |   1 
summary\.total\_objects\_successful | numeric |  |   1   

## action: 'delete ioc'
Deletes a single active or expired IOC from the local IOC Repository

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**id** |  required  | The MD5 ID of the IOC to be deleted | string |  `md5`  `cofense vision ioc id` 
**source** |  required  | A single IOC source value, to fetch the IOCs added or modified by that particular source | string |  `cofense vision source` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action\_result\.status | string |  |   success  failed 
action\_result\.parameter\.id | string |  `md5`  `cofense vision ioc id`  |   27b609152ff01a84e0a7e421d7fd0fc7 
action\_result\.parameter\.source | string |  `cofense vision source`  |   Triage\-1 
action\_result\.data\.\*\.attributes\.threat\_type | string |  |   URL 
action\_result\.data\.\*\.attributes\.threat\_value | string |  `cofense vision threat value`  `domain`  `md5`  `sha256`  `url`  |   http\://test\.com/demo 
action\_result\.data\.\*\.id | string |  `md5`  `cofense vision ioc id`  |   41ecc26bd356dd706cc1a0cd839cad2c 
action\_result\.data\.\*\.metadata\.quarantine\.created\_at | string |  |   2022\-07\-07T09\:58\:57\.170\+00\:00 
action\_result\.data\.\*\.metadata\.quarantine\.expired | boolean |  |   True  False 
action\_result\.data\.\*\.metadata\.quarantine\.expires\_at | string |  |   2030\-10\-30T00\:00\:00\.000\+00\:00 
action\_result\.data\.\*\.metadata\.quarantine\.first\_quarantined\_at | string |  |  
action\_result\.data\.\*\.metadata\.quarantine\.last\_quarantined\_at | string |  |  
action\_result\.data\.\*\.metadata\.quarantine\.match\_count | numeric |  |  
action\_result\.data\.\*\.metadata\.quarantine\.quarantine\_count | numeric |  |  
action\_result\.data\.\*\.metadata\.quarantine\.wildcard | boolean |  |   True  False 
action\_result\.data\.\*\.metadata\.source\.created\_at | string |  |   2020\-01\-30T00\:00\:00\.000\+00\:00 
action\_result\.data\.\*\.metadata\.source\.id | string |  |   arbitrary source identifier 
action\_result\.data\.\*\.metadata\.source\.requested\_expiration | string |  |   2030\-10\-30T00\:00\:00\.000\+00\:00 
action\_result\.data\.\*\.metadata\.source\.threat\_level | string |  |   Malicious 
action\_result\.data\.\*\.metadata\.source\.updated\_at | string |  |   2020\-03\-30T00\:00\:00\.000\+00\:00 
action\_result\.data\.\*\.type | string |  |   ioc 
action\_result\.summary | string |  |  
action\_result\.message | string |  |   Delete IOC action ran successfully 
summary\.total\_objects | numeric |  |   1 
summary\.total\_objects\_successful | numeric |  |   1   

## action: 'stop quarantine job'
Issues a request to stop the quarantine job identified by ID

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**id** |  required  | ID of the quarantine job in cofense vision to be stopped | numeric |  `cofense vision quarantine job id` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action\_result\.status | string |  |   success  failed 
action\_result\.parameter\.id | numeric |  `cofense vision quarantine job id`  |   1234 
action\_result\.data\.\*\.autoQuarantine | boolean |  |   True  False 
action\_result\.data\.\*\.createdBy | string |  |   cds 
action\_result\.data\.\*\.createdDate | string |  |   2022\-07\-07T11\:47\:47\.831045 
action\_result\.data\.\*\.emailCount | numeric |  |   2 
action\_result\.data\.\*\.id | numeric |  `cofense vision quarantine job id`  |   1234 
action\_result\.data\.\*\.modifiedBy | string |  |   cds 
action\_result\.data\.\*\.modifiedDate | string |  |   2023\-01\-16T07\:08\:42\.068037 
action\_result\.data\.\*\.quarantineEmails\.\*\.createdDate | string |  |   2022\-07\-07T11\:19\:18\.498196 
action\_result\.data\.\*\.quarantineEmails\.\*\.errorMessage | string |  |   No primary addresses were found for 34/xxxxx\@cofense\.com 
action\_result\.data\.\*\.quarantineEmails\.\*\.ewsMessageId | string |  |  
action\_result\.data\.\*\.quarantineEmails\.\*\.id | numeric |  |   34 
action\_result\.data\.\*\.quarantineEmails\.\*\.internetMessageId | string |  |   <BYAPR11MB2824EF099FE06D3740572200DC8D0\@BYAPR11MB2824\.namprd11\.prod\.outlook\.com> 
action\_result\.data\.\*\.quarantineEmails\.\*\.originalFolderId | string |  |  
action\_result\.data\.\*\.quarantineEmails\.\*\.quarantinedDate | string |  |  
action\_result\.data\.\*\.quarantineEmails\.\*\.recipientAddress | string |  |   svc\-nextgen\-sw\-2\@cofense\.com 
action\_result\.data\.\*\.quarantineEmails\.\*\.status | string |  |   UNKNOWN\_MAILBOX 
action\_result\.data\.\*\.quarantineJobRuns\.\*\.completedDate | string |  |   2022\-07\-07T11\:47\:54\.77392 
action\_result\.data\.\*\.quarantineJobRuns\.\*\.error | numeric |  |   2 
action\_result\.data\.\*\.quarantineJobRuns\.\*\.id | numeric |  |   106 
action\_result\.data\.\*\.quarantineJobRuns\.\*\.jobRunType | string |  |   QUARANTINE 
action\_result\.data\.\*\.quarantineJobRuns\.\*\.startedDate | string |  |   2022\-07\-07T11\:47\:54\.270013 
action\_result\.data\.\*\.quarantineJobRuns\.\*\.status | string |  |   COMPLETED 
action\_result\.data\.\*\.quarantineJobRuns\.\*\.total | numeric |  |   2 
action\_result\.data\.\*\.searchId | string |  |  
action\_result\.data\.\*\.stopRequested | boolean |  |   True  False 
action\_result\.summary | string |  |  
action\_result\.message | string |  |   Successfully stopped the quarantine job 
summary\.total\_objects | numeric |  |   1 
summary\.total\_objects\_successful | numeric |  |   1   

## action: 'create message search'
Creates a new search based on the user\-specified filters

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**subjects** |  optional  | A comma\-separated string of subjects to create a search for an email's subject\. Max 3 values are allowed | string | 
**senders** |  optional  | A comma\-separated string of senders to create a search for an email's sender\. Max 3 values are allowed | string | 
**attachment\_names** |  optional  | A comma\-separated string of attachment names to create a search for an email's attachments\. Max 3 values are allowed | string | 
**attachment\_hash\_match\_criteria** |  optional  | The type of matching performed on the hashes specified in the attachment\_hashes argument\. Allowed values are ANY and ALL | string | 
**attachment\_hashes** |  optional  | A comma\-separated string of attachment hashes to create a search for an email's attachment hashes\. Supported format\: hashtype1\:hashvalue1\. Example \: md5\:938c2cc0dcc05f2b68c4287040cfcf71\. Max 3 values are allowed | string | 
**attachment\_mime\_types** |  optional  | A comma\-separated string of MIME types to create a search for an email's attachment MIME type\. Max 3 values are allowed | string | 
**attachment\_exclude\_mime\_types** |  optional  | A comma\-separated string of MIME types to create a search for excluding an email's attachment MIME type\. Max 3 values are allowed | string | 
**domain\_match\_criteria** |  optional  | The type of matching to perform on the domains specified in the domains argument\. Allowed values ANY and ALL | string | 
**domains** |  optional  | A comma\-separated string of domains to create a search for domains in an email's body or its attachment\. Max 3 values are allowed | string | 
**headers** |  optional  | A comma\-separated string of key\-value pairs, defining the additional criteria to search for in the email header\. Max 3 values are allowed | string | 
**internet\_message\_id** |  optional  | The unique identifier of the email, enclosed in angle brackets\. This argument is case\-sensitive | string |  `cofense vision internet message id` 
**partial\_ingest** |  optional  | Whether to create a search with partially ingested emails \(true\) or without partially ingested emails \(false\) | boolean | 
**received\_after\_date** |  optional  | Date and time to create a search for emails which are received on or after the specified UTC date and time | string | 
**received\_before\_date** |  optional  | Date and time to create a search for emails which are received before or on the specified UTC date and time | string | 
**recipient** |  optional  | Create a search with the specified recipient\. Supports one or more wildcard characters \(\*\) in any position of a recipient's email address | string | 
**url** |  optional  | Create a search with the specified url\. Supports one or more wildcard characters \(\*\) in any position of the URL | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action\_result\.status | string |  |   success  failed 
action\_result\.parameter\.attachment\_exclude\_mime\_types | string |  |   image/png 
action\_result\.parameter\.attachment\_hash\_match\_criteria | string |  |   ANY 
action\_result\.parameter\.attachment\_hashes | string |  |   md5\:938c2cc0dcc05f2b68c4287040cfcf71 
action\_result\.parameter\.attachment\_mime\_types | string |  |   image/png 
action\_result\.parameter\.attachment\_names | string |  |   test\.png 
action\_result\.parameter\.domain\_match\_criteria | string |  |   ANY 
action\_result\.parameter\.domains | string |  |   test\.com 
action\_result\.parameter\.headers | string |  |   X\-MS\-Exchange\-Organization\-AuthSource\:DM6PR19MB3772\.namprd19\.prod\.test\.com 
action\_result\.parameter\.internet\_message\_id | string |  `cofense vision internet message id`  |   <1C626FCE\-6749\-4DE9\-884C\-C025173F80BB\@phishme\.com> 
action\_result\.parameter\.partial\_ingest | boolean |  |   True  False 
action\_result\.parameter\.received\_after\_date | string |  |   2022\-12\-22T12\:27\:29\.768 
action\_result\.parameter\.received\_before\_date | string |  |   2022\-12\-22T12\:27\:29\.768 
action\_result\.parameter\.recipient | string |  |   fname\.lname\@phishme\.com 
action\_result\.parameter\.senders | string |  |   fname\.lname\@phishme\.com 
action\_result\.parameter\.subjects | string |  |   This is a test subject 
action\_result\.parameter\.url | string |  |   https\://test\.com 
action\_result\.data\.\*\.attachmentHashCriteria\.attachmentHashes\.\*\.hashString | string |  |   938c2cc0dcc05f2b68c4287040cfcf71 
action\_result\.data\.\*\.attachmentHashCriteria\.attachmentHashes\.\*\.hashType | string |  |   MD5 
action\_result\.data\.\*\.attachmentHashCriteria\.type | string |  |   ANY 
action\_result\.data\.\*\.createdBy | string |  |   cds 
action\_result\.data\.\*\.createdDate | string |  |   2022\-12\-22T12\:27\:29\.768 
action\_result\.data\.\*\.domainCriteria\.type | string |  |   ANY 
action\_result\.data\.\*\.headers\.\*\.key | string |  |   X\-MS\-Exchange\-Organization\-AuthSource 
action\_result\.data\.\*\.id | numeric |  `cofense vision search id`  |   3972 
action\_result\.data\.\*\.internetMessageId | string |  |   <1C626FCE\-6749\-4DE9\-884C\-C025173F80BB\@phishme\.com> 
action\_result\.data\.\*\.modifiedBy | string |  |   cds 
action\_result\.data\.\*\.modifiedDate | string |  |   2022\-12\-22T12\:27\:29\.768 
action\_result\.data\.\*\.partialIngest | boolean |  |   True  False 
action\_result\.data\.\*\.receivedAfterDate | string |  |   2023\-01\-01T12\:27\:29\.768 
action\_result\.data\.\*\.receivedBeforeDate | string |  |   2023\-01\-03T12\:27\:29\.768 
action\_result\.data\.\*\.recipient | string |  |   test\@test\.com 
action\_result\.data\.\*\.url | string |  |   https\://test\.com 
action\_result\.summary | string |  |  
action\_result\.summary\.search\_id | numeric |  |   3646 
action\_result\.message | string |  |   Search id\: 3482 
summary\.total\_objects | numeric |  |   1 
summary\.total\_objects\_successful | numeric |  |   1   

## action: 'get last ioc'
Retrieves the last updated IOC from the local IOC Repository\. It may return an active or an expired IOC

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**source** |  required  | A single IOC source value, to fetch the IOCs added or modified by that particular source | string |  `cofense vision source` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action\_result\.status | string |  |   success  failed 
action\_result\.parameter\.source | string |  `cofense vision source`  |   Triage\-1 
action\_result\.data\.\*\.attributes\.threat\_type | string |  |   URL 
action\_result\.data\.\*\.attributes\.threat\_value | string |  `cofense vision threat value`  `domain`  `md5`  `sha256`  `url`  |   http\://test\.com/demo 
action\_result\.data\.\*\.id | string |  `md5`  `cofense vision ioc id`  |   41ecc26bd356dd706cc1a0cd839cad2c 
action\_result\.data\.\*\.metadata\.quarantine\.created\_at | string |  |   2022\-07\-07T09\:58\:57\.170\+00\:00 
action\_result\.data\.\*\.metadata\.quarantine\.expired | boolean |  |   True  False 
action\_result\.data\.\*\.metadata\.quarantine\.expires\_at | string |  |   2030\-10\-30T00\:00\:00\.000\+00\:00 
action\_result\.data\.\*\.metadata\.quarantine\.first\_quarantined\_at | string |  |  
action\_result\.data\.\*\.metadata\.quarantine\.last\_quarantined\_at | string |  |  
action\_result\.data\.\*\.metadata\.quarantine\.match\_count | numeric |  |  
action\_result\.data\.\*\.metadata\.quarantine\.quarantine\_count | numeric |  |  
action\_result\.data\.\*\.metadata\.quarantine\.wildcard | boolean |  |   True  False 
action\_result\.data\.\*\.metadata\.source\.created\_at | string |  |   2020\-01\-30T00\:00\:00\.000\+00\:00 
action\_result\.data\.\*\.metadata\.source\.id | string |  |   arbitrary source identifier 
action\_result\.data\.\*\.metadata\.source\.requested\_expiration | string |  |   2030\-10\-30T00\:00\:00\.000\+00\:00 
action\_result\.data\.\*\.metadata\.source\.threat\_level | string |  |   Malicious 
action\_result\.data\.\*\.metadata\.source\.updated\_at | string |  |   2020\-03\-30T00\:00\:00\.000\+00\:00 
action\_result\.data\.\*\.type | string |  |   ioc 
action\_result\.summary | string |  |  
action\_result\.summary\.ioc\_id | string |  |   d1c54c37fd53d37094ef1dc7530ca949 
action\_result\.message | string |  |   Get Last IOC Action succeeded 
summary\.total\_objects | numeric |  |   1 
summary\.total\_objects\_successful | numeric |  |   1   

## action: 'update iocs'
Updates one or more IOCs stored in the local IOC repository

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**source** |  required  | Single IOC source | string |  `cofense vision source` 
**iocs\_json** |  optional  | List of JSON data containing IOC detail to be updated in the IOC local repository | string | 
**threat\_type** |  optional  | Type of IOC | string | 
**threat\_value** |  optional  | Actual value of the IOC to match in the email | string |  `cofense vision threat value`  `domain`  `md5`  `sha256`  `url` 
**threat\_level** |  optional  | The severity of the IOC | string | 
**source\_id** |  optional  | Unique identifier assigned by the IOC source | string | 
**created\_at** |  optional  | The UTC date and time the IOC source included the IOC for the first time | string | 
**updated\_at** |  optional  | The UTC date and time the IOC source last updated the IOC | string | 
**requested\_expiration** |  optional  | Expiration date and time for this IOC in UTC | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action\_result\.status | string |  |   success  failed 
action\_result\.parameter\.created\_at | string |  |   4/10/2022 
action\_result\.parameter\.iocs\_json | string |  |   \[\{"threat\_type"\: "Domain","threat\_value"\: "test1\.com","threat\_level"\: "Malicious","created\_at"\: "20/08/2032","source\_id"\: "test\_source\_1","updated\_at"\: "20/08/2032","requested\_expiration"\: "30/08/2032"\},\{"threat\_type"\: "Domain","threat\_value"\: "test2\.com","threat\_level"\: "Malicious","created\_at"\: "20/08/2032","source\_id"\: "test\_source\_2","updated\_at"\: "20/08/2032","requested\_expiration"\: "30/08/2032"\}\] 
action\_result\.parameter\.requested\_expiration | string |  |   4/12/2022 
action\_result\.parameter\.source | string |  `cofense vision source`  |   Vision\-UI 
action\_result\.parameter\.source\_id | string |  |   test\_source\_id 
action\_result\.parameter\.threat\_level | string |  |   Malicious 
action\_result\.parameter\.threat\_type | string |  |   URL 
action\_result\.parameter\.threat\_value | string |  `cofense vision threat value`  `domain`  `md5`  `sha256`  `url`  |   https\://domain\.com 
action\_result\.parameter\.updated\_at | string |  |   4/11/2022 
action\_result\.data\.\*\.attributes\.threat\_type | string |  |   URL 
action\_result\.data\.\*\.attributes\.threat\_value | string |  `cofense vision threat value`  `domain`  `md5`  `sha256`  `url`  |   https\://domain\.com 
action\_result\.data\.\*\.id | string |  `md5`  `cofense vision ioc id`  |   7a89dc65140fdd10a71bf4c4721df6f4 
action\_result\.data\.\*\.metadata\.quarantine\.created\_at | string |  |   2022\-12\-28T08\:53\:19\.112\+00\:00 
action\_result\.data\.\*\.metadata\.quarantine\.expired | boolean |  |   True  False 
action\_result\.data\.\*\.metadata\.quarantine\.expires\_at | string |  |   2025\-04\-17T14\:05\:00\.000\+00\:00 
action\_result\.data\.\*\.metadata\.quarantine\.first\_quarantined\_at | string |  |  
action\_result\.data\.\*\.metadata\.quarantine\.last\_quarantined\_at | string |  |  
action\_result\.data\.\*\.metadata\.quarantine\.match\_count | numeric |  |  
action\_result\.data\.\*\.metadata\.quarantine\.quarantine\_count | numeric |  |  
action\_result\.data\.\*\.metadata\.quarantine\.wildcard | boolean |  |   True  False 
action\_result\.data\.\*\.metadata\.source\.created\_at | string |  |   2022\-04\-10T00\:00\:00\.000\+00\:00 
action\_result\.data\.\*\.metadata\.source\.id | string |  |   test\_source\_id 
action\_result\.data\.\*\.metadata\.source\.requested\_expiration | string |  |   2022\-04\-12T00\:00\:00\.000\+00\:00 
action\_result\.data\.\*\.metadata\.source\.threat\_level | string |  |   Malicious 
action\_result\.data\.\*\.metadata\.source\.updated\_at | string |  |   2022\-04\-11T00\:00\:00\.000\+00\:00 
action\_result\.data\.\*\.type | string |  |   ioc 
action\_result\.summary\.total\_iocs\_updated | numeric |  |   1 
action\_result\.message | string |  |   Total iocs updated\: 1 
summary\.total\_objects | numeric |  |   1 
summary\.total\_objects\_successful | numeric |  |   1   

## action: 'update ioc'
Updates the IOC identified by its unique MD5 ID

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**id** |  required  | The ID of the IOC to be updated | string |  `md5`  `cofense vision ioc id` 
**expires\_at** |  required  | Expiration date and time of the IOC in UTC | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action\_result\.status | string |  |   success  failed 
action\_result\.parameter\.expires\_at | string |  |   2080\-05\-15 
action\_result\.parameter\.id | string |  `md5`  `cofense vision ioc id`  |   7a785c76033e6e2f1464ba3f41ffb23a 
action\_result\.data\.\*\.attributes\.threat\_type | string |  |   URL 
action\_result\.data\.\*\.attributes\.threat\_value | string |  `cofense vision threat value`  `domain`  `md5`  `sha256`  `url`  |   https\://test\.com 
action\_result\.data\.\*\.id | string |  `md5`  `cofense vision ioc id`  |   7a785c76033e6e2f1464ba3f41ffb23a 
action\_result\.data\.\*\.metadata\.quarantine\.created\_at | string |  |   2023\-01\-02T09\:43\:38\.392\+00\:00 
action\_result\.data\.\*\.metadata\.quarantine\.expired | boolean |  |   True  False 
action\_result\.data\.\*\.metadata\.quarantine\.expires\_at | string |  |   2080\-05\-15T00\:00\:00\.000\+00\:00 
action\_result\.data\.\*\.metadata\.quarantine\.first\_quarantined\_at | string |  |  
action\_result\.data\.\*\.metadata\.quarantine\.last\_quarantined\_at | string |  |  
action\_result\.data\.\*\.metadata\.quarantine\.match\_count | numeric |  |  
action\_result\.data\.\*\.metadata\.quarantine\.quarantine\_count | numeric |  |  
action\_result\.data\.\*\.metadata\.quarantine\.wildcard | boolean |  |   True  False 
action\_result\.data\.\*\.metadata\.source | string |  |  
action\_result\.data\.\*\.type | string |  |   ioc 
action\_result\.summary | string |  |  
action\_result\.message | string |  |  
summary\.total\_objects | numeric |  |  
summary\.total\_objects\_successful | numeric |  |    

## action: 'list iocs'
Lists the IOCs stored in the local IOC Repository

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**source** |  required  | A single IOC source value | string |  `cofense vision source` 
**since** |  optional  | Include only IOCs that were added to the repository after the given UTC date | string | 
**page** |  optional  | Start page of the results\. The value must be a positive integer or 0 | numeric | 
**size** |  optional  | Number of results to fetch per page\. The value must be a positive integer up to 2000 | numeric | 
**sort** |  optional  | The name\-value pair defining the order of the response\. Comma separated values are supported | string | 
**include\_expired** |  optional  | Whether to include expired IOCs \(true\) or not include expired IOCs \(false\) | boolean | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action\_result\.status | string |  |   success  failed 
action\_result\.parameter\.include\_expired | boolean |  |   True  False 
action\_result\.parameter\.page | numeric |  |   0 
action\_result\.parameter\.since | string |  |   4/10/2022 
action\_result\.parameter\.size | numeric |  |   50 
action\_result\.parameter\.sort | string |  |   UpdatedAt\:asc 
action\_result\.parameter\.source | string |  `cofense vision source`  |   Vision\-UI 
action\_result\.data\.\*\.attributes\.threat\_type | string |  |   URL 
action\_result\.data\.\*\.attributes\.threat\_value | string |  `cofense vision threat value`  `domain`  `md5`  `sha256`  `url`  |   http\://test\.com/demo 
action\_result\.data\.\*\.id | string |  `md5`  `cofense vision ioc id`  |   e2c28ae167b51ad9e2eb8c656ab88ccb 
action\_result\.data\.\*\.metadata\.quarantine\.created\_at | string |  |   2022\-12\-28T09\:35\:32\.011\+00\:00 
action\_result\.data\.\*\.metadata\.quarantine\.expired | boolean |  |   True  False 
action\_result\.data\.\*\.metadata\.quarantine\.expires\_at | string |  |   2030\-10\-30T00\:00\:00\.000\+00\:00 
action\_result\.data\.\*\.metadata\.quarantine\.first\_quarantined\_at | string |  |  
action\_result\.data\.\*\.metadata\.quarantine\.last\_quarantined\_at | string |  |  
action\_result\.data\.\*\.metadata\.quarantine\.match\_count | numeric |  |   1 
action\_result\.data\.\*\.metadata\.quarantine\.quarantine\_count | numeric |  |   1 
action\_result\.data\.\*\.metadata\.quarantine\.wildcard | boolean |  |   True  False 
action\_result\.data\.\*\.metadata\.source\.created\_at | string |  |   2021\-02\-03T00\:00\:00\.000\+00\:00 
action\_result\.data\.\*\.metadata\.source\.id | string |  |   sid\_12345 
action\_result\.data\.\*\.metadata\.source\.requested\_expiration | string |  |   2030\-10\-30T00\:00\:00\.000\+00\:00 
action\_result\.data\.\*\.metadata\.source\.threat\_level | string |  |   Malicious 
action\_result\.data\.\*\.metadata\.source\.updated\_at | string |  |   2020\-03\-28T00\:00\:00\.000\+00\:00 
action\_result\.data\.\*\.type | string |  |   ioc 
action\_result\.summary\.total\_iocs | numeric |  |   5 
action\_result\.message | string |  |  
summary\.total\_objects | numeric |  |   1 
summary\.total\_objects\_successful | numeric |  |   1   

## action: 'get ioc'
Retrieves the IOC identified by its unique MD5 ID

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**id** |  required  | The MD5 ID of the IOC | string |  `md5`  `cofense vision ioc id` 
**source** |  required  | A single IOC source value, to fetch the IOCs added or modified by that particular source | string |  `cofense vision source` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action\_result\.status | string |  |   success  failed 
action\_result\.parameter\.id | string |  `md5`  `cofense vision ioc id`  |   27b609152ff01a84e0a7e421d7fd0fc7 
action\_result\.parameter\.source | string |  `cofense vision source`  |   Triage\-1 
action\_result\.data\.\*\.attributes\.threat\_type | string |  |   URL 
action\_result\.data\.\*\.attributes\.threat\_value | string |  `cofense vision threat value`  `domain`  `md5`  `sha256`  `url`  |   http\://test\.com/demo 
action\_result\.data\.\*\.id | string |  `md5`  |   41ecc26bd356dd706cc1a0cd839cad2c 
action\_result\.data\.\*\.metadata\.quarantine\.created\_at | string |  |   2022\-07\-07T09\:58\:57\.170\+00\:00 
action\_result\.data\.\*\.metadata\.quarantine\.expired | boolean |  |   True  False 
action\_result\.data\.\*\.metadata\.quarantine\.expires\_at | string |  |   2030\-10\-30T00\:00\:00\.000\+00\:00 
action\_result\.data\.\*\.metadata\.quarantine\.first\_quarantined\_at | string |  |  
action\_result\.data\.\*\.metadata\.quarantine\.last\_quarantined\_at | string |  |  
action\_result\.data\.\*\.metadata\.quarantine\.match\_count | numeric |  |  
action\_result\.data\.\*\.metadata\.quarantine\.quarantine\_count | numeric |  |  
action\_result\.data\.\*\.metadata\.quarantine\.wildcard | boolean |  |   True  False 
action\_result\.data\.\*\.metadata\.source\.created\_at | string |  |   2020\-01\-30T00\:00\:00\.000\+00\:00 
action\_result\.data\.\*\.metadata\.source\.id | string |  |   arbitrary source identifier 
action\_result\.data\.\*\.metadata\.source\.requested\_expiration | string |  |   2030\-10\-30T00\:00\:00\.000\+00\:00 
action\_result\.data\.\*\.metadata\.source\.threat\_level | string |  |   Malicious 
action\_result\.data\.\*\.metadata\.source\.updated\_at | string |  |   2020\-03\-30T00\:00\:00\.000\+00\:00 
action\_result\.data\.\*\.type | string |  |   ioc 
action\_result\.summary | string |  |  
action\_result\.message | string |  |   Get IOC action passed 
summary\.total\_objects | numeric |  |   1 
summary\.total\_objects\_successful | numeric |  |   1   

## action: 'list searchable headers'
Retrieves a list of configured header keys that can be used to create a message search

Type: **investigate**  
Read only: **True**

#### Action Parameters
No parameters are required for this action

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action\_result\.status | string |  |   success  failed 
action\_result\.data\.\*\.header | string |  |  
action\_result\.summary | string |  |  
action\_result\.message | string |  |  
summary\.total\_objects | numeric |  |  
summary\.total\_objects\_successful | numeric |  |    

## action: 'download logs'
Downloads the log files for all Cofense Vision components

Type: **investigate**  
Read only: **True**

#### Action Parameters
No parameters are required for this action

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action\_result\.status | string |  |   success  failed 
action\_result\.data\.\*\.aka\.\* | string |  |   test\.txt 
action\_result\.data\.\*\.container | string |  |   Test 
action\_result\.data\.\*\.container\_id | numeric |  |   5 
action\_result\.data\.\*\.create\_time | string |  |   0 minutes ago 
action\_result\.data\.\*\.created\_via | string |  |   automation 
action\_result\.data\.\*\.hash | string |  `vault id`  |   31c194010afedb76694517e6250b5339d72ed518 
action\_result\.data\.\*\.id | numeric |  |   29 
action\_result\.data\.\*\.metadata\.sha1 | string |  `sha1`  |   31c194010afedb76694517e6250b5339d72ed518 
action\_result\.data\.\*\.metadata\.sha256 | string |  `sha256`  |   ef7247f075e010e7a9f4af6fa8f8dd4436b1cc12355226bbdc270a0fb1c885d0 
action\_result\.data\.\*\.mime\_type | string |  |   text/plain 
action\_result\.data\.\*\.name | string |  |   logfiles\_2023\-01\-06\_06\:49\:00\.536505\.zip 
action\_result\.data\.\*\.path | string |  |   /opt/phantom/vault/31/c1/31c194010afedb76694517e6250b5339d72ed518 
action\_result\.data\.\*\.size | numeric |  |   3079266 
action\_result\.data\.\*\.task | string |  |  
action\_result\.data\.\*\.user | string |  |   admin 
action\_result\.data\.\*\.vault\_document | numeric |  |   29 
action\_result\.data\.\*\.vault\_id | string |  `vault id`  |   31c194010afedb76694517e6250b5339d72ed518 
action\_result\.summary\.vault\_id | string |  `vault id`  |   31c194010afedb76694517e6250b5339d72ed518 
action\_result\.message | string |  |   Vault id\: 31c194010afedb76694517e6250b5339d72ed518 
summary\.total\_objects | numeric |  |   1 
summary\.total\_objects\_successful | numeric |  |   1 
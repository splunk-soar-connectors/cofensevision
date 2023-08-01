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

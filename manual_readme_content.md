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

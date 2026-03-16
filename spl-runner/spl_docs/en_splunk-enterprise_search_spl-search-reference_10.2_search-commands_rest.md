
# rest


## Description

The rest command reads a Splunk REST API endpoint and returns the resource data as a search result.

Splunk Cloud Platform

For information about Splunk REST API endpoints, see the Splunk platform REST API Reference Manual .

Splunk Enterprise

For information about the REST API, see the Splunk platform REST API User Manual . For information about Splunk REST API endpoints, see the Splunk platform REST API Reference Manual .


## Syntax

The required syntax is in bold .

| rest &lt;rest-uri&gt;

[count=&lt;int&gt;]

[strict=&lt;bool&gt;]

[splunk_server=&lt;wc-string&gt;]

[splunk_server_group=&lt;wc-string&gt;]...

[timeout=&lt;int&gt;]

[&lt;get-arg-name&gt;=&lt;get-arg-value&gt;]...


### Required arguments

rest-uri

Syntax: &lt;uri&gt;

Description: URI path to the Splunk REST API endpoint.


### Optional arguments

count

Syntax: count=&lt;int&gt;

Description: Limits the number of results returned from each REST call. For example, you have four indexers and one search head. You set the limit to count=25000 . This results in a total limit of 125000, which is 25000 x 5.

When count=0, there is no limit.

Default: 0

get-arg-name

Syntax: &lt;string&gt;

Description: REST argument name for the REST endpoint. For the specific set of arguments supported by a specific endpoint, see the Splunk platform REST API Reference Manual .

get-arg-value

Syntax: &lt;string&gt;

Description: REST argument value for the REST endpoint. For the specific set of arguments supported by a specific endpoint, see the Splunk platform REST API Reference Manual .

splunk_server

Syntax: splunk_server=&lt;wc-string&gt;

Description: Specifies the distributed search peer from which to return results. You can specify only one splunk_server argument, However, you can use a wildcard character when you specify the server name to indicate multiple servers. For example, you can specify splunk_server=peer01 or splunk_server=peer\* . Use local to refer to the search head.

Default: All configured search peers return information

splunk_server_group

Syntax: splunk_server_group=&lt;wc-string&gt;...

Description: Limits the results to one or more server groups. You can specify a wildcard character in the string to indicate multiple server groups.

strict

Syntax: strict=&lt;bool&gt;

Description: When set to true this argument forces the search to fail completely if rest raises an error. This happens even when the errors apply to a subsearch. When set to false , many rest error conditions return warning messages but do not otherwise cause the search to fail. Certain error conditions cause the search to fail even when strict=false .

Default: false

timeout

Syntax: timeout=&lt;int&gt;

Description: Specify the timeout, in seconds, to wait for the REST endpoint to respond. Specify timeout=0 to indicate no limit on the time to wait for the REST endpoint to respond.

Default: 60


## Usage

The rest command authenticates using the ID of the person that runs the command.


### Strict error handling

Use the strict argument to make rest searches fail whenever they encounter an error condition. You can set this at the system level for all rest searches by changing restprocessor_errors_fatal in limits.conf .




> **Note: If you use Splunk Cloud Platform, file a Support ticket to change the restprocessor_errors_fatal setting.**


Use the strict argument to override the restprocessor_errors_fatal setting for a rest search.


## Examples


### 1. Access saved search jobs

CODE

Copy

| rest /services/search/jobs count=0 splunk_server=local | search isSaved=1


```spl

| rest /services/search/jobs count=0 splunk_server=local | search isSaved=1

```



### 2. Find all saved searches with searches that include a specific sourcetype

Find all saved searches with search strings that include the speccsv sourcetype.

CODE

Copy

| rest /services/saved/searches splunk_server=local | rename search AS saved_search | fields author, title, saved_search | search saved_search=\*speccsv\*


```spl

| rest /services/saved/searches splunk_server=local | rename search AS saved_search | fields author, title, saved_search | search saved_search=*speccsv*

```



### 3. Showing events only associated with the current user

To create reports that only show events associated with the logged in user, you can add the current search user to all events.

CODE

Copy

\* | head 10 | join [ | rest splunk_server=local /services/authentication/current-context | rename username as auth_user_id | fields auth_user_id ]


```spl

* | head 10 | join [ | rest splunk_server=local /services/authentication/current-context | rename username as auth_user_id | fields auth_user_id ]

```



### 4. Use the GET method pagination and filtering arguments

Most GET methods support a set of pagination and filtering arguments.

To determine if an endpoint supports these arguments, find the endpoint in the Splunk platform REST API Reference Manual . Click Expand on the GET method and look for a link to the Pagination and filtering arguments topic. For more information about the Pagination and filtering arguments, see the Request and response details in the Splunk Cloud Platform REST API Reference manual .

The following example uses the search argument for the saved/searches endpoint to identify if a search is scheduled and deactivated. The search looks for scheduled searches on Splunk servers that match the Monitoring Console role of "search heads".

CODE

Copy

| rest /servicesNS/-/-/saved/searches splunk_server_group=dmc_group_search_head timeout=0 search="is_scheduled=1" search="disabled=0"


```spl

| rest /servicesNS/-/-/saved/searches splunk_server_group=dmc_group_search_head timeout=0 search="is_scheduled=1" search="disabled=0"

```


Here is an explanation for each part of this search:


| Description | Part of the search |
| --- | --- |
| The name of the REST call. | CODECopy\|rest /servicesNS/-/-/saved/searches\|rest /servicesNS/-/-/saved/searches |
| Look only at Splunk servers that match the Monitoring Console role of "search heads". | CODECopysplunk_server_group=dmc_group_search_headsplunk_server_group=dmc_group_search_head |
| Don't time out waiting for the REST call to finish. | CODECopytimeout=0timeout=0 |
| Look only for scheduled searches. | CODECopysearch="is_scheduled=1"search="is_scheduled=1" |
| Look only for active searches (not deactivated). | CODECopysearch="disabled=0"search="disabled=0" |



### 5. Return a table of results with custom endpoints

When you create a custom endpoint, you can format the response to return a table of results. The following example shows a custom endpoint:

CODE

Copy

| rest /servicesNS/-/myapp/myapp/endpoint


```spl

| rest /servicesNS/-/myapp/myapp/endpoint

```


Here's an example of the response you can use to return a table of results:

JSON

Copy

{
        "links": {},
        "entry": [
                {"content": {"name": "world", "fish": "salmon"}},
                {"content": {"name": "muu", "fish": "whale"}}
            ]
    }


```spl

{
        "links": {},
        "entry": [
                {"content": {"name": "world", "fish": "salmon"}},
                {"content": {"name": "muu", "fish": "whale"}}
            ]
    }

```


# loadjob


## Description

Loads events or results of a previously completed search job. The artifacts to load are identified either by the search job id &lt;sid&gt; or a scheduled search name and the time range of the current search. If a saved search name is provided and multiple artifacts are found within that range, the latest artifacts are loaded.




> **Note: You cannot run the loadjob command on real-time searches.**



## Syntax

The required syntax is in bold .

| loadjob

(&lt;sid&gt; | &lt;savedsearch&gt;)

[&lt;events&gt;]

[&lt;job_delegate&gt;]

[&lt;artifact_offset&gt;]

[&lt;ignore_running&gt;]


### Required arguments

You must specify either sid or savedsearch .

sid

Syntax: &lt;string&gt;

Description: The search ID of the job whose artifacts need to be loaded, for example: 1233886270.2 . You can locate the sid through the Job Inspector or the addinfo command.

savedsearch

Syntax: savedsearch="&lt;user-string&gt;:&lt;app-string&gt;:&lt;search-name-string&gt;"

Description: The unique identifier of a saved search whose artifacts need to be loaded. A saved search is uniquely identified by the triplet {user, app, savedsearch name}, for example: savedsearch="admin:search:my Saved Search" There is no method to specify a wildcard or match-all behavior. All portions of the triplet must be provided.


### Optional arguments

artifact_offset

Syntax: artifact_offset=&lt;int&gt;

Description: Selects a search artifact other than the most recent matching one. For example, if artifact_offset=1 , the second most recent artifact will be used. If artifact_offset=2 , the third most recent artifact will be used. If artifact_offset=0 , selects the most recent. A value that selects past all available artifacts will result in an error.

Default: 0

job_delegate

Syntax: job_delegate=&lt;string&gt;

Description: When specifying a saved search, this option selects search jobs that were started by the given user. Scheduled jobs will be run by the delegate "scheduler". Dashboard-embedded searches are run in accordance with the saved search's dispatchAs parameter, typically the owner of the search.

Defaults: scheduler

ignore_running

Syntax: ignore_running=&lt;bool&gt;

Description: Skip over artifacts whose search is still running.

Default: true

events

Syntax: events=&lt;bool&gt;

Description: Specifies whether to load events or results of a previously completed search job. To load events, set events=true . To load results, set events=false .

Default: false


## Usage

The loadjob command is an event-generating command . See Command types .

Generating commands use a leading pipe character and should be the first command in a search.

The loadjob command can be used for a variety of purposes, but one of the most useful is to run a fairly expensive search that calculates statistics. You can use loadjob searches to display those statistics for further aggregation, categorization, field selection and other manipulations for charting and display.

After a search job has completed and the results are cached, you can use this command to access or load the results.


### Search head clusters

A search head cluster can run the loadjob command only on scheduled saved searches. A search head cluster runs searches on results or artifacts that the search head cluster replicates.

For more information on artifact replication, see Search head clustering architecture in the Distributed Search manual.


### Controlling truncation in search results

To improve the speed of searches, Splunk software truncates the output of a search by default. For example, if the full output set is 10,000 events, the loadjob command might return only 1,000 events.




> **Note: When a successful search is run, it returns either events or results. Events are returned if the commands in the search only filter the data. Results are returned if one of the commands in the search is a transforming command, such as the table command.**


If your search returns events and you don't want the output truncated, you can add the table command to the end of your search. The table command returns results instead of events. For example:

CODE

Copy

sourcetype=access_\* | table host, source, event_message, node_path


```spl

sourcetype=access_* | table host, source, event_message, node_path

```


Because the search returns results and not events, when you use the loadjob command all of the results are returned.


### Splunk Enterprise

If search performance is not a concern, you can use the read_final_results_from_timeliner setting in the limits.conf file to control whether results are truncated when running the loadjob command.

When read_final_results_from_timeliner is set to 'true', which is the default, the loadjob search returns the sample of the final results, not the full result set. For example, if the full result set is 10,000 results, the search might return only 1,000 results. When read_final_results_from_timeliner is set to 'false', the loadjob search returns the full set of search results. For example, if the full result set is 10,000 results, the search returns 10,000 results.

To change the read_final_results_from_timeliner setting, follow these steps.

Prerequisites

- Only users with file system access, such as system administrators, can edit configuration files.

- Review the steps in How to edit a configuration file in the Splunk Enterprise Admin Manual .




> **CAUTION: Never change or copy the configuration files in the default directory. The files in the default directory must remain intact and in their original location. Make changes to the files in the local directory.**


Steps

- Open or create a local limits.conf file at $SPLUNK_HOME/etc/system/local.

- In the [search] stanza, add the line read_final_results_from_timeliner = true to truncate search results, or read_final_results_from_timeliner = false to output the full set of search results.


## Examples


### 1. Load the results of a saved search

Loads the results of the latest scheduled execution of saved search MySavedSearch in the 'search' application owned by the user admin .

CODE

Copy

| loadjob savedsearch="admin:search:MySavedSearch"


```spl

| loadjob savedsearch="admin:search:MySavedSearch"

```



### 2. Specifying a saved search with a space in the name

Loads the results of the latest scheduled execution of saved search Potential Threats in the 'search' application owned by the user maria .

CODE

Copy

| loadjob savedsearch="maria:search:Potential Threats"


```spl

| loadjob savedsearch="maria:search:Potential Threats"

```



### 3. Load the results from a specific search job

Loads the events that were generated by the search job with id=1233886270.2.

CODE

Copy

| loadjob 1233886270.2 events=true


```spl

| loadjob 1233886270.2 events=true

```



## See also

Commands

addinfo

inputcsv

savedsearch

Related information

Manage search jobs
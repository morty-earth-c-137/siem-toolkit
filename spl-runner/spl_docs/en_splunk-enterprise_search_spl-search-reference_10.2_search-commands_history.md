
# history


## Description

Use this command to view your search history in the current application. This search history is presented as a set of events or as a table.


## Syntax

| history [events=&lt;bool&gt;]


### Required arguments

None.


### Optional arguments

events

Syntax: events=&lt;bool&gt;

Description: When you specify events=true , the search history is returned as events. This invokes the event-oriented UI which allows for convenient highlighting, or field-inspection. When you specify events=false , the search history is returned in a table format for more convenient aggregate viewing.

Default: false

Fields returned when events=false .


| Output field | Description |
| --- | --- |
| _time | The time that the search was started. |
| api_et | The earliest time of the API call, which is the earliest time for which events were requested. |
| api_lt | The latest time of the API call, which is the latest time for which events were requested. |
| event_count | If the search retrieved or generated events, the count of events returned with the search. |
| exec_time | The execution time of the search in integer quantity of seconds into the Unix epoch. |
| is_realtime | Indicates whether the search was real-time (1) or historical (0). |
| result_count | If the search is a transforming search, the count of results for the search. |
| scan_count | The number of events retrieved from a Splunk index at a low level. |
| search | The search string. |
| search_et | The earliest time set for the search to run. |
| search_lt | The latest time set for the search to run. |
| sid | The search job ID. |
| splunk_server | The host name of the machine where the search was run. |
| status | The status of the search. |
| total_run_time | The total time it took to run the search in seconds. |



## Usage

The history command is a generating command and should be the first command in the search. Generating commands use a leading pipe character.

The history command returns your search history only from the application where you run the command.


## Examples


### Return search history in a table

Return a table of the search history. You do not have to specify events=false , since that this the default setting.

CODE

Copy

| history


```spl

| history

```





### Return search history as events

Return the search history as a set of events.

CODE

Copy

| history events=true


```spl

| history events=true

```





## See also

Commands

search
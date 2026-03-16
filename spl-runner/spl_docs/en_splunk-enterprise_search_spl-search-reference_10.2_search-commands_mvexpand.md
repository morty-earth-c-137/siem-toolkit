
# mvexpand


## Description

Expands the values of a multivalue field into separate events, one event for each value in the multivalue field. For each result, the mvexpand command creates a new result for every multivalue field.




> **Note: The mvexpand command can't be applied to internal fields.**


See Use default fields in the Knowledge Manager Manual .


## Syntax

mvexpand &lt;field&gt; [limit=&lt;int&gt;]


### Required arguments

field

Syntax: &lt;field&gt;

Description: The name of a multivalue field.


### Optional arguments

limit

Syntax: limit=&lt;int&gt;

Description: Specify the number of values of &lt;field&gt; to use for each input event.

Default: 0, or no limit


## Usage

The mvexpand command is a distributable streaming command. See Command types .

You can use evaluation functions and statistical functions on multivalue fields or to return multivalue fields.


### Limits

A limit exists on the amount of RAM that the mvexpand command is permitted to use while expanding a batch of results. By default the limit is 500MB. The input chunk of results is typically maxresultrows or smaller in size, and the expansion of all these results resides in memory at one time. The total necessary memory is the average result size multiplied by the number of results in the chunk multiplied by the average size of the multivalue field being expanded.

If this attempt exceeds the configured maximum on any chunk, the chunk is truncated and a warning message is emitted. If you have Splunk Enterprise, you can adjust the limit by editing the max_mem_usage_mb setting in the limits.conf file.

Prerequisites

- Have the permissions to increase the maxresultrows and max_mem_usage_mb settings. Only users with file system access, such as system administrators, can increase the maxresultrows and max_mem_usage_mb settings using configuration files.

- Know how to edit configuration files. Review the steps in How to edit a configuration file in the Splunk Enterprise Admin Manual .

- Decide which directory to store configuration file changes in. There can be configuration files with the same name in your default, local, and app directories. See Where you can place (or find) your modified configuration files in the Splunk Enterprise Admin Manual .




> **CAUTION: Never change or copy the configuration files in the default directory. The files in the default directory must remain intact and in their original location. Make changes to the files in the local directory.**


If you use Splunk Cloud Platform and encounter problems because of this limit, file a Support ticket.


## Examples


### Example 1:

Create new events for each value of multivalue field, "foo".

CODE

Copy

... | mvexpand foo


```spl

... | mvexpand foo

```



### Example 2:

Create new events for the first 100 values of multivalue field, "foo".

CODE

Copy

... | mvexpand foo limit=100


```spl

... | mvexpand foo limit=100

```



### Example 3:

The mvexpand command only works on one multivalue field. This example walks through how to expand an event with more than one multivalue field into individual events for each field value. For example, given these events, with sourcetype=data:

CODE

Copy

2018-04-01 00:11:23 a=22 b=21 a=23 b=32 a=51 b=24
2018-04-01 00:11:22 a=1 b=2 a=2 b=3 a=5 b=2


```spl

2018-04-01 00:11:23 a=22 b=21 a=23 b=32 a=51 b=24
2018-04-01 00:11:22 a=1 b=2 a=2 b=3 a=5 b=2

```


First, use the rex command to extract the field values for a and b. Then use the eval command and mvzip function to create a new field from the values of a and b.

CODE

Copy

source="mvexpandData.csv"
| rex field=_raw "a=(?&lt;a&gt;\d+)" max_match=5 
| rex field=_raw "b=(?&lt;b&gt;\d+)" max_match=5 
| eval fields = mvzip(a,b)  
| table _time fields


```spl

source="mvexpandData.csv"
| rex field=_raw "a=(?<a>\d+)" max_match=5 
| rex field=_raw "b=(?<b>\d+)" max_match=5 
| eval fields = mvzip(a,b)  
| table _time fields

```


The results appear on the Statistics tab and look something like this:


| _time | fields |
| --- | --- |
| 2018-04-01 00:11:23 | 22,2123,3251,24 |
| 2018-04-01 00:11:22 | 1,22,35,2 |




Use the mvexpand command and the

rex command

on the new field,

fields

, to create new events and extract the alpha and beta values:



CODE

Copy

source="mvexpandData.csv"
| rex field=_raw "a=(?&lt;a&gt;\d+)" max_match=5 
| rex field=_raw "b=(?&lt;b&gt;\d+)" max_match=5 
| eval fields = mvzip(a,b) 
| mvexpand fields 
| rex field=fields "(?&lt;alpha&gt;\d+),(?&lt;beta&gt;\d+)" 
| table _time alpha beta


```spl

source="mvexpandData.csv"
| rex field=_raw "a=(?<a>\d+)" max_match=5 
| rex field=_raw "b=(?<b>\d+)" max_match=5 
| eval fields = mvzip(a,b) 
| mvexpand fields 
| rex field=fields "(?<alpha>\d+),(?<beta>\d+)" 
| table _time alpha beta

```


Use the table command to display only the _time, alpha, and beta fields in a results table.

The results appear on the Statistics tab and look something like this:


| _time | alpha | beta |
| --- | --- | --- |
| 2018-04-01 00:11:23 | 23 | 32 |
| 2018-04-01 00:11:23 | 51 | 24 |
| 2018-04-01 00:11:22 | 1 | 2 |
| 2018-04-01 00:11:22 | 2 | 3 |
| 2018-04-01 00:11:22 | 5 | 2 |


(Thanks to Splunk user Duncan for this example.)


## See also

Commands:

makemv

mvcombine

nomv



Functions:

Multivalue eval functions

Multivalue stats and chart functions

split


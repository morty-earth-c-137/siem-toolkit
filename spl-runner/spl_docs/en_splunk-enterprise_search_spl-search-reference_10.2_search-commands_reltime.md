
# reltime


## Description

Creates one or more relative time fields and adds the field or fields to returned events. Each added relative time field provides a human-readable value of the difference between "now" (the start time of the search) and the timestamp value of a corresponding field in the returned event. Human-readable values look like 5 days ago , 1 minute ago , 2 years ago , and so on.


## Syntax

The required syntax is in bold .

| reltime

[timefield=&lt;field-list&gt;]

[prefix=&lt;string&gt;]


### Optional arguments

timefield

Syntax: timefield=&lt;field-list&gt;

Description: Specifies one or more time fields in the events returned by the search. The reltime command uses these fields as the basis for the relative time field that it adds to the events. timefield can specify only fields with values that are valid timestamps. timefield can specify multiple time fields as a comma-separated list bounded by double quotation marks.

Default: _time

prefix

Syntax: prefix=&lt;string&gt;

Description: Sets a prefix string for relative time field names. Use it to help others identify fields added by reltime or to provide unique field names when you identify multiple timefield values. If you specify multiple values for timefield but do not specify a prefix , the reltime command prefixes the relative time fields that it adds with reltime_ .


## Usage

The reltime command adds one or more relative time fields to your events. Each field added provides a human-readable value that represents the difference between now (the start time of the search) and the timestamp value of a field in the event.

For example, say you tie reltime to the _time fields in your events. If you run a search at 6 a.m., and the search returns an event with a _time value that translates to 5 a.m., reltime adds a field to that event named reltime with the value 1 hour ago .

If you use reltime without arguments, the command adds a relative time field to your events named reltime . This new field will be based on the _time field in each of your events.

The following table explains how reltime defines and names the fields that it adds.


| Customtimefieldspecified? | Customprefixspecified? | Basis for field(s) added byreltime | Name(s) of field(s) added byreltime |
| --- | --- | --- | --- |
| None | No | _time | reltime |
| Onetimefieldspecified | No | The time field you specified fortimefield | reltime |
| Onetimefieldspecified | Yes | The time field you specified fortimefield | reltime, prefixed by your customprefixstring |
| Multiple time fields specified | No | The list of time fields you specified fortimefield | The names of the fields you specified fortimefield, prefixed byreltime_ |
| Multiple time fields specified | Yes | The list of time fields you specified fortimefield | The names of the fields you specified fortimefield, prefixed by your customprefixstring |


The reltime command is a distributable streaming command. See Command types .


## Examples


### Example 1:

Adds a field called reltime to the events returned by the search, based on the _time field in those events.

CODE

Copy

... | reltime


```spl

... | reltime

```



### Example 2:

Adds a field called reltime to events returned by the search, based on the earliest_time field in those events.

CODE

Copy

... | reltime timefield=earliest_time


```spl

... | reltime timefield=earliest_time

```



### Example 3:

Adds a field called reltime_now_current_time to events, based on the current_time field in those events.

CODE

Copy

... | reltime timefield=current_time prefix=reltime_now_


```spl

... | reltime timefield=current_time prefix=reltime_now_

```



### Example 4:

Adds three new relative time fields called reltime_max_time , reltime_min_time , and reltime_current_time to returned events with max_time , min_time , and current_time fields.

CODE

Copy

... | reltime timefield="max_time,min_time,current_time"


```spl

... | reltime timefield="max_time,min_time,current_time"

```



### Example 5:

Adds two new relative time fields called usr_prefix_max_time and usr_prefix_min_time to returned events with max_time and min_time fields.

CODE

Copy

... | reltime timefield="max_time,min_time" prefix=usr_prefix_


```spl

... | reltime timefield="max_time,min_time" prefix=usr_prefix_

```



## See also

convert
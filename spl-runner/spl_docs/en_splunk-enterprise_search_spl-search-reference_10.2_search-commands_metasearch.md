
# metasearch


## Description

Retrieves event metadata from indexes based on terms in the &lt;logical-expression&gt;.


## Syntax

metasearch [&lt;logical-expression&gt;]


### Optional arguments

&lt;logical-expression&gt;

Syntax: &lt;time-opts&gt; | &lt;search-modifier&gt; | [NOT] &lt;logical-expression&gt; | &lt;index-expression&gt; | &lt;comparison-expression&gt; | &lt;logical-expression&gt; [OR &lt;logical-expression&gt;]

Description: Includes time and search modifiers, comparison and index expressions.


### Logical expression

&lt;comparison-expression&gt;

Syntax: &lt;field&gt;&lt;cmp&gt;&lt;value&gt;

Description: Compare a field to a literal value or values of another field.

&lt;index-expression&gt;

Syntax: "&lt;string&gt;" | &lt;term&gt; | &lt;search-modifier&gt;

&lt;time-opts&gt;

Syntax: [&lt;timeformat&gt;] [&lt;time-modifier&gt;]...


### Comparison expression

&lt;cmp&gt;

Syntax: = | != | &lt; | &lt;= | &gt; | &gt;=

Description: Comparison operators.

&lt;field&gt;

Syntax: &lt;string&gt;

Description: The name of one of the fields returned by the metasearch command. See Usage .

&lt;lit-value&gt;

Syntax: &lt;string&gt; | &lt;num&gt;

Description: An exact, or literal, value of a field that is used in a comparison expression.

&lt;value&gt;

Syntax: &lt;lit-value&gt; | &lt;field&gt;

Description: In comparison-expressions, the literal value of a field or another field name. The &lt;lit-value&gt; must be a number or a string.


### Index expression

&lt;search-modifier&gt;

Syntax: &lt;field-specifier&gt; | &lt;savedsplunk-specifier&gt; | &lt;tag-specifier&gt;


### Time options

The search allows many flexible options for searching based on time. For a list of time modifiers, see the topic Time modifiers for search in the Search Manual .

&lt;timeformat&gt;

Syntax: timeformat=&lt;string&gt;

Description: Set the time format for starttime and endtime terms. By default, timestamp is formatted: timeformat=%m/%d/%Y:%H:%M:%S .

&lt;time-modifier&gt;

Syntax: earliest=&lt;time_modifier&gt; | latest=&lt;time_modifier&gt;

Description: Specify start and end times using relative or absolute time. For more about the time modifier index, see Specify time modifiers in your search in the Search Manual .


## Usage

The metasearch command is an event-generating command . See Command types .

Generating commands use a leading pipe character and should be the first command in a search.

The metasearch command returns these fields:


| Field | Description |
| --- | --- |
| host | A default field that contains the host name or IP address of the network device that generated an event. |
| index | The repository for data. When the Splunk platform indexes raw data, it transforms the data into searchable events. |
| source | A default field that identifies the source of an event, that is, where the event originated. |
| sourcetype | A default field that identifies the data structure of an event. |
| splunk_server | The name of the instance where Splunk Enterprise is installed. |
| _time | The _time field contains an event's timestamp expressed in UNIX time. |



## Examples


### Example 1:

Return metadata on the default index for events with "404" and from host "webserver1".

CODE

Copy

| metasearch 404 host="webserver1"


```spl

| metasearch 404 host="webserver1"

```



## See also

Commands

metadata

search
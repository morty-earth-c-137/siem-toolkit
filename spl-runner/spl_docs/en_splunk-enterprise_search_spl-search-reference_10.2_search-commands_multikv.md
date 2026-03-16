
# multikv


## Description

Extracts field-values from table-formatted search results, such as the results of the top , tstats , and so on. The multikv command creates a new event for each table row and assigns field names from the title row of the table.

An example of the type of data the multikv command is designed to handle:

CODE

Copy

Name     Age   Occupation
Josh     42    SoftwareEngineer
Francine 35    CEO
Samantha 22    ProjectManager


```spl

Name     Age   Occupation
Josh     42    SoftwareEngineer
Francine 35    CEO
Samantha 22    ProjectManager

```


The key properties here are:

- Each line of text represents a conceptual record.

- The columns are aligned.

- The first line of text provides the names for the data in the columns.

The multikv command can transform this table from one event into three events with the relevant fields. It works more easily with the fixed-alignment though can sometimes handle merely ordered fields.

The general strategy is to identify a header, offsets, and field counts, and then determine which components of subsequent lines should be included into those field names. Multiple tables in a single event can be handled (if multitable=true), but might require ensuring that the secondary tables have capitalized or ALLCAPS names in a header row.

Auto-detection of header rows favors rows that are text, and are ALLCAPS or Capitalized.


> **Note: For Splunk Cloud Platform, you must create a private app to extract field-value pairs from table-formatted search results. If you are a Splunk Cloud administrator with experience creating private apps, see Manage private apps in your Splunk Cloud deployment in the Splunk Cloud Admin Manual . If you have not created private apps, contact your Splunk account representative for help with this customization.**



## Syntax

multikv [conf=&lt;stanza_name&gt;] [&lt;multikv-option&gt;...]


### Optional arguments

conf

Syntax: conf=&lt;stanza_name&gt;

Description: If you have a field extraction defined in multikv.conf , use this argument to reference the stanza in your search. For more information, refer to the configuration file reference for multikv.conf in the Admin Manual .

&lt;multikv-option&gt;

Syntax: copyattrs=&lt;bool&gt; | fields &lt;field-list&gt; | filter &lt;term-list&gt; | forceheader=&lt;int&gt; | multitable=&lt;bool&gt; | noheader=&lt;bool&gt; | rmorig=&lt;bool&gt;

Description: Options for extracting fields from tabular events.


### Descriptions for multikv options

copyattrs

Syntax: copyattrs=&lt;bool&gt;

Description: When true, multikv copies all fields from the original event to the events generated from that event. When false, no fields are copied from the original event. This means that the events will have no _time field and the UI will not know how to display them.

Default: true

fields

Syntax: fields &lt;field-list&gt;

Description: Limit the fields set by the multikv extraction to this list. Ignores any fields in the table which are not on this list.

filter

Syntax: filter &lt;term-list&gt;

Description: If specified, multikv skips over table rows that do not contain at least one of the strings in the filter list. Quoted expressions are permitted, such as "multiple words" or "trailing_space ".

forceheader

Syntax: forceheader=&lt;int&gt;

Description: Forces the use of the given line number (1 based) as the table's header. Does not include empty lines in the count.

Default: The multikv command attempts to determine the header line automatically.

multitable

Syntax: multitable=&lt;bool&gt;

Description: Controls whether or not there can be multiple tables in a single _raw in the original events.

Default: true

noheader

Syntax: noheader=&lt;bool&gt;

Description: Handle a table without header row identification. The size of the table will be inferred from the first row, and fields will be named Column_1, Column_2, ... noheader=true implies multitable=false .

Default: false

rmorig

Syntax: rmorig=&lt;bool&gt;

Description: When true, the original events will not be included in the output results. When false, the original events are retained in the output results, with each original emitted after the batch of generated results from that original.

Default: true


## Usage

The multikv command is a distributable streaming command. See Command types .


## Examples

Example 1: Extract the "COMMAND" field when it occurs in rows that contain "splunkd".

CODE

Copy

... | multikv fields COMMAND filter splunkd


```spl

... | multikv fields COMMAND filter splunkd

```


Example 2: Extract the "pid" and "command" fields.

CODE

Copy

... | multikv fields pid command


```spl

... | multikv fields pid command

```



## See also

extract , kvform , rex , spath , xmlkv ,
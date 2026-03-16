
# pivot


## Description

The pivot command makes simple pivot operations fairly straightforward, but can be pretty complex for more sophisticated pivot operations. Fundamentally this command is a wrapper around the stats and xyseries commands.

The pivot command does not add new behavior, but it might be easier to use if you are already familiar with how Pivot works. See the Pivot Manual . Also, read how to open non-transforming searches in Pivot .

Run pivot searches against a particular data model object. This requires a large number of inputs: the data model, the data model object, and pivot elements.


## Syntax

| pivot &lt;datamodel-name&gt; &lt;object-name&gt; &lt;pivot-element&gt;


### Required arguments

datamodel-name

Syntax: &lt;string&gt;

Description: The name of the data model to search.

objectname

Syntax: &lt;string&gt;

Description: The name of a data model object to search.

pivot element

Syntax: (&lt;cellvalue&gt;)\* (SPLITROW &lt;rowvalue&gt;)\* (SPLITCOL colvalue [options])\* (FILTER &lt;filter expression&gt;)\* (LIMIT &lt;limit expression&gt;)\* (ROWSUMMARY &lt;true | false&gt;)\* (COLSUMMARY &lt;true | false&gt;)\* (SHOWOTHER &lt;true | false&gt;)\* (NUMCOLS &lt;num&gt;)\* (rowsort [options])\*

Description: Use pivot elements to define your pivot table or chart. Pivot elements include cell values, split rows, split columns, filters, limits, row and column formatting, and row sort options. Cell values always come first. They are followed by split rows and split columns, which can be interleaved, for example: avg(val), SPLITCOL foo, SPLITROW bar, SPLITCOL baz .


### Cell value

&lt;cellvalue&gt;

Syntax: &lt;function&gt;(fieldname) [AS &lt;label&gt;]

Description: Define the values of a cell and optionally rename it. Here, label is the name of the cell in the report.

The set of allowed functions depend on the data type of the fieldname :

- Strings: list, values, first, last, count, and distinct_count (dc)

- Numbers: sum, count, avg, max, min, stdev, list, and values

- Timestamps: duration, earliest, latest, list, and values

- Object or child counts: count


### Descriptions for row split-by elements

SPLITROW &lt;rowvalue&gt;

Syntax: SPLITROW &lt;field&gt; [AS &lt;label&gt;] [RANGE start=&lt;value&gt; end=&lt;value&gt; max=&lt;value&gt; size=&lt;value&gt;] [PERIOD (auto | year | month | day | hour | minute | second)] [TRUELABEL &lt;label&gt;] [FALSELABEL &lt;label&gt;]

Description: You can specify one or more of these options on each SPLITROW. The options can appear in any order. You can rename the &lt;field&gt; using "AS &lt;label&gt;", where "label" is the name of the row in the report.

Other options depend on the data type of the &lt;field&gt; specified:

- RANGE applies only for numbers. You do not need to specify all of the options (start, end, max, and size).

- PERIOD applies only for timestamps. Use it to specify the period to bucket by.

- TRUELABEL applies only for booleans. Use it to specify the label for true values.

- FALSELABEL applies only for booleans. Use it to specify the label for false values.


### Descriptions for column split-by elements

SPLITCOL colvalue &lt;options&gt;

Syntax: fieldname [ RANGE start=&lt;value&gt; end=&lt;value&gt; max=&lt;value&gt; size=&lt;value&gt;] [PERIOD (auto | year | month| day | hour | minute | second)] [TRUELABEL &lt;label&gt;] [FALSELABEL &lt;label&gt;]

Description: You can have none, some, or all of these options on each SPLITCOL. They may appear in any order.

Other options depend on the data type of the field specified (fieldname):

- RANGE applies only for numbers. The options (start, end, max, and size) do not all have to be specified.

- PERIOD applies only for timestamps. Use it to specify the period to bucket by.

- TRUELABEL applies only for booleans. Use it to specify the label for true values.

- FALSELABEL applies only for booleans. Use it to specify the label for false values.


### Descriptions for filter elements

Filter &lt;filter expression&gt;

Syntax: &lt;fieldname&gt; &lt;comparison-operator&gt; &lt;value&gt;

Description: The expression used to identify values in a field. The comparison operator that you use depends on the type of field value.

- Strings: is, contains, in, isNot, doesNotContain, startsWith, endsWith, isNull, isNotNull

For example: ... filter fieldname in ( value1 , value2 , ...)

- ipv4: is, contains, isNot, doesNotContain, startsWith, isNull, isNotNull

- Numbers: =, !=, &lt;, &lt;=, &gt;, &gt;=, isNull, isNotNull

- Booleans: is, isNull, isNotNull


### Descriptions for limit elements

Limit &lt;limit expression&gt;

Syntax: LIMIT &lt;fieldname&gt; BY &lt;limittype&gt; &lt;number&gt; &lt;stats-function&gt;(&lt;fieldname&gt;)

Description: Use to limit the number of elements in the pivot. The limittype argument specifies where to place the limit. The valid values are top or bottom . The number argument must be a positive integer. You can use any stats function, such as min , max , avg , and sum .

Example: LIMIT foo BY TOP 10 avg(bar)


## Usage

The pivot command is a report-generating command . See Command types .

Generating commands use a leading pipe character and should be the first command in a search.


## Examples

Example 1: This command counts the number of events in the "HTTP Requests" object in the "Tutorial" data model.

CODE

Copy

| pivot Tutorial HTTP_requests count(HTTP_requests) AS "Count of HTTP requests"


```spl

| pivot Tutorial HTTP_requests count(HTTP_requests) AS "Count of HTTP requests"

```


This can be formatted as a single value report in the dashboard panel:



Example 2:

Using the Tutorial data model, create a pivot table for the count of "HTTP Requests" per host.



CODE

Copy

| pivot Tutorial HTTP_requests count(HTTP_requests) AS "Count" SPLITROW host AS "Server" SORT 100 host


```spl

| pivot Tutorial HTTP_requests count(HTTP_requests) AS "Count" SPLITROW host AS "Server" SORT 100 host

```





## See also

datamodel , stats , xyseries
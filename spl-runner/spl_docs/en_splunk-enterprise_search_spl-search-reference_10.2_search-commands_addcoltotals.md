
# addcoltotals


## Description

The addcoltotals command appends a new result to the end of the search result set. The result contains the sum of each numeric field or you can specify which fields to summarize. Results are displayed on the Statistics tab. If the labelfield argument is specified, a column is added to the statistical results table with the name specified.


## Syntax

addcoltotals [labelfield=&lt;field&gt;] [label=&lt;string&gt;] [&lt;wc-field-list&gt;]


### Optional arguments

&lt;wc-field-list&gt;

Syntax: &lt;field&gt; ...

Description: A space delimited list of valid field names. The addcoltotals command calculates the sum only for the fields in the list you specify. You can use the asterisk ( \* ) as a wildcard to specify a list of fields with similar names. For example, if you want to specify all fields that start with "value", you can use a wildcard such as value\* .

Default: Calculates the sum for all of the fields.

labelfield

Syntax: labelfield=&lt;fieldname&gt;

Description: Specify a field name to add to the result set.

Default: none

label

Syntax: label=&lt;string&gt;

Description: Used with the labelfield argument to add a label in the summary event. If the labelfield argument is absent, the label argument has no effect.

Default: Total


## Basic examples


### 1. Compute the sums of all the fields

Compute the sums of all the fields, and put the sums in a summary event called "change_name".

CODE

Copy

... | addcoltotals labelfield=change_name label=ALL


```spl

... | addcoltotals labelfield=change_name label=ALL

```



### 2. Add a column total for two specific fields

Add a column total for two specific fields in a table.

CODE

Copy

sourcetype=access_\* | table userId bytes avgTime duration | addcoltotals bytes duration


```spl

sourcetype=access_* | table userId bytes avgTime duration | addcoltotals bytes duration

```



### 3. Create the totals for a field that match a field name pattern

Filter fields for two name-patterns, and get totals for one of them.

CODE

Copy

...  | fields user\*, \*size | addcoltotals \*size


```spl

...  | fields user*, *size | addcoltotals *size

```



### 4. Specify a field name for the column totals

Augment a chart with a total of the values present.

CODE

Copy

index=_internal source="metrics.log" group=pipeline | stats avg(cpu_seconds) by processor | addcoltotals labelfield=processor


```spl

index=_internal source="metrics.log" group=pipeline | stats avg(cpu_seconds) by processor | addcoltotals labelfield=processor

```



## Extended example


### 1. Generate a total for a column


| This example uses the sample data from the Search Tutorial but should work with any format of Apache web access log. To try this example on your own Splunk instance, you must download the sample data and follow the instructions toget the tutorial data into Splunk. Use the time rangeAll timewhen you run the search. |
| --- |


The following search looks for events from web access log files that were successful views of strategy games. A count of the events by each product ID is returned.

CODE

Copy

sourcetype=access_\* status=200 categoryId=STRATEGY | chart count AS views by productId


```spl

sourcetype=access_* status=200 categoryId=STRATEGY | chart count AS views by productId

```


The results appear on the Statistics tab and look like this:


| productId | views |
| --- | --- |
| DB-SG-G01 | 1796 |
| DC-SG-G02 | 1642 |
| FS-SG-G03 | 1482 |
| PZ-SG-G05 | 1300 |


You can use the addcoltotals command to generate a total of the views and display the total at the bottom of the column.

CODE

Copy

sourcetype=access_\* status=200 categoryId=STRATEGY | chart count AS views by productId | addcoltotals


```spl

sourcetype=access_* status=200 categoryId=STRATEGY | chart count AS views by productId | addcoltotals

```


The results appear on the Statistics tab and look something like this:


| productId | views |
| --- | --- |
| DB-SG-G01 | 1796 |
| DC-SG-G02 | 1642 |
| FS-SG-G03 | 1482 |
| PZ-SG-G05 | 1300 |
|  | 6220 |


You can use add a field to the results that labels the total.

CODE

Copy

sourcetype=access_\* status=200 categoryId=STRATEGY | chart count AS views by productId | addcoltotals labelfield="Total views"


```spl

sourcetype=access_* status=200 categoryId=STRATEGY | chart count AS views by productId | addcoltotals labelfield="Total views"

```


The results appear on the Statistics tab and look something like this:


| productId | views | Total views |
| --- | --- | --- |
| DB-SG-G01 | 1796 |  |
| DC-SG-G02 | 1642 |  |
| FS-SG-G03 | 1482 |  |
| PZ-SG-G05 | 1300 |  |
|  | 6220 | Total |



## See also

Commands

addtotals

stats
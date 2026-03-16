
# fieldsummary


## Description

The fieldsummary command calculates summary statistics for all fields or a subset of the fields in your events. The summary information is displayed as a results table.


## Syntax

fieldsummary [maxvals=&lt;unsigned_int&gt;] [&lt;wc-field-list&gt;]


### Optional arguments

maxvals

Syntax: maxvals=&lt;unsigned_int&gt;

Description: Specifies the maximum distinct values to return for each field. Cannot be negative. Set maxvals = 0 to return all available distinct values for each field.

Default : 100

wc-field-list

Syntax: &lt;field&gt; ...

Description: A single field name or a space-delimited list of field names. You can use the asterisk ( \* ) as a wildcard to specify a list of fields with similar names. For example, if you want to specify all fields that start with "value", you can use a wildcard such as value\* .


## Usage

The fieldsummary command is a dataset processing command. See Command types .

The fieldsummary command displays the summary information in a results table. The following information appears in the results table:


| Summary field name | Description |
| --- | --- |
| field | The field name in the event. |
| count | The number of events/results with that field. |
| distinct_count | The number of unique values in the field. |
| is_exact | Whether or not the field is exact. This is related to the distinct count of the field values. If the number of values of the field exceedsmaxvals, thenfieldsummarywill stop retaining all the values and compute an approximate distinct count instead of an exact one. 1 means it is exact, 0 means it is not. |
| max | If the field is numeric, the maximum of its value. |
| mean | If the field is numeric, the mean of its values. |
| min | If the field is numeric, the minimum of its values. |
| numeric_count | The count of numeric values in the field. This would not include NULL values. |
| stdev | If the field is numeric, the standard deviation of its values. |
| values | The distinct values of the field and count of each value. The values are sorted first by highest count and then by distinct value, in ascending order. |



## Examples


### 1. Return summaries for all fields

This example returns summaries for all fields in the _internal index from the last 15 minutes.

CODE

Copy

index=_internal earliest=-15m latest=now | fieldsummary


```spl

index=_internal earliest=-15m latest=now | fieldsummary

```


In this example, the results in the max , min , and stdev fields are formatted to display up to 4 decimal points.




### 2. Return summaries for specific fields

This example returns summaries for fields in the _internal index with names that contain "size" and "count". The search returns only the top 10 values for each field from the last 15 minutes.

CODE

Copy

index=_internal earliest=-15m latest=now | fieldsummary maxvals=10 \*size\* \*count\*


```spl

index=_internal earliest=-15m latest=now | fieldsummary maxvals=10 *size* *count*

```





## See also

analyzefields , anomalies , anomalousvalue , stats
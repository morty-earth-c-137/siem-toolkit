
# Statistical and charting functions

You can use the statistical and charting functions with the chart , stats , and timechart commands.


## Support for related commands

The functions can also be used with related statistical and charting commands. The following table lists the commands supported by the statistical and charting functions and the related command that can also use these functions.


| Command | Supported related commands |
| --- | --- |
| chart | sichart |
| stats | eventstatsstreamstatsgeostatssistatsFor thetstatsand themstatscommands, see the documentation for each command for a list of the supported functions. |
| timechart | sitimechart |


Functions that you can use to create sparkline charts are noted in the documentation for each function. Sparkline is a function that applies to only the chart and stats commands, and allows you to call other functions. For more information, see Add sparklines to search results in the Search Manual .


## How field values are processed

Most of the statistical and charting functions expect the field values to be numbers. All of the values are processed as numbers, and any non-numeric values are ignored.

The following functions process the field values as literal string values, even though the values are numbers.


| countdistinct_countearliest | estdcestdc_errorfirst | latestlastlist | maxminmodevalues |
| --- | --- | --- | --- |


For example, you use the distinct_count function and the field contains values such as "1", "1.0", and "01". Each value is considered a distinct string value.

The only exceptions are the max and min functions. These functions process values as numbers if possible. For example, the values "1", "1.0", and "01" are processed as the same numeric value.


## Supported functions and syntax

There are two ways that you can see information about the supported statistical and charting functions:

- Function list by category

- Alphabetical list of functions


### Function list by category

The following table is a quick reference of the supported statistical and charting functions, organized by category. This table provides a brief description for each functions. Use the links in the table to learn more about each function and to see examples.


| Type of function | Supported functions and syntax | Description |
| --- | --- | --- |
| Aggregate functions | avg(&lt;value&gt;) | Returns the average of the values in the field specified. |
| count(&lt;value&gt;) | Returns the number of occurrences where the field that you specify contains any value (is not empty). You can also count the occurrences of a specific value in the field by using theevalcommand with thecountfunction. For example:count( eval(field_name="value")). |  |
| distinct_count(&lt;value&gt;) | Returns the count of distinct values in the field specified. |  |
| estdc(&lt;value&gt;) | Returns the estimated count of the distinct values in the field specified. |  |
| estdc_error(&lt;value&gt;) | Returns the theoretical error of the estimated count of the distinct values in the field specified. The error represents a ratio of theabsolute_value(estimate_distinct_count - real_distinct_count)/real_distinct_count. |  |
| exactperc&lt;percentile&gt;(&lt;value&gt;) | Returns a percentile value of the numeric field specified. Provides the exact value, but is very resource expensive for high cardinality fields. An alternative isperc. |  |
| max(&lt;value&gt;) | Returns the maximum value in the field specified. If the field values are non-numeric, the maximum value is found using lexicographical ordering. This function processes field values as numbers if possible, otherwise processes field values as strings. |  |
| mean(&lt;value&gt;) | Returns the arithmetic mean of the values in the field specified. |  |
| median(&lt;value&gt;) | Returns the middle-most value of the values in the field specified. |  |
| min(&lt;value&gt;) | Returns the minimum value in the field specified. If the field values are non-numeric, the minimum value is found using lexicographical ordering. |  |
| mode(&lt;value&gt;) | Returns the most frequent value in the field specified. |  |
| percentile&lt;percentile&gt;(&lt;value&gt;) | Returns the N-th percentile value of all the values in the numeric field specified. Valid field values are integers from 1 to 99.Additional percentile functions areupperperc&lt;percentile&gt;(&lt;value&gt;)andexactperc&lt;percentile&gt;(&lt;value&gt;). |  |
| range(&lt;value&gt;) | If the field values are numeric, returns the difference between the maximum and minimum values in the field specified. |  |
| stdev(&lt;value&gt;) | Returns the sample standard deviation of the values in the field specified. |  |
| stdevp(&lt;value&gt;) | Returns the population standard deviation of the values in the field specified. |  |
| sum(&lt;value&gt;) | Returns the sum of the values in the field specified. |  |
| sumsq(&lt;value&gt;) | Returns the sum of the squares of the values in the field specified. |  |
| upperperc&lt;percentile&gt;(&lt;value&gt;) | Returns an approximate percentile value, based on the requested percentile of the numeric field.When there are more than 1000 values, the upperperc function gives the approximate upper bound for the percentile requested. Otherwise the upperperc function returns the same percentile as thepercfunction. |  |
| var(&lt;value&gt;) | Returns the sample variance of the values in the field specified. |  |
| varp(&lt;value&gt;) | Returns the population variance of the values in the field specified. |  |
| Event order functions | first(&lt;value&gt; | Returns the first seen value in a field. In general, the first seen value of the field is the most recent instance of this field, relative to the input order of events into the stats command. |
| last(&lt;value&gt;) | Returns the last seen value in a field. In general, the last seen value of the field is the oldest instance of this field relative to the input order of events into the stats command. |  |
| Multivalue stats and chart functions | list(&lt;value&gt;) | Returns a list of up to 100 values in a field as a multivalue entry. The order of the values reflects the order of input events. |
| values(&lt;value&gt;) | Returns the list of all distinct values in a field as a multivalue entry. The order of the values is lexicographical. |  |
| Time functions | earliest(&lt;value&gt;) | Returns the chronologically earliest (oldest) seen occurrence of a value in a field. |
| earliest_time(&lt;value&gt;) | Returns the UNIX time of the earliest (oldest) occurrence of a value of the field. Used in conjunction with theearliest,latest, andlatest_timefunctions to calculate the rate of increase for an accumulating counter. |  |
| latest(&lt;value&gt;) | Returns the chronologically latest (most recent) seen occurrence of a value in a field. |  |
| latest_time(&lt;value&gt;) | Returns the UNIX time of the latest (most recent) occurrence of a value of the field. Used in conjunction with theearliest,earliest_time, andlatestfunctions to calculate the rate of increase for an accumulating counter. |  |
| per_day(&lt;value&gt;) | Returns the values in a field or eval expression for each day. |  |
| per_hour(&lt;value&gt;) | Returns the values in a field or eval expression for each hour. |  |
| per_minute(&lt;value&gt;) | Returns the values in a field or eval expression for each minute. |  |
| per_second(&lt;value&gt;) | Returns the values in a field or eval expression for each second. |  |
| rate(&lt;value&gt;) | Returns the per-second rate change of the value of the field. Represents(latest - earliest) / (latest_time - earliest_time)Requires theearliestandlatestvalues of the field to be numerical, and theearliest_timeandlatest_timevalues to be different. |  |
| rate_avg(&lt;value&gt;) | Returns the average rates for the time series associated with a specified accumulating counter metric. |  |
| rate_sum(&lt;value&gt;) | Returns the summed rates for the time series associated with a specified accumulating counter metric. |  |



### Alphabetical list of functions

The following table is a quick reference of the supported statistical and charting functions, organized alphabetically. This table provides a brief description for each function. Use the links in the table to learn more about each function and to see examples.


| Supported functions and syntax | Description | Type of function |
| --- | --- | --- |
| avg(&lt;value&gt;) | Returns the average of the values in the field specified. | Aggregate functions |
| count(&lt;value&gt;) | Returns the number of occurrences where the field that you specify contains any value (is not empty). You can also count the occurrences of a specific value in the field by using theevalcommand with thecountfunction. For example:count(eval(field_name="value")). | Aggregate functions |
| distinct_count(&lt;value) | Returns the count of distinct values in the field specified. | Aggregate functions |
| earliest(&lt;value&gt;) | Returns the chronologically earliest (oldest) seen occurrence of a value in the field specified. | Time functions |
| earliest_time(&lt;value&gt;) | Returns the UNIX time of the earliest (oldest) occurrence of a value in the field specified. Used in conjunction with theearliest,latest, andlatest_timefunctions to calculate the rate of increase for an accumulating counter. | Time functions |
| estdc(&lt;value&gt;) | Returns the estimated count of the distinct values in the field specified. | Aggregate functions |
| estdc_error(&lt;value&gt;) | Returns the theoretical error of the estimated count of the distinct values in the field specified. The error represents a ratio of theabsolute_value(estimate_distinct_count - real_distinct_count)/real_distinct_count. | Aggregate functions |
| exactperc&lt;percentile&gt;(&lt;value&gt;) | Returns a percentile value for the numeric field specified. Provides the exact value, but is very resource expensive for high cardinality fields. An alternative isperc. | Aggregate functions |
| first(&lt;value&gt;) | Returns the first seen value in a field. In general, the first seen value of the field is the most recent instance of this field, relative to the input order of events into the stats command. | Event order functions |
| last(&lt;value&gt;) | Returns the last seen value in a field. In general, the last seen value of the field is the oldest instance of this field relative to the input order of events into the stats command. | Event order functions |
| latest(&lt;value&gt;) | Returns the chronologically latest (most recent) seen occurrence of a value in a field. | Time functions |
| latest_time(&lt;value&gt;) | Returns the UNIX time of the latest (most recent) occurrence of a value of the field. Used in conjunction with theearliest,earliest_time, andlatestfunctions to calculate the rate of increase for an accumulating counter. | Time functions |
| list(&lt;value&gt;) | Returns a list of up to 100 values in a field as a multivalue entry. The order of the values reflects the order of input events. | Multivalue stats and chart functions |
| max(&lt;value&gt;) | Returns the maximum value in the field specified. If the field values are non-numeric, the maximum value is found using lexicographical ordering. This function processes field values as numbers if possible, otherwise processes field values as strings. | Aggregate functions |
| mean(&lt;value&gt;) | Returns the arithmetic mean of the values in the field specified. | Aggregate functions |
| median(&lt;value&gt;) | Returns the middle-most value of the values in the field specified. | Aggregate functions |
| min(&lt;value&gt;) | Returns the minimum value in the field specified. If the field values are non-numeric, the minimum value is found using lexicographical ordering. | Aggregate functions |
| mode(&lt;value&gt;) | Returns the most frequent value in the field specified. | Aggregate functions |
| perc&lt;percentile&gt;(&lt;value&gt;) | Returns the N-th percentile value of all the values in the numeric field specified. Valid field values are integers from 1 to 99.Additional percentile functions areupperpercandexactperc. | Aggregate functions |
| per_day(&lt;value&gt;) | Returns the values in a field or eval expression for each day. | Time functions |
| per_hour(&lt;value&gt;) | Returns the values in a field or eval expression for each hour. | Time functions |
| per_minute(&lt;value&gt;) | Returns the values in a field or eval expression for each minute. | Time functions |
| per_second(&lt;value&gt;) | Returns the values in a field or eval expression for each second. | Time functions |
| range(&lt;value&gt;) | If the field values are numeric, returns the difference between the maximum and minimum values in the field specified. | Aggregate functions |
| rate(&lt;value&gt;) | Returns the per-second rate change of the value of the field. Represents(latest - earliest) / (latest_time - earliest_time)Requires theearliestandlatestvalues of the field to be numerical, and theearliest_timeandlatest_timevalues to be different. | Time functions |
| rate_avg(&lt;value&gt;) | Returns the average rates for the time series associated with a specified accumulating counter metric. | Time functions |
| rate_sum(&lt;value&gt;) | Returns the summed rates for the time series associated with a specified accumulating counter metric. | Time functions |
| stdev(&lt;value&gt;) | Returns the sample standard deviation of the values in the field specified. | Aggregate functions |
| stdevp(&lt;value&gt;) | Returns the population standard deviation of the values in the field specified. | Aggregate functions |
| sum(&lt;value&gt;) | Returns the sum of the values in the field specified. | Aggregate functions |
| sumsq(&lt;value&gt;) | Returns the sum of the squares of the values in the field specified. | Aggregate functions |
| upperperc&lt;percentile&gt;(&lt;value&gt;) | Returns an approximate percentile value, based on the requested percentile of the numeric field.When there are more than 1000 values, the upperperc function gives the approximate upper bound for the percentile requested. Otherwise the upperperc function returns the same percentile as thepercfunction. | Aggregate functions |
| values(&lt;value&gt;) | Returns the list of all distinct values in a field as a multivalue entry. The order of the values is lexicographical. | Multivalue stats and chart functions |
| var(&lt;value&gt;) | Returns the sample variance of the values in the field specified. | Aggregate functions |
| varp(&lt;value&gt;) | Returns the population variance of the values in the field specified. | Aggregate functions |



## See also

Commands

chart

geostats

eventstats

stats

streamstats

timechart

Functions

Evaluation functions


## Answers

Have questions? Visit Splunk Answers and search for a specific function or command.
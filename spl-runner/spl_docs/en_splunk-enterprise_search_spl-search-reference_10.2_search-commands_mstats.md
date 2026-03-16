
# mstats


## Description

Use the mstats command to analyze metrics. This command performs statistics on the measurement , metric_name , and dimension fields in metric indexes. You can use mstats in historical searches and real-time searches . When you use mstats in a real-time search with a time window, a historical search runs first to backfill the data.




> **Note: The mstats command provides the best search performance when you use it to search a single metric_name value or a small number of metric_name values.**





> **Note: Certain restricted search commands, including mpreview and mstats might stop working if your organization uses field filters to protect sensitive data. See Plan for field filters in your organization in Securing the Splunk Platform .**



## Syntax

The required syntax is in bold .

| mstats

[chart=&lt;bool&gt;]

[&lt;chart-options&gt;]

[prestats=&lt;bool&gt;]

[append=&lt;bool&gt;]

[backfill=&lt;bool&gt;]

[update_period=&lt;integer&gt;]

[fillnull_value=&lt;string&gt;]

[chunk_size=&lt;unsigned int&gt;]

&lt;stats-metric-term&gt;...

WHERE [&lt;logical-expression&gt;]...

[ (BY|GROUPBY) &lt;field-list&gt; ]

[&lt;span-length&gt;]


### Required arguments

&lt;stats-metric-term&gt;

Syntax: &lt;stats-func&gt; | &lt;stats-func-value&gt;

Description: Provides two options for performing statistical calculations on metrics. Use &lt;stats-func&gt; to perform statistical calculations on one or more metrics that you name in the argument. Use &lt;stats-func-value&gt; for cases where a wildcard can be used to represent several metrics. You cannot blend the &lt;stats-func&gt; syntax and the &lt;stats-func-value syntax in a single mstats search.

Use the &lt;stats-func&gt; syntax for most cases. You only need to use the &lt;stats-func-value&gt; syntax in cases where a single metric may be represented by several different metric names, such as cpu.util and cpu.utilization . In these cases you can apply a wildcard to catch all of the permutations of the metric_name .

See Stats metric term options for details on the &lt;stats-func&gt; and &lt;stats-func-value&gt; syntax options.


### Optional arguments

append

Syntax: append=&lt;bool&gt;

Description: Valid only when prestats=true . This argument runs the mstats command and adds the results to an existing set of results instead of generating new results.

Default: false

backfill

Syntax: backfill=&lt;bool&gt;

Description: Valid only with real-time searches that have a time window. When backfill=true , the mstats command runs a search on historical data to backfill events before searching the in-memory real-time data.

Default: true

chart

Syntax: chart=&lt;bool&gt;

Description: When set to chart=t , the mstats data output has a format suitable for charting. The mstats charting mode is valid only when prestats=f .

When a span is provided, the mstats chart mode format resembles that of the timechart command, and can support at most one group-by field, which is used as the series splitting field.

When no span is provided, the chart mode follows a format similar to that of the chart or timechart commands. Without a span , the mstats chart mode requires one or two grouping fields. The first grouping field represents the chart x-axis. The second grouping field represents the y-axis and is a series split field.

Default: chart=f

&lt;chart-options&gt;

Syntax: chart.limit | chart.agg | chart.usenull | chart.useother | chart.nullstr | chart.otherstr

Description: Options that you can specify to refine the result. See the Chart options section in this topic.

chunk_size

Syntax: chunk_size=&lt;unsigned_int&gt;

Description: Advanced option. This argument controls how many metric time series are retrieved at a time from a single time-series index file ( .tsidx file) when the Splunk software processes searches. Lower this setting from its default only when you find a particular mstats search is using too much memory, or when it infrequently returns events. This can happen when a search groups by excessively high-cardinality dimensions (dimensions with very large amounts of distinct values). In such situations, a lower chunk_size value can make mstats searches more responsive, but potentially slower to complete. A higher chunk_size , on the other hand, can help long-running searches to complete faster, with the potential tradeoff of causing the search to be less responsive. For mstats , chunk_size cannot be set lower than 10000 .

Default: 10000000 (10 million)

fillnull_value

Description: This argument sets a user-specified value that the mstats command substitutes for null values for any field within its group-by field list. Null values include field values that are missing from a subset of the returned events as well as field values that are missing from all of the returned events. If you do not provide a fillnull_value argument, mstats omits rows for events with one or more null field values from its results.

Default: empty string

&lt;field-list&gt;

Syntax: &lt;field&gt;, ...

Description: Specifies one or more fields to group the results by. Required when using the BY clause.

&lt;logical-expression&gt;

Syntax: &lt;time-opts&gt;|&lt;search-modifier&gt;|((NOT)? &lt;logical-expression&gt;)|&lt;search-modifier&gt;|&lt;comparison-expression&gt;|(&lt;logical-expression&gt; (OR)? &lt;logical-expression&gt;)

Description: An expression describing the filters that are applied to your search. Includes time and search modifiers, and comparison expressions. See the following sections for descriptions of each of these logical expression components.

Cannot filter on metric_name . Does not support CASE or TERM directives. You also cannot use the WHERE clause to search for terms or phrases.

prestats

Syntax: prestats=true | false

Description: Specifies whether to use the prestats format. The prestats format is a Splunk internal format that is designed to be consumed by commands that generate aggregate calculations. When you use the prestats format, you can pipe the data into the chart , stats , or timechart commands, which are designed to accept the prestats format. When prestats is set to true , instructions with the AS clause are not relevant. The field names for the aggregates are determined by the command that consumes the prestats format and produces the aggregate output.

Default: false

&lt;span-length&gt;

Syntax: span=&lt;int&gt;&lt;timescale&gt; [every=&lt;int&gt;&lt;timescale&gt;]

Description: The span of each time bin. If used with a &lt;timescale&gt; , the &lt;span-length&gt; is treated as a time range. If not, this is an absolute bucket length. If you do not specify a &lt;span-length&gt; , the default is auto , which means that the number of time buckets adjusts to produce a reasonable number of results. For example, if seconds are used initially for the &lt;timescale&gt; and too many results are returned, the &lt;timescale&gt; is changed to a longer value, such as minutes, to return fewer time buckets.

To improve the performance of mstats searches you can optionally use the every argument in conjunction with span to cause the search to reduce the amount of data it samples per span. In other words you could design a search where the search head samples a span of only ten minutes of data for every hour covered by the search. See Span length options .

update_period

Syntax: update_period=&lt;integer&gt;

Description: Valid only with real-time searches. Specifies how frequently, in milliseconds, the real-time summary for the mstats command is updated. A larger number means less frequent updates to the summary and less impact on index processing.

Default: 1000 (1 second)


### Stats metric term options

&lt;stats-func&gt;

Syntax: &lt;stats-func&gt; | &lt;mstats-specific-func&gt; "("&lt;metric_name&gt;")" [AS &lt;string&gt;]...

Description: Perform statistical calculations on one or more metric_name fields. You can rename the result of each function using the AS clause, unless prestats is set to true . The metric_name must be enclosed in parenthesis.

When you use the &lt;stats-func&gt; syntax, the WHERE clause cannot filter on metric_name .

&lt;mstats-specific-func&gt;

Syntax: rate_avg | rate_sum

Description: Two functions that are specific to mstats . rate_avg computes the per metric time series rates for an accumulating counter metric and then returns the average of those rates. rate_sum does the same thing as rate_avg except that it returns the sum of the rates. For more about counter metrics and these functions see Investigate counter metrics in Metrics .

&lt;stats-func-value&gt;

Syntax: count(_value) | &lt;function&gt;(_value) [AS &lt;string&gt;] WHERE metric_name=&lt;metric_name&gt;

Description: Specify a basic count of the _value field or a function on the _value field. The _value field uses a specific format to store the numeric value of the metric. You can specify one or more functions. You can rename the result of the function using AS unless prestats=true .

When you use the &lt;stats-func-value&gt; syntax, the WHERE clause must filter on the metric_name . Wildcards are okay.


> **Note: The stats-func-value syntax does not support real-time searches . If you must run a real-time search, use the stats-func syntax instead.**


The following table lists the supported functions for the mstats command by type of function. Use the links in the table to see descriptions and examples for each function.


| Type of function | Supported functions and syntax |  |  |
| --- | --- | --- | --- |
| Aggregate functions | avg()count()max()median()min() | perc&lt;num&gt;range()stdev()stdevp() | sum()sumsq()upperperc&lt;num&gt;var()varp() |
| Time functions | earliest()earliest_time()latest() | latest_time()rate() | rate_avg()rate_sum() |


For an overview of using functions with commands, see Statistical and charting functions .


### Chart options

chart.limit

Syntax: chart.limit=(top | bottom)&lt;int&gt;

Description: Only valid when a column-split is specified. Use the chart.limit option to specify the number of results that should appear in the output. When you set chart.limit=N the top or bottom N values are retained, based on the sum of each series and the prefix you have selected. If chart.limit=0 , all results are returned. If you opt not to provide a top or bottom prefix before the chart.limit value, the Splunk software provides the top N results. For example, if you set chart.limit=10 the Splunk software defaults to providing the top 10 results.

This argument is identical to the limit argument of the chart and timechart commands.

Default: top10

chart.agg

Syntax: chart.agg=( &lt;stats-func&gt; ( &lt;evaled-field&gt; | &lt;wc-field&gt; ) [AS &lt;wc-field&gt;] )

Description: A statistical aggregation function. See the table of supported functions in Stats metric term options . The function can be applied to an eval expression, or to a field or set of fields. Use the AS clause to place the result into a new field with a name that you specify. You can use wild card characters in field names. This argument is identical to the agg argument of the chart and timechart commands.

Default: sum

chart.nullstr

Syntax: chart.nullstr=&lt;string&gt;

Description: If chart.usenull is true, this series is labeled by the value of the chart.nullstr option, and defaults to NULL. This argument is identical to the nullstr argument of the chart and timechart commands.

chart.otherstr

Syntax: chart.otherstr=&lt;string&gt;

Description: If chart.useother is true, this series is labeled by the value of the code.otherstr option, and defaults to OTHER. This argument is identical to the otherstr argument of the chart and timechart commands.

chart.usenull

Syntax: chart.usenull=&lt;bool&gt;

Description: Determines whether a series is created for events that do not contain the split-by field. This argument is identical to the usenull argument of the chart and timechart commands.

chart.useother

Syntax: chart.useother=&lt;bool&gt;

Description: Specifies whether a series should be added for data series not included in the graph because they did not meet the criteria of the WHERE clause. This argument is identical to the useother argument of the chart and timechart commands.


### Logical expression options

&lt;comparison-expression&gt;

Syntax: &lt;field&gt;&lt;comparison-operator&gt;&lt;value&gt; | &lt;field&gt; IN (&lt;value-list&gt;)

Description: Compares a field to a literal value or provides a list of values that can appear in the field.

&lt;search-modifier&gt;

Syntax: &lt;sourcetype-specifier&gt; | &lt;host-specifier&gt; | &lt;source-specifier&gt; | &lt;splunk_server-specifier&gt;

Description: Search for events from specified fields. For example, search for one or a combination of hosts, sources, and source types. See searching with default fields in the Knowledge Manager manual .

&lt;time-opts&gt;

Syntax: [&lt;timeformat&gt;] (&lt;time-modifier&gt;)\*

Description: Describes the format of the &lt;starttime&gt; and &lt;endtime&gt; terms of the search.


### Comparison expression options

&lt;comparison-operator&gt;

Syntax: = |  != | &lt; | &lt;= | &gt; | &gt;=

Description: Use comparison expressions when searching field-value pairs. Comparison expressions with the equal ( = ) or not equal ( != ) operator compare string values. For example, "1" does not match "1.0". Comparison expressions with greater than or less than operators &lt; &gt; &lt;= &gt;= numerically compare two numbers and lexicographically compare other values. See Usage .

&lt;field&gt;

Syntax: &lt;string&gt;

Description: The name of a field.

&lt;value&gt;

Syntax: &lt;literal-value&gt;

Description: In comparison expressions, this is the literal number or string value of a field.

&lt;value-list&gt;

Syntax: (&lt;literal-value&gt;, &lt;literal-value&gt;, ...)

Description: Used with the IN operator to specify two or more values. For example use error IN (400, 402, 404, 406) instead of error=400 OR error=402 OR error=404 OR error=406 .


### Search modifier options

&lt;sourcetype-specifier&gt;

Syntax: sourcetype=&lt;string&gt;

Description: Search for events from the specified sourcetype field.

&lt;host-specifier&gt;

Syntax: host=&lt;string&gt;

Description: Search for events from the specified host field.

&lt;source-specifier&gt;

Syntax: source=&lt;string&gt;

Description: Search for events from the specified source field.

&lt;splunk_server-specifier&gt;

Syntax: splunk_server=&lt;string&gt;

Description: Search for events from a specific server. Use "local" to refer to the search head.


### Span length options

every

Syntax : every=&lt;int&gt;&lt;timescale&gt;

Description : Use in conjunction with span to search data in discrete time intervals over the full timespan of a search. The every argument is valid only when span is set to a valid value other than auto . Set the every timespan to a value that is greater than the span timespan.

This method of "downsampling" the search data improves search performance at the expense of data granularity. For example, this search returns an average of the active_logins measurement for the first ten seconds of every twenty seconds covered by the time range of the search: | mstats avg(active_logins) span=10s every=20s


> **Note: Month intervals for every are exactly 30 days long. Year intervals for every are exactly 365 days long.**


&lt;timescale&gt;

Syntax: &lt;sec&gt; | &lt;min&gt; | &lt;hr&gt; | &lt;day&gt; | &lt;month&gt; | &lt;subseconds&gt;

Description: Time scale units.

Default: sec


| Time scale | Syntax | Description |
| --- | --- | --- |
| &lt;sec&gt; | s \| sec \| secs \| second \| seconds | Time scale in seconds. |
| &lt;min&gt; | m \| min \| mins \| minute \| minutes | Time scale in minutes. |
| &lt;hr&gt; | h \| hr \| hrs \| hour \| hours | Time scale in hours. |
| &lt;day&gt; | d \| day \| days | Time scale in days. |
| &lt;month&gt; | mon \| month \| months | Time scale in months. |
| &lt;subseconds&gt; | us \| ms \| cs \| ds | Time scale in microseconds (us), milliseconds (ms), centiseconds (cs), or deciseconds (ds) |



> **Note: mstats only supports subsecond timescales such as ms when it is searching metric indexes that are configured for millisecond timestamp resolution.**


For more information about enabling metrics indexes to index metric data points with millisecond timestamp precision, see:

- Manage Splunk Cloud Platform indexes in the Splunk Cloud Platform Admin Manual if you use Splunk Cloud Platform.

- Create custom indexes in Managing indexers and clusters of indexers if you use Splunk Enterprise.


### Time options

&lt;timeformat&gt;

Syntax: timeformat=&lt;string&gt;

Description: Set the time format for starttime and endtime terms.

Default: timeformat=%m/%d/%Y:%H:%M:%S.

For more about setting exact times with the available timeformat options, see Date and time format variables .

Subsecond options are only available if you are searching over a metrics index with millisecond timestamp resolution.

&lt;time-modifier&gt;

Syntax: starttime=&lt;string&gt; | endtime=&lt;string&gt; | earliest=&lt;time_modifier&gt; | latest=&lt;time_modifier&gt;

Description: Specify start and end times using relative or absolute time.


> **Note: You can also use the earliest and latest arguments to specify absolute and relative time ranges for your search.**


For more about the relative &lt;time_modifier&gt; syntax, see Time modifiers .

For more information about setting absolute time ranges see Date and time format variables . Subsecond options are only available if you are searching over a metrics index with millisecond timestamp resolution.

starttime

Syntax: starttime=&lt;string&gt;

Description: Events must be later or equal to this time. The starttime must match the timeformat .

endtime

Syntax: endtime=&lt;string&gt;

Description: All events must be earlier or equal to this time.


## Usage

The mstats command is a report-generating command , except when append=true . See Command types .

Generating commands use a leading pipe character and should be the first command in a search, except when append=true is specified with the command.

Use the mstats command to search metrics data. The metrics data uses a specific format for the metrics fields. See Metrics data format in Metrics .




> **Note: All metrics search commands are case sensitive. This means, for example, that mstats treats as the following as three distinct values of metric_name : cap.gear , CAP.GEAR , and Cap.Gear .**


mstats searches cannot return results for metric data points with metric_name fields that are empty or which contain blank spaces.


### Append mstats searches together

The mstats command does not support subsearches. You can use the append argument to add the results of an mstats search to the results of a preceding mstats search. See the topic on the tstats command for an append usage example.


### Aggregations

If you are using the &lt;stats-func&gt; syntax, numeric aggregations are only allowed on specific values of the metric_name field. The metric name must be enclosed in parenthesis. If there is no data for the specified metric_name in parenthesis, the search is still valid.

If you are using the &lt;stats-func-value&gt; syntax, numeric aggregations are only allowed on the _value field.

Aggregations are not allowed for values of any other field, including the _time field.




> **Note: When prestats = true and you run an mstats search that uses the c and count aggregation functions without an aggregation field, the Splunk software processes them as if they are actually count(_value) . In addition, any statistical functions that follow in the search string must reference the _value field. For example: | mstats count | timechart count(_value)**



### Wildcard characters

The mstats command supports wildcard characters in any search filter, with the following exceptions:

- You cannot use wildcard characters in the GROUP BY clause.

- If you are using the &lt;stats_func_value&gt; syntax, you cannot use wildcard characters in the _value field.

- If you are using wildcard characters in your aggregations and you are renaming them, your rename must have matching wildcards.

For example, this search is invalid:

CODE

Copy

| mstats sum(\*.free) as FreeSum


```spl

| mstats sum(*.free) as FreeSum

```


This search is valid:

CODE

Copy

| mstats sum(\*.free) as \*FreeSum


```spl

| mstats sum(*.free) as *FreeSum

```


- Real-time mstats searches cannot utilize wildcarded metric aggregations when you use the &lt;stats-func&gt; syntax.

For example, this search is invalid, when you set it up as a real-time search:

CODE

Copy

| mstats avg(cpu.\*) max(cpu.\*) where index=sysmetrics


```spl

| mstats avg(cpu.*) max(cpu.*) where index=sysmetrics

```


This real-time search is valid:

CODE

Copy

| mstats avg(cpu.sys) max(cpu.usr) where index=sysmetrics


```spl

| mstats avg(cpu.sys) max(cpu.usr) where index=sysmetrics

```



### WHERE clause

Use the WHERE clause to filter by any of the supported dimensions.

If you are using the &lt;stats-func&gt; syntax, the WHERE clause cannot filter by metric_name . Filtering by metric_name is performed based on the metric_name fields specified with the &lt;stats-func&gt; argument.

If you are using the &lt;stats-func-value&gt; syntax, the WHERE clause must filter by metric_name .

The WHERE clause is case-sensitive when it filters mstats results by field values. For example, these two searches return different result sets:

- CODE Copy | mstats max(df.used) as "Disk Utilization" WHERE (itsi_entity_type_nix_metrics_indexes) AND host=test | mstats max(df.used) as "Disk Utilization" WHERE (itsi_entity_type_nix_metrics_indexes) AND host=test

- CODE Copy | mstats max(df.used) as "Disk Utilization" WHERE (itsi_entity_type_nix_metrics_indexes) AND host=Test | mstats max(df.used) as "Disk Utilization" WHERE (itsi_entity_type_nix_metrics_indexes) AND host=Test

If you do not specify an index name in the WHERE clause, the mstats command returns results from the default metrics indexes associated with your role. If you do not specify an index name and you have no default metrics indexes associated with your role, mstats returns no results. To search against all metrics indexes use WHERE index=\* .

The WHERE clause must come before the BY or GROUPBY clause, if they are both used in conjunction with mstats .

For more information about defining default metrics indexes for a role, see Add and edit roles with Splunk Web in Securing Splunk Enterprise .


### Group results by metric name and dimension

You can group results by the metric_name and dimension fields.

You can also group by time. You must specify a timespan using the &lt;span-length&gt; argument to group by time buckets. For example, span=1hr or span=auto . The &lt;span-length&gt; argument is separate from the BY clause and can be placed at any point in the search between clauses.

Grouping by the _value or _time fields is not allowed.


### Group by metric time series

You can group results by metric time series . A metric time series is a set of metric data points that share the same metrics and the same dimension field-value pairs. Grouping by metric time series ensures that you are not mixing up data points from different metric data sources when you perform statistical calculations on them.

Use BY _timeseries to group by metric time series. The _timeseries field is internal and won't display in your results. If you want to display the _timeseries values in your search, add | rename _timeseries AS timeseries to the search.

For a detailed overview of the _timeseries field with examples, see Perform statistical calculations on metric time series in Metrics .


### Time dimensions

The mstats command does not recognize the following time-related dimensions.


| Unsupported dimensions |  |  |
| --- | --- | --- |
| date_hourdate_mdaydate_minutedate_monthdate_second | date_wdaydate_yeardate_zonemetric_timestamptime | timeendpostimestamptimestartpos |



### Subsecond bin time spans

You can only use subsecond span timescales, which are time spans that are made up of deciseconds (ds), centiseconds (cs), milliseconds (ms), or microseconds (us), for mstats searches over metrics indexes that have been configured to have millisecond timestamp resolution.

Subsecond span timescales should be numbers that divide evenly into a second. For example, 1s = 1000ms. This means that valid millisecond span values are 1, 2, 4, 5, 8, 10, 20, 25, 40, 50, 100, 125, 200, 250, or 500ms. In addition, span = 1000ms is not allowed. Use span = 1s instead.

For more information about giving indexes millisecond timestamp resolution:

- For Splunk Cloud Platform: See Manage Splunk Cloud Platform indexes in the Splunk Cloud Platform Admin Manual .

- For Splunk Enterprise: See Create custom indexes in Managing indexes and clusters of indexes .


### Search over a set of indexes with varying levels of timestamp resolution

If you run an mstats search over multiple metrics indexes with varying levels of timestamp resolution, the results of the search may contain results with timestamps of different resolutions.

For example, say you have two metrics indexes. Your "metrics-second" metrics index has a second timestamp resolution. Your "metrics-ms" metrics index has a millisecond timestamp resolution. You run the following search over both indexes: | mstats count(\*) WHERE index=metric\* span=100ms .

The search produces the following results:


| _time | count(cpu.nice) |
| --- | --- |
| 1549496110 | 48 |
| 1549496110.100 | 2 |


The 11549496110 row counts results from both indexes. The count from "metric-ms" includes only metric data points with timestamps from 1549496110.000 to 1549496110.099 . The "metric-ms" metric data points with timestamps from 1549496110.100 to 1549496110.199 appear in the 1549496110.100 row.

Meanwhile, the metric data points in the "metric-second" index do not have millisecond timestamp precision. The 1549496110 row only counts those "metric-second" metric data points with the 11549496110 timestamp, and no metric data points from "metric-second" are counted in the 1549496110.100 row.


### Time bin limits for mstats search jobs

Splunk software regulates mstats search jobs that use span or a similar method to group results by time. When Splunk software processes these jobs, it limits the number of "time bins" that can be allocated within a single .tsidx file.

For metrics indexes with second timestamp resolution, this only affects searches with large time ranges and very small time spans, such as a search over a year with span = 1s . If you are searching on a metrics index with millisecond timestamp resolution, you might encounter this limit over shorter ranges, such as a search over an hour with span = 1ms .

This limit is set by time_bin_limit in limits.conf , which is set to 1 million bins by default. If you need to run these kinds of mstats search jobs, lower this value if they are using too much memory per search. Raise this value if these kinds of search jobs are returning errors.

The Splunk platform estimates the number of time bins that a search requires by dividing the search time range by its group-by span. If this produces a number that is larger than the time_bin_limit , the Splunk platform returns an error.

The search time range is determined by the earliest and latest values of the search. Some kinds of searches, such as all-time searches, do not have earliest and latest . In such cases the Splunk platform checks within each single TSIDX file to derive a time range for the search.




> **Note: Metrics indexes have second timestamp resolution by default. You can give a metrics index a millisecond timestamp resolution when you create it, or you can edit an existing metrics index to switch it to millisecond timestamp resolution.**


If you use Splunk Cloud, see Manage Splunk Cloud Platform indexes in the Splunk Cloud Platform Admin Manual . If you use Splunk Enterprise, see Create custom indexes in Managing indexes and clusters of indexes .


### Memory and mstats search performance

A pair of limits.conf settings strike a balance between the performance of mstats searches and the amount of memory they use during the search process, in RAM and on disk. If your mstats searches are consistently slow to complete you can adjust these settings to improve their performance, but at the cost of increased search-time memory usage, which can lead to search failures.

If you use Splunk Cloud Platform, you will need to file a Support ticket to change these settings.

For more information, see Memory and stats search performance in the Search Manual .


### Lexicographical order

Lexicographical order sorts items based on the values used to encode the items in computer memory. In Splunk software, this is almost always UTF-8 encoding, which is a superset of ASCII.

- Numbers are sorted before letters. Numbers are sorted based on the first digit. For example, the numbers 10, 9, 70, 100 are sorted lexicographically as 10, 100, 70, 9.

- Uppercase letters are sorted before lowercase letters.

- Symbols are not standard. Some symbols are sorted before numeric values. Other symbols are sorted before or after letters.

You can specify a custom sort order that overrides the lexicographical order. See the blog Order Up! Custom Sort Orders .


## Examples


### 1. Calculate a single metric grouped by time

Return the average value of the aws.ec2.CPUUtilization metric in the mymetricdata metric index. Bucket the results into 30 second time spans.

CODE

Copy

| mstats avg(aws.ec2.CPUUtilization) WHERE index=mymetricdata span=30s


```spl

| mstats avg(aws.ec2.CPUUtilization) WHERE index=mymetricdata span=30s

```



### 2. Combine metrics with different metric names

Return the average value of both the aws.ec2.CPUUtilization metric and the os.cpu.utilization metric. Group the results by host and bucket the results into 1 minute time spans. Both metrics are combined and considered a single metric series.

CODE

Copy

| mstats avg(aws.ec2.CPUUtilization) avg(os.cpu.utilization) WHERE index=mymetricdata BY host span=1m


```spl

| mstats avg(aws.ec2.CPUUtilization) avg(os.cpu.utilization) WHERE index=mymetricdata BY host span=1m

```



### 3. Use chart=t mode to chart metric event counts by the top ten hosts

Return a chart of the number of aws.ec2.CPUUtilization metric data points for each day, split by the top ten hosts.

CODE

Copy

| mstats chart=t count(aws.ec2.CPUUtilization) WHERE index=mymetricdata by host span=1d chart.limit=top10


```spl

| mstats chart=t count(aws.ec2.CPUUtilization) WHERE index=mymetricdata by host span=1d chart.limit=top10

```



### 4. Filter the results on a dimension value and split by the values of another dimension

Return the average value of the aws.ec2.CPUUtilization metric for all measurements with host=www2 and split the results by the values of the app dimension.

CODE

Copy

| mstats avg(aws.ec2.CPUUtilization) WHERE host=www2 BY app


```spl

| mstats avg(aws.ec2.CPUUtilization) WHERE host=www2 BY app

```



### 5. Specify multiple aggregations of multiple metrics

Return the average and maximum of the resident set size and virtual memory size. Group the results by metric_name and bucket them into 1 minute spans

CODE

Copy

| mstats avg(os.mem.rss) AS "AverageRSS" max(os.mem.rss) AS "MaxRSS" avg(os.mem.vsz) AS "AverageVMS" max(os.mem.vsz) AS "MaxVMS" WHERE index=mymetricdata BY metric_name span=1m


```spl

| mstats avg(os.mem.rss) AS "AverageRSS" max(os.mem.rss) AS "MaxRSS" avg(os.mem.vsz) AS "AverageVMS" max(os.mem.vsz) AS "MaxVMS" WHERE index=mymetricdata BY metric_name span=1m

```



### 6. Aggregate a metric across all of your default metrics indexes, using downsampling to speed up the search

Find the median of the aws.ec2.CPUUtilization metric. Do not include an index filter to search for measurements in all of the default metrics indexes associated with your role. Speed up the search by using every to compute the median for one minute of every five minutes covered by the search.

CODE

Copy

| mstats median(aws.ec2.CPUUtilization) span=1m every=5m


```spl

| mstats median(aws.ec2.CPUUtilization) span=1m every=5m

```



### 7. Get the rate of an accumulating counter metric and group the results by time series

See Perform statistical calculations on metric time series in Metrics for more information.

CODE

Copy

| mstats rate(spl.intr.resource_usage.PerProcess.data.elapsed) as data.elapsed where index=_metrics BY _timeseries | rename _timeseries AS timeseries


```spl

| mstats rate(spl.intr.resource_usage.PerProcess.data.elapsed) as data.elapsed where index=_metrics BY _timeseries | rename _timeseries AS timeseries

```



### 8. Stats-func-value example

Use the &lt;stats-func-value&gt; syntax to get a count of all of the measurements for the aws.ec2.CPUUtilization metric in the mymetricdata index.

CODE

Copy

| mstats count(_value) WHERE metric_name=aws.ec2.CPUUtilization AND index=mymetricdata


```spl

| mstats count(_value) WHERE metric_name=aws.ec2.CPUUtilization AND index=mymetricdata

```



## See also

Related information

Overview of metrics in Metrics
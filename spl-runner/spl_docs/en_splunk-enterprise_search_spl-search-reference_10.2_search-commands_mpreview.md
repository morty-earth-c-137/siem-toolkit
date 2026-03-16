
# mpreview


## Description

Use mpreview to get an idea of the kinds of metric time series that are stored in your metrics indexes and to troubleshoot your metrics data.

mpreview returns a preview of the raw metric data points in a specified metric index that match a provided filter. By default, mpreview retrieves a target of five metric data points per metric time series from each metrics time-series index file ( .tsidx file) associated with the search. You can change this target amount with the target_per_timeseries argument.

By design, mpreview returns metric data points in JSON format.




> **Note: The mpreview command cannot search data that was indexed prior to your upgrade to the 8.0.x version of the Splunk platform.**


You can use the mpreview command only if your role has the run_msearch capability. See Define roles on the Splunk platform with capabilities in Securing Splunk Enterprise .




> **Note: Certain restricted search commands, including mpreview and mstats might stop working if your organization uses field filters to protect sensitive data. See Plan for field filters in your organization in Securing the Splunk Platform .**



## Syntax

The required syntax is in bold .

| mpreview

[filter=&lt;string&gt;]

[&lt;index-opt&gt;]...

[splunk_server=&lt;wc-string&gt;]

[splunk_server_group=&lt;wc-string&gt;]...

[earliest=&lt;time-specifier&gt;]

[latest=&lt;time-specifier&gt;] :

[chunk_size=&lt;unsigned-integer&gt;]

[target_per_timeseries=&lt;unsigned-integer&gt;]


### Required arguments

None. By default all types of terms are returned.


### Optional arguments

chunk_size

Syntax: chunk_size=&lt;unsigned-integer&gt;

Description: Advanced option. This argument controls how many metric time series are retrieved at a time from a single time-series index file ( .tsidx file) when the Splunk software processes searches. Lower this setting from its default only when you find a particular mpreview search is using too much memory, or when it infrequently returns events. This can happen when a search groups by excessively high-cardinality dimensions (dimensions with very large amounts of distinct values). In such situations, a lower chunk_size value can make mpreview searches more responsive, but potentially slower to complete. A higher chunk_size , on the other hand, can help long-running searches to complete faster, with the potential tradeoff of causing the search to be less responsive. For mpreview , chunk_size cannot be set lower than 10.

For more information about this setting, see Use chunk_size to regulate mpreview performance .

Default: 1000


> **Note: For Splunk Enterprise: The default value for the the chunk_size argument is set by the chunk_size setting for the [msearch] stanza in limits.conf .**


earliest

Syntax: earliest=&lt;time-specifier&gt;

Description: Specify the earliest _time for the time range of your search. You can specify the time in the following formats:

- Exact time (in ISO8601 format). For example, earliest="2023-09-05T11:52:43-05:00" or earliest="2023-09-05T11:52:43.123-05:00" .

- Relative time. For example, earliest=-h or earliest=@w0 .

- UNIX time. For example, earliest=1696812434 .

For more information about setting exact times see Date and time format variables . For more information about setting relative times, see Time modifiers . Subsecond options are available only if you are searching over a metrics index with millisecond timestamp resolution.

filter

Syntax: filter= "&lt;string&gt;"

Description: An arbitrary boolean expression over the dimension or metric_name .

index-opt

Syntax: index=&lt;index-name&gt; (index=&lt;index-name&gt;)...

Description: Limits the search to results from one or more indexes. You can use wildcard characters (\*). To match non-internal indexes, use index=\* . To match internal indexes, use index=_\* .

latest

Syntax: latest=&lt;time-specifier&gt;

Description: Specify the latest time for the _time range of your search. You can specify the time in the following formats:

- Exact time (in ISO8601 format). For example, latest="2023-09-12T11:52:43-05:00" or earliest="2023-09-12T11:52:43.123-05:00" .

- Relative time. For example, latest=-30m or latest=@w6 .

- UNIX time. For example, latest=1699490848 .

For more information about setting exact times see Date and time format variables . For more information about setting relative times, see Time modifiers . Subsecond options are available only if you are searching over a metrics index with millisecond timestamp resolution.

splunk_server

Syntax: splunk_server=&lt;wc-string&gt;

Description: Specifies the distributed search peer from which to return results. If you are using Splunk Enterprise, you can specify only one splunk_server argument. However, you can use a wildcard when you specify the server name to indicate multiple servers. For example, you can specify splunk_server=peer01 or splunk_server=peer\* . Use local to refer to the search head.

splunk_server_group

Syntax: splunk_server_group=&lt;wc-string&gt;

Description: Limits the results to one or more server groups. If you are using Splunk Cloud Platform, omit this parameter. You can specify a wildcard character in the string to indicate multiple server groups.

target_per_timeseries

Syntax: target_per_timeseries=&lt;unsigned-integer&gt;

Description Determines the target number of metric data points to retrieve per metric time series from each metrics time-series index file ( .tsidx file) associated with the mpreview search. If a time series has less than the target_per_timeseries of data points within a .tsidx file, the search head retrieves all of the data points for that time series within that particular .tsidx file.


> **CAUTION: If you set target_per_timeseries to 0 it returns all data points available within the given time range for each time series. This search will likely be very large in scale and therefore very slow to complete. If you must search on a large number of metric data points, use mstats instead.**


For more information about this setting, see How the target_per_timeseries argument works .

Default: 5


> **Note: The default value for the the target_per_timeseries argument is set by the target_per_timeseries setting for the [msearch] stanza in limits.conf**



## Usage

This search command generates a list of individual metric data points from a specified metric index that match a provided filter. The filter can be any arbitrary boolean expression over the dimensions or the metric_name . Specify earliest and latest to override the time range picker settings.

For more information about setting earliest and latest , see Time modifiers .

The mpreview command is designed to display individual metric data points in JSON format. If you want to aggregate metric data points, use the mstats command.


> **Note: All metrics search commands are case sensitive. This means, for example, that mpreview treats as the following as three distinct values of metric_name : cap.gear , CAP.GEAR , and Cap.Gear .**



### How the target_per_timeseries argument works

Unfiltered mpreview searches can cover extremely large numbers of raw metric data points. In some cases the sheer number of data points covered by the search can cause such searches to be slow or unresponsive.

The target_per_timeseries argument makes the mpreview command more responsive while giving you a relatively broad preview of your metric data. It limits the number of metric data points that mpreview can return from each metric time series in each .tsidx file covered by the search.

For example, if you have 10 metrics tsidx files that each contain 100 metric time series, and each time series has &gt;=5 data points. If you set target_per_timeseries=5 in the search, you should expect a maximum of 10 x 100 x 5 = 5000 metric data points to be returned by the search.

On the other hand, say you have 10 metrics tsidx files that each contain 100 metric time series, but in this case, 50 of those time series have 3 data points and the other 50 of those time series have &gt;=5 data points. If you set target_per_timeseries=5 in the search, you should expect to get 10 x ((50 x 3) + (50 x 5)) = 4000 data points.


> **Note: The target_per_timeseries argument is especially useful when the number of metric data points covered by your mpreview search is significantly larger than the number of metric time series covered by the search. It's not particularly helpful if the number of data points in your search are slightly larger than or equal to the number of metric time series in the search.**


You can run this search to determine the number of metric data points that could potentially be covered by an mpreview search:

CODE

Copy

| metadata index=&lt;metric_index_name&gt; type=hosts datatype=metric | fields totalCount


```spl

| metadata index=<metric_index_name> type=hosts datatype=metric | fields totalCount

```


You can run this search to determine the number of metric time series that could potentially be covered by an mpreview search:

CODE

Copy

| mstats count(\*) WHERE index=&lt;metric_index_name&gt;  by _timeseries | stats count


```spl

| mstats count(*) WHERE index=<metric_index_name>  by _timeseries | stats count

```



### Use chunk_size to regulate mpreview performance

If you find that mpreview is slow or unresponsive despite the target_per_timeseries argument you can also use chunk_size to regulate mpreview behavior. Reduce the chunk_size to make the search more responsive with the potential tradeoff of making the search slower to complete. Raise the chunk_size to help the mpreview search to complete faster, with the potential tradeoff of making it less responsive.


## Examples


### 1. Return data points that match a specific filter

This search returns individual data points from the _metrics index that match a specific filter.

CODE

Copy

| mpreview index=_metrics filter="group=queue name=indexqueue metric_name=\*.current_size"


```spl

| mpreview index=_metrics filter="group=queue name=indexqueue metric_name=*.current_size"

```


Here is an example of a JSON-formatted result of the above search.




### 2. Return individual data points from the metrics index

CODE

Copy

| mpreview index=_metrics


```spl

| mpreview index=_metrics

```



### 3. Lower chunk_size to improve mpreview performance

The following search lowers chunk_size so that it returns 100 metric time series worth of metric data points in batches from tsidx files that belong to the _metrics index. Ordinarily it would return 1000 metric time series in batches.

CODE

Copy

| mpreview index=_metrics chunk_size=100


```spl

| mpreview index=_metrics chunk_size=100

```



### 4. Speed up an mpreview search with target_per_timeseries

The following search uses target_per_timeseries to return a maximum of five metric data points per time series in each tsidx file searched in the _metrics index.

CODE

Copy

| mpreview index=_metrics target_per_timeseries=5


```spl

| mpreview index=_metrics target_per_timeseries=5

```



## See also

Commands

mcatalog

mcollect

mstats
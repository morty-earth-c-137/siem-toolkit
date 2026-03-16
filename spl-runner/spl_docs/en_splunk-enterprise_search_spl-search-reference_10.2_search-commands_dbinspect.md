
# dbinspect


## Description

Returns information about the buckets in the specified index. If you are using Splunk Enterprise, this command helps you understand where your data resides so you can optimize disk usage as required. Searches on an indexer cluster return results from the primary buckets and replicated copies on other peer nodes.

The Splunk index is the repository for data ingested by Splunk software. As incoming data is indexed and transformed into events , Splunk software creates files of rawdata and metadata ( index files ). The files reside in sets of directories organized by age. These directories are called buckets .

For more information, see Indexes, indexers, and clusters and How the indexer stores indexes in Managing Indexers and Clusters of Indexers .


## Syntax

The required syntax is in bold .

| dbinspect

[index=&lt;wc-string&gt;]...

[&lt;span&gt; | &lt;timeformat&gt;]

[corruptonly=&lt;bool&gt;]

[cached=&lt;bool&gt;]


### Required arguments

None.


### Optional arguments

index

Syntax: index=&lt;wc-string&gt;...

Description: Specifies the name of an index to inspect. You can specify more than one index. For all internal and non-internal indexes, you can specify an asterisk ( \* ) in the index name.

Default: The default index, which is typically main .

&lt;span&gt;

Syntax: span=&lt;int&gt; | span=&lt;int&gt;&lt;timescale&gt;

Description: Specifies the span length of the bucket. If using a timescale unit (second, minute, hour, day, month, or subseconds), this is used as a time range. If not, this is an absolute bucket "length".

When you invoke the dbinspect command with a bucket span, a table of the spans of each bucket is returned. When span is not specified, information about the buckets in the index is returned. See Information returned when no span is specified .

&lt;timeformat&gt;

Syntax: timeformat=&lt;string&gt;

Description: Sets the time format for the modTime field.

Default: timeformat=%m/%d/%Y:%H:%M:%S

&lt;corruptonly&gt;

Syntax: corruptonly=&lt;bool&gt;

Description: Specifies that each bucket is checked to determine if any buckets are corrupted and displays only the corrupted buckets. A bucket is corrupt when some of the files in the bucket are incorrect or missing such as Hosts.data or tsidx . A corrupt bucket might return incorrect data or render the bucket unsearchable. In most cases the software will auto-repair corrupt buckets.

When corruptonly=true , each bucket is checked and the following informational message appears.

Not supported on Splunk SmartStore indexes.

INFO: The "corruptonly" option will check each of the specified buckets. This search might be slow and will take time.

Default: false

cached

Syntax: cached=&lt;bool&gt;

Description: If set to cached=true , the dbinspect command gets the statistics from the bucket's manifest. If set to cached=false , the dbinspect command examines the bucket itself. For SmartStore buckets, cached=false examines an indexer's local copy of the bucket. However, specifying cached=true examines instead the bucket's manifest, which contains information about the canonical version of the bucket that resides in the remote store. For more information see Troubleshoot SmartStore in Managing Indexers and Clusters of Indexers .

Default: For non-SmartStore indexes, the default is false . For SmartStore indexes, the default is true .


### Time scale units

These are options for specifying a timescale as the bucket span.

&lt;timescale&gt;

Syntax: &lt;sec&gt; | &lt;min&gt; | &lt;hr&gt; | &lt;day&gt; | &lt;month&gt; | &lt;subseconds&gt;

Description: Time scale units.


| Time scale | Syntax | Description |
| --- | --- | --- |
| &lt;sec&gt; | s \| sec \| secs \| second \| seconds | Time scale in seconds. |
| &lt;min&gt; | m \| min \| mins \| minute \| minutes | Time scale in minutes. |
| &lt;hr&gt; | h \| hr \| hrs \| hour \| hours | Time scale in hours. |
| &lt;day&gt; | d \| day \| days | Time scale in days. |
| &lt;month&gt; | mon \| month \| months | Time scale in months. |
| &lt;subseconds&gt; | us \| ms \| cs \| ds | Time scale in microseconds (us), milliseconds (ms), centiseconds (cs), or deciseconds (ds) |



### Information returned when no span is specified

When you invoke the dbinspect command without the span argument, the following information about the buckets in the index is returned.


| Field name | Description |
| --- | --- |
| bucketId | A string comprised of&lt;index&gt;~&lt;id&gt;~&lt;guId&gt;, where the delimiters are tilde characters. For example,summary~2~4491025B-8E6D-48DA-A90E-89AC3CF2CE80. |
| endEpoch | The timestamp for the last event in the bucket, which is the time-edge of the bucket furthest towards the future. Specify the timestamp in the number of seconds from the UNIX epoch. |
| eventCount | The number of events in the bucket. |
| guId | The globally unique identifier (GUID) of the server that hosts the index. This is relevant for index replication. |
| hostCount | The number of unique hosts in the bucket. |
| id | The local ID number of the bucket, generated on the indexer on which the bucket originated. |
| index | The name of the index specified in your search. You can specifyindex=\*to inspect all of the indexes, and the index field will vary accordingly. |
| modTime | The timestamp for the last time the bucket was modified or updated, in a format specified by thetimeformatflag. |
| path | The location to the bucket. The naming convention for the bucketpathvaries slightly, depending on whether the bucket rolled to warm while its indexer was functioning as a cluster peer:For non-clustered buckets:db_&lt;newest_time&gt;_&lt;oldest_time&gt;_&lt;localid&gt;For clustered original bucket copies:db_&lt;newest_time&gt;_&lt;oldest_time&gt;_&lt;localid&gt;_&lt;guid&gt;For clustered replicated bucket copies:rb_&lt;newest_time&gt;_&lt;oldest_time&gt;_&lt;localid&gt;_&lt;guid&gt;For more information, read"How Splunk stores indexes"and"Basic cluster architecture"inManaging Indexers and Clusters of Indexers. |
| rawSize | The volume in bytes of the raw data files in each bucket. This value represents the volume before compression and the addition of index files. |
| sizeOnDiskMB | The size in MB of disk space that the bucket takes up expressed as a floating point number. This value represents the volume of the compressed raw data files and the index files. |
| sourceCount | The number of unique sources in the bucket. |
| sourceTypeCount | The number of unique sourcetypes in the bucket. |
| splunk_server | The name of the Splunk server that hosts the index in a distributed environment. |
| startEpoch | The timestamp for the first event in the bucket (the time-edge of the bucket furthest towards the past), in number of seconds from the UNIX epoch. |
| state | Specifies whether the bucket is warm, hot, cold. |
| tsidxState | Specifies whether each bucket contains full-size or reduced tsidx files. If the value of this field in the results isfull, the tsidx files are full-size. If the value ismini, the tsidx files are reduced. SeeDetermine whether a bucket is reducedin Splunk EnterpriseManaging Indexers and Clusters of Indexers. |
| corruptReason | Specifies the reason why the bucket is corrupt. The corruptReason field appears only whencorruptonly=true. |



## Usage

The dbinspect command is a generating command. See Command types .

Generating commands use a leading pipe character and should be the first command in a search.


### Accessing data and security

If no data is returned from the index that you specify with the dbinspect command, it is possible that you do not have the authorization to access that index. The ability to access data in the Splunk indexes is controlled by the authorizations given to each role. See Use access control to secure Splunk data in Securing Splunk Enterprise .


### Non-searchable bucket copies

For hot non-searchable bucket copies on target peers, tsidx and other metadata files are not maintained. Because accurate information cannot be reported, the following fields show NULL:

- eventCount

- hostCount

- sourceCount

- sourceTypeCount

- startEpoch

- endEpoch


## Examples


### 1. CLI use of the dbinspect command

Display a chart with the span size of 1 day, using the command line interface (CLI).

CODE

Copy

myLaptop $ splunk search "| dbinspect index=_internal span=1d"


```spl

myLaptop $ splunk search "| dbinspect index=_internal span=1d"

```


The results look like this:

CODE

Copy

_time            hot-3 warm-1 warm-2
--------------------------- ----- ------ ------
2015-01-17 00:00:00.000 PST            0       
2015-01-17 14:56:39.000 PST            0       
2015-02-19 00:00:00.000 PST            0      1
2015-02-20 00:00:00.000 PST     2             1


```spl

_time            hot-3 warm-1 warm-2
--------------------------- ----- ------ ------
2015-01-17 00:00:00.000 PST            0       
2015-01-17 14:56:39.000 PST            0       
2015-02-19 00:00:00.000 PST            0      1
2015-02-20 00:00:00.000 PST     2             1

```



### 2. Default dbinspect output

Default dbinspect output for a local _internal index.

CODE

Copy

| dbinspect index=_internal


```spl

| dbinspect index=_internal

```


The results look like this:



This screenshot does not display all of the columns in the output table. On your computer, scroll to the right to see the other columns.


### 3. Check for corrupt buckets

Use the corruptonly argument to display information about corrupted buckets, instead of information about all buckets. The output fields that display are the same with or without the corruptonly argument.

CODE

Copy

| dbinspect index=_internal corruptonly=true


```spl

| dbinspect index=_internal corruptonly=true

```



### 4. Count the number of buckets for each Splunk server

Use this command to verify that the Splunk servers in your distributed environment are included in the dbinspect command. Counts the number of buckets for each server.

CODE

Copy

| dbinspect index=_internal | stats count by splunk_server


```spl

| dbinspect index=_internal | stats count by splunk_server

```



### 5. Find the index size of buckets in GB

Use dbinspect to find the index size of buckets in GB. For current numbers, run this search over a recent time range.

CODE

Copy

| dbinspect index=_internal | eval GB=sizeOnDiskMB/1024| stats sum(GB)


```spl

| dbinspect index=_internal | eval GB=sizeOnDiskMB/1024| stats sum(GB)

```



### 6. Determine whether a bucket is reduced

Run the dbinspect search command:

CODE

Copy

| dbinspect index=_internal


```spl

| dbinspect index=_internal

```


If the value of the tsidxState field for each bucket is full , the tsidx files are full-size. If the value is mini , the tsidx files are reduced.
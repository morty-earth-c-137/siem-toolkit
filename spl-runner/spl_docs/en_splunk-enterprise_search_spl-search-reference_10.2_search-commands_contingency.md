
# contingency


## Description

In statistics, contingency tables are used to record and analyze the relationship between two or more (usually categorical) variables. Many metrics of association or independence, such as the phi coefficient or the Cramer's V , can be calculated based on contingency tables.

You can use the contingency command to build a contingency table, which in this case is a co-occurrence matrix for the values of two fields in your data. Each cell in the matrix displays the count of events in which both of the cross-tabulated field values exist. This means that the first row and column of this table is made up of values of the two fields. Each cell in the table contains a number that represents the count of events that contain the two values of the field in that row and column combination.

If a relationship or pattern exists between the two fields, you can spot it easily just by analyzing the information in the table. For example, if the column values vary significantly between rows (or vice versa), there is a contingency between the two fields (they are not independent). If there is no contingency, then the two fields are independent.


## Syntax

contingency [&lt;contingency-options&gt;...] &lt;field1&gt; &lt;field2&gt;


### Required arguments

&lt;field1&gt;

Syntax: &lt;field&gt;

Description: Any field. You cannot specify wildcard characters in the field name.

&lt;field2&gt;

Syntax: &lt;field&gt;

Description: Any field. You cannot specify wildcard characters in the field name.


### Optional arguments

contingency-options

Syntax: &lt;maxopts&gt; | &lt;mincover&gt; | &lt;usetotal&gt; | &lt;totalstr&gt;

Description: Options for the contingency table.


### Contingency options

maxopts

Syntax: maxrows=&lt;int&gt; | maxcols=&lt;int&gt;

Description: Specify the maximum number of rows or columns to display. If the number of distinct values of the field exceeds this maximum, the least common values are ignored. A value of 0 means a maximum limit on rows or columns. This limit comes from the maxvalues setting in the [ctable] stanza in the limits.conf file.

Default: 1000

mincover

Syntax: mincolcover=&lt;num&gt; | minrowcover=&lt;num&gt;

Description: Specify a percentage of values per column or row that you would like represented in the output table. As the table is constructed, enough rows or columns are included to reach this ratio of displayed values to total values for each row or column. The maximum rows or columns take precedence if those values are reached.

Default: 1.0

usetotal

Syntax: usetotal=&lt;bool&gt;

Description: Specify whether or not to add row, column, and complete totals.

Default: true

totalstr

Syntax: totalstr=&lt;field&gt;

Description: Field name for the totals row and column.

Default: TOTAL


## Usage

The contingency command is a transforming command. See Command types .

This command builds a contingency table for two fields. If you have fields with many values, you can restrict the number of rows and columns using the maxrows and maxcols arguments.


### Totals

By default, the contingency table displays the row totals, column totals, and a grand total for the counts of events that are represented in the table. If you don't want the totals to appear in the results, include the usetotal=false argument with the contingency command.


### Empty values

Values which are empty strings ("") will be represented in the results table as EMPTY_STR.


### Limits

There is a limit on the value of maxrows or maxcols , which means more than 1000 values for either field will not be used.


## Examples


### 1. Build a contingency table of recent data


| This search uses recent earthquake data downloaded from theUSGS Earthquakes website. The data is a comma separated ASCII text file that contains magnitude (mag), coordinates (latitude, longitude), region (place), etc., for each earthquake recorded.You can download a current CSV file from theUSGS Earthquake Feedsand upload the file to your Splunk instance. This example uses theAll Earthquakesdata from the past 30 days. Use the time rangeAll timewhen you run the searches. |
| --- |


You want to build a contingency table to look at the relationship between the magnitudes and depths of recent earthquakes. You start with a simple search.

CODE

Copy

source=all_month.csv | contingency mag depth | sort mag


```spl

source=all_month.csv | contingency mag depth | sort mag

```


There are quite a range of values for the Magnitude and Depth fields, which results in a very large table. The magnitude values appear in the first column. The depth values appear in the first row. The list is sorted by magnitude.

The results appear on the Statistics tab. The following table shows only a small portion of the table of results returned from the search.


| mag | 10 | 0 | 5 | 35 | 8 | 12 | 15 | 11.9 | 11.8 | 6.4 | 5.4 | 8.2 | 6.5 | 8.1 | 5.6 | 10.1 | 9 | 8.5 | 9.8 | 8.7 | 7.9 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| -0.81 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| -0.59 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| -0.56 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| -0.45 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| -0.43 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |


As you can see, earthquakes can have negative magnitudes. Only where an earthquake occurred that matches the magnitude and depth will a count appear in the table.

To build a more usable contingency table, you should reformat the values for the magnitude and depth fields. Group the magnitudes and depths into ranges.

CODE

Copy

source=all_month.csv  
| eval Magnitude=case(mag&lt;=1, "0.0 - 1.0", mag&gt;1 AND mag&lt;=2, "1.1 - 2.0", mag&gt;2 
  AND mag&lt;=3, "2.1 - 3.0", mag&gt;3 AND mag&lt;=4, "3.1 - 4.0", mag&gt;4 
  AND mag&lt;=5, "4.1 - 5.0", mag&gt;5 AND mag&lt;=6, "5.1 - 6.0", mag&gt;6 
  AND mag&lt;=7, "6.1 - 7.0", mag&gt;7,"7.0+") 
| eval Depth=case(depth&lt;=70, "Shallow", depth&gt;70 AND depth&lt;=300, "Mid", depth&gt;300 
  AND depth&lt;=700, "Deep") 
| contingency Magnitude Depth 
| sort Magnitude


```spl

source=all_month.csv  
| eval Magnitude=case(mag<=1, "0.0 - 1.0", mag>1 AND mag<=2, "1.1 - 2.0", mag>2 
  AND mag<=3, "2.1 - 3.0", mag>3 AND mag<=4, "3.1 - 4.0", mag>4 
  AND mag<=5, "4.1 - 5.0", mag>5 AND mag<=6, "5.1 - 6.0", mag>6 
  AND mag<=7, "6.1 - 7.0", mag>7,"7.0+") 
| eval Depth=case(depth<=70, "Shallow", depth>70 AND depth<=300, "Mid", depth>300 
  AND depth<=700, "Deep") 
| contingency Magnitude Depth 
| sort Magnitude

```


This search uses the eval command with the case() function to redefine the values of Magnitude and Depth, bucketing them into a range of values. For example, the Depth values are redefined as "Shallow", "Mid", or "Deep". Use the sort command to sort the results by magnitude. Otherwise the results are sorted by the row totals.

The results appear on the Statistics tab and look something like this:


| Magnitude | Shallow | Mid | Deep | TOTAL |
| --- | --- | --- | --- | --- |
| 0.0 - 1.0 | 3579 | 33 | 0 | 3612 |
| 1.1 - 2.0 | 3188 | 596 | 0 | 3784 |
| 2.1 - 3.0 | 1236 | 131 | 0 | 1367 |
| 3.1 - 4.0 | 320 | 63 | 1 | 384 |
| 4.1 - 5.0 | 400 | 157 | 43 | 600 |
| 5.1 - 6.0 | 63 | 12 | 3 | 78 |
| 6.1 - 7.0 | 2 | 2 | 1 | 5 |
| TOTAL | 8788 | 994 | 48 | 9830 |


There were a lot of quakes in this month. Do higher magnitude earthquakes have a greater depth than lower magnitude earthquakes? Not really. The table shows that the majority of the recent earthquakes in all of magnitude ranges were shallow. There are significantly fewer earthquakes in the mid-to-deep range. In this data set, the deep-focused quakes were all in the mid-range of magnitudes.


### 2. Identify potential component issues in the Splunk deployment

Determine if there are any components that might be causing issues in your Splunk deployment. Build a contingency table to see if there is a relationship between the values of log_level and component . Run the search using the time range All time and limit the number of columns returned.

CODE

Copy

index=_internal | contingency maxcols=5 log_level component


```spl

index=_internal | contingency maxcols=5 log_level component

```


Your results should appear something like this:



These results show you any components that might be causing issues in your Splunk deployment. The


```spl

component

```


field has more than 50 values. In this search, the


```spl

maxcols

```


argument is used to show 5 components with the highest values.




## See also

associate , correlate
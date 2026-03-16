
# join


## Description

You can use the join command to combine the results of a main search (left-side dataset) with the results of either another dataset or a subsearch (right-side dataset). You can also combine a search result set to itself using the selfjoin command.

The left-side dataset is the set of results from a search that is piped into the join command and then merged on the right side with the either a dataset or the results from a subsearch. The left-side dataset is sometimes referred to as the source data.

The following search example joins the source data from the search pipeline with a subsearch on the right side. Rows from each dataset are merged into a single row if the where predicate is satisfied.

CODE

Copy

&lt;left-dataset&gt; 
| join left=L right=R where L.pid = R.pid [subsearch]


```spl

<left-dataset> 
| join left=L right=R where L.pid = R.pid [subsearch]

```


A maximum of 50,000 rows in the right-side dataset can be joined with the left-side dataset over a maximum runtime of 60 seconds. These maximum defaults are set to limit the impact of the join command on performance and resource consumption.

If you are familiar with SQL but new to SPL, see Splunk SPL for SQL users .




## Alternative commands

For flexibility and performance, consider using one of the following commands if you do not require join semantics. These commands provide event grouping and correlations using time and geographic location, transactions, subsearches, field lookups, and joins.


| Command | Use |
| --- | --- |
| append | To append the results of a subsearch to the results of your current search. The events from both result sets are retained.Use only with historical data. Theappendcommand does not produce correct results if used in a real-time search.If you useappendto combine the events, use astatscommand to group the events in a meaningful way. You cannot use atransactioncommand after you use anappendcommand. |
| appendcols | Appends the fields of thesubsearchresults with the input search result fields. The first subsearch result is merged with the first main result, the second subsearch result is merged with the second main result, and so on. |
| lookup | Use when one of the result sets or source files remains static or rarely changes. For example, a file from an external system such as a CSV file.The lookup cannot be a subsearch. |
| search | In the most simple scenarios, you might need to search only for sources using the OR operator and then use astatsortransactioncommand to perform the grouping operation on the events. |
| stats | To group events by a field and perform a statistical function on the events. For example to determine the average duration of events by host name.To usestats, the field must have a unique identifier.To view the raw event data, use thetransactioncommand instead. |
| transaction | Usetransactionin the following situations.To group events by using theevalcommand with a conditional expression, such asif,case, ormatch.To group events by using a recycled field value, such as an ID or IP address.To group events by using a pattern, such as a start or end time for the event.To break up groups larger than a certain duration. For example, when a transaction does not explicitly end with a message and you want to specify a maximum span of time after the start of the transaction.To display the raw event data for the grouped events. |




For information about when to use a join, see the flowchart in

About event grouping and correlation

in the

Search Manual

.




## Syntax

The required syntax is in bold .

join

[&lt;join-options&gt;...]

[&lt;field-list&gt;] | [left=&lt;left-alias&gt;] [right=&lt;right-alias&gt;] where &lt;left-alias&gt;.&lt;field&gt;=&lt;right-alias&gt;.&lt;field&gt; [&lt;left-alias&gt;.&lt;field&gt;=&lt;right-alias&gt;.&lt;field&gt;]...

&lt;dataset-type&gt;:&lt;dataset-name&gt; | &lt;subsearch&gt;


### Required arguments

dataset-type

Syntax: datamodel | savedsearch | inputlookup

Description: The type of dataset that you want to use to join with the source data. The dataset must be a dataset that you created or are authorized to use. You can specify datamodel , savedsearch , or inputlookup . The dataset type must precede the dataset name. For example, savedsearch:&lt;dataset-name&gt; .

You can use either &lt;dataset-type&gt;:&lt;dataset-name&gt; or &lt;subsearch&gt; with the join command, but not both.

dataset-name

Syntax: &lt;dataset-name&gt;

Description: The name of the dataset that you want to use to join with the source data. The dataset must be a dataset that you created or are authorized to use. The dataset name must follow the dataset type. For example, if the dataset name is january and the dataset type is datamodel, you specify datamodel:january .

You can use either &lt;dataset-type&gt;:&lt;dataset-name&gt; or &lt;subsearch&gt; with the join command, but not both.

subsearch

Syntax: [&lt;subsearch&gt;]

Description: A secondary search or dataset that specifies the source of the events that you want to join to. The subsearch must be enclosed in square brackets. The results of the subsearch should not exceed available memory.

You can use either &lt;dataset-type&gt;:&lt;dataset-name&gt; or &lt;subsearch&gt; in a search, but not both. When [&lt;subsearch&gt;] is used in a search by itself with no join keys, the Splunk software autodetects common fields and combines the search results before the join command with the results of the subsearch.


### Optional arguments

join-options

Syntax: type=(inner | outer | left) | usetime=&lt;bool&gt; | earlier=&lt;bool&gt; | overwrite=&lt;bool&gt; | max=&lt;int&gt;

Description: Arguments to the join command. Use either outer or left to specify a left outer join. See Descriptions for the join-options argument in this topic.

field-list

Syntax: &lt;field&gt; &lt;field&gt; ...

Description: Specify the list of fields to use for the join. For example, to join fields ProductA , ProductB , and ProductC , you would specify | join ProductA ProductB ProductC... . If &lt;field-list&gt; is specified, one or more of the fields must be common to each dataset. If no fields are specified, all of the fields that are common to both datasets are used.

The values of the fields used in &lt;field-list&gt; are case sensitive. For example, a value that is all uppercase in the main search will not match the same value that is all lowercase in the subsearch. See the example later in this topic about performing a case-insensitive join .

left alias

Syntax: left=&lt;left-alias&gt;

Description: The alias to use with the left-side dataset, the source data, to avoid naming collisions. Must be combined with the right alias and where clause, or the alias is ignored.

The left alias must be used together with the right alias.

right alias

Syntax: right=&lt;right-alias&gt;

Description: The alias to use with the right-side dataset to avoid naming collisions. Must be combined with the left alias and the where clause, or the alias is ignored.

The right alias must be used together with the left alias.

where clause

Syntax: where &lt;left-alias&gt;.&lt;field&gt;=&lt;right-alias&gt;.&lt;field&gt;...

Description: Identifies the names of the fields in the left-side dataset and the right-side dataset that you want to join on. You must specify the left and right aliases and the field name. Fields that are joined from the left and right datasets do not have to have the same names. For example: where L.host=R.user matches events in the host field from the left dataset with events in the user field from the right dataset.

The where clause must be used with the right and left aliases and field name.

You can specify the aliases and fields in a where clause on either side of the equal sign. For example:

where &lt;left-alias&gt;.&lt;left-field&gt;=&lt;right-alias&gt;.&lt;right-field&gt;

or

where &lt;right-alias&gt;.&lt;right-field&gt;=&lt;left-alias&gt;.&lt;left-field&gt;


### Descriptions for the join-options argument

type

Syntax: type=inner | outer | left

Description: Indicates the type of join to perform. The difference between an inner and a left (or outer ) join is how the events are treated in the main search that do not match any of the events in the subsearch. In both inner and left joins, events that match are joined. The results of an inner join do not include events from the main search that have no matches in the subsearch. The results of a left (or outer ) join includes all of the events in the main search and only those values in the subsearch have matching field values.

Default: inner

usetime

Syntax: usetime=&lt;bool&gt;

Description: A Boolean value that Indicates whether to use time to limit the matches in the subsearch results. Used with the earlier option to limit the subsearch results to matches that are earlier or later than the main search results.

If you use the join command with usetime=true and type=left , the search results are similar to those of an inner join. This is because there might be non-matching results when using the left join that are the same as those produced by an inner join.

Default: false

earlier

Syntax: earlier=&lt;bool&gt;

Description: If usetime=true and earlier=true , the main search results are matched only against earlier results from the subsearch. If earlier=false , the main search results are matched only against later results from the subsearch. Results that occur at the same time (second) are not eliminated by either value.

Default: true

overwrite

Syntax: overwrite=&lt;bool&gt;

Description: If fields in the main search results and subsearch results have the same name, indicates whether fields from the subsearch results overwrite the fields from the main search results.

Default: true

max

Syntax: max=&lt;int&gt;

Description: Specifies the maximum number of subsearch results that each main search result can join with. If set to max=0 , there is no limit.

Default: 1


## Usage

The join command is a centralized streaming command when there is a defined set of fields to join to. Otherwise the command is a dataset processing command. See Command types .

A subsearch can be initiated through a search command such as the join command. See Initiating subsearches with search commands in the Splunk Cloud Platform Search Manual .


### Limitations on subsearches in joins

Use the join command when the results of the subsearch are relatively small, for example 50,000 rows or less. To minimize the impact of this command on performance and resource consumption, Splunk software imposes some default limitations on the subsearch.

Limitations on the subsearch for the join command are specified in the limits.conf file. The default limitations include a maximum of 50,000 rows in the subsearch to join against, and a maximum search time of 60 seconds for the subsearch. See Subsearches in the Search Manual .

Splunk Cloud Platform

To change the limits.conf settings subsearch_maxout or subsearch_maxtime , use one of the following methods:

- The Configure limits page in Splunk Web. For more information, see Configure limits using Splunk Web in the Splunk Cloud Platform Admin Manual .

- The Admin Config Service (ACS) API. For more information, see Manage limits.conf configurations in Splunk Cloud Platform in the Splunk Cloud Platform Admin Config Service Manual .

- The Admin Config Service (ACS) command line interface (CLI). For more information, see Administer Splunk Cloud Platform using the ACS CLI in the Splunk Cloud Platform Admin Config Service Manual .

Splunk Enterprise

To change the subsearch_maxout or subsearch_maxtime settings in your limits.conf file for join command subsearches, follow these steps.

Prerequisites

- Only users with file system access, such as system administrators, can edit configuration files.

- Review the steps in How to edit a configuration file in the Splunk Enterprise Admin Manual .


> **CAUTION: Never change or copy the configuration files in the default directory. The files in the default directory must remain intact and in their original location. Make changes to the files in the local directory.**


Steps

- Open or create a local limits.conf file at $SPLUNK_HOME/etc/system/local on the search head.

- Under the [join] stanza, add the line subsearch_maxout = &lt;value&gt; or subsearch_maxtime = &lt;value&gt; .


### One-to-many and many-to-many relationships

To return matches for one-to-many, many-to-one, or many-to-many relationships, include the max argument in your join syntax and set the value to 0. By default max=1 , which means that the subsearch returns only the first result from the subsearch. Setting the value to a higher number or to 0, which is unlimited, returns multiple results from the subsearch.


## Basic examples


### 1. A basic join

Combine the results from a main search with the results from a subsearch search vendors . The result sets are joined on the product_id field, which is common to both sources.

CODE

Copy

... | join product_id [search vendors]


```spl

... | join product_id [search vendors]

```



### 2. Returning all subsearch rows

By default, only the first row of the subsearch that matches a row of the main search is returned. To return all of the matching subsearch rows, include the max=&lt;int&gt; argument and set the value to 0. This argument joins each matching subsearch row with the corresponding main search row.

CODE

Copy

... | join product_id max=0 [search vendors]


```spl

... | join product_id max=0 [search vendors]

```



### 3. Join datasets on fields that have the same name

Combine the results from a search with the vendors dataset. The data is joined on the product_id field, which is common to both datasets.

CODE

Copy

... | join left=L right=R where L.product_id=R.product_id [search vendors]


```spl

... | join left=L right=R where L.product_id=R.product_id [search vendors]

```



### 4. Join datasets on fields that have different names

Combine the results from a search with the vendors dataset. The data is joined on a product ID field, which have different field names in each dataset. The field in the left-side dataset is product_id . The field in the right-side dataset is pid .

CODE

Copy

... | join left=L right=R where L.product_id=R.pid [search vendors]


```spl

... | join left=L right=R where L.product_id=R.pid [search vendors]

```



### 5. Use words instead of letters as aliases

You can use words for the aliases to help identify the datasets involved in the join. This example uses products and vendors for the aliases.

CODE

Copy

... | join left=products right=vendors where products.product_id=vendors.pid [search vendors]


```spl

... | join left=products right=vendors where products.product_id=vendors.pid [search vendors]

```



### 6. Perform a case-insensitive join

Say you want to join a field with values that have prefixes that use both upper and lower case letters. But, the &lt;field-list&gt; argument for the join command is case sensitive. To work around this limitation, you can make the case consistent before and after you perform the join by using the lower() or upper() evaluation function. In this example, the value for the myfield field is converted to lower case, which makes the case consistent for the join command.

CODE

Copy

... | eval myfield=lower(myfield) | join myfield [... | eval myfield=lower(myfield)]


```spl

... | eval myfield=lower(myfield) | join myfield [... | eval myfield=lower(myfield)]

```


See Evaluation functions .


## Extended examples


### 1. Specifying dataset aliases with a saved search dataset

This example joins each matching right-side dataset row with the corresponding source data row. This example uses products , which is a savedsearch type of dataset, for the right-side dataset. The field names in the left-side dataset and the right-side dataset are different. This search returns all of the matching rows in the left and right datasets by including max=0 in the search.

CODE

Copy

... | join max=0 left=L right=R where L.vendor_id=R.vid  savedsearch:products


```spl

... | join max=0 left=L right=R where L.vendor_id=R.vid  savedsearch:products

```



### 2. Use aliasing with commands following the join

Commands following the join can take advantage of the aliasing provided through the join command. For example, you can use the aliasing in another command like stats as shown in the following example.

CODE

Copy

... | join left=L right=R where L.product_id=R.pid [search vendors] | stats count by L.product_id


```spl

... | join left=L right=R where L.product_id=R.pid [search vendors] | stats count by L.product_id

```



### 3. Using a join to display resource usage information

The dashboards and alerts in the distributed management console shows you performance information about your Splunk deployment. The Resource Usage: Instance dashboard contains a table that shows the machine, number of cores, physical memory capacity, operating system, and CPU architecture.

To display the information in the table, use the following search. This search includes the join command. The search uses the information in the dmc_assets table to look up the instance name and machine name. The search then uses the serverName field to join the information with information from the /services/server/info REST endpoint. The /services/server/info is the URI path to the Splunk REST API endpoint that provides hardware and operating system information for the machine. The $splunk_server$ part of the search is a dashboard token variable.

CODE

Copy

| inputlookup dmc_assets 
| search serverName = $splunk_server$ 
| stats first(serverName) AS serverName, first(host) AS host, first(machine) AS machine
| join type=left serverName 
   [ | rest splunk_server=$splunk_server$ /services/server/info
   | fields serverName, numberOfCores, physicalMemoryMB, os_name, cpu_arch]
| fields machine numberOfCores physicalMemoryMB os_name cpu_arch 
| rename machine AS Machine, numberOfCores AS "Number of Cores", 
  physicalMemoryMB AS "Physical Memory Capacity (MB)", os_name AS "Operating System", 
  cpu_arch AS "CPU Architecture"


```spl

| inputlookup dmc_assets 
| search serverName = $splunk_server$ 
| stats first(serverName) AS serverName, first(host) AS host, first(machine) AS machine
| join type=left serverName 
   [ | rest splunk_server=$splunk_server$ /services/server/info
   | fields serverName, numberOfCores, physicalMemoryMB, os_name, cpu_arch]
| fields machine numberOfCores physicalMemoryMB os_name cpu_arch 
| rename machine AS Machine, numberOfCores AS "Number of Cores", 
  physicalMemoryMB AS "Physical Memory Capacity (MB)", os_name AS "Operating System", 
  cpu_arch AS "CPU Architecture"

```



## See also

selfjoin , append , set , appendcols
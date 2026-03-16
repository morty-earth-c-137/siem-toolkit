
# top


## Description

Finds the most common values for the fields in the field list. Calculates a count and a percentage of the frequency the values occur in the events. If the &lt;by-clause&gt; is included, the results are grouped by the field you specify in the &lt;by-clause&gt;.


## Syntax

top [&lt;N&gt;] [&lt;top-options&gt;...] &lt;field-list&gt; [&lt;by-clause&gt;]


### Required arguments

&lt;field-list&gt;

Syntax: &lt;field&gt;, &lt;field&gt;, ...

Description: Comma-delimited list of field names.


### Optional arguments

&lt;N&gt;

Syntax: &lt;int&gt;

Description: The number of results to return.

Default: 10

&lt;top-options&gt;

Syntax: countfield=&lt;string&gt; | limit=&lt;int&gt; | otherstr=&lt;string&gt; | percentfield=&lt;string&gt; | showcount=&lt;bool&gt; | showperc=&lt;bool&gt; | useother=&lt;bool&gt;

Description: Options for the top command. See Top options .

&lt;by-clause&gt;

Syntax: BY &lt;field-list&gt;

Description: The name of one or more fields to group by.


### Top options

countfield

Syntax: countfield=&lt;string&gt;

Description: For each value returned by the top command, the results also return a count of the events that have that value. This argument specifies the name of the field that contains the count. The count is returned by default. If you do not want to return the count of events, specify showcount=false .

Default: count

limit

Syntax: limit=&lt;int&gt;

Description: Specifies how many results to return. To return all values, specify zero ( 0 ). Specifying top limit=&lt;int&gt; is the same as specifying top N .

Default: 10

otherstr

Syntax: otherstr=&lt;string&gt;

Description: If useother=true , a row representing all other values is added to the results. Use otherstr=&lt;string&gt; to specify the name of the label for the row.

Default: OTHER

percentfield

Syntax: percentfield=&lt;string&gt;

Description: For each value returned by the top command, the results also return a percentage of the events that have that value. This argument specifies the name of the field that contains the percentage. The percentage is returned by default. If you do not want to return the percentage of events, specify showperc=false .

Default: percent

showcount

Syntax: showcount=&lt;bool&gt;

Description: Specify whether to create a field called "count" (see "countfield" option) with the count of that tuple.

Default: true

showperc

Syntax: showperc=&lt;bool&gt;

Description: Specify whether to create a field called "percent" (see "percentfield" option) with the relative prevalence of that tuple.

Default: true

useother

Syntax: useother=&lt;bool&gt;

Description: Specify whether or not to add a row that represents all values not included due to the limit cutoff.

Default : false


## Usage

The top command is a transforming command . See Command types .


### Default fields

When you use the top command, two fields are added to the results: count and percent .


| Field | Description |
| --- | --- |
| count | The number of events in your search results that contain the field values that are returned by the top command. See thecountfieldandshowcountarguments. |
| percent | The percentage of events in your search results that contain the field values that are returned by the top command. See thepercentfieldandshowpercarguments. |



### Default maximum number of results

By default the top command returns a maximum of 50,000 results. This maximum is controlled by the maxresultrows setting in the [top] stanza in the limits.conf file. Increasing this limit can result in more memory usage.




> **Note: Only users with file system access, such as system administrators, can edit the configuration files. Never change or copy the configuration files in the default directory. The files in the default directory must remain intact and in their original location. Make the changes in the local directory.**


See How to edit a configuration file .

If you have Splunk Cloud Platform, you need to file a Support ticket to change this limit.


### Lexicographic order of results

In searches that use the limit option with multiple sets of field lists, only the last lexicographical value of the &lt;field-list&gt; is returned in the search results. For example, in the following search, Orlando is the only location field that is returned because it's the last value when sorted lexicographically.

CODE

Copy

| makeresults
| eval location="Orlando Dallas Atlanta"
| makemv location
| mvexpand location
| eval user="Alex Kai Morgan"
| makemv user
| mvexpand user
| top limit=1 location by user


```spl

| makeresults
| eval location="Orlando Dallas Atlanta"
| makemv location
| mvexpand location
| eval user="Alex Kai Morgan"
| makemv user
| mvexpand user
| top limit=1 location by user

```


The search results look something like this.


| user | location | count | percent |
| --- | --- | --- | --- |
| Alex | Orlando | 1 | 33.333333 |
| Kai | Orlando | 1 | 33.333333 |
| Morgan | Orlando | 1 | 33.333333 |



## Examples


### Example 1: Return the 20 most common values for a field

This search returns the 20 most common values of the "referer" field. The results show the number of events (count) that have that a count of referer, and the percent that each referer is of the total number of events.

CODE

Copy

sourcetype=access_\* | top limit=20 referer


```spl

sourcetype=access_* | top limit=20 referer

```





### Example 2: Return top values for one field organized by another field

This search returns the top "action" values for each "referer_domain".

CODE

Copy

sourcetype=access_\* | top action by referer_domain


```spl

sourcetype=access_* | top action by referer_domain

```


Because a limit is not specified, this returns all the combinations of values for "action" and "referer_domain" as well as the counts and percentages:




### Example 3: Returns the top product purchased for each category


| This example uses the sample dataset fromthe Search Tutorialand a field lookup to add more information to the event data.Download the data set fromAdd data tutorialand follow the instructions to load the tutorial data.Download the CSV file fromUse field lookups tutorialand follow the instructions to set up the lookup definition to add price and productName to the events.After you configure the field lookup, you can run this search using the time range,All time. |
| --- |


This search returns the top product purchased for each category. Do not show the percent field. Rename the count field to "total".

CODE

Copy

sourcetype=access_\* status=200 action=purchase | top 1 productName by categoryId showperc=f countfield=total


```spl

sourcetype=access_* status=200 action=purchase | top 1 productName by categoryId showperc=f countfield=total

```





## See also

rare , sitop , stats
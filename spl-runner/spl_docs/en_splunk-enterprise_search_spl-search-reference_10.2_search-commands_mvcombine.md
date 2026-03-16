
# mvcombine


## Description

Takes a group of events that are identical except for the specified field, which contains a single value, and combines those events into a single event. The specified field becomes a multivalue field that contains all of the single values from the combined events.


> **Note: The mvcombine command does not apply to internal fields.**


See Use default fields in the Knowledge Manager Manual .


## Syntax

mvcombine [delim=&lt;string&gt;] &lt;field&gt;


### Required arguments

field

Syntax: &lt;field&gt;

Description: The name of a field to merge on, generating a multivalue field.


### Optional arguments

delim

Syntax: delim=&lt;string&gt;

Description: Defines the string to use as the delimiter for the values that get combined into the multivalue field. For example, if the values of your field are "1", "2", and "3", and delim is a semi-colon ( ; ), then the combined multivalue field is "1";"2";"3" .

Default : a single space, (" ")


> **Note: To see the output of the delim argument, you must use the nomv command immediately after the mvcombine command. See Usage**



## Usage

The mvcombine command is a transforming command . See Command types .

You can use evaluation functions and statistical functions on multivalue fields or to return multivalue fields.

The mvcombine command accepts a set of input results and finds groups of results where all field values are identical, except the specified field. All of these results are merged into a single result, where the specified field is now a multivalue field.

Because raw events have many fields that vary, this command is most useful after you reduce the set of available fields by using the fields command. The command is also useful for manipulating the results of certain transforming commands, like stats or timechart .


### Specifying delimiters

The mvcombine command creates a multivalue version of the field you specify, as well as a single value version of the field. The multivalue version is displayed by default.

The single value version of the field is a flat string that is separated by a space or by the delimiter that you specify with the delim argument.

By default the multivalue version of the field is displayed in the results. To display the single value version with the delimiters, add the | nomv command to the end of your search. For example ...| mvcombine delim= "," host | nomv host .

Some modes of search result investigation prefer this single value representation, such as exporting to CSV in the UI, or running a command line search with splunk search "..." -output csv . Some commands that are not multivalue aware might use this single value as well.

Most ways of accessing the search results prefer the multivalue representation, such as viewing the results in the UI, or exporting to JSON, requesting JSON from the command line search with splunk search "..." -output json or requesting JSON or XML from the REST API. For these forms of, the selected delim has no effect.


### Other ways of turning multivalue fields into single-value fields

If your primary goal is to convert a multivalue field into a single-value field, mvcombine is probably not your best option. mvcombine is mainly meant for the creation of new multivalue fields. Instead, try either the nomv command or the mvjoin eval function.


| Conversion option | Description | For more information |
| --- | --- | --- |
| nomvcommand | Use for simple multivalue field to single-value field conversions. Provide the name of a multivalue field in your search results andnomvwill convert each instance of the field into a single-value field. | nomv |
| mvjoinevalfunction | Use when you want to perform multivalue field to single-value field conversion where the former multivalues are separated by a delimiter that you supply. For example, you start with a multivalue field that contains the values1,2,3,4,5. You can usemvjointo transform your multivalue field into a single-valued field withORas the delimiter. The new single value of the field is1 OR 2 OR 3 OR 4 OR 5. | Multivalue eval functions |



## Examples


### 1. Creating a multivalue field


| This example uses the sample dataset fromthe Search Tutorial. To try this example yourself, download the data set fromGet the tutorial data into Splunkand follow the instructions in the Search Tutorial to upload the data. |
| --- |


To understand how mvcombine works, let's explore the data.

- Set the time range to All time .

- Run the following search. CODE Copy index=\* | stats max(bytes) AS max, min(bytes) AS min BY host index=\* | stats max(bytes) AS max, min(bytes) AS min BY host The results show that the max and min fields have duplicate entries for the hosts that start with www . The other hosts show no results for the max and min fields.

- To remove the other hosts from your results, modify the search to add host=www\* to the search criteria. CODE Copy index=\* host=www\* | stats max(bytes) AS max, min(bytes) AS min BY host index=\* host=www\* | stats max(bytes) AS max, min(bytes) AS min BY host Because the values in the max and min columns contain the exact same values, you can use the mvcombine to combine the host values into a multivalue result.

- Add | mvcombine host to your search and run the search again. CODE Copy index=\* host=www\* | stats max(bytes) AS max, min(bytes) AS min BY host | mvcombine host index=\* host=www\* | stats max(bytes) AS max, min(bytes) AS min BY host | mvcombine host Instead of three rows, one row is returned. The host field is now a multvalue field.


### 2. Returning the delimited values

As mentioned in the Usage section, by default the delimited version of the results are not returned in the output. To return the results with the delimiters, you must return the single value string version of the field.

Add the nomv command to your search. For example:

CODE

Copy

index=\* host=www\* | stats max(bytes) AS max, min(bytes) AS min BY host | mvcombine delim="," host | nomv host


```spl

index=* host=www* | stats max(bytes) AS max, min(bytes) AS min BY host | mvcombine delim="," host | nomv host

```




The search results that are returned are shown in the following table.




| host | max | min |
| --- | --- | --- |
| www1,www2,www3 | 4000 | 200 |


To return the results with a space after each comma, specify delim=", " .


### Example 3:

In multivalue events:

CODE

Copy

sourcetype="WMI:WinEventLog:Security" | fields EventCode, Category,RecordNumber | mvcombine delim="," RecordNumber | nomv RecordNumber


```spl

sourcetype="WMI:WinEventLog:Security" | fields EventCode, Category,RecordNumber | mvcombine delim="," RecordNumber | nomv RecordNumber

```



### Example 4:

Combine the values of "foo" with a colon delimiter.

CODE

Copy

... | mvcombine delim=":" foo


```spl

... | mvcombine delim=":" foo

```



## See also

Commands:

makemv

mvexpand

nomv



Functions:

Multivalue eval functions

Multivalue stats and chart functions

split



# format


## Description

This command is used implicitly by subsearches. This command takes the results of a subsearch , formats the results into a single result and places that result into a new field called search .

The format command performs similar functions as the return command.


## Syntax

The required syntax is in bold .

format

[mvsep="&lt;mv separator&gt;"]

[maxresults=&lt;int&gt;]

["&lt;row prefix&gt;" "&lt;column prefix&gt;" "&lt;column separator&gt;" "&lt;column end&gt;" "&lt;row separator&gt;" "&lt;row end&gt;"]

[emptystr="&lt;string&gt;"]

If you want to specify a row or column options, you must specify all of the row and column options.


### Required arguments

None.


### Optional arguments

mvsep

Syntax: mvsep="&lt;string&gt;"

Description: The separator to use for multivalue fields.

Default: OR

maxresults

Syntax: maxresults=&lt;int&gt;

Description: The maximum results to return.

Default: 0, which means no limitation on the number of results returned.

&lt;row prefix&gt;

Syntax: "&lt;string&gt;"

Description: The value to use for the row prefix.

Default: The open parenthesis character "("

&lt;column prefix&gt;

Syntax: "&lt;string&gt;"

Description: The value to use for the column prefix.

Default: The open parenthesis character "("

&lt;column separator&gt;

Syntax: "&lt;string&gt;"

Description: The value to use for the column separator.

Default: AND

&lt;column end&gt;

Syntax: "&lt;string&gt;"

Description: The value to use for the column end.

Default: The close parenthesis character ")"

&lt;row separator&gt;

Syntax: "&lt;string&gt;"

Description: The value to use for the row separator.

Default: OR

&lt;row end&gt;

Syntax: "&lt;string&gt;"

Description: The value to use for the column end.

Default: The close parenthesis character ")"

emptystr

Syntax: emptystr="&lt;string&gt;"

Description: The value that the format command outputs instead of the default empty string NOT( ) if the results generated up to that point are empty and no fields or values other than internal fields are returned. You can set this argument to a custom string that is displayed instead of the default empty string whenever your search results are empty.

Default: NOT( )


## Usage

By default, when you do not specify any of the optional row and column arguments, the output of the format command defaults to: "(" "(" "AND" ")" "OR" ")" .


### Specifying row and column arguments

There are several reasons to specify the row and column arguments:

Subsearches

There is an implicit format at the end of a subsearch that uses the default values for column and row arguments. For example, you can specify OR for the column separator by including the format command at the end of the subsearch.

Export the search to a different system

Specify the row and column arguments when you need to export the search to another system that requires different formatting.


## Examples


### 1. Example with no optional parameters

Suppose that you have results that look like this:


| source | sourcetype | host |
| --- | --- | --- |
| syslog.log | syslog | my_laptop |
| bob-syslog.log | syslog | bobs_laptop |
| laura-syslog.log | syslog | lauras_laptop |


The following search returns the top 2 results, and creates a search based on the host, source, and sourcetype fields. The default format settings are used.

CODE

Copy

... | head 2 | fields source, sourcetype, host | format


```spl

... | head 2 | fields source, sourcetype, host | format

```


This search returns the syntax for a search that is based on the field values in the top 2 results. The syntax is placed into a new field called search .


| source | sourcetype | host | search |
| --- | --- | --- | --- |
|  |  |  | ( ( host="mylaptop" AND source="syslog.log" AND sourcetype="syslog" ) OR ( host="bobslaptop" AND source="bob-syslog.log" AND sourcetype="syslog" ) ) |



### 2. Example using the optional parameters

You want to produce output that is formatted to use on an external system.

CODE

Copy

...  | format  "[" "[" "&&" "]" "||" "]"


```spl

...  | format  "[" "[" "&&" "]" "||" "]"

```


Using the data in Example 1, the result is:


| source | sourcetype | host | search |
| --- | --- | --- | --- |
|  |  |  | [ [ host="mylaptop" && source="syslog.log" && sourcetype="syslog" ] \| \| [ host="bobslaptop" && source="bob-syslog.log" && sourcetype="syslog" ] ] |



### 3. Multivalue separator example

The following search uses the eval command to create a field called "foo" that contains one value "eventtype,log_level". The makemv command is used to make the foo field a mulitvalue field and specifies the comma as the delimiter between the values. The search then outputs only the foo field and formats that field.

CODE

Copy

index=_internal |head 1 |eval foo="eventtype,log_level" | makemv delim="," foo | fields foo | format mvsep="mvseparator" "{" "[" "AND" "]" "AND" "}"


```spl

index=_internal |head 1 |eval foo="eventtype,log_level" | makemv delim="," foo | fields foo | format mvsep="mvseparator" "{" "[" "AND" "]" "AND" "}"

```


This results in the following output:


| foo | search |
| --- | --- |
|  | { [ ( foo="eventtype" mvseparator foo="log_level" ) ] } |



### 4. Use emptystr to indicate empty results

When a search generates empty results, the format command returns internal fields and the contents of emptystr . You can change the value of emptystr from the default to a custom string. For example, the results in the following search are empty, so format returns a customized string "Error Found" in a new field called search .

CODE

Copy

| makeresults count=1 | format emptystr="Error Found"


```spl

| makeresults count=1 | format emptystr="Error Found"

```


The results look something like this.


| search |
| --- |
| Error Found |


If your search doesn't include emptystr like the following example, the format command displays the default empty string to indicate that the results are empty.

CODE

Copy

| makeresults count=1 | format


```spl

| makeresults count=1 | format

```


The results look like this.


| search |
| --- |
| NOT ( ) |



### 5. Use emptystr in a subsearch as a failsafe

Customizing your empty string as shown in the last example is one way to use emptystr . However, it is more typical to use the format command as a subsearch that is operating as a search filter, and then use emptystr as a failsafe in case your search returns empty results. For example, perhaps your index isn't generating results because one of the fields you're specifying in the subsearch doesn't exist or there's a typo or some other error in your search. You can include the emptystr argument and set it to a default source type that you know is always present, such as splunkd . Then, instead of returning nothing, your search will return some results that you can use for further filtering.

You can use the following sample search to make sure you get results even if your search contains errors.

CODE

Copy

index=_internal sourcetype=
    [search index=does_not_exist | head 1 
    | fields sourcetype 
    | format emptystr="splunkd"]


```spl

index=_internal sourcetype=
    [search index=does_not_exist | head 1 
    | fields sourcetype 
    | format emptystr="splunkd"]

```


The results look something like this.


| i | Time | Event |
| --- | --- | --- |
| &gt; | 11/16/213:11:33.745 PM | 11-16-2021 15:11:33.745 -0800 INFO Metrics - group=thruput, name=thruput, instantaneous_kbps=4.984, instantaneous_eps=20.935, average_kbps=1.667, total_k_processed=182447.000, kb=154.505, ev=649host = PF32198Dsource = C:\Program Files\Splunk\var\log\splunk\metrics.logsourcetype = splunkd |
| &gt; | 11/16/213:11:33.745 PM | 11-16-2021 15:11:33.745 -0800 INFO Metrics - group=thruput, name=syslog_output, instantaneous_kbps=0.000, instantaneous_eps=0.000, average_kbps=0.000, total_k_processed=0.000, kb=0.000, ev=0 host = PF32198Dsource = C:\Program Files\Splunk\var\log\splunk\metrics.logsourcetype = splunkd |
| &gt; | 11/16/213:11:33.745 PM | 11-16-2021 15:11:33.745 -0800 INFO Metrics - group=thruput, name=index_thruput, instantaneous_kbps=4.971, instantaneous_eps=19.355, average_kbps=1.667, total_k_processed=182424.000, kb=154.094, ev=600 host = PF32198Dsource = C:\Program Files\Splunk\var\log\splunk\metrics.logsourcetype = splunkd |
| &gt; | 11/16/213:11:33.745 PM | 11-16-2021 15:11:33.745 -0800 INFO Metrics - group=queue, name=winparsing, max_size_kb=500, current_size_kb=0, current_size=0, largest_size=0, smallest_size=0 host = PF32198Dsource = C:\Program Files\Splunk\var\log\splunk\metrics.logsourcetype = splunkd |



## See also

search , return
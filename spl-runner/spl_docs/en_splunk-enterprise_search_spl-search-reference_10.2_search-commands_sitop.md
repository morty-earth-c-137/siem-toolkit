
# sitop

Summary indexing is a method you can use to speed up long-running searches that do not qualify for report acceleration, such as searches that use commands that are not streamable before the reporting command. For more information, see Overview of summary-based search acceleration and Use summary indexing for increased reporting efficiency in the Knowledge Manager Manual .


## Description

The sitop command is the summary indexing version of the top command, which returns the most frequent value of a field or combination of fields. The sitop command populates a summary index with the statistics necessary to generate a top report. After you populate the summary index, use the regular top command with the exact same search string as the sitop command search to report against it.


## Syntax

sitop [&lt;N&gt;] [&lt;top-options&gt;...] &lt;field-list&gt; [&lt;by-clause&gt;]


> Note: This is the exact same syntax as that of the top command.


### Required arguments

&lt;field-list&gt;

Syntax: &lt;field&gt;, ...

Description: Comma-delimited list of field names.


### Optional arguments

&lt;N&gt;

Syntax: &lt;int&gt;

Description: The number of results to return.

&lt;top-options&gt;

Syntax: countfield=&lt;string&gt; | limit=&lt;int&gt; | otherstr=&lt;string&gt; | percentfield=&lt;string&gt; | showcount=&lt;bool&gt; | showperc=&lt;bool&gt; | useother=&lt;bool&gt;

Description: Options for the sitop command. See Top options .

&lt;by-clause&gt;

Syntax: BY &lt;field-list&gt;

Description: The name of one or more fields to group by.


### Top options

countfield

Syntax: countfield=&lt;string&gt;

Description: The name of a new field that the value of count is written to.

Default: count

limit

Syntax: limit=&lt;int&gt;

Description: Specifies how many tuples to return, "0" returns all values.

Default: "10"

otherstr

Syntax: otherstr=&lt;string&gt;

Description: If useother is true, specify the value that is written into the row representing all other values.

Default: "OTHER"

percentfield

Syntax: percentfield=&lt;string&gt;

Description: Name of a new field to write the value of percentage.

Default: "percent"

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

Default: false


## Examples


### Example 1:

Compute the necessary information to later do 'top foo bar' on summary indexed results.

CODE

Copy

... | sitop foo bar


```spl

... | sitop foo bar

```



### Example 2:

Populate a summary index with the top source IP addresses in a scheduled search that runs daily:

CODE

Copy

eventtype=firewall | sitop src_ip


```spl

eventtype=firewall | sitop src_ip

```


Save the search as, "Summary - firewall top src_ip".

Later, when you want to retrieve that information and report on it, run this search over the past year:

CODE

Copy

index=summary search_name="summary - firewall top src_ip" |top src_ip


```spl

index=summary search_name="summary - firewall top src_ip" |top src_ip

```


Additionally, because this search specifies the search name, it filters out other data that have been placed in the summary index by other summary indexing searches.


## See also

collect , overlap , sichart , sirare , sistats , sitimechart
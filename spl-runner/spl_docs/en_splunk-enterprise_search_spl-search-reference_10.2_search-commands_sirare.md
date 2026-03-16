
# sirare

Summary indexing is a method you can use to speed up long-running searches that do not qualify for report acceleration, such as searches that use commands that are not streamable before the reporting command. For more information, see "About report accelleration and summary indexing" and "Use summary indexing for increased reporting efficiency" in the Knowledge Manager Manual .


## Description

The sirare command is the summary indexing version of the rare command, which returns the least common values of a field or combination of fields. The sirare command populates a summary index with the statistics necessary to generate a rare report. After you populate the summary index, use the regular rare command with the exact same search string as the rare command search to report against it.


## Syntax

sirare [&lt;top-options&gt;...] &lt;field-list&gt; [&lt;by-clause&gt;]


### Required arguments

&lt;field-list&gt;

Syntax: &lt;string&gt;,...

Description: Comma-delimited list of field names.


### Optional arguments

&lt;by-clause&gt;

Syntax: BY &lt;field-list&gt;

Description: The name of one or more fields to group by.

&lt;top-options&gt;

Syntax: countfield=&lt;string&gt; | limit=&lt;int&gt; | percentfield=&lt;string&gt; | showcount=&lt;bool&gt; | showperc=&lt;bool&gt;

Description: Options that specify the type and number of values to display. These are the same &lt;top-options&gt; used by the rare and top commands.


### Top options

countfield

Syntax: countfield=&lt;string&gt;

Description: Name of a new field to write the value of count.

Default: "count"

limit

Syntax: limit=&lt;int&gt;

Description: Specifies how many tuples to return, "0" returns all values.

percentfield

Syntax: percentfield=&lt;string&gt;

Description: Name of a new field to write the value of percentage.

Default: "percent"

showcount

Syntax: showcount=&lt;bool&gt;

Description: Specify whether to create a field called "count" (see "countfield" option) with the count of that tuple.

Default: true

showpercent

Syntax: showpercent=&lt;bool&gt;

Description: Specify whether to create a field called "percent" (see "percentfield" option) with the relative prevalence of that tuple.

Default: true


## Examples


### Example 1:

Compute the necessary information to later do 'rare foo bar' on summary indexed results.

CODE

Copy

... | sirare foo bar


```spl

... | sirare foo bar

```



## See also

collect , overlap , sichart , sistats , sitimechart , sitop
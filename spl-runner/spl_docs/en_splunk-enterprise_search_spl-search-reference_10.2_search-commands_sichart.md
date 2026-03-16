
# sichart

Summary indexing is a method you can use to speed up long-running searches that do not qualify for report acceleration, such as searches that use commands that are not streamable before the reporting command. For more information, see "About report accelleration and summary indexing" and "Use summary indexing for increased reporting efficiency" in the Knowledge Manager Manual .


## Description

The summary indexing version of the chart command. The sichart command populates a summary index with the statistics necessary to generate a chart visualization. For example, it can create a column, line, area, or pie chart. After you populate the summary index, you can use the chart command with the exact same search that you used with the sichart command to search against the summary index.


## Syntax

Required syntax is in bold .

sichart

[sep=&lt;string&gt;]

[format=&lt;string&gt;]

[cont=&lt;bool&gt;]

[limit=&lt;int&gt;]

[agg=&lt;stats-agg-term&gt;]

( &lt;stats-agg-term&gt; | &lt;sparkline-agg-term&gt; | "("&lt;eval-expression&gt;")" )...

[ BY &lt;field&gt; [&lt;bins-options&gt;... ] [&lt;split-by-clause&gt;] ] | [ OVER &lt;field&gt; [&lt;bins-options&gt;...] [BY &lt;split-by-clause&gt;] ]

For syntax descriptions, refer to the chart command.


## Usage


### Supported functions

You can use a wide range of functions with the sichart command. For general information about using functions, see Statistical and charting functions .

- For a list of functions by category, see Function list by category

- For an alphabetical list of functions, see Alphabetical list of functions


## Examples


### Example 1:

Compute the necessary information to later do 'chart avg(foo) by bar' on summary indexed results.

CODE

Copy

... | sichart avg(foo) by bar


```spl

... | sichart avg(foo) by bar

```



## See also

chart , collect , overlap , sirare , sistats , sitimechart , sitop
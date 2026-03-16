
# sitimechart

Summary indexing is a method you can use to speed up long-running searches that do not qualify for report acceleration, such as searches that use commands that are not streamable before the transforming command. For more information, see "About report accelleration and summary indexing" and "Use summary indexing for increased reporting efficiency" in the Knowledge Manager Manual .


## Description

The sitimechart command is the summary indexing version of the timechart command, which creates a time-series chart visualization with a corresponding table of statistics. The sitimechart command populates a summary index with the statistics necessary to generate a timechart report. After you use an sitimechart search to populate the summary index, use the regular timechart command with the exact same search string as the sitimechart search to report against the summary index.


## Syntax

The required syntax is in bold .

sitimechart

[sep=&lt;string&gt;]

[partial=&lt;bool&gt;]

[cont=&lt;bool&gt;]

[limit=&lt;int&gt;]

[agg=&lt;stats-agg-term&gt;]

[&lt;bin-options&gt;... ]

&lt;single-agg&gt; [BY &lt;split-by-clause&gt;] | &lt;eval-expression&gt; BY &lt;split-by-clause&gt;

When specifying sitimechart command arguments, either &lt;single-agg&gt; or &lt;eval-expression&gt; BY &lt;split-by-clause&gt; is required.

For descriptions of each of these arguments, see the timechart command .


## Usage


### Supported functions

You can use a wide range of functions with the sitimechart command. For general information about using functions, see Statistical and charting functions .

- For a list of functions by category, see Function list by category

- For an alphabetical list of functions, see Alphabetical list of functions


## Examples


### Example 1:

Use the collect command to populate a summary index called mysummary with the statistics about CPU usage organized by host,

CODE

Copy

... | sitimechart avg(cpu) BY host | collect index=mysummary


```spl

... | sitimechart avg(cpu) BY host | collect index=mysummary

```





> **Note: The collect command adds the results of a search to a summary index that you specify. You must create the summary index before you invoke the collect command.**


Then use the timechart command with the same search to generate a timechart report.

CODE

Copy

index=mysummary | timechart avg(cpu) BY host


```spl

index=mysummary | timechart avg(cpu) BY host

```



## See also

collect , overlap , sichart , sirare , sistats , sitop
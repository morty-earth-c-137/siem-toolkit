
# appendpipe


## Description

Appends the result of the subpipeline to the search results. Unlike a subsearch, the subpipeline is not run first. The subpipeline is run when the search reaches the appendpipe command. The appendpipe command is used to append the output of transforming commands , such as chart , timechart , stats , and top .


## Syntax

appendpipe [run_in_preview=&lt;bool&gt;] [&lt;subpipeline&gt;]


### Optional Arguments

run_in_preview

Syntax: run_in_preview=&lt;bool&gt;

Description: Specifies whether or not display the impact of the appendpipe command in the preview. When set to FALSE, the search runs and the preview shows the results as if the appendpipe command is not part of the search. However, when the search finishes, the results include the impact of the appendpipe command.

Default: True

subpipeline

Syntax: &lt;subpipeline&gt;

Description: A list of commands that are applied to the search results from the commands that occur in the search before the appendpipe command.


## Usage

The appendpipe command can be useful because it provides a summary, total, or otherwise descriptive row of the entire dataset when you are constructing a table or chart. This command is also useful when you need the original results for additional calculations.


## Examples


### Example 1:

Append subtotals for each action across all users.

CODE

Copy

index=_audit | stats count by action user | appendpipe [stats sum(count) as count by action | eval user = "TOTAL - ALL USERS"] | sort action


```spl

index=_audit | stats count by action user | appendpipe [stats sum(count) as count by action | eval user = "TOTAL - ALL USERS"] | sort action

```


The results appear on the Statistics tab and look something like this:


| action | user | count |
| --- | --- | --- |
| accelerate_search | admin | 209 |
| accelerate_search | buttercup | 345 |
| accelerate_search | can-delete | 6 |
| accelerate_search | TOTAL - ALL USERS | 560 |
| add | n/a | 1 |
| add | TOTAL - ALL USERS | 1 |
| change_authentication | admin | 50 |
| change_authentication | buttercup | 9 |
| change_authentication | can-delete | 24 |
| change_authentication | TOTAL - ALL USERS | 83 |



## See also

append , appendcols , join , set
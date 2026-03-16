
# reverse


## Description

Reverses the order of the results.

The reverse command does not affect which results are returned by the search, only the order in which the results are displayed. For the CLI, this includes any default or explicit maxout setting.




> **Note: On very large result sets, which means sets with millions of results or more, reverse command requires large amounts of temporary storage, I/O, and time.**



## Syntax

reverse


## Usage

The reverse command is a dataset processing command. See Command types .


## Examples


### Example 1:

Reverse the order of a result set.

CODE

Copy

... | reverse


```spl

... | reverse

```



## See also

Commands

head

sort

tail
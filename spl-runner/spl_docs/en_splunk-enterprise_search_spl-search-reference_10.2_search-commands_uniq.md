
# uniq


## Description

The uniq command works as a filter on the search results that you pass into it. This command removes any search result if that result is an exact duplicate of the previous result. This command does not take any arguments.




> **Note: We do not recommend running this command against a large dataset.**



## Syntax

uniq




## Examples


### Example 1:

Keep only unique results from all web traffic in the past hour.

CODE

Copy

eventtype=webtraffic earliest=-1h@s | uniq


```spl

eventtype=webtraffic earliest=-1h@s | uniq

```



## See also

dedup
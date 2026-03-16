
# tail


## Description

Returns the last N number of specified results. The events are returned in reverse order, starting at the end of the result set. The last 10 events are returned if no integer is specified


## Syntax

tail [&lt;N&gt;]


### Required arguments

None.


### Optional arguments

&lt;N&gt;

Syntax: &lt;int&gt;

Description: The number of results to return.

Default: 10


## Usage

The tail command is a dataset processing command. See Command types .


## Examples


### Example 1:

Return the last 20 results in reverse order.

CODE

Copy

... | tail 20


```spl

... | tail 20

```



## See also

head , reverse
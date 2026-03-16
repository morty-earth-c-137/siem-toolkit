
# findtypes


## Description

Generates suggested event types by taking the results of a search and producing a list of potential event types. At most, 5000 events are analyzed for discovering event types.


## Syntax

findtypes max=&lt;int&gt; [notcovered] [useraw]


### Required arguments

max

Datatype: &lt;int&gt;

Description: The maximum number of events to return.

Default : 10


### Optional arguments

notcovered

Description: If this keyword is used, the findtypes command returns only event types that are not already covered.

useraw

Description: If this keyword is used, the findtypes command uses phrases in the _raw text of events to generate event types.


## Examples


### Example 1:

Discover 10 common event types.

CODE

Copy

... | findtypes


```spl

... | findtypes

```



### Example 2:

Discover 50 common event types and add support for looking at text phrases.

CODE

Copy

... | findtypes max=50 useraw


```spl

... | findtypes max=50 useraw

```



## See also

typer
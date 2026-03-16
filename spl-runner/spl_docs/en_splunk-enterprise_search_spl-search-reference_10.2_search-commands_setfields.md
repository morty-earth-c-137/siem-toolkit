
# setfields


## Description

Sets the field values for all results to a common value.

Sets the value of the given fields to the specified values for each event in the result set. Delimit multiple definitions with commas. Missing fields are added, present fields are overwritten.

Whenever you need to change or define field values, you can use the more general purpose eval command. See usage of an eval expression to set the value of a field in Example 1.


## Syntax

setfields &lt;setfields-arg&gt;, ...


### Required arguments

&lt;setfields-arg&gt;

Syntax: string="&lt;string&gt;", ...

Description: A key-value pair, with the value quoted. If you specify multiple key-value pairs, separate each pair with a comma. Standard key cleaning is performed. This means all non-alphanumeric characters are replaced with '_' and leading '_' are removed.


## Examples


### Example 1:

Specify a value for the ip and foo fields.

CODE

Copy

... | setfields ip="10.10.10.10", foo="foo bar"


```spl

... | setfields ip="10.10.10.10", foo="foo bar"

```


To do this with the eval command:

CODE

Copy

... | eval ip="10.10.10.10" | eval foo="foo bar"


```spl

... | eval ip="10.10.10.10" | eval foo="foo bar"

```



## See also

eval , fillnull , rename
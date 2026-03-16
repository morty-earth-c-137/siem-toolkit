
# where


## Description

The where command uses eval-expressions to filter search results. These eval-expressions must be Boolean expressions, where the expression returns either true or false. The where command returns only the results for which the eval expression returns true.


## Syntax

where &lt;eval-expression&gt;


### Required arguments

eval-expression

Syntax: &lt;eval-mathematical-expression&gt; | &lt;eval-concatenate-expression&gt; | &lt;eval-comparison-expression&gt; | &lt;eval-boolean-expression&gt; | &lt;eval-function-call&gt;

Description: A combination of values, variables, operators, and functions that represent the value of your destination field. See Usage .

The &lt;eval-expression&gt; is case-sensitive. The syntax of the eval expression is checked before running the search, and an exception is thrown for an invalid expression.

The following table describes characteristics of eval expressions that require special handling.


| Expression characteristics | Description | Example |
| --- | --- | --- |
| Field names starting with numeric characters | If the expression references a field name that starts with a numeric character, the field name must be surrounded by single quotation marks. | '5minutes'="late"This expression is a field name equal to a string value. Because the field starts with a numeric it must be enclosed in single quotations. Because the value is a string, it must be enclosed in double quotations. |
| Field names with non-alphanumeric characters | If the expression references a field name that contains non-alphanumeric characters, the field name must be surrounded by single quotation marks. | new=count+'server-1'This expression could be interpreted as a mathematical equation, where the dash is interpreted as a minus sign. To avoid this, you must enclose the field nameserver-1in single quotation marks. |
| Literal strings | If the expression references a literal string, the literal string must be surrounded by double quotation marks. | new="server-"+countThere are two issues with this example. First,server-could be interpreted as a field name or as part of a mathematical equation, that uses a minus sign and a plus sign. To ensure thatserver-is interpreted as a literal string, enclose the string in double quotation marks. |



## Usage

The where command is a distributable streaming command. See Command types .

The &lt;eval-expression&gt; is case-sensitive.

The where command uses the same expression syntax as the eval command. Also, both commands interpret quoted strings as literals. If the string is not quoted, it is treated as a field name. Because of this, you can use the where command to compare two different fields, which you cannot use the search command to do.


| Command | Example | Description |
| --- | --- | --- |
| Where | CODECopy... \| where ipaddress=clientip... \| where ipaddress=clientip | This search looks for events where the fieldipaddressis equal to the fieldclientip. |
| Search | CODECopy\| search host=www2\| search host=www2 | This search looks for events where the fieldhostcontains the string valuewww2. |
| Where | CODECopy... \| where host="www2"... \| where host="www2" | This search looks for events where the value in the fieldhostis the string valuewww2. |





### Boolean expressions

The order in which Boolean expressions are evaluated with the where command is:

- Expressions within parentheses

- NOT clauses

- AND clauses

- OR clauses

- XOR clauses

This evaluation order is different than the order used with the search command, which evaluates OR before AND clauses, and doesn't support XOR.

See Boolean expressions with logical operators in the Splunk platform Search Manual .


### Using a wildcard with the where command

You can only specify a wildcard by using the like function with the where command. The percent ( % ) symbol is the wildcard that you use with the like function. See the like() evaluation function.


### Supported functions

You can use a wide range of evaluation functions with the where command. For general information about using functions, see Evaluation functions .

- For a list of functions by category, see Function list by category .

- For an alphabetical list of functions, see Alphabetical list of functions .


## Examples


### 1. Specify a wildcard with the where command

You can only specify a wildcard with the where command by using the like function. The percent ( % ) symbol is the wildcard you must use with the like function. The where command returns like=TRUE if the ipaddress field starts with the value 198. .

CODE

Copy

... | where like(ipaddress, "198.%")


```spl

... | where like(ipaddress, "198.%")

```



### 2. Match IP addresses or a subnet using the where command

Return "CheckPoint" events that match the IP or is in the specified subnet.

CODE

Copy

host="CheckPoint" | where like(src, "10.9.165.%") OR cidrmatch("10.9.165.0/25", dst)


```spl

host="CheckPoint" | where like(src, "10.9.165.%") OR cidrmatch("10.9.165.0/25", dst)

```



### 3. Specify a calculation in the where command expression

Return "physicsjobs" events with a speed is greater than 100.

CODE

Copy

sourcetype=physicsjobs | where distance/time &gt; 100


```spl

sourcetype=physicsjobs | where distance/time > 100

```



## See also

eval , search , regex
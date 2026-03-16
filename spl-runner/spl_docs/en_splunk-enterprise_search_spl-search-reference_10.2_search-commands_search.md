
# search


## Description

Use the search command to retrieve events from indexes or filter the results of a previous search command in the pipeline. You can retrieve events from your indexes, using keywords, quoted phrases, wildcards, and field-value expressions. The search command is implied at the beginning of any search. You do not need to specify the search command at the beginning of your search criteria.

You can also use the search command later in the search pipeline to filter the results from the previous command in the pipeline.

The search command can also be used in a subsearch. See about subsearches in the Search Manual .

After you retrieve events , you can apply commands to transform, filter, and report on the events. Use the vertical bar ( | ) , or pipe character, to apply a command to the retrieved events.

The search command supports IPv4 and IPv6 addresses and subnets that use CIDR notation.


## Syntax

search &lt;logical-expression&gt;


### Required arguments

&lt;expression&gt;

Syntax: &lt;logical-expression&gt; | &lt;time-opts&gt; | &lt;search-modifier&gt; | NOT &lt;logical-expression&gt; | &lt;index-expression&gt; | &lt;comparison-expression&gt; | &lt;logical-expression&gt; [OR] &lt;logical-expression&gt;

Description: Includes all keywords or field-value pairs used to describe the events to retrieve from the index. Include parenthesis as necessary. Use Boolean expressions, comparison operators, time modifiers, search modifiers, or combinations of expressions for this argument.

The AND operator is always implied between terms and expressions. For example, web error is the same as web AND error . Specifying clientip=192.0.2.255 earliest=-1h@h is the same as clientip=192.0.2.255 AND earliest=-1h@h . So unless you want to include it for clarity reasons, you do not need to specify the AND operator.


### Logical expression options

&lt;comparison-expression&gt;

Syntax: &lt;field&gt;&lt;comparison-operator&gt;&lt;value&gt; | &lt;field&gt; IN (&lt;value-list&gt;)

Description: Compare a field to a literal value or provide a list of values that can appear in the field.

&lt;index-expression&gt;

Syntax: "&lt;string&gt;" | &lt;term&gt; | &lt;search-modifier&gt;

Description: Describe the events you want to retrieve from the index using literal strings and search modifiers.

&lt;time-opts&gt;

Syntax: [&lt;timeformat&gt;] (&lt;time-modifier&gt;)...

Description: Describe the format of the starttime and endtime terms of the search. See Time options .


### Comparison expression options

&lt;comparison-operator&gt;

Syntax: = |  != | &lt; | &lt;= | &gt; | &gt;=

Description: You can use comparison operators when searching field/value pairs. Comparison expressions with the equal ( = ) or not equal ( != ) operator compare string values. For example, "1" does not match "1.0". Comparison expressions with greater than or less than operators &lt; &gt; &lt;= &gt;= numerically compare two numbers and lexicographically compare other values. See Usage .

&lt;field&gt;

Syntax: &lt;string&gt;

Description: The name of a field.

&lt;value&gt;

Syntax: &lt;literal-value&gt;

Description: In comparison-expressions, the literal number or string value of a field.

&lt;value-list&gt;

Syntax: (&lt;literal-value&gt;, &lt;literal-value&gt;, ...)

Description: Used with the IN operator to filter events by specifying two or more values. For example use error IN (400, 402, 404, 500) instead of error=400 OR error=402 OR error=404 OR error=500 . You can also use a wildcard character ( \* ) to specify values that are similar, such as error IN (40\*) .

See the "Multiple field-value comparisons with the IN operator" section in Usage .


### Index expression options

&lt;string&gt;

Syntax: "&lt;string&gt;"

Description: Specify keywords or quoted phrases to match. When searching for strings and quoted strings (anything that's not a search modifier), Splunk software searches the _raw field for the matching events or results.

&lt;search-modifier&gt;

Syntax: &lt;sourcetype-specifier&gt; | &lt;host-specifier&gt; | &lt;hosttag-specifier&gt; | &lt;source-specifier&gt; | &lt;savedsplunk-specifier&gt; | &lt;eventtype-specifier&gt; | &lt;eventtypetag-specifier&gt; | &lt;splunk_server-specifier&gt;

Description:

Search for events from specified fields or field tags. For example, search for one or a combination of hosts, sources, source types, saved searches, and event types. Also, search for the field tag, with the format:


```spl

tag::<field>=<string>

```


.

- Read more about searching with default fields in the Knowledge Manager manual .

- Read more about using tags and field aliases in the Knowledge Manager manual .

&lt;sourcetype-specifier&gt;

Syntax: sourcetype=&lt;string&gt;

Description: Search for events from the specified sourcetype field.

&lt;host-specifier&gt;

Syntax: host=&lt;string&gt;

Description: Search for events from the specified host field.

&lt;hosttag-specifier&gt;

Syntax: hosttag=&lt;string&gt;

Description: Search for events that have hosts that are tagged by the string.

&lt;eventtype-specifier&gt;

Syntax: eventtype=&lt;string&gt;

Description: Search for events that match the specified event type.

&lt;eventtypetag-specifier&gt;

Syntax: eventtypetag=&lt;string&gt;

Description: Search for events that would match all eventtypes tagged by the string.

&lt;savedsplunk-specifier&gt;

Syntax: savedsearch=&lt;string&gt; | savedsplunk=&lt;string&gt;

Description: Search for events that would be found by the specified saved search.

&lt;source-specifier&gt;

Syntax: source=&lt;string&gt;

Description: Search for events from the specified source field.

&lt;splunk_server-specifier&gt;

Syntax: splunk_server=&lt;string&gt;

Description: Search for events from a specific server. Use "local" to refer to the search head.


### Time options

For a list of time modifiers, see Time modifiers for search .

&lt;timeformat&gt;

Syntax: timeformat=&lt;string&gt;

Description: Set the time format for starttime and endtime terms.

Default: timeformat=%m/%d/%Y:%H:%M:%S.

&lt;time-modifier&gt;

Syntax: starttime=&lt;string&gt; | endtime=&lt;string&gt; | earliest=&lt;time_modifier&gt; | latest=&lt;time_modifier&gt;

Description: Specify start and end times using relative or absolute time.


> **Note: You can also use the earliest and latest attributes to specify absolute and relative time ranges for your search. For more about this time modifier syntax, see Specify time modifiers in your search in the Search Manual.**


starttime

Syntax: starttime=&lt;string&gt;

Description: Events must be later or equal to this time. Must match timeformat .

endtime

Syntax: endtime=&lt;string&gt;

Description: All events must be earlier or equal to this time.


## Usage

The search command is an event-generating command when it is the first command in the search, before the first pipe. When the search command is used further down the pipeline, it is a distributable streaming command . See Command types .

A subsearch can be initiated through a search command such as the search command. See Initiating subsearches with search commands in the Splunk Cloud Platform Search Manual .


### The implied search command

The search command is implied at the beginning of every search.

When search is the first command in the search, you can use terms such as keywords, phrases, fields, boolean expressions, and comparison expressions to specify exactly which events you want to retrieve from Splunk indexes. If you don't specify a field, the search looks for the terms in the the _raw field.

Some examples of search terms are:

- keywords: error login , which is the same as specifying for error AND login

- quoted phrases: "database error"

- boolean operators: login NOT (error OR fail)

- wildcards: fail\*

- field-value pairs: status=404, status!=404, or status&gt;200




> **Note: To search field values that are SPL operators or keywords, such as country=IN , country=AS , iso=AND , or state=OR , you must enclose the operator or keyword in quotation marks. For example: country="IN" .**


See Use the search command in the Search Manual .


### Using the search command later in the search pipeline

In addition to the implied search command at the beginning of all searches, you can use the search command later in the search pipeline. The search terms that you can use depend on which fields are passed into the search command.

If the _raw field is passed into the search command, you can use the same types of search terms as you can when the search command is the first command in a search.

However, if the _raw field is not passed into the search command, you must specify field-values pairs that match the fields passed into the search command. Transforming commands, such as stats and chart , do not pass the _raw field to the next command in the pipeline.


### Boolean expressions

The order in which Boolean expressions are evaluated with the search command is:

- Expressions within parentheses

- NOT clauses

- OR clauses

- AND clauses

This evaluation order is different than the order used with the eval and where commands, which evaluate AND before OR clauses. The search command doesn't support XOR.

See Boolean expressions with logical operators in the Splunk platform Search Manual .


### Comparing two fields

To compare two fields, do not specify index=myindex fieldA=fieldB or index=myindex fieldA!=fieldB with the search command. When specifying a comparison_expression, the search command expects a &lt;field&gt; compared with a &lt;value&gt;. The search command interprets fieldB as the value, and not as the name of a field.

Use the where command to compare two fields.

CODE

Copy

index=myindex | where fieldA=fieldB


```spl

index=myindex | where fieldA=fieldB

```




For not equal comparisons, you can specify the criteria in several ways.



CODE

Copy

index=myindex | where fieldA!=fieldB


```spl

index=myindex | where fieldA!=fieldB

```


or

CODE

Copy

index=myindex | where NOT fieldA=fieldB


```spl

index=myindex | where NOT fieldA=fieldB

```




See

Difference between NOT and !=

in the

Search Manual

.




### Filter using the IN operator

Use the IN operator when you want to determine if a field contains one of several values.

For example, use this syntax:

CODE

Copy

... error_code IN (400, 402, 404, 500) | ...


```spl

... error_code IN (400, 402, 404, 500) | ...

```


Instead of this syntax:

CODE

Copy

... error_code=400 OR error_code=402 OR error_code=404 OR error_code=500 | ...


```spl

... error_code=400 OR error_code=402 OR error_code=404 OR error_code=500 | ...

```


When used with the search command, you can use a wildcard character ( \* ) in the list of values for the IN operator. For example:

CODE

Copy

... error_code IN (40\*, 500) | ...


```spl

... error_code IN (40*, 500) | ...

```


You can use the NOT operator with the IN operator. For example:

CODE

Copy

... NOT clientip IN (211.166.11.101, 182.236.164.11, 128.241.220.82) | ...


```spl

... NOT clientip IN (211.166.11.101, 182.236.164.11, 128.241.220.82) | ...

```


There is also an IN function that you can use with the eval and where commands. Wild card characters are not allowed in the values list when the IN function is used with the eval and where commands. See Comparison and Conditional functions .


### CIDR matching

The search command can perform a CIDR match on a field that contains IPv4 and IPv6 addresses.

Suppose the ip field contains these values:

10.10.10.12

50.10.10.17

10.10.10.23

If you specify ip="10.10.10.0/24" , the search returns the events with the first and last values: 10.10.10.12 and 10.10.10.23.


### Lexicographical order

Lexicographical order sorts items based on the values used to encode the items in computer memory. In Splunk software, this is almost always UTF-8 encoding, which is a superset of ASCII.

- Numbers are sorted before letters. Numbers are sorted based on the first digit. For example, the numbers 10, 9, 70, 100 are sorted lexicographically as 10, 100, 70, 9.

- Uppercase letters are sorted before lowercase letters.

- Symbols are not standard. Some symbols are sorted before numeric values. Other symbols are sorted before or after letters.

You can specify a custom sort order that overrides the lexicographical order. See the blog Order Up! Custom Sort Orders .


### Quotes and escaping characters

In general, you need quotation marks around phrases and field values that include white spaces, commas, pipes, quotations, and brackets. Quotation marks must be balanced. An opening quotation must be followed by an unescaped closing quotation. For example:

- A search such as error | stats count will find the number of events containing the string error.

- A search such as ... | search "error | stats count" would return the raw events containing error, a pipe, stats, and count, in that order.

Additionally, use quotation marks around keywords and phrases if you don't want to search for their default meaning, such as Boolean operators and field/value pairs. For example:

- A search for the keyword AND without meaning the Boolean operator: error "AND"

- A search for this field/value phrase: error "startswith=foo"



The backslash character (&nbsp\&nbsp) is used to escape quotes, pipes, and the backslash character itself. Backslash escape sequences are expanded inside quotation marks. For example:



- The sequence \| as part of a search sends a pipe character to the command, instead of using the pipe as a split between commands.

- The sequence \" sends a literal quotation mark to the command. For example, this is useful if you want to search for a literal quotation mark or insert a literal quotation mark into a field using regular expressions.

- The \\ sequence sends a literal backslash to the command.



Unrecognized backslash sequences are not altered:



- For example, \s in a search string is available as \s to the command, because \s is not a known escape sequence.

- However, the search string \\s is available as \s to the command, because \\ is a known escape sequence that is converted to \ .

See Backslashes in the Search Manual .


### Search with TERM()

You can use the TERM() directive to force Splunk software to match whatever is inside the parentheses as a single term in the index. TERM is more useful when the term contains minor segmenters, such as periods, and is bounded by major segmenters, such as spaces or commas. In fact, TERM does not work for terms that are not bounded by major breakers.

See Use CASE and TERM to match phrases in the Search Manual .


### Search with CASE()

You can use the CASE() directive to search for terms and field values that are case-sensitive.

See Use CASE and TERM to match phrases in the Search Manual .


## Examples

These examples demonstrate how to use the search command. You can find more examples in the Start Searching topic of the Search Tutorial .


### 1. Field-value pair matching

This example demonstrates field-value pair matching for specific values of source IP (src) and destination IP (dst).

CODE

Copy

src="10.9.165.\*" OR dst="10.9.165.8"


```spl

src="10.9.165.*" OR dst="10.9.165.8"

```



### 2. Using boolean and comparison operators

This example demonstrates field-value pair matching with boolean and comparison operators. Search for events with code values of either 10 or 29, and any host that isn't "localhost", and an xqp value that is greater than 5.

CODE

Copy

(code=10 OR code=29) host!="localhost" xqp&gt;5


```spl

(code=10 OR code=29) host!="localhost" xqp>5

```


In this example you could also use the IN operator since you are specifying two field-value pairs on the same field. The revised search is:

CODE

Copy

code IN(10, 29) host!="localhost" xqp&gt;5


```spl

code IN(10, 29) host!="localhost" xqp>5

```



### 3. Using wildcards

This example demonstrates field-value pair matching with wildcards. Search for events from all the web servers that have an HTTP client or server error status.

CODE

Copy

host=webserver\* (status=4\* OR status=5\*)


```spl

host=webserver* (status=4* OR status=5*)

```


In this example you could also use the IN operator since you are specifying two field-value pairs on the same field. The revised search is:

CODE

Copy

host=webserver\* status IN(4\*, 5\*)


```spl

host=webserver* status IN(4*, 5*)

```



### 4. Using the IN operator

This example shows how to use the IN operator to specify a list of field-value pair matchings. In the events from an access.log file, search the action field for the values addtocart or purchase .

CODE

Copy

sourcetype=access_combined_wcookie action IN (addtocart, purchase)


```spl

sourcetype=access_combined_wcookie action IN (addtocart, purchase)

```



### 5. Specifying a secondary search

This example uses the search command twice. The search command is implied at the beginning of every search with the criteria eventtype=web-traffic . The search command is used again later in the search pipeline to filter out the results. This search defines a web session using the transaction command and searches for the user sessions that contain more than three events.

CODE

Copy

eventtype=web-traffic | transaction clientip startswith="login" endswith="logout" | search eventcount&gt;3


```spl

eventtype=web-traffic | transaction clientip startswith="login" endswith="logout" | search eventcount>3

```



### 6. Using the NOT or != comparisons

Searching with the boolean "NOT"comparison operator is not the same as using the "!=" comparison.

The following search returns everything except fieldA="value2", including all other fields.

CODE

Copy

NOT fieldA="value2"


```spl

NOT fieldA="value2"

```


The following search returns events where fieldA exists and does not have the value "value2".

CODE

Copy

fieldA!="value2"


```spl

fieldA!="value2"

```


If you use a wildcard for the value, NOT fieldA=\* returns events where fieldA is null or undefined, and fieldA!=\* never returns any events.

See Difference between NOT and != in the Search Manual .


### 7. Using search to perform CIDR matching

You can use the search command to match IPv4 and IPv6 addresses and subnets that use CIDR notation. For example, this search identifies whether the specified IPv4 address is located in the subnet.

CODE

Copy

| makeresults 
| eval ip="192.0.2.56" 
| search ip="192.0.2.0/24"


```spl

| makeresults 
| eval ip="192.0.2.56" 
| search ip="192.0.2.0/24"

```


The IP address is located in the subnet, so search displays it in the search results, which look like this.


| time | ip |
| --- | --- |
| 2020-11-19 16:43:31 | 192.0.2.56 |


Note that you can get identical results using the eval command with the cidrmatch("X",Y) function, as shown in this example.

CODE

Copy

| makeresults 
| eval ip="192.0.2.56" 
| where cidrmatch("192.0.2.0/24", ip)


```spl

| makeresults 
| eval ip="192.0.2.56" 
| where cidrmatch("192.0.2.0/24", ip)

```


Alternatively, if you're using IPv6 addresses, you can use the search command to identify whether the specified IPv6 address is located in the subnet.

CODE

Copy

| makeresults 
| eval ip="2001:0db8:ffff:ffff:ffff:ffff:ffff:ff99"
| search ip="2001:0db8:ffff:ffff:ffff:ffff:ffff:ff00/120"


```spl

| makeresults 
| eval ip="2001:0db8:ffff:ffff:ffff:ffff:ffff:ff99"
| search ip="2001:0db8:ffff:ffff:ffff:ffff:ffff:ff00/120"

```


The IP address is in the subnet, so the search results look like this.


| time | ip |
| --- | --- |
| 2020-11-19 16:43:31 | 2001:0db8:ffff:ffff:ffff:ffff:ffff:ff99 |



### See also

Commands

iplocation

lookup

Functions

cidrmatch
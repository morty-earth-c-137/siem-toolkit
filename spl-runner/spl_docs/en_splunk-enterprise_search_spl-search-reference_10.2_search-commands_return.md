
# return


## Description

Use the return command to return values from a subsearch. return replaces the incoming events with one event, with one attribute: "search". To improve performance, the return command automatically limits the number of incoming results with the head command and the resulting fields with the fields command.

By default, the return command uses only the first row of results. Use the count argument to specify the number of results to use.


## Syntax

return [&lt;count&gt;] [&lt;alias&gt;=&lt;field&gt;...] [&lt;field&gt;...] [$&lt;field&gt;...]


### Required arguments

None.


### Optional arguments

&lt;count&gt;

Syntax: &lt;int&gt;

Description: Specify the number of rows.

Default: 1, which is the first row of results passed into the command.

&lt;alias&gt;

Syntax: &lt;alias&gt;=&lt;field&gt;...

Description: Specify the field alias and value to return. You can specify multiple pairs of aliases and values, separated by spaces. The &lt;alias&gt; argument does not support spaces before and after the '=' sign.

&lt;field&gt;

Syntax: &lt;field&gt;...

Description: Specify one or more fields to return, separated by spaces.

&lt;$field&gt;

Syntax: &lt;$field&gt;

Description: Specify one or more field values to return, separated by spaces.


## Usage

The command is convenient for outputting a field name, an alias-value pair, or just a field value.


| Output | Example |
| --- | --- |
| Field name | return source |
| Alias=value | return ip=srcip |
| Value | return $srcip |


By default, the return command uses only the first row of results. You can specify multiple rows, for example ' return 2 ip '. Each row is viewed as an OR clause, that is, output might be ' (ip=10.1.11.2) OR (ip=10.2.12.3) '. Multiple values can be specified and are placed within OR clauses. So, ' return 2 user ip ' might output ' (user=bob ip=10.1.11.2) OR (user=fred ip=10.2.12.3) '.

In most cases, using the return command at the end of a subsearch removes the need for head , fields , rename , format , and dedup .


### Duplicate values

Suppose you have the following search:

CODE

Copy

sourcetype=WinEventLog:Security | return 2 user


```spl

sourcetype=WinEventLog:Security | return 2 user

```


You might logically expect the command to return the first two distinct users. Instead the command looks at the first two events, based on the ordering from the implied head command. The return command returns the users within those two events. The command does not determine if the user value is unique. If the same user is listed in these events, the command returns only the one user.

To return unique values, you need to include the dedup command in your search. For example:

CODE

Copy

sourcetype=WinEventLog:Security | dedup user | return 2 user


```spl

sourcetype=WinEventLog:Security | dedup user | return 2 user

```



### When the input for 'return' is 0 events

When the input to the return command is 0 events, the results of the search can be misleading. To avoid this, test your subsearches outside of the main search to verify that they return events.

For example, say you have the following search:

CODE

Copy

index=B [index=A test_error | return clientip]


```spl

index=B [index=A test_error | return clientip]

```


If index=A test_errror returns 0 events, the subsearch returns an empty string. The final result of the full search is all events from index=B . If you are unaware of the result of the subsearch, this could lead you to believe that all events from index=B satisfied the condition of having test_error for their clientip , when in fact none did.


### Quotations in returned fields

The return command does not escape quotation marks that are in the fields that are returned. You must use an eval command to escape the quotation marks before you use the return command. For example:

CODE

Copy

...[search eval field2=replace(field1,"\"","\\\"") | return field2]


```spl

...[search eval field2=replace(field1,"\"","\\\"") | return field2]

```



### If you encounter problems with the return command

If you encounter difficulties when running the return command, consider running the oldreturn command instead. oldreturn is a deprecated version of return that does not require spaces around the = symbol for the alias argument. The tradeoff is that oldreturn searches complete slower than return searches.


## Examples


### Example 1:

Search for ' error ip=&lt;someip&gt; ', where &lt;someip&gt; is the most recent ip used by user 'boss'.

CODE

Copy

error [ search user=boss | return ip ]


```spl

error [ search user=boss | return ip ]

```



### Example 2:

Search for ' error (user=user1 ip=ip1) OR (user=user2 ip=ip2) ', where the users and IPs come from the two most-recent logins.

CODE

Copy

error [ search login | return 2 user ip ]


```spl

error [ search login | return 2 user ip ]

```



### Example 3:

Return to eval the userid of the last user, and increment it by 1.

CODE

Copy

... | eval nextid = 1 + [ search user=\* | return $id ] | ...


```spl

... | eval nextid = 1 + [ search user=* | return $id ] | ...

```



## See also

format , search
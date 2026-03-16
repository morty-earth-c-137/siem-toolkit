
# Understanding SPL syntax

The following sections describe the syntax used for the Splunk SPL commands . For additional information about using keywords, phrases, wildcards, and regular expressions, see Search command primer .


## Required and optional arguments

SPL commands consist of required and optional arguments.

- Required arguments are shown in angle brackets &lt; &gt;.

- Optional arguments are enclosed in square brackets [ ].

Consider this command syntax:

bin [&lt;bins-options&gt;...] &lt;field&gt; [AS &lt;newfield&gt;]

The required argument is &lt;field&gt; . To use this command, at a minimum you must specify bin &lt;field&gt; .

The optional arguments are [&lt;bins-options&gt;...] and [AS &lt;newfield&gt;] .


## User input arguments

Consider this command syntax:

replace (&lt;wc-string&gt; WITH &lt;wc-string&gt;)... [IN &lt;field-list&gt;]

The user input arguments are: &lt;wc-string&gt; and &lt;field-list&gt; . The argument &lt;wc-string&gt; is an abbreviation for &lt;wildcard-string&gt; and indicates that the argument accepts a wildcard character in the string that you provide. See Wildcards in the Search Reference .


## Repeating arguments

Some arguments can be specified multiple times. The syntax displays ellipsis ... to specify which part of an argument can be repeated. The ellipsis always appear immediately after the part of the syntax that you can repeat.

Consider this command:

convert [timeformat=string] (&lt;convert-function&gt; [AS &lt;field&gt;])...

The required argument is &lt;convert-function&gt; , with an option to specify a field with the [AS &lt;field&gt;] clause.

Notice the ellipsis at the end of the syntax, just after the close parenthesis. In this example, the syntax that is inside the parenthesis can be repeated &lt;convert-function&gt; [AS &lt;field&gt;] .

In the following syntax, you can repeat the &lt;bins-options&gt;... .

bin [&lt;bins-options&gt;...] &lt;field&gt; [AS &lt;newfield&gt;]


## Grouped arguments

Sometimes the syntax must display arguments as a group to show that the set of arguments are used together. Parenthesis ( ) are used to group arguments.

For example in this syntax:

replace (&lt;wc-string&gt; WITH &lt;wc-string&gt;)... [IN &lt;field-list&gt;]

The grouped argument is (&lt;wc-string&gt; WITH &lt;wc-string&gt;)... . This is a required set of arguments that you can repeat multiple times.


## Keywords

Many commands use keywords with some of the arguments or options. Examples of keywords include:

- AS

- BY

- OVER

- WHERE



You can specify these keywords in uppercase or lowercase in your search. However, for readability, the syntax in the Splunk documentation uses uppercase on all keywords.




## Quoted elements

If an element is in quotation marks, you must include that element in your search. The most common quoted elements are parenthesis.

Consider the syntax for the chart command:

CODE

Copy

chart [&lt;chart-options&gt;] [agg=&lt;stats-agg-term&gt;]
( &lt;stats-agg-term&gt; | &lt;sparkline-agg-term&gt; | "("&lt;eval-expression&gt;")" )...
[ BY &lt;row-split&gt; &lt;column-split&gt; ] | [ OVER &lt;row-split&gt; ] [BY &lt;column-split&gt;] ]


```spl

chart [<chart-options>] [agg=<stats-agg-term>]
( <stats-agg-term> | <sparkline-agg-term> | "("<eval-expression>")" )...
[ BY <row-split> <column-split> ] | [ OVER <row-split> ] [BY <column-split>] ]

```


There are quotation marks on the parenthesis surrounding the &lt;eval-expression&gt; . This means that you must enclose the &lt;eval-expression&gt; in parenthesis in your search.

In the following search example, the &lt;eval-expression&gt; is avg(size)/max(delay) and is enclosed in parenthesis.

CODE

Copy

... | chart eval(avg(size)/max(delay)) AS ratio BY host user


```spl

... | chart eval(avg(size)/max(delay)) AS ratio BY host user

```



## Argument order

In the command syntax, the command arguments are presented in the order in which the arguments are meant to be used.

In the descriptions of the arguments, the Required arguments and Optional argument sections, the arguments are listed alphabetically. For each argument, there is a Syntax and Description. Additionally, for Optional arguments, there might be a Default.


## Data types

The nomenclature used for the data types in SPL syntax are described in the following table.


| Syntax | Data type | Notes |
| --- | --- | --- |
| &lt;bool&gt; | boolean | Usetrueorfalse. Other variations are accepted. For example, fortrueyou can also use 't', 'T', 'TRUE', 'yes', or the number one ( 1 ). Forfalseyou can also specify 'no', the number zero ( 0 ), and variations of the wordfalse, similar to the variations of the wordtrue. |
| &lt;field&gt; | A field name. You cannot specify a wild card for the field name. | See &lt;wc-field&gt;. |
| &lt;int&gt; or &lt;integer&gt; | An integer that can be a positive or negative value. | Sometimes referred to as a "signed" integer. See &lt;unsigned int&gt;. |
| &lt;string&gt; | string | See &lt;wc-string&gt;. |
| &lt;unsigned int&gt; | unsigned integer | An unsigned integer must be positive value. Unsigned integers can be larger numbers than signed integers. |
| &lt;wc-field&gt; | A field name or a partial name with a wildcard character to specify multiple, similarly named fields. | Use the asterisk ( \* ) character as the wildcard character. |
| &lt;wc-string&gt; | A string value or partial string value with a wildcard character. | Use the asterisk ( \* ) character as the wildcard character. |





## Logical operators

When a logical operator is included in the syntax of a command, you must always specify the operator in uppercase. Logical operators include:

- AND

- OR

- NOT

- XOR

The search command evaluates operates logical operators in a different order of precedence than the eval and where commands.. To learn more about the order in which boolean expressions are evaluated, along with some examples, see Boolean expressions with logical operators in the Search Manual .

To learn more about the the NOT operator, see Difference between NOT and != in the Search Manual .


## BY clauses

A &lt;by-clause&gt; and a &lt;split-by-clause&gt; are not the same argument.

When you use a &lt;by-clause&gt;, one row is returned for each distinct value &lt;by-clause&gt; field. A &lt;by-clause&gt; displays each unique item in a separate row. Think of the &lt;by-clause&gt; as a grouping.

The &lt;split-by-clause&gt; displays each unique item in a separate column. Think of the &lt;split-by-clause&gt; as a splitting or dividing.

Wildcard characters ( \* ) are not accepted in BY clauses.


## Fields and wildcard fields

When the syntax contains &lt;field&gt; you specify a field name from your events.

Consider this syntax:

bin [&lt;bins-options&gt;...] &lt;field&gt; [AS &lt;newfield&gt;]

The &lt;field&gt; argument is required. You can specify that the field displays a different name in the search results by using the [AS &lt;newfield&gt;] argument. This argument is optional.

For example, if the field is categoryId and you want the field to be named CategoryID in the output, you would specify:

categoryId AS CategoryID

The &lt;wc-field&gt; argument indicates that you can use wild card characters when specifying field names. For example, if you have a set of fields that end with "log" you can specify \*log to return all of those fields.

If you use a wild card character in the middle of a value, especially as a wild card for punctuation, the results might be unpredictable.


## Repeating expressions

With many commands you can specify multiple expressions. Some commands use a space between expressions, while other commands use a comma between expressions. In the syntax for a command you will see something like &lt;field-list to indicate that you can specify one or more expressions.

For example, the stats command includes a &lt;field-list argument. The list of fields must be separated by commas:

CODE

Copy

sourcetype=access_\* | stats count BY status, host


```spl

sourcetype=access_* | stats count BY status, host

```


With the outlier command, the &lt;field-list argument expects the field names to be space-separated:

CODE

Copy

...| outlier bytes clientip


```spl

...| outlier bytes clientip

```



## See also

In the Search Manual :

- Anatomy of a search

- Wildcards

- Field expressions

- Quotes and escaping characters

# makemv


## Description

Converts a single valued field into a multivalue field by splitting the values on a string delimiter or by using a regular expression. The delimiter can be a multicharacter delimiter.


> **Note: The makemv command does not apply to internal fields.**


See Use default fields in the Knowledge Manager Manual .


## Syntax

makemv [delim=&lt;string&gt; | tokenizer=&lt;string&gt;] [allowempty=&lt;bool&gt;] [setsv=&lt;bool&gt;] &lt;field&gt;


### Required arguments

field

Syntax: &lt;field&gt;

Description: The name of a field to generate the multivalues from.


### Optional arguments

delim

Syntax: delim=&lt;string&gt;

Description: A string value used as a delimiter. Splits the values in field on every occurrence of this delimiter.

Default: A single space (" ").

tokenizer

Syntax: tokenizer=&lt;string&gt;

Description: A regular expression with a capturing group that is repeat-matched against the values in the field. For each match, the first capturing group is used as a value in the newly created multivalue field.

allowempty

Syntax: allowempty=&lt;bool&gt;

Description: Specifies whether to permit empty string values in the multivalue field. When using delim=true , repeats of the delimiter string produce empty string values in the multivalue field. For example if delim="," and field="a,,b" , by default does not produce any value for the empty string. When using the tokenizer argument, zero length matches produce empty string values. By default they produce no values.

Default: false

setsv

Syntax: setsv=&lt;bool&gt;

Description: If true, the makemv command combines the decided values of the field into a single value, which is set on the same field. (The simultaneous existence of a multivalue and a single value for the same field is a problematic aspect of this flag.)

Default: false


## Usage

The makemv command is a distributable streaming command. See Command types .

You can use evaluation functions and statistical functions on multivalue fields or to return multivalue fields.


## Examples


### 1. Use a comma to separate field values

For sendmail search results, separate the values of "senders" into multiple values. Display the top values.

CODE

Copy

eventtype="sendmail" | makemv delim="," senders | top senders


```spl

eventtype="sendmail" | makemv delim="," senders | top senders

```



### 2. Use a colon delimiter and allow empty values

Separate the value of "product_info" into multiple values.

CODE

Copy

... | makemv delim=":" allowempty=true product_info


```spl

... | makemv delim=":" allowempty=true product_info

```



### 3. Use a regular expression to separate values

The following search creates a result and adds three values to the my_multival field. The makemv command is used to separate the values in the field by using a regular expression.

CODE

Copy

| makeresults
| eval my_multival="one,two,three"
| makemv tokenizer="([^,]+),?" my_multival


```spl

| makeresults
| eval my_multival="one,two,three"
| makemv tokenizer="([^,]+),?" my_multival

```



## See also

Commands:

mvcombine

mvexpand

nomv



Functions:

Multivalue eval functions

Multivalue stats and chart functions

split


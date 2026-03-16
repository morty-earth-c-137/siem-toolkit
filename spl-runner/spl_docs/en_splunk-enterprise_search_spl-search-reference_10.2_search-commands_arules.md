
# arules


## Description

The arules command looks for associative relationships between field values. The command returns a table with the following columns: Given fields, Implied fields, Strength, Given fields support, and Implied fields support. The given and implied field values are the values of the fields you supply. The Strength value indicates the relationship between (among) the given and implied field values.

Implements the arules algorithm as discussed in Michael Hahsler, Bettina Gruen and Kurt Hornik (2012). arules: Mining Association Rules and Frequent Itemsets. R package version 1.0-12 . This algorithm is similar to the algorithms used for online shopping websites which suggest related items based on what items other customers have viewed or purchased.


## Syntax

arules [&lt;arules-option&gt;... ] &lt;field-list&gt;...


### Required arguments

field-list

Syntax: &lt;field&gt; &lt;field&gt; ...

Description: The list of field names. At least two fields must be specified.


### Optional arguments

&lt;arules-option&gt;

Syntax: &lt;support&gt; | &lt;confidence&gt;

Description: Options for arules command.


### arules options

support

Syntax: sup=&lt;int&gt;

Description: Specify a support limit. Associations with computed support levels smaller than this value are not included in the output results. The support option must be a positive integer.

Default: 3

confidence

Syntax: conf=&lt;float&gt;

Description: Specify a confidence limit. Associations with a confidence (expressed as Strength field) are not included in the output results. Must be between 0 and 1.

Default: .5


## Usage

The arules command is a streaming command that is both distributable streaming and centralized streaming. See Command types .


## Examples

Example 1: Search for the likelihood that the fields are related.

CODE

Copy

... | arules field1 field2 field3


```spl

... | arules field1 field2 field3

```


Example 2:

CODE

Copy

... | arules sup=3 conf=.6 field1 field2 field3


```spl

... | arules sup=3 conf=.6 field1 field2 field3

```



## See also

associate , correlate
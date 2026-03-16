
# autoregress


## Description

Prepares your events for calculating the autoregression, or the moving average , by copying one or more of the previous values for field into each event.

The first few events will lack the augmentation of prior values, since the prior values do not exist.


## Syntax

autoregress &lt;field&gt; [AS &lt;newfield&gt;] [ p=&lt;int&gt; | p=&lt;int&gt;-&lt;int&gt; ]


### Required arguments

field

Syntax: &lt;string&gt;

Description: The name of a field. Most usefully a field with numeric values.


### Optional arguments

p

Syntax: p=&lt;int&gt; | p=&lt;int&gt;-&lt;int&gt;

Description: Specifies which prior events to copy values from. You can specify a single integer or a numeric range. For a single value, such as 3, the autoregress command copies field values from the third prior event into a new field. For a range, the autoregress command copies field values from the range of prior events. For example, if you specify a range such as p=2-4 , then the field values from the second, third, and fourth prior events are copied into new fields.

Default: 1

newfield

Syntax: &lt;field&gt;

Description: If p is set to a single integer, the newfield argument specifies a field name to copy the single field value into. Invalid if p is set to a range.

If the newfield argument is not specified, the single or multiple values are copied into fields with the names &lt;field&gt;_p&lt;num&gt; . For example, if p=2-4 and field=count , the field names are count_p2, count_p3, count_p4.


## Usage

The autoregress command is a centralized streaming command. See Command types .


## Examples


### Example 1:

For each event, copy the 3rd previous value of the 'ip' field into the field 'old_ip'.

CODE

Copy

... | autoregress ip AS old_ip p=3


```spl

... | autoregress ip AS old_ip p=3

```



### Example 2:

For each event, copy the 2nd, 3rd, 4th, and 5th previous values of the 'count' field.

CODE

Copy

... | autoregress count p=2-5


```spl

... | autoregress count p=2-5

```


Since the new field argument is not specified, the values are copied into the fields 'count_p2', 'count_p3', 'count_p4', and 'count_p5'.


### Example 3:

Calculate a moving average of event size over the current event and the four prior events. This search omits the moving_average for the initial events, where the field would be wrong, because summing null fields is considered null.

CODE

Copy

... | eval rawlen=len(_raw) | autoregress rawlen p=1-4 | eval moving_average=(rawlen + rawlen_p1 + rawlen_p2 + rawlen_p3 +rawlen_p4 ) /5


```spl

... | eval rawlen=len(_raw) | autoregress rawlen p=1-4 | eval moving_average=(rawlen + rawlen_p1 + rawlen_p2 + rawlen_p3 +rawlen_p4 ) /5

```



## See also

accum , delta , streamstats , trendline

# trendline


## Description

Computes the moving averages of fields: simple moving average (sma), exponential moving average (ema), and weighted moving average (wma) The output is written to a new field, which you can specify.

SMA and WMA both compute a sum over the period of most recent values. WMA puts more weight on recent values rather than past values. EMA is calculated using the following formula.

CODE

Copy

EMA(t) = alpha \* EMA(t-1) + (1 - alpha) \* field(t)


```spl

EMA(t) = alpha * EMA(t-1) + (1 - alpha) * field(t)

```


where alpha = 2/(period + 1) and field(t) is the current value of a field.


## Syntax

trendline ( &lt;trendtype&gt;&lt;period&gt;"("&lt;field&gt;")" [AS &lt;newfield&gt;] )...


### Required arguments

trendtype

Syntax: sma | ema | wma

Description: The type of trend to compute. Current supported trend types include simple moving average (sma), exponential moving average (ema), and weighted moving average (wma).

period

Syntax: &lt;num&gt;

Description: The period over which to compute the trend, an integer between 2 and 10000.

&lt;field&gt;

Syntax: "("&lt;field&gt;")"

Description: The name of the field on which to calculate the trend.


### Optional arguments

&lt;newfield&gt;

Syntax: &lt;field&gt;

Description: Specify a new field name to write the output to.

Default: &lt;trendtype&gt;&lt;period&gt;(&lt;field&gt;)


## Usage


## Examples

Example 1: Computes a five event simple moving average for field 'foo' and writes the result to new field called 'smoothed_foo.' Also, in the same line, computes ten event exponential moving average for field 'bar'. Because no AS clause is specified, writes the result to the field 'ema10(bar)'.

CODE

Copy

... | trendline sma5(foo) AS smoothed_foo ema10(bar)


```spl

... | trendline sma5(foo) AS smoothed_foo ema10(bar)

```


Example 2: Overlay a trendline over a chart of events by month.

CODE

Copy

index="bar" | stats count BY date_month | trendline sma2(count) AS trend | fields \* trend


```spl

index="bar" | stats count BY date_month | trendline sma2(count) AS trend | fields * trend

```



## See also

accum , autoregress , delta , streamstats
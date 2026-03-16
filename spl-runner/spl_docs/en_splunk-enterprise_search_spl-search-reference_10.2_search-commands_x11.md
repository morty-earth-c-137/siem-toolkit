
# x11


## Description

The x11 command removes the seasonal pattern in your time-based data series so that you can see the real trend in your data. This command has a similar purpose to the trendline command , but it uses the more sophisticated and industry popular X11 method.

The seasonal component of your time series data can be either additive or multiplicative, defined as the two types of seasonality that you can calculate with x11: add() for additive and mult() for multiplicative. See About time-series forecasting in the Search Manual .


## Syntax

x11 [&lt;type&gt;] [&lt;period&gt;] (&lt;fieldname&gt;) [AS &lt;newfield&gt;]


### Required arguments

&lt;fieldname&gt;

Syntax: &lt;field&gt;

Description: The name of the field to calculate the seasonal trend.


### Optional arguments

&lt;type&gt;

Syntax: add() | mult()

Description: Specify the type of x11 to compute, additive or multiplicative.

Default: mult()

&lt;period&gt;

Syntax: &lt;int&gt;

Description: The period of the data relative to the number of data points, expressed as an integer between 5 and 1000. If the period is 7, the command expects the data to be periodic every 7 data points. If you omit this parameter, Splunk software calculates the period automatically. The algorithm does not work if the period is less than 5 and will be too slow if the period is greater than 1000.

&lt;newfield&gt;

Syntax: &lt;string&gt;

Description: Specify a field name for the output of the x11 command.

Default: None


## Examples

Example 1: In this example, the type is the default mult and the period is 15. The field name specified is count .

CODE

Copy

index=download | timechart span=1d count(file) as count | x11 mult15(count)


```spl

index=download | timechart span=1d count(file) as count | x11 mult15(count)

```





> **Note: Because span=1d, every data point accounts for 1 day. As a result, the period in this example is 15 days. You can change the syntax in this example to ... | x11 15(count) because the mult type is the default type.**


Example 2: In this example, the type is add and the period is 20. The field name specified is count .

CODE

Copy

index=download | timechart span=1d count(file) as count | x11 add20(count)


```spl

index=download | timechart span=1d count(file) as count | x11 add20(count)

```





## See also

predict , trendline
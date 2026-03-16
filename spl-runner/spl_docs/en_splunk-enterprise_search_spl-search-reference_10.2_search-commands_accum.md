
# accum


## Description

For each event where field is a number, the accum command calculates a running total or sum of the numbers. The accumulated sum can be returned to either the same field, or a newfield that you specify.


## Syntax

accum &lt;field&gt; [AS &lt;newfield&gt;]


### Required arguments

field

Syntax: &lt;string&gt;

Description: The name of the field that you want to calculate the accumulated sum for. The field must contain numeric values.


### Optional arguments

newfield

Syntax: &lt;string&gt;

Description: The name of a new field where you want the results placed.


## Basic example


### 1. Create a running total of a field


| This example uses the sample data from the Search Tutorial but should work with any format of Apache web access log. To try this example on your own Splunk instance, you must download the sample data and follow the instructions toget the tutorial data into Splunk. Use the time rangeAll timewhen you run the search. |
| --- |


The following search looks for events from web access log files that were successful views of strategy games. A count of the events by each product ID is returned.

CODE

Copy

sourcetype=access_\* status=200 categoryId=STRATEGY | chart count AS views by productId


```spl

sourcetype=access_* status=200 categoryId=STRATEGY | chart count AS views by productId

```


The results appear on the Statistics tab and look something like this:


| productId | views |
| --- | --- |
| DB-SG-G01 | 1796 |
| DC-SG-G02 | 1642 |
| FS-SG-G03 | 1482 |
| PZ-SG-G05 | 1300 |


You can use the accum command to generate a running total of the views and display the running total in a new field called "TotalViews".

CODE

Copy

sourcetype=access_\* status=200 categoryId=STRATEGY | chart count AS views by productId | accum views as TotalViews


```spl

sourcetype=access_* status=200 categoryId=STRATEGY | chart count AS views by productId | accum views as TotalViews

```


The results appear on the Statistics tab and look something like this:


| productId | views | TotalViews |
| --- | --- | --- |
| DB-SG-G01 | 1796 | 1796 |
| DC-SG-G02 | 1642 | 3438 |
| FS-SG-G03 | 1482 | 4920 |
| PZ-SG-G05 | 1300 | 6220 |



## See also

autoregress , delta , streamstats , trendline
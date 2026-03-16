
# rangemap


## Description

Use the rangemap command to categorize the values in a numeric field. The command adds in a new field called range to each event and displays the category in the range field. The values in the range field are based on the numeric ranges that you specify.

Set the range field to the names of any attribute_name that the value of the input field is within. If no range is matched, the range value is set to the default value.

The ranges that you set can overlap. If you have overlapping values, the range field is created as a multivalue field containing all the values that apply. For example, if low=1-10, elevated=5-15, and the input field value is 10, range=low and code=elevated .


## Syntax

The required syntax is in bold .

rangemap

field=&lt;string&gt;

[&lt;attribute_name&gt;=&lt;numeric_range&gt;]...

[default=&lt;string&gt;]


### Required arguments

field

Syntax: field=&lt;string&gt;

Description: The name of the input field. This field must contain numeric values.


### Optional arguments

attribute_name=numeric_range

Syntax: &lt;string&gt;=&lt;num&gt;-&lt;num&gt;

Description: The &lt;attribute_name&gt; is a string value that is output when the &lt;numeric_range&gt; matches the value in the &lt;field&gt;. The &lt;attribute_name&gt; is a output to the range field. The &lt;numeric_range&gt; is the starting and ending values for the range. The values can be integers or floating point numbers. The first value must be lower than the second. The &lt;numeric_range&gt; can include negative values.

Example: Dislike=-5--1 DontCare=0-0 Like=1-5

default

Syntax: default=&lt;string&gt;

Description: If the input field does not match a range, use this to define a default value.

Default: "None"


## Usage

The rangemap command is a distributable streaming command. See Command types .


## Basic examples


### Example 1:

Set range to "green" if the date_second is between 1-30; "blue", if between 31-39; "red", if between 40-59; and "gray", if no range matches (for example, if date_second=0).

CODE

Copy

... | rangemap field=date_second green=1-30 blue=31-39 red=40-59 default=gray


```spl

... | rangemap field=date_second green=1-30 blue=31-39 red=40-59 default=gray

```



### Example 2:

Sets the value of each event's range field to "low" if its count field is 0 (zero); "elevated", if between 1-100; "severe", otherwise.

CODE

Copy

... | rangemap field=count low=0-0 elevated=1-100 default=severe


```spl

... | rangemap field=count low=0-0 elevated=1-100 default=severe

```



## Extended example


| This example uses recent earthquake data downloaded from theUSGS Earthquakes website. The data is a comma separated ASCII text file that contains magnitude (mag), coordinates (latitude, longitude), region (place), etc., for each earthquake recorded.You can download a current CSV file from theUSGS Earthquake Feedsand add it as an input. The following examples uses theAll Earthquakesunder thePast 30 dayslist. |
| --- |


This search counts the number and magnitude of each earthquake that occurred in and around Alaska. Then a color is assigned to each magnitude using the rangemap command.

CODE

Copy

source=all_month.csv place=\*alaska\* mag&gt;=3.5 
| stats count BY mag 
| rename mag AS magnitude 
| rangemap field=magnitude light=3.9-4.3 strong=4.4-4.9 severe=5.0-9.0 default=weak


```spl

source=all_month.csv place=*alaska* mag>=3.5 
| stats count BY mag 
| rename mag AS magnitude 
| rangemap field=magnitude light=3.9-4.3 strong=4.4-4.9 severe=5.0-9.0 default=weak

```




The results look something like this:




| magnitude | count | range |
| --- | --- | --- |
| 3.7 | 15 | weak |
| 3.8 | 31 | weak |
| 3.9 | 29 | light |
| 4 | 22 | light |
| 4.1 | 30 | light |
| 4.2 | 15 | light |
| 4.3 | 10 | light |
| 4.4 | 22 | strong |
| 4.5 | 3 | strong |
| 4.6 | 8 | strong |
| 4.7 | 9 | strong |
| 4.8 | 6 | strong |
| 4.9 | 6 | strong |
| 5 | 2 | severe |
| 5.1 | 2 | severe |
| 5.2 | 5 | severe |



### Summarize the results by range value

CODE

Copy

source=all_month.csv place=\*alaska\* mag&gt;=3.5 
| stats count BY mag 
| rename mag AS magnitude 
| rangemap field=magnitude green=3.9-4.2 yellow=4.3-4.6 red=4.7-5.0 default=gray 
| stats sum(count) by range


```spl

source=all_month.csv place=*alaska* mag>=3.5 
| stats count BY mag 
| rename mag AS magnitude 
| rangemap field=magnitude green=3.9-4.2 yellow=4.3-4.6 red=4.7-5.0 default=gray 
| stats sum(count) by range

```


The results look something like this:


| range | sum(count) |
| --- | --- |
| gray | 127 |
| green | 96 |
| red | 23 |
| yellow | 43 |



### Arrange the results in a custom sort order

By default the values in the search results are in descending order by the sum(count) field. You can apply a custom sort order to the results using the eval command with the case function.

CODE

Copy

source=all_month.csv place=\*alaska\* mag&gt;=3.5 
| stats count BY mag 
| rename mag AS magnitude 
| rangemap field=magnitude green=3.9-4.2 yellow=4.3-4.6 red=4.7-5.0 default=gray 
| stats sum(count) by range
| eval sort_field=case(range="red",1, range="yellow",2, range="green",3, range="gray",4)
| sort sort_field


```spl

source=all_month.csv place=*alaska* mag>=3.5 
| stats count BY mag 
| rename mag AS magnitude 
| rangemap field=magnitude green=3.9-4.2 yellow=4.3-4.6 red=4.7-5.0 default=gray 
| stats sum(count) by range
| eval sort_field=case(range="red",1, range="yellow",2, range="green",3, range="gray",4)
| sort sort_field

```


The results look something like this:


| range | sum(count) | sort_field |
| --- | --- | --- |
| red | 23 | 1 |
| yellow | 43 | 2 |
| green | 96 | 3 |
| gray | 127 | 4 |



## See also

Commands

eval

Blogs

Order Up! Custom Sort Orders

# xyseries

This topic walks through how to use the xyseries command.


## Description

Converts results into a tabular format that is suitable for graphing. This command is the inverse of the untable command.


## Syntax

xyseries [grouped=&lt;bool&gt;] &lt;x-field&gt; &lt;y-name-field&gt; &lt;y-data-field&gt;... [sep=&lt;string&gt;] [format=&lt;string&gt;]


### Required arguments

&lt;x-field&gt;

Syntax: &lt;field&gt;

Description: The name of the field to use for the x-axis label. The values of this field appear as labels for the data series plotted on the x-axis.

&lt;y-name-field&gt;

Syntax: &lt;field&gt;

Description: The field that contains the values to use as labels for the data series.

&lt;y-data-field&gt;

Syntax: &lt;field&gt; [,&lt;field&gt;] ...

Description: One or more fields that contain the data to chart. When specifying multiple fields, separate the field names with commas.


### Optional arguments

format

Syntax: format=&lt;string&gt;

Description: Used to construct output field names when multiple data series are used in conjunction with a split-by-field and separate the &lt;y-name-field&gt; and the &lt;y-data-field&gt;. format takes precedence over sep and lets you specify a parameterized expression with the stats aggregator and function ($AGG$) and the value of the split-by-field ($VAL$).

grouped

Syntax: grouped= true | false

Description: If true, indicates that the input is sorted by the value of the &lt;x-field&gt; and multifile input is allowed.

Default: false

sep

Syntax: sep=&lt;string&gt;

Description: Used to construct output field names when multiple data series are used in conjunctions with a split-by field. This is equivalent to setting format to $AGG$&lt;sep&gt;$VAL$ .


## Usage

The xyseries command is a distributable streaming command , unless grouped=true is specified and then the xyseries command is a transforming command . See Command types .


### Alias

The alias for the xyseries command is maketable .


### Results with duplicate field values

When you use the xyseries command to converts results into a tabular format, results that contain duplicate values are removed.

You can use the streamstats command create unique record numbers and use those numbers to retain all results. For an example, see the Extended example for the untable command .


## Example

Let's walk through an example to learn how to reformat search results with the xyseries command.


### Write a search


| This example uses the sample data from the Search Tutorial but should work with any format of Apache web access log. To try this example on your own Splunk instance, you must download the sample data and follow the instructions toget the tutorial data into Splunk. Use the time rangeAll timewhen you run the search. |
| --- |


Run this search in the search and reporting app:

CODE

Copy

sourcetype=access_\* status=200 action=purchase | top categoryId


```spl

sourcetype=access_* status=200 action=purchase | top categoryId

```


The top command automatically adds the count and percent fields to the results. For each categoryId, there are two values, the count and the percent.

The search results look like this:


| categoryId | count | percent |
| --- | --- | --- |
| STRATEGY | 806 | 30.495649 |
| ARCADE | 493 | 18.653046 |
| TEE | 367 | 13.885736 |
| ACCESSORIES | 348 | 13.166856 |
| SIMULATION | 246 | 9.307605 |
| SHOOTER | 245 | 9.269769 |
| SPORTS | 138 | 5.221339 |



### Identify your fields in the xyseries command syntax

In this example:

- &lt;x-field&gt; = categoryId

- &lt;y-name-field&gt; = count

- &lt;y-data-field&gt; = percent


### Reformat search results with xyseries

When you apply the xyseries command, the categoryId serves as the &lt;x-field&gt; in your search results. The results of the calculation count become the columns, &lt;y-name-field&gt;, in your search results. The &lt;y-data-field&gt;, percent , corresponds to the values in your search results.

Run this search in the search and reporting app:

CODE

Copy

sourcetype=access_\* status=200 action=purchase | top categoryId | xyseries categoryId count percent


```spl

sourcetype=access_* status=200 action=purchase | top categoryId | xyseries categoryId count percent

```


The search results look like this:


| categoryId | 138 | 245 | 246 | 348 | 367 | 493 | 806 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SPORTS | 5.221339 |  |  |  |  |  |  |
| ACCESSORIES |  |  |  | 13.166856 |  |  |  |
| ARCADE |  |  |  |  |  | 18.653046 |  |
| SHOOTER |  | 9.269769 |  |  |  |  |  |
| SIMULATION |  |  | 9.307605 |  |  |  |  |
| STRATEGY |  |  |  |  |  |  | 30.495649 |
| TEE |  |  |  |  |  | 13.885736 |  |



## Extended example

Let's walk through an example to learn how to add optional arguments to the xyseries command.


### Write a search

To add the optional arguments of the xyseries command, you need to write a search that includes a split-by-field command for multiple aggregates. Use the sep and format arguments to modify the output field names in your search results.

Run this search in the search and reporting app:

CODE

Copy

sourcetype=access_combined_wcookie | stats count(host) count(productId) by clientip, referer_domain


```spl

sourcetype=access_combined_wcookie | stats count(host) count(productId) by clientip, referer_domain

```


This search sorts referrer domain, count(host) and count(productId) by clientIp.

Run this search in the search and reporting app:

CODE

Copy

sourcetype=access_combined_wcookie | stats count(host) count(productId) by clientip, referer_domain  | xyseries clientip referer_domain count(host), count(productId)


```spl

sourcetype=access_combined_wcookie | stats count(host) count(productId) by clientip, referer_domain  | xyseries clientip referer_domain count(host), count(productId)

```


In this example:

- &lt;x-field&gt; = clientip

- &lt;y-name-field&gt; = referrer domain

- &lt;y-data-field&gt; = host, productId

The xyseries command needs two aggregates, in this example they are: count(host) count(productId). The first few search results look like this:


### Add optional argument: sep

Add a string to the sep argument to change the default character that separates the &lt;y-name-field&gt; host,and the &lt;y-data-field&gt; productId. The format argument adds the &lt;y-name-field&gt; and separates the field name and field value by the default ":"

Run this search in the search and reporting app:

CODE

Copy

sourcetype=access_combined_wcookie | stats count(host) count(productId) by clientip, referer_domain  | xyseries clientip referer_domain count(host), count(productId) sep="-"


```spl

sourcetype=access_combined_wcookie | stats count(host) count(productId) by clientip, referer_domain  | xyseries clientip referer_domain count(host), count(productId) sep="-"

```


The first few search results look like this:


### Add optional argument: format

The format argument adds the &lt;y-name-field&gt; and separates the field name and field value by the default ":" For example, the default for this example looks like count(host):referrer_domain

When you specify a string to separate the &lt;y-name-field&gt; and &lt;y-data-field&gt; with the format argument, it overrides any assignment from the sep argument. In the following example, the sep argument assigns the "-" character to separate the &lt;y-name-field&gt; and &lt;y-data-field&gt; fields. The format argument assigns a "+" and this assignment takes precedence over sep. In this case $VAL$ and $AGG$ represent both the &lt;y-name-field&gt; and &lt;y-data-field&gt;. As seen in the search results, the &lt;y-name-field&gt;, host, and &lt;y-data-field&gt;, productId can correspond to either $VAL$ or $AGG$.

Run this search in the search and reporting app:

CODE

Copy

sourcetype=access_combined_wcookie | stats count(host) count(productId) by clientip, referer_domain  | xyseries clientip referer_domain count(host), count(productId) sep="-" format="$AGG$  + $VAL$ TEST"


```spl

sourcetype=access_combined_wcookie | stats count(host) count(productId) by clientip, referer_domain  | xyseries clientip referer_domain count(host), count(productId) sep="-" format="$AGG$  + $VAL$ TEST"

```


The first few search results look like this:


### Add optional argument: grouped

The grouped argument determines whether the xyseries command runs as a distributable streaming command , or a transforming command . The default state grouped=FALSE for the xyseries command runs as a streaming command.


## See also

Commands

untable
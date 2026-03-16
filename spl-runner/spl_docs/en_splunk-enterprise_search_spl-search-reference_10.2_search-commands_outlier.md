
# outlier


## Description

This command is used to remove outliers, not detect them. It removes or truncates outlying numeric values in selected fields. If no fields are specified, then the outlier command attempts to process all fields.

To identify outliers and create alerts for outliers, see finding and removing outliers in the Search Manual .




> **Note: Use current Splunk machine learning (ML) tools to take advantage of the latest algorithms and get the most powerful results. See About the Splunk Machine Learning Toolkit in the Splunk Machine Learning Toolkit .**



## Syntax

outlier &lt;outlier-options&gt;... [&lt;field-list&gt;]


### Optional arguments

&lt;outlier-options&gt;

Syntax: &lt;action&gt; | &lt;mark&gt; | &lt;param&gt; | &lt;uselower&gt;

Description: Outlier options.

&lt;field-list&gt;

Syntax: &lt;field&gt; ...

Description: A space-delimited list of field names.


### Outlier options

&lt;action&gt;

Syntax: action=remove | transform

Description: Specifies what to do with the outliers. The remove option removes events that containing the outlying numerical values. The transform option truncates the outlying values to the threshold for outliers. If action=transform and mark=true , prefixes the values with "000".

Abbreviations: The remove action can be shorted to rm . The transform action can be shorted to tf .

Default: transform

&lt;mark&gt;

Syntax: mark=&lt;bool&gt;

Description: If action=transform and mark=true , prefixes the outlying values with "000". If action=remove , the mark argument has no effect.

Default: false

&lt;param&gt;

Syntax: param=&lt;num&gt;

Description: Parameter controlling the threshold of outlier detection. An outlier is defined as a numerical value that is outside of param multiplied by the inter-quartile range (IQR).

Default: 2.5

&lt;uselower&gt;

Syntax: uselower=&lt;bool&gt;

Description: Controls whether to look for outliers for values below the median in addition to above.

Default: false


## Usage

The outlier command is a dataset processing command. See Command types .

Filtering is based on the inter-quartile range (IQR), which is computed from the difference between the 25th percentile and 75th percentile values of the numeric fields. If the value of a field in an event is less than (25th percentile) - param\*IQR or greater than (75th percentile) + param\*IQR , that field is transformed or that event is removed based on the action parameter.


## Examples

Example 1: For a timechart of webserver events, transform the outlying average CPU values.

CODE

Copy

404 host="webserver" | timechart avg(cpu_seconds) by host | outlier action=tf


```spl

404 host="webserver" | timechart avg(cpu_seconds) by host | outlier action=tf

```


Example 2: Remove all outlying numerical values.

CODE

Copy

... | outlier


```spl

... | outlier

```



## See also

anomalies , anomalousvalue , cluster , kmeans

Finding and removing outliers
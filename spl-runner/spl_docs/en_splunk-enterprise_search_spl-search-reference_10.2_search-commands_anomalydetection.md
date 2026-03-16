
# anomalydetection


## Description

A transforming command that identifies anomalous events by computing a probability for each event and then detecting unusually small probabilities. The probability is defined as the product of the frequencies of each individual field value in the event.

- For categorical fields, the frequency of a value X is the number of times X occurs divided by the total number of events.

- For numerical fields, we first build a histogram for all the values, then compute the frequency of a value X as the size of the bin that contains X divided by the number of events.

The anomalydetection command includes the capabilities of the existing anomalousvalue and outlier commands and offers a histogram-based approach for detecting anomalies.


> **Note: Use current Splunk machine learning (ML) tools to take advantage of the latest algorithms and get the most powerful results. See About the Splunk Machine Learning Toolkit in the Splunk Machine Learning Toolkit .**



## Syntax

anomalydetection [&lt;method-option&gt;] [&lt;action-option&gt;] [&lt;pthresh-option&gt;] [&lt;cutoff-option&gt;] [&lt;field-list&gt;]


### Optional arguments

&lt;method-option&gt;

Syntax: method = histogram | zscore | iqr

Description: Select the method of anomaly detection. When method=zscore , performs like the anomalousvalue command. When method=iqr , performs like the outlier command. See Usage .

Default: method=histogram

&lt;action-option&gt;

Syntax for method=histogram or method=zscore: action = filter | annotate | summary

Syntax for method=iqr: action = remove | transform

Description: The actions and defaults depend on the method that you specify. See the detailed descriptions for the actions for each method below.

&lt;pthresh-option&gt;

Syntax: pthresh=&lt;num&gt;

Description: Used with method=histogram or method=zscore . Sets the probability threshold, as a decimal number, that has to be met for an event to be deemed anomalous.

Default: For method=histogram , the command calculates pthresh for each data set during analysis. For method=zscore , the default is 0.01. If you try to use this when method=iqr , it returns an invalid argument error.

&lt;cutoff-option&gt;

Syntax: cutoff=&lt;bool&gt;

Description: Sets the upper bound threshold on the number of anomalies. This option applies to only the histogram method. If cutoff=false , the algorithm uses the formula threshold = 1st-quartile - 1.5 \* IRQ without modification. If cutoff=true , the algorithm modifies the formula in order to come up with a smaller number of anomalies.

Default: true

&lt;field-list&gt;

Syntax: &lt;string&gt; &lt;string&gt; ...

Description: A list of field names.


### Histogram actions

&lt;action-option&gt;

Syntax: action=annotate | filter | summary

Description: Specifies whether to return all events with additional fields (annotate), to filter out events with anomalous values (filter), or to return a summary of anomaly statistics (summary).

Default: filter

When action=filter , the command returns anomalous events and filters out other events. Each returned event contains four new fields. When action=annotate , the command returns all the original events with the same four new fields added when action=filter .


| Field | Description |
| --- | --- |
| log_event_prob | The natural logarithm of the event probability. |
| probable_cause | The name of the field that best explains why the event is anomalous. No one field causes anomaly by itself, but often some field value occurs too rarely to make the event probability small. |
| probable_cause_freq | The frequency of the value in the probable_cause field. |
| max_freq | Maximum frequency for all field values in the event. |


When action=summary , the command returns a single event containing six fields.


| Output field | Description |
| --- | --- |
| num_anomalies | The number of anomalous events. |
| thresh | The event probability threshold that separates anomalous events. |
| max_logprob | The maximum of all log(event_prob). |
| min_logprob | The minimum of all log(event_prob). |
| 1st_quartile | The first quartile of all log(event_prob). |
| 3rd_quartile | The third quartile of all log(event_prob). |



### Zscore actions

&lt;action-option&gt;

Syntax: action=annotate | filter | summary

Description: Specifies whether to return the anomaly score (annotate), filter out events with anomalous values (filter), or a summary of anomaly statistics (summary).

Default: filter

When action=filter , the command returns events with anomalous values while other events are dropped. The kept events are annotated, like the annotate action.

When action=annotate , the command adds new fields, Anomaly_Score_Cat(field) and Anomaly_Score_Num(field) , to the events that contain anomalous values.

When action=summary , the command returns a table that summarizes the anomaly statistics for each field is generated. The table includes how many events contained this field, the fraction of events that were anomalous, what type of test (categorical or numerical) were performed, and so on.


### IQR actions

&lt;action-option&gt;

Syntax: action=remove | transform

Description: Specifies what to do with outliers. The remove action removes the event containing the outlying numerical value. The transform action transforms the event by truncating the outlying value to the threshold for outliers. If mark=true , the transform action prefixes the value with "000".

Abbreviations: The abbreviation for remove is rm . The abbreviation for transform is tf .

Default: action=transform


## Usage

The anomalydetection command is a streaming command command. See Command types .


### The zscore method

When you specify method=zscore , the anomalydetection command performs like the anomalousvalue command. You can specify the syntax components of the anomalousvalue command when you use the anomalydetection command with method=zscore . See the anomalousvalue command.


### The iqr method

When you specify method=iqr , the anomalydetection command performs like the outlier command. You can specify the syntax components of the outlier command when you specify method=iqr with the anomalydetection command. For example, you can specify the outlier options &lt;action&gt;, &lt;mark&gt;, &lt;param&gt;, and &lt;uselower&gt;. See the outlier command.


## Examples


### Example 1: Return only anomalous events

These two searches return the same results. The arguments specified in the second search are the default values.

CODE

Copy

... | anomalydetection


```spl

... | anomalydetection

```


CODE

Copy

... | anomalydetection method=histogram action=filter


```spl

... | anomalydetection method=histogram action=filter

```



### Example 2: Return a short summary of how many anomalous events are there

Return a short summary of how many anomalous events are there and some other statistics such as the threshold value used to detect them.

CODE

Copy

... | anomalydetection action=summary


```spl

... | anomalydetection action=summary

```



### Example 3: Return events with anomalous values

This example specifies method=zscore to return anomalous values. The search uses the filter action to filter out events that do not have anomalous values. Events must meet the probability threshold pthresh before being considered an anomalous value.

CODE

Copy

... | anomalydetection method=zscore action=filter pthresh=0.05


```spl

... | anomalydetection method=zscore action=filter pthresh=0.05

```



### Example 4: Return outliers

This example uses the outlier options from the outlier command. The abbreviation tf is used for the transform action in this example.

CODE

Copy

... | anomalydetection method=iqr action=tf param=4 uselower=true mark=true


```spl

... | anomalydetection method=iqr action=tf param=4 uselower=true mark=true

```



## See also

analyzefields , anomalies , anomalousvalue , cluster , kmeans , outlier
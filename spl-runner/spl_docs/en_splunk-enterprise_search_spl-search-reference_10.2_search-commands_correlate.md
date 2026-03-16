
# correlate


## Description

Calculates the correlation between different fields.

You can use the correlate command to see an overview of the co-occurrence between fields in your data. The results are presented in a matrix format, where the cross tabulation of two fields is a cell value. The cell value represents the percentage of times that the two fields exist in the same events.

The field the result is specific to is named in the value of the RowField field, while the fields it is compared against are the names of the other fields.


> **Note: This command looks at the relationship among all the fields in a set of search results. If you want to analyze the relationship between the values of fields, refer to the contingency command, which counts the co-ocurrence of pairs of field values in events.**



## Syntax

correlate


## Limits

There is a limit on the number of fields that correlate considers in a search. From limits.conf, stanza [correlate], the maxfields sets this ceiling. The default is 1000.

If more than this many fields are encountered, the correlate command continues to process data for the first N (eg thousand) field names encountered, but ignores data for additional fields. If this occurs, the notification from the search or alert contains a message "correlate: input fields limit (N) reached. Some fields may have been ignored."

As with all designed-in limits, adjusting this might have significant memory or cpu costs.


## Examples


### Example 1:

Look at the co-occurrence between all fields in the _internal index.

CODE

Copy

index=_internal | correlate


```spl

index=_internal | correlate

```


Here is a snapshot of the results.



Because there are different types of logs in the _internal , you can expect to see that many of the fields do not co-occur.


### Example 2:

Calculate the co-occurrences between all fields in Web access events.

CODE

Copy

sourcetype=access_\* | correlate


```spl

sourcetype=access_* | correlate

```


You expect all Web access events to share the same fields: clientip, referer, method, and so on. But, because the sourcetype=access_\* includes both access_common and access_combined Apache log formats, you should see that the percentages of some of the fields are less than 1.0.


### Example 3:

Calculate the co-occurrences between all the fields in download events.

CODE

Copy

eventtype=download | correlate


```spl

eventtype=download | correlate

```


The more narrow your search is before you pass the results into correlate , the more likely it is that all the field value pairs have a correlation of 1.0. A correlation of 1.0 means the values co-occur in 100% of the search results. For these download events, you might be able to spot an issue depending on which pairs have less than 1.0 co-occurrence.


## See also

associate , contingency
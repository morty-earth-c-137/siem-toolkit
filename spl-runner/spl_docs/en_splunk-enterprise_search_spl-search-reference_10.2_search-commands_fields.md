
# fields


## Description

Keeps or removes fields from search results based on the field list criteria.


## Syntax

fields [+|-] &lt;wc-field-list&gt;


### Required arguments

&lt;wc-field-list&gt;

Syntax: &lt;field&gt;, &lt;field&gt;, ...

Description: Comma-delimited list of fields to keep or remove. You can use the asterisk ( \* ) as a wildcard to specify a list of fields with similar names. For example, if you want to specify all fields that start with "value", you can use a wildcard such as value\* . To specify the wildcard pattern for internal fields, use _\* .


### Optional arguments

+ | -

Syntax: + | -

Description: If the plus ( + ) symbol is specified, only the fields in the wc-field-list are kept in the results. If the negative ( - ) symbol is specified, the fields in the wc-field-list are removed from the results.

Default: +


## Usage

The fields command is a distributable streaming command. See Command types .


### Internal fields and Splunk Web

The leading underscore is reserved for names of internal fields such as _raw and _time . By default, the internal fields _raw and _time are included in the search results in Splunk Web. The fields command does not remove these internal fields unless you explicitly specify that the fields should not appear in the output in Splunk Web.

For example, to remove all internal fields, you specify:

... | fields - _\*

To exclude a specific field, such as _raw , you specify:

... | fields - _raw




> **Note: Be cautious removing the _time field. Statistical commands, such as timechart and chart , cannot display date or time information without the _time field.**



### Displaying internal fields in Splunk Web

Other than the _raw and _time fields, internal fields do not display in Splunk Web, even if you explicitly specify the fields in the search. For example, the following search does not show the _bkt field in the results.

CODE

Copy

index=_internal | head 5 | fields + _bkt | table _bkt


```spl

index=_internal | head 5 | fields + _bkt | table _bkt

```


To display an internal field in the results, the field must be copied or renamed to a field name that does not include the leading underscore character. For example:

CODE

Copy

index=_internal | head 5 | fields + _bkt | eval bkt=_bkt | table bkt


```spl

index=_internal | head 5 | fields + _bkt | eval bkt=_bkt | table bkt

```



### Internal fields and the outputcsv command

You can include additional internal fields in your search results by using the &lt;codeph&gt;outputcsv&lt;/codeph&gt; command. When the outputcsv command is used in the search, there are additional internal fields that are automatically added to the CSV file. The most common internal fields that are added are:

- _raw

- _time

- _indextime



To exclude internal fields from the output, specify each field that you want to exclude. For example:



CODE

Copy

... | fields - _raw _indextime _sourcetype _serial | outputcsv MyTestCsvFile


```spl

... | fields - _raw _indextime _sourcetype _serial | outputcsv MyTestCsvFile

```



### You cannot match wildcard characters in searches that use the fields command

You can use the asterisk ( \* ) in your searches as a wildcard character, but you can't use a backslash ( \ ) to escape an asterisk in search strings. A backslash \ and an asterisk \* match the characters \\* in searches, not an escaped wildcard \* character. Because Splunk platform doesn't support escaping wildcards, asterisk ( \* ) characters in field names can't be matched in searches that keep or remove fields from search results.


### Support for backslash characters ( \ ) in the fields command

To match a backslash character ( \ ) in a field name when using the fields command, use 2 backslashes for each backslash. For example, to display fields that contain http:\\ , use the following command in your search:

CODE

Copy

... | fields http:\\\\\*


```spl

... | fields http:\\\\*

```


See Backslashes in the Search Manual .


## Examples


### Example 1:

Remove the host and ip fields from the results

CODE

Copy

... | fields - host, ip


```spl

... | fields - host, ip

```



### Example 2:

Keep only the host and ip fields. Remove all of the internal fields. The internal fields begin with an underscore character, for example _time .

CODE

Copy

... | fields host, ip | fields - _\*


```spl

... | fields host, ip | fields - _*

```



### Example 3:

Remove unwanted internal fields from the output CSV file. The fields to exclude are _raw _indextime , _sourcetype , _subsecond , and _serial .

CODE

Copy

index=_internal sourcetype="splunkd" | head 5 | fields - _raw, _indextime, _sourcetype, _subsecond, _serial | outputcsv MyTestCsvfile


```spl

index=_internal sourcetype="splunkd" | head 5 | fields - _raw, _indextime, _sourcetype, _subsecond, _serial | outputcsv MyTestCsvfile

```



### Example 4:

Keep only the fields source , sourcetype , host , and all fields beginning with error .

CODE

Copy

... | fields source, sourcetype, host, error\*


```spl

... | fields source, sourcetype, host, error*

```



## See also

rename , table
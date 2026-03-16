
# dedup


## Description

Removes the events that contain an identical combination of values for the fields that you specify.

With the dedup command, you can specify the number of duplicate events to keep for each value of a single field, or for each combination of values among several fields. Events returned by dedup are based on search order. For historical searches , the most recent events are searched first. For real-time searches , the first events that are received are searched, which are not necessarily the most recent events.

You can specify the number of events with duplicate values, or value combinations, to keep. You can sort the fields, which determines which event is retained. Other options enable you to retain events with the duplicate fields removed, or to keep events where the fields specified do not exist in the events.


## Syntax

The required syntax is in bold .

dedup

[&lt;int&gt;]

&lt;field-list&gt;

[keepevents=&lt;bool&gt;]

[keepempty=&lt;bool&gt;]

[consecutive=&lt;bool&gt;]

[sortby &lt;sort-by-clause&gt;]


### Required arguments

&lt;field-list&gt;

Syntax: &lt;string&gt; &lt;string&gt; ...

Description: A list of field names to remove duplicate values from.


### Optional arguments

consecutive

Syntax: consecutive=&lt;bool&gt;

Description: If true, only remove events with duplicate combinations of values that are consecutive.

Default: false

keepempty

Syntax: keepempty=&lt;bool&gt;

Description: If set to true, keeps every event where one or more of the specified fields is not present (null).

Default: false. All events where any of the selected fields are null are dropped.

The keepempty=true argument keeps every event that does not have one or more of the fields in the field list. To keep N representative events for combinations of field values including null values, use the fillnull command to provide a non-null value for these fields. For example:

CODE

Copy

...| fillnull value="MISSING" field1 field2 | dedup field1 field2


```spl

...| fillnull value="MISSING" field1 field2 | dedup field1 field2

```


keepevents

Syntax: keepevents=&lt;bool&gt;

Description: If true, keep all events, but will remove the selected fields from events after the first event containing a particular combination of values.

Default: false. Events are dropped after the first event of each particular combination.

&lt;N&gt;

Syntax: &lt;int&gt;

Description: The dedup command retains multiple events for each combination when you specify N . The number for N must be greater than 0. If you do not specify a number, only the first occurring event is kept. All other duplicates are removed from the results.

&lt;sort-by-clause&gt;

Syntax: sortby ( - | + ) &lt;sort-field&gt; [(- | +) &lt;sort_field&gt; ...]

Description: List of the fields to sort by and the sort order. Use the dash symbol ( - ) for descending order and the plus symbol ( + ) for ascending order. You must specify the sort order for each field specified in the &lt;sort-by-clause&gt;. The &lt;sort-by-clause&gt; determines which of the duplicate events to keep. When the list of events is sorted, the top-most event, of the duplicate events in the sorted list, is retained.


### Sort field options

&lt;sort-field&gt;

Syntax: &lt;field&gt; | auto(&lt;field&gt;) | str(&lt;field&gt;) | ip(&lt;field&gt;) | num(&lt;field&gt;)

Description: The options that you can specify to sort the events.

&lt;field&gt;

Syntax: &lt;string&gt;

Description: The name of the field to sort.

auto

Syntax: auto(&lt;field&gt;)

Description: Determine automatically how to sort the field values.

ip

Syntax: ip(&lt;field&gt;)

Description: Interpret the field values as IP addresses.

num

Syntax: num(&lt;field&gt;)

Description: Interpret the field values as numbers.

str

Syntax: str(&lt;field&gt;)

Description: Order the field values by using the lexicographic order.


## Usage

The dedup command is a streaming command or a dataset processing command, depending on which arguments are specified with the command. For example, if you specify the &lt;sort-by-clause , the dedup command acts as a dataset processing command. All of the results must be collected before sorting. See Command types .

Avoid using the dedup command on the _raw field if you are searching over a large volume of data. If you search the _raw field, the text of every event in memory is retained which impacts your search performance. This is expected behavior. This behavior applies to any field with high cardinality and large size.


### Multivalue fields

To use the dedup command on multivalue fields, the fields must match all values to be deduplicated.


### Lexicographical order

Lexicographical order sorts items based on the values used to encode the items in computer memory. In Splunk software, this is almost always UTF-8 encoding, which is a superset of ASCII.

- Numbers are sorted before letters. Numbers are sorted based on the first digit. For example, the numbers 10, 9, 70, 100 are sorted lexicographically as 10, 100, 70, 9.

- Uppercase letters are sorted before lowercase letters.

- Symbols are not standard. Some symbols are sorted before numeric values. Other symbols are sorted before or after letters.


## Examples


### 1. Remove duplicate results based on one field

Remove duplicate search results with the same host value.

CODE

Copy

... | dedup host


```spl

... | dedup host

```



### 2. Remove duplicate results and sort results in ascending order

Remove duplicate search results with the same source value and sort the results by the _time field in ascending order.

CODE

Copy

... | dedup source sortby +_time


```spl

... | dedup source sortby +_time

```



### 3. Remove duplicate results and sort results in descending order

Remove duplicate search results with the same source value and sort the results by the _size field in descending order.

CODE

Copy

... | dedup source sortby -_size


```spl

... | dedup source sortby -_size

```



### 4. Keep the first 3 duplicate results

For search results that have the same source value, keep the first 3 that occur and remove all subsequent results.

CODE

Copy

... | dedup 3 source


```spl

... | dedup 3 source

```



### 5. Keep results that have the same combination of values in multiple fields

For search results that have the same source AND host values, keep the first 2 that occur and remove all subsequent results.

CODE

Copy

... | dedup 2 source host


```spl

... | dedup 2 source host

```



### 6. Remove only consecutive duplicate events

Remove only consecutive duplicate events. Keep non-consecutive duplicate events. In this example duplicates must have the same combination of values the source and host fields.

CODE

Copy

... | dedup consecutive=true source host


```spl

... | dedup consecutive=true source host

```



## See also

uniq
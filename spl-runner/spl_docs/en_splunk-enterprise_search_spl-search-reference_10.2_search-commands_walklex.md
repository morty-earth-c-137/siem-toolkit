
# walklex


## Description

Generates a list of terms or indexed fields from each bucket of event indexes.

Watch this Splunk How-To video, Using the Walklex Command , to see a demonstration about how to use this command.




> **Note: Due to the variable nature of merged_lexicon.lex and .tsidx files, the walklex command does not always return consistent results. The walklex command doesn't work on hot buckets. This command only works on warm or cold buckets, after the buckets have a merged lexicon file or single time-series index (tsidx) file. If neither of these files exist, a message is returned, as expected. This message doesn't indicate that there is a problem with the health of your environment.**



## Syntax

The required syntax is in bold .

| walklex

[ type=&lt;walklex-type&gt; ]

[ prefix=&lt;string&gt; | pattern=&lt;wc-string&gt; ]

&lt;index-list&gt;

[ splunk_server=&lt;wc-string&gt; ]

[ splunk_server_group=&lt;wc-string&gt; ]...


### Required arguments

&lt;index-list&gt;

Syntax: index=&lt;index-name&gt; index=&lt;index-name&gt; ...

Description: Limits the search to one or more indexes. For example, index=_internal .


### Optional arguments

prefix | pattern

Syntax: prefix=&lt;string&gt; | pattern=&lt;wc-string&gt;

Description: Limits results to terms that match a specific pattern or prefix. Either prefix or pattern can be specified but not both. Includes only buckets with a merged_lexicon file or a single tsidx file. This means that hot buckets are generally not included.

Default: pattern=\*

splunk_server

Syntax: splunk_server=&lt;wc-string&gt;

Description:

Specifies the distributed search peers from which to return results.

- If you are using Splunk Cloud Platform, omit this parameter.

- If you are using Splunk Enterprise, you can specify only one splunk_server argument. However, you can use a wildcard when you specify the server name to indicate multiple servers. For example, you can specify splunk_server=peer01 or splunk_server=peer\* . Use local to refer to the search head.

Default: All configured search peers return information

splunk_server_group

Syntax: splunk_server_group=&lt;wc-string&gt;

Description:

Limits the results to one or more server groups. You can specify a wildcard character in the string to indicate multiple server groups with similar names.

- If you are using Splunk Cloud Platform, omit this parameter.

Default: None

type

Syntax: type = ( all | field | fieldvalue | term )

Description:

Specifies which type of terms to return in the

lexicon

. See

Usage

for more information about using the


```spl

type

```


argument options.

- Use field to return only the unique field names in each index bucket.

- Use fieldvalue to include only indexed field terms.

- Use term to exclude all indexed field terms of the form &lt;field&gt;::&lt;value&gt; .

Default: all


## Usage

The walklex command is a generating command , which use a leading pipe character. The walklex command must be the first command in a search. See Command types .

When the Splunk software indexes event data, it segments each event into raw tokens using rules specified in segmenters.conf file. You might end up with raw tokens that are actually key-value pairs separated by an arbitrary delimiter such as an equal ( = ) symbol.

The following search uses the walklex and where commands to find the raw tokens in your index. It uses the stats command to count the raw tokens.

CODE

Copy

| walklex index=&lt;target-index&gt; | where NOT like(term, "%::%") | stats sum(count) by term


```spl

| walklex index=<target-index> | where NOT like(term, "%::%") | stats sum(count) by term

```



### Return only indexed field names

Specify the type=field argument to have walklex return only the field names from indexed fields.

The indexed fields returned by walklex can include default fields such as host , source , sourcetype , the date_\* fields, punct , and so on. It can also include additional indexed fields configured as such in props.conf and transforms.conf and created with the INDEXED_EXTRACTIONS setting or other WRITE_META methods. The discovery of this last set of additional indexed fields is likely to help you with accelerating your searches.


### Return the set of terms that are indexed fields with indexed values

Specify type=fieldvalue argument to have walklex return the set of terms from the index that are indexed fields with indexed values.

The type=fieldvalue argument returns the list terms from the index that are indexed fields with indexed values. Unlike the type=field argument, where the values returned are only the field names themselves, the type=fieldvalue argument returns indexed field names that have any field value.

For example, if the indexed field term is runtime::0.04 , the value returned by the type=fieldvalue argument is runtime::0.04 . The value returned by the type=field argument is runtime .


### Return all TSIDX keywords that are not part of an indexed field structure

Specify type=term to have walklex return the keywords from the TSIDX files that are not part of any indexed field structure. In other words, it excludes all indexed field terms of the form &lt;field&gt;::&lt;value&gt; .


### Return terms of all three types

When you do not specify a type, or when you specify type=all , walklex uses the default type=all argument. This causes walklex to return the terms in the index of all three types: field , fieldvalue , and term .




> **Note: When you use type=all , the indexed fields are not called out as explicitly as the fields are with the type=field argument. You need to split the term field on :: to obtain the field values from the indexed term.**



### Support for hot buckets

Because the walklex command doesn't work on hot buckets, recently loaded data displays in search results only after buckets have rolled over from hot to warm. You can either wait for buckets of an index to roll over from hot to warm on their own, or you can restart Splunk platform or manually roll the buckets over to warm. See Rolling buckets manually from hot to warm .


### Restrictions

The walklex command applies only to event indexes. It cannot be used with metrics indexes.

People who have search filters applied to one or more of their roles cannot use walklex unless they also have a role with either the run_walklex capability or the admin_all_objects capability. For more information about role-based search filters, see Create and manage roles with Splunk Web in Securing the Splunk Platform . For more information about role-based capabilities, see Define roles on the Splunk platform with capabilities , in Securing the Splunk Platform .


## Basic examples


### 1. Return the total count for each term in a specific bucket

The following example returns all of the terms in each bucket of the _internal index and finds the total count for each term.

CODE

Copy

| walklex index=_internal | stats sum(count) BY term


```spl

| walklex index=_internal | stats sum(count) BY term

```



### 2. Specifying multiple indexes

The following example returns all of the terms that start with foo in each bucket of the _internal and _audit indexes.

CODE

Copy

| walklex prefix=foo index=_internal index=_audit


```spl

| walklex prefix=foo index=_internal index=_audit

```



### 3. Use a pattern to locate indexed field terms

The following example returns all of the indexed field terms for each bucket that end with bar in the _internal index.

CODE

Copy

| walklex pattern=\*bar type=fieldvalue index=_internal


```spl

| walklex pattern=*bar type=fieldvalue index=_internal

```



### 4. Return all field names of indexed fields

The following example returns all of the field names of indexed fields in each bucket of the _audit index.

CODE

Copy

| walklex type=field index=_audit


```spl

| walklex type=field index=_audit

```



## See also

Commands

metadata

tstats
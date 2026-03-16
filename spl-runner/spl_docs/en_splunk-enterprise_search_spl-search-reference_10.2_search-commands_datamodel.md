
# datamodel


## Description

Examine and search data model datasets.

Use the datamodel command to return the JSON for all or a specified data model and its datasets. You can also search against the specified data model or a dataset within that datamodel.

A data model is a hierarchically-structured search-time mapping of semantic knowledge about one or more datasets. A data model encodes the domain knowledge necessary to build a variety of specialized searches of those datasets. For more information, see About data models and Design data models in the Knowledge Manager Manual .

The datamodel search command lets you search existing data models and their datasets from the search interface.

The datamodel command is a generating command and should be the first command in the search. Generating commands use a leading pipe character.


## Syntax

| datamodel [&lt;data model name&gt;] [&lt;dataset name&gt;] [&lt;data model search mode&gt;] [strict_fields=&lt;bool&gt;] [allow_old_summaries=&lt;bool&gt;] [summariesonly=&lt;bool&gt;]


### Required arguments

None


### Optional arguments

data model name

Syntax: &lt;string&gt;

Description: The name of the data model to search. When only the data model is specified, the search returns the JSON for the single data model.

dataset name

Syntax: &lt;string&gt;

Description: The name of a data model dataset to search. Must be specified after the data model name. The search returns the JSON for the single dataset.

data model search mode

Syntax: &lt;data model search result mode&gt; | &lt;data model search string mode&gt;

Description: You can use datamodel to run a search against a data model or a data model dataset that returns either results or a search string. If you want to do this, you must provide a &lt;data model search mode&gt; . There are two &lt;data model search mode&gt; subcategories: modes that return results and modes that return search strings. See Data model search mode options .

allow_old_summaries

Syntax: allow_old_summaries=&lt;bool&gt;

Description: This argument applies only to accelerated data models. When you change the constraints that define a data model but the Splunk software has not fully updated the summaries to reflect that change, the summaries may have some data that matches the old definition and some data that matches the new definition. By default, allow_old_summaries = false , which means that the search head does not use summary directories that are older than the new summary definition. This ensures that the datamodel search results always reflect your current configuration. When you set allow_old_summaries = true , datamodel uses both current summary data and summary data that was generated prior to the definition change. You can set allow_old_summaries=true in your search if you feel that the old summary data is close enough to the new summary data that its results are reliable.

Default: false

summariesonly

Syntax: summariesonly=&lt;bool&gt;

Description: This argument applies only to accelerated data models. When set to false, the datamodel search returns both summarized and unsummarized data for the selected data model. When set to true, the search returns results only from the data that has been summarized in TSIDX format for the selected data model. You can use this argument to identify what data is currently summarized for a given data model, or to ensure that a particular data model search runs efficiently.

Default: false

strict_fields

Syntax: strict_fields=&lt;bool&gt;

Description: Determines the scope of the datamodel search in terms of fields returned. When strict_fields=true , the search returns only default fields and fields that are included in the constraints of the specified data model dataset. When strict_fields=false , the search returns all fields defined in the data model, including fields inherited from parent data model datasets, extracted fields, calculated fields, and fields derived from lookups.

You can also arrange for strict_fields to default to false for a specific data model. See Design data models in the Knowledge Manager Manual .

Default: true


### Data model search mode options

data model search result mode

Syntax: search | flat | acceleration_search

Description: The modes for running searches on a data model or data model dataset that return results.


| Mode | Description |
| --- | --- |
| search | Returns the search results exactly how they are defined. |
| flat | Returns the same results as thesearch, except that it strips the hierarchical information from the field names. For example, wheresearchmode might return a field nameddmdataset.server, theflatmode returns a field namedserver. |
| acceleration_search | Runs the search that the search head uses to accelerate the data model. This mode works only on root event datasets and root search datasets that only use streaming commands. |


data model search string mode

Syntax: search_string | flat_string | acceleration_search_string

Description: These modes return the strings for the searches that the Splunk software is actually running against the data model when it runs your SPL through the corresponding &lt;data model search result mode&gt; . For example, if you choose acceleration_search_string , the Splunk software returns the search string it would actually use against the data model when you run your SPL through acceleration_search mode.


## Usage

The datamodel command is a report-generating command. See Command types .

Generating commands use a leading pipe character and should be the first command in a search.


## Examples


### 1. Return the JSON for all data models

Return JSON for all data models available in the current app context.

CODE

Copy

| datamodel


```spl

| datamodel

```





### 2. Return the JSON for a specific datamodel

Return JSON for the Splunk's Internal Audit Logs - SAMPLE data model, which has the model ID internal_audit_logs .

CODE

Copy

| datamodel internal_audit_logs


```spl

| datamodel internal_audit_logs

```





### 3. Return the JSON for a specific dataset

Return JSON for Buttercup Games's Client_errors dataset.

CODE

Copy

| datamodel Tutorial Client_errors


```spl

| datamodel Tutorial Client_errors

```



### 4. Run a search on a specific dataset

Run the search for Buttercup Games's Client_errors.

CODE

Copy

| datamodel Tutorial Client_errors search


```spl

| datamodel Tutorial Client_errors search

```



### 5. Run a search on a dataset for specific criteria

Search Buttercup Games's Client_errors dataset for 404 errors and count the number of events.

CODE

Copy

| datamodel Tutorial Client_errors search | search Tutorial.status=404  | stats count


```spl

| datamodel Tutorial Client_errors search | search Tutorial.status=404  | stats count

```



### 6. For an accelerated data model, reveal what data has been summarized over a selected time range

After the Tutorial data model is accelerated, this search uses the summariesonly argument in conjunction with timechart to reveal what data has been summarized for the Client_errors dataset over a selected time range.

CODE

Copy

| datamodel Tutorial summariesonly=true search | timechart span=1h count


```spl

| datamodel Tutorial summariesonly=true search | timechart span=1h count

```



## See also

pivot
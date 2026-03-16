
# savedsearch


## Description

Runs a saved search, or report, and returns the search results of a saved search. If the search contains replacement placeholder terms, such as $replace_me$ , the search processor replaces the placeholders with the strings you specify. For example:

CODE

Copy

|savedsearch mysearch replace_me="value"


```spl

|savedsearch mysearch replace_me="value"

```



## Syntax

| savedsearch &lt;savedsearch_name&gt; [&lt;savedsearch-options&gt;...]


### Required arguments

savedsearch_name

Syntax: &lt;string&gt;

Description: Name of the saved search to run.


### Optional arguments

savedsearch-options

Syntax: &lt;substitution-control&gt; | &lt;replacement&gt;

Description: Specify whether substitutions are allowed. If allowed, specify the key-value pair to use in the string substitution replacement.

substitution-control

Syntax: nosubstitution=&lt;bool&gt;

Description: If true, no string substitution replacements are made.

Default: false

replacement

Syntax: &lt;field&gt;=&lt;string&gt;

Description: A key-value pair to use in string substitution replacement.


## Usage

The savedsearch command is a generating command and must start with a leading pipe character.

The savedsearch command always runs a new search. To reanimate the results of a previously run search, use the loadjob command.

When the savedsearch command runs a saved search, the command always applies the permissions associated with the role of the person running the savedsearch command to the search. The savedsearch command never applies the permissions associated with the role of the person who created and owns the search to the search. This happens even when a saved search has been set up to run as the report owner.

See Determine whether to run reports as the report owner or user in the Reporting Manual .


### Time ranges

- If you specify All Time in the time range picker, the savedsearch command uses the time range that was saved with the saved search.

- If you specify any other time in the time range picker, the time range that you specify overrides the time range that was saved with the saved search.


### In standard mode federated searches over remote Splunk platform deployments

If you use Federated Search for Splunk to run searches over datasets on remote Splunk platform deployments, you can use the savedsearch command to run federated searches over saved search datasets on standard mode federated providers. See Run federated searches over remote Splunk platform deployments in Federated Search .

If you use savedsearch to run a federated search over a remote saved search dataset, you can use the command's string substitution replacement syntax to replace certain strings in the remote saved search with strings of your design, if the remote saved search string contains replacement placeholder terms. You can also use the nosubstitution argument to block string replacements in the remote saved search.

For example, say you have a federated index named remote1_ss_index_df_1 . This federated index maps to a saved search dataset on your remote standard mode federated provider that is based on a saved search with a replacement placeholder term for the value of the sourcetype field.

CODE

Copy

index=index_df_1 sourcetype=$replace_me$


```spl

index=index_df_1 sourcetype=$replace_me$

```


You can run the following federated search to insert a sourcetype value of universal_data_json into that remote saved search.

CODE

Copy

| savedsearch federated:remote1_ss_index_df_1 replace_me="universal_data_json"


```spl

| savedsearch federated:remote1_ss_index_df_1 replace_me="universal_data_json"

```





> **Note: If you use savedsearch to reference a saved search dataset that requires a string substitution and you do not provide a replacement string, Splunk software will return an "Error while replacing variable name" error message.**



## Examples


### Example 1

Run the saved search "mysecurityquery".

CODE

Copy

| savedsearch mysecurityquery


```spl

| savedsearch mysecurityquery

```



### Example2

Run the saved search "mysearch". Where the replacement placeholder term $replace_me$ appears in the saved search, use "value" instead.

CODE

Copy

|savedsearch mysearch replace_me="value"...


```spl

|savedsearch mysearch replace_me="value"...

```



## See also

search , loadjob
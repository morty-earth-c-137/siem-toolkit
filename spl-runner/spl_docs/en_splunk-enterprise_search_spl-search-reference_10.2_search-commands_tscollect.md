
# tscollect


| This feature is deprecated. |
| --- |
| Thetscollectcommand is deprecated in the Splunk platform as of version 7.3.0. Although this command continues to function, it might be removed in a future version. This command has been superseded by data models. SeeAccelerate data modelsin theKnowledge Manager Manual.In the version 7.3.0 Release Notes, seeDeprecated features. |



## Description

The tscollect command uses indexed fields to create time series index (tsidx) files in a namespace that you define. The result tables in these files are a subset of the data that you have already indexed. This then enables you to use the tstats command to search and report on these tsidx files instead of searching raw data. Because you are searching on a subset of the full index, the search should complete faster than it would otherwise.

The tscollect command creates multiple tsidx files in the same namespace. The command will begin a new tsidx file when it determines that the tsidx file it is currently creating has gotten big enough.

Only users with the indexes_edit capability can run this command. See Usage .




> **CAUTION: This command is considered risky because, if used incorrectly, it can pose a security risk or potentially lose data when it runs. As a result, this command triggers SPL safeguards. See SPL safeguards for risky commands in Securing the Splunk Platform .**



## Syntax

... | tscollect [namespace=&lt;string&gt;] [squashcase=&lt;bool&gt;] [keepresults=&lt;bool&gt;]


### Optional arguments

keepresults

Syntax: keepresults = true | false

Description: If true, tscollect outputs the same results it received as input. If false, tscollect returns the count of results processed (this is more efficient since it does not need to store as many results).

Default: false

namespace

Syntax: namespace=&lt;string&gt;

Description: Define a location for the tsidx file(s). If namespace is provided, the tsidx files are written to a directory of that name under the main tsidxstats directory (that is, within $SPLUNK_DB/tsidxstats ). These namespaces can be written to multiple times to add new data.

Default: If namespace is not provided, the files are written to a directory within the job directory of that search, and will live as long as the job does. If you have Splunk Enterprise, you can configure the namespace location by editing indexes.conf and setting the attribute tsidxStatsHomePath .

squashcase

Syntax: squashcase = true | false

Description: Specify whether or not the case for the entire field::value tokens are case sensitive when it is put into the lexicon. To create indexed field tsidx files that are similar to those created by Splunk Enterprise, set squashcase=true for results to be converted to all lowercase.

Default: false


## Usage

You must have the indexes_edit capability to run the tscollect command. By default, the admin role has this capability and the user and power roles do not have this capability.


## Examples

Example 1: Write the results table to tsidx files in namespace foo.

CODE

Copy

... | tscollect namespace=foo


```spl

... | tscollect namespace=foo

```


Example 2: Retrieve events from the main index and write the values of field foo to tsidx files in the job directory.

CODE

Copy

index=main | fields foo | tscollect


```spl

index=main | fields foo | tscollect

```



## See also

collect , stats , tstats
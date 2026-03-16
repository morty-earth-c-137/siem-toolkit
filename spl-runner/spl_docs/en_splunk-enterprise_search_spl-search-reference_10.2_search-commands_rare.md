
# rare


## Description

Displays the least common values in a field.

Finds the least frequent tuple of values of all fields in the field list. If the &lt;by-clause&gt; is specified, this command returns rare tuples of values for each distinct tuple of values of the group-by fields.

This command operates identically to the top command, except that the rare command finds the least frequent values instead of the most frequent values.


## Syntax

rare [&lt;rare-options&gt;...] &lt;field-list&gt; [&lt;by-clause&gt;]


### Required arguments

&lt;field-list&gt;

Syntax: &lt;string&gt;,...

Description: Comma-delimited list of field names.


### Optional arguments

&lt;rare-options&gt;

Syntax: countfield=&lt;string&gt; | limit=&lt;int&gt; | percentfield=&lt;string&gt; | showcount=&lt;bool&gt; | showperc=&lt;bool&gt;

Description: Options that specify the type and number of values to display. These are the same as the &lt;top-options&gt; used by the top command.

&lt;by-clause&gt;

Syntax: BY &lt;field-list&gt;

Description: The name of one or more fields to group by.


### Rare options

countfield

Syntax: countfield=&lt;string&gt;

Description: The name of a new field to write the value of count into.

Default: "count"

limit

Syntax: limit=&lt;int&gt;

Description: Specifies how many tuples to return. If you specify limit=0 , all values up to the maxresultrows are returned. Specifying a value larger than the maxresultrows produces an error. See Usage .

Default: 10

percentfield

Syntax: percentfield=&lt;string&gt;

Description: Name of a new field to write the value of percentage.

Default: "percent"

showcount

Syntax: showcount=&lt;bool&gt;

Description: Specifies whether to add a field to your results with the count of the tuple. The name of the field is controlled by the countield argument.

Default: true

showperc

Syntax: showperc=&lt;bool&gt;

Description: Specifies whether to add a field to your results with the relative prevalence of that tuple. The name of the field is controlled by the percentfield argument.

Default: true


## Usage

The rare command is a transforming command . See Command types .


### Limit maximum

The number of results returned by the rare command is controlled by the limit argument. The default value for the limit argument is 10. The default maximum is 50,000, which effectively keeps a ceiling on the memory that the rare command uses.

You can change this limit up to the maximum value specified in the maxresultrows setting in the [rare] stanza in the limits.conf file.

Splunk Cloud Platform

To change the maxresultrows setting, request help from Splunk Support. If you have a support contract, file a new case using the Splunk Support Portal at Support and Services . Otherwise, contact Splunk Customer Support .

Splunk Enterprise

To change the the maxresultrows setting in the limits.conf file, follow these steps.

Prerequisites

- Only users with file system access, such as system administrators, can edit configuration files.

- Review the steps in How to edit a configuration file in the Splunk Enterprise Admin Manual .


> **CAUTION: Never change or copy the configuration files in the default directory. The files in the default directory must remain intact and in their original location. Make changes to the files in the local directory.**


Steps

- Open or create a local limits.conf file in the desired path. For example, use the $SPLUNK_HOME/etc/apps/search/local path to apply this change only to the Search app.

- Under the [rare] stanza, change the value for the maxresultrows setting.


## Examples


### 1. Return the least common values in a field

Return the least common values in the url field. Limits the number of values returned to 5.

CODE

Copy

... | rare url limit=5


```spl

... | rare url limit=5

```



### 2. Return the least common values organized by host

Find the least common values in the user field for each host value. By default, a maximum of 10 results are returned.

CODE

Copy

... | rare user by host


```spl

... | rare user by host

```



## See also

Related commands

top

stats

sirare
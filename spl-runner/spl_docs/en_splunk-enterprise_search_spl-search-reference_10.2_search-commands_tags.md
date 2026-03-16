
# tags


## Description

Annotates specified fields in your search results with tags . If there are fields specified, only annotates tags for those fields. Otherwise, this command looks for tags for all fields. See About tags and aliases in the Knowledge Manager Manual .


## Syntax

The required syntax is in bold .

tags

[outputfield=&lt;field&gt;]

[inclname=&lt;bool&gt;]

[inclvalue=&lt;bool&gt;]

[allowed_tags=&lt;string&gt;]

&lt;field-list&gt;


### Required arguments

None.


### Optional arguments

allowed_tags

Syntax: allowed_tags=&lt;string&gt; | allowed_tags="&lt;string-list&gt;"

Description: If specified, returns only the tag names in the allowed_tags argument. You can specify multiple tags using a comma-separated, double-quoted string. For example: allowed_tags="host, sourcetype" .

Default : None

&lt;field-list&gt;

Syntax: &lt;field&gt; &lt;field&gt; ...

Description: Specify the fields that you want to output the tags from. The tag names are written to the outputfield .

Default : All fields

inclname

Syntax: inclname=true | false

Description: If outputfield is specified, this controls whether or not the event field name is added to the output field, along with the tag names. Specify true to include the field name.

Default : false

inclvalue

Syntax: inclvalue=true | false

Description: If outputfield is specified, controls whether or not the event field value is added to the output field, along with the tag names. Specify true to include the event field value.

Default : false

outputfield

Syntax: outputfield=&lt;field&gt;

Description: If specified, the tag names for all of the fields are written to this one new field. If not specified, a new field is created for each field that contains tags. The tag names are written to these new fields using the naming convention tag_name::&lt;field&gt; . In addition, a new field is created called tags that lists all of the tag names in all of the fields.

Default : New fields are created and the tag names are written to the new fields.


## Usage

The tags command is a distributable streaming command. See Command types .


### Viewing tag information

To view the tags in a table format, use a command before the tags command such as the stats command. Otherwise, the fields output from the tags command appear in the list of Interesting fields . See Examples .


### Using the &lt;outputfield&gt; argument

If outputfield is specified, the tag names for the fields are written to this field. By default, the tag names are written in the format &lt;field&gt;::&lt;tag_name&gt;. For example, sourcetype::apache .

If outputfield is specified, the inclname and inclvalue arguments control whether or not the field name and field values are added to the outputfield . If both inclname and inclvalue are set to true , then the format is &lt;field&gt;::&lt;value&gt;::&lt;tag_name&gt;. For example, sourcetype::access_combined_wcookie::apache .


## Examples


### 1. Results using the default settings


| This example uses the sample data from the Search Tutorial but should work with any format of Apache web access log. To try this example on your own Splunk instance, you must download the sample data and follow the instructions toget the tutorial data into Splunk. Use the time rangeAll timewhen you run the search. |
| --- |


This search looks for web access events and counts those events by host.

CODE

Copy

sourcetype=access_\*  | stats count by host


```spl

sourcetype=access_*  | stats count by host

```




The results look something like this:




| host | count |
| --- | --- |
| www1 | 13628 |
| www2 | 12912 |
| www3 | 12992 |


When you use the tags command without any arguments, two new fields are added to the results tag and tag::host .

CODE

Copy

sourcetype=access_\*  | stats count by host | tags


```spl

sourcetype=access_*  | stats count by host | tags

```




The results look something like this:




| host | count | tag | tag::host |
| --- | --- | --- | --- |
| www1 | 13628 | tag2 | tag2 |
| www2 | 12912 | tag1 | tag1 |
| www3 | 12992 |  |  |


There are no tags for host=www3 .



Add the


```spl

 sourcetype

```


field to the


```spl

stats

```


command BY clause.



CODE

Copy

sourcetype=access_\*  | stats count by host sourcetype | tags


```spl

sourcetype=access_*  | stats count by host sourcetype | tags

```




The results look something like this:




| host | sourcetype | count | tag | tag:host | tag::sourcetype |
| --- | --- | --- | --- | --- | --- |
| www1 | access_combined_wcookie | 13628 | apachetag2 | tag2 | apache |
| www2 | access_combined_wcookie | 12912 | apachetag1 | tag1 | apache |
| www3 | access_combined_wcookie | 12992 | apache |  | apache |


The tag field list all of the tags used in the events that contain the combination of host and sourcetype.

The tag::host field list all of the tags used in the events that contain that host value.

The tag::sourcetype field list all of the tags used in the events that contain that sourcetype value.


### 2. Specifying a list of fields

Return the tags for the host and eventtype fields.

CODE

Copy

... | tags host eventtype


```spl

... | tags host eventtype

```



### 3. Specifying an output field

Write the tags for all fields to the new field test .

CODE

Copy

...  | stats count by host sourcetype | tags outputfield=test


```spl

...  | stats count by host sourcetype | tags outputfield=test

```


The results look like this:


| host | sourcetype | count | test |
| --- | --- | --- | --- |
| www1 | access_combined_wcookie | 13628 | apachetag2 |
| www2 | access_combined_wcookie | 12912 | apachetag1 |
| www3 | access_combined_wcookie | 12992 | apache |



### 4. Including the field names in the search results

Write the tags for the host and sourcetype fields into the test field. New fields are returned in the output using the format host::&lt;tag&gt; or sourcetype::&lt;tag&gt; . Include the field name in the output.

CODE

Copy

...  | stats count by host sourcetype | tags outputfield=test inclname=t


```spl

...  | stats count by host sourcetype | tags outputfield=test inclname=t

```


The results look like this:


| host | sourcetype | count | test |
| --- | --- | --- | --- |
| www1 | access_combined_wcookie | 13628 | sourcetype::apachehost::tag2 |
| www2 | access_combined_wcookie | 12912 | sourcetype::apachehost::tag1 |
| www3 | access_combined_wcookie | 12992 | sourcetype::apache |



### 5. Identifying a specific a list of tags to return

Write the "error" and "group" tags for the host field into the test field. New fields are returned in the output using the format host::&lt;tag&gt; . Include the field name in the output.

CODE

Copy

index=main | tags outputfield=test inclname=t allowed_tags="error, group" host


```spl

index=main | tags outputfield=test inclname=t allowed_tags="error, group" host

```


If you don't have a command before the tags command that organizes the results in a table format, you will see the output of the tags command in the Interesting fields list, as shown in the following image:



Notice that the tag field in the list of Interesting fields shows that there are 3 tag values. Because the search specified that only the error and group tags should be returned to the test output field, those are the only tag values that appear in the image.


## See also

Related information

About tags and aliases in the Knowledge Manager Manual

Tag field-value pairs in Search in the Knowledge Manager Manual

Define and manage tags in Settings in the Knowledge Manager Manual

Commands

eval
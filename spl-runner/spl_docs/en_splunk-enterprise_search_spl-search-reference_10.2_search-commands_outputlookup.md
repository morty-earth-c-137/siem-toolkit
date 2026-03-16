
# outputlookup


## Description

Writes search results to a static lookup table, or KV store collection, that you specify.


> **CAUTION: This command is considered risky because, if used incorrectly, it can pose a security risk or potentially lose data when it runs. As a result, this command triggers SPL safeguards. See SPL safeguards for risky commands in Securing the Splunk Platform .**



## Syntax

The required syntax is in bold .

| outputlookup

[append=&lt;bool&gt;]

[create_empty=&lt;bool&gt;]

[override_if_empty=&lt;bool&gt;]

[max=&lt;int&gt;]

[key_field=&lt;field&gt;]

[allow_updates=&lt;bool&gt;]

[createinapp=&lt;bool&gt;]

[create_context=&lt;string&gt;]

[output_format=&lt;string&gt;]

&lt;filename&gt; | &lt;tablename&gt;


### Required arguments

You must specify one of the following required arguments, either filename or tablename .

filename

Syntax: &lt;string&gt;

Description: The name of the lookup file. The file must end with .csv or .csv.gz .

tablename

Syntax: &lt;string&gt;

Description: The name of the lookup table as specified by a stanza name in transforms.conf , which corresponds to the lookup definition. The lookup table can be configured for any lookup type (CSV, external, or KV store).

If your lookup file and the lookup definition that it is associated with have the same name, you can provide a tablename that is the same value as the corresponding filename without the .csv extension. For example, say you have a lookup file named staff.csv. If you associate that file with a lookup called staff , you can use either staff.csv or staff as the tablename with the outputlookup command. See Create a CSV lookup definition in the Splunk Enterprise Knowledge Manager Manual .


### Optional arguments

allow_updates

Syntax: allow_updates=&lt;bool&gt;

Description: The allow_updates argument is set to true by default if either the append argument is set to true or if the key_field argument is set to a valid field name. If allow_updates is set to true , the outputlookup command updates existing records and inserts new records. If allow_updates is set to false , the outputlookup only inserts records.

append

Syntax: append=&lt;bool&gt;

Description: The default setting, append=false , writes the search results to the .csv file or KV store collection. Fields that are not in the current search results are removed from the file. If append=true , the outputlookup command attempts to append search results to an existing .csv file or KV store collection. Otherwise, it creates a file. If there is an existing .csv file, the outputlookup command writes only the fields that are present in the previously existing .csv file. An outputlookup search that is run with append=true might result in a situation where the lookup table or collection is only partially updated. This means that a subsequent lookup or inputlookup search on that lookup table or collection might return stale data along with new data. The outputlookup command cannot append to .gz files.

Default: false

create_context

Syntax: create_context= app | user | system

Description: Specifies where the lookup table file is created. Ignored in favor of the createinapp argument if both arguments are used in the search. See Usage for details.

Default: app

create_empty

Syntax: create_empty=&lt;bool&gt;

Description: If set to true and there are no results, a zero-length file is created. When set to false and there are no results, no file is created. If the file previously existed, the file is deleted.

For example, suppose there is a system-level lookup called "test" with the lookup defined in "test.csv". There is also an app-level lookup with the same name. If an app overrides that "test.csv" in it's own app directory with an empty file create_empty=true , the app-level lookup behaves as if the lookup is empty. However, if there's no file at all create_empty=false at the app level, then the lookup file in the system-level is used.

Default: false

createinapp

Syntax: createinapp=&lt;bool&gt;

Description: Specifies whether the lookup table file is created in the system directory or the lookups directory for the current app context. Overrides the create_context argument if both arguments are used in the search. See Usage for details.

Default: true

key_field

Syntax: key_field=&lt;field&gt;

Description: For KV store-based lookups, uses the specified field name as the key to a value and replaces that value. An outputlookup search using the key_field argument might result in a situation where the lookup table or collection is only partially updated. A subsequent lookup or inputlookup search on that collection might return stale data along with new data. A partial update only occurs with concurrent searches, one with the outputlookup command and a search with the inputlookup command. It is possible that the inputlookup occurs when the outputlookup is still updating some of the records.

When key_field is used in an outputlookup search, by default, append is set to true , which appends search results to an existing KV store collection. You can override this default behavior by directly setting key_field with append set to false .

max

Syntax: max=&lt;int&gt;

Description: Specifies whether there is a limit to the number of rows to output to a CSV file or a KV store collection. For example, to write 50,000 rows to a CSV file or KV store collection, set max=50000 in your outputlookup search.

Default: no limit

output_format

Syntax: output_format=splunk_sv_csv | splunk_mv_csv

Description: Controls the output data format of the lookup. Use output_format=splunk_mv_csv when you want to output multivalued fields to a lookup table file, and then read the fields back into Splunk using the inputlookup command. The default, splunk_sv_csv outputs a CSV file which excludes the _mv_&lt;fieldname&gt; fields.

Default: splunk_sv_csv

override_if_empty

Syntax: override_if_empty=&lt;bool&gt;

Description: If override_if_empty=true and no results are passed to the output file, the existing output file is deleted, If override_if_empty=false and no results are passed to the output file, the command does not delete the existing output file.

Default: true


## Usage

The lookup table must be a CSV or GZ file, or a table name specified with a lookup table configuration in transforms.conf . The lookup table can refer to a KV store collection or a CSV lookup. The outputlookup command cannot be used with external lookups.

If you specify a lookup table file name with the .gz extension, the file that's created is compressed.


### Determine where the lookup table file is created

For CSV lookups, outputlookup creates a lookup table file for the results of the search. There are three locations where outputlookup can put the file it creates:

- The system lookups directory: $SPLUNK_HOME/etc/system/local/lookups

- The lookups directory for the current app context: $SPLUNK_HOME/etc/apps/&lt;app&gt;/lookups

- The app-based lookups directory for the user running the search: etc/users/&lt;user&gt;/&lt;app&gt;/lookups

You can use the createinapp or create_context arguments to determine where outputlookup creates the lookup table for a given search. If you try to use both of these arguments in the same search, createinapp argument overrides the create_context argument.

If you do not use either argument in your search, the create_context setting in limits.conf determines where outputlookup creates the lookup table file. This setting defaults to app if there is an app context when you run the search, or to system , if there is not an app context when you run the search.

To have outputlookup create the lookup table file in the system lookups directory, set createinapp=false or set create_context=system . Alternatively, if you do not have an app context when you run the search, leave both arguments out of the search and rely on the limits.conf version of create_context to put the lookup table file in the system directory. This last approach only works if the create_context setting in limits.conf has not been set to user .

To have outputlookup create the lookup table file in the lookups directory for the current app context, set createinapp=true or set create_context=app . Alternatively, if you do have an app context when you run the search, leave both arguments out of the search and rely on the limits.conf version of create_context to put the lookup table file in the app directory. This last approach only works if the create_context setting in limits.conf has not been set to user .

To have outputlookup create the lookup table file in the lookups directory for the user running the search, set create_context=user . Alternatively, if you want all outputlookup searches to create lookup table files in user lookup directories by default, you can set create_context=user in limits.conf . The createinapp and create_context arguments can override this setting if they are used in the search.


> **Note: If the lookup table file already exists in the location to which it is written, the existing version of the file is overwritten with the results of the outputlookup search.**



### Restrict write access to lookup table files with check_permission

For permissions in CSV lookups in Splunk Enterprise deployments, use the check_permission field in transforms.conf and outputlookup_check_permission in limits.conf to restrict write access to users with the appropriate permissions when using the outputlookup command. Both check_permission and outputlookup_check_permission default to false , which means that, by default, Splunk software doesn't perform any permissions checks. As a result, all users can write to lookup table files, regardless of their capabilities.

To ensure that only users who have the admin or power role can write to a shared CSV lookup file by default, instruct Splunk software to verify permission settings for lookups for users by setting check_permission and outputlookup_check_permission to true . Note that the permission checks are performed only after the lookup stanza has been created.

For Splunk Cloud deployments, direct editing of configuration files, such as transforms.conf , is not supported. Instead, users must set permissions at the application level in the correct transforms.conf file.

For more information about creating lookups, see About lookups in the Knowledge Manager Manual .

For more information about App Key Value Store collections, see About KV store in the Admin Manual .


### Append results

Suppose you have an existing CSV file that contains fields A, D, and J. The results of your search are fields A, C, and J. If you run a search with outputlookup append=false , then fields A, C, and J are written to the CSV file. Field D is not retained.

If you run a search with outputlookup append=true , then only the fields that are currently in the file are preserved. In this example, fields A and J are written to the CSV file. Field C is lost because it does not already exist in the CSV file. Field D is retained.

You can work around this issue by using the eval command to add a field to your CSV file before you run the search. For example, if your CSV file is named users , you would do something like this:

CODE

Copy

| inputlookup users | eval c=null | outputlookup users append=false ....


```spl

| inputlookup users | eval c=null | outputlookup users append=false ....

```


Then run your search and pipe the results to the fields command for the fields in the file that you want to preserve.

CODE

Copy

... | fields A C J | outputlookup append=true users


```spl

... | fields A C J | outputlookup append=true users

```



### Multivalued fields

When you output to a static lookup table, the outputlookup command merges values in a multivalued field into single space-delimited value. This does not apply to a KV store collection.


## Examples


### 1. Write to a lookup table using settings in the transforms.conf file

Write to usertogroup lookup table as specified in the transforms.conf file.

CODE

Copy

| outputlookup usertogroup


```spl

| outputlookup usertogroup

```



### 2. Write to a lookup file in a specific system or app directory

Write to users.csv lookup file under $SPLUNK_HOME/etc/system/lookups or $SPLUNK_HOME/etc/apps/\*/lookups .

CODE

Copy

| outputlookup users.csv


```spl

| outputlookup users.csv

```



### 3. Specify not to override the lookup file if no results are returned

Write to users.csv lookup file, if results are returned, under $SPLUNK_HOME/etc/system/lookups or $SPLUNK_HOME/etc/apps/\*/lookups . Do not delete the users.csv file if no results are returned.

CODE

Copy

| outputlookup users.csv override_if_empty=false


```spl

| outputlookup users.csv override_if_empty=false

```



### 4. Write to a KV store collection

Write food inspection events for Shalimar Restaurant to a KV store collection called kvstorecoll . This collection is referenced in a lookup table called kvstorecoll_lookup .

CODE

Copy

index=sf_food_health sourcetype=sf_food_inspections name="SHALIMAR RESTAURANT" | outputlookup kvstorecoll_lookup


```spl

index=sf_food_health sourcetype=sf_food_inspections name="SHALIMAR RESTAURANT" | outputlookup kvstorecoll_lookup

```



### 5. Overwrite KV store collections

By default, append is set to true when the key_field is used with the outputlookup command. If you don't want to append search results to an existing KV store collection, you can override the default behavior by directly setting key_field with append=false .

For example, in the following outputlookup search, the KV store called accounts is appended. This is because key_field sets append=true by default.

CODE

Copy

| makeresults 
| eval key=1 
| outputlookup key_field=key accounts


```spl

| makeresults 
| eval key=1 
| outputlookup key_field=key accounts

```


However, in the following outputlookup search, the KV store called accounts is overwritten because append=false . In this case, the append subsearch runs before the main search, which empties the entire KV store before the fields are written to accounts .

CODE

Copy

| makeresults 
| eval key=1 
| outputlookup append=false key_field=key accounts


```spl

| makeresults 
| eval key=1 
| outputlookup append=false key_field=key accounts

```


Alternatively, if you want your entire lookup to reflect your search results and you don't mind using the default system-generated keys, eliminate key_field=key from your outputlookup search, like this.

CODE

Copy

| makeresults 
| eval key=1 
| outputlookup accounts


```spl

| makeresults 
| eval key=1 
| outputlookup accounts

```



### 6. Write from a CSV file to a KV store collection

Write the contents of a CSV file to the KV store collection kvstorecoll using the lookup table kvstorecoll_lookup . This requires usage of both inputlookup and outputlookup commands.

CODE

Copy

| inputlookup customers.csv | outputlookup kvstorecoll_lookup


```spl

| inputlookup customers.csv | outputlookup kvstorecoll_lookup

```



### 7. Update field values for a single KV store collection record

Update field values for a single KV store collection record. This requires you to use the inputlookup , outputlookup , and eval commands. The record is indicated by the value of its internal key ID (the _key field) and is updated with a new customer name and customer city. The record belongs to the KV store collection kvstorecoll , which is accessed through the lookup table kvstorecoll_lookup .

CODE

Copy

| inputlookup kvstorecoll_lookup | search _key=544948df3ec32d7a4c1d9755 | eval CustName="Vanya Patel" | eval CustCity="Springfield" | outputlookup kvstorecoll_lookup append=True key_field=_key


```spl

| inputlookup kvstorecoll_lookup | search _key=544948df3ec32d7a4c1d9755 | eval CustName="Vanya Patel" | eval CustCity="Springfield" | outputlookup kvstorecoll_lookup append=True key_field=_key

```


To learn how to obtain the internal key ID values of the records in a KV store collection, see Example 5 for the inputlookup command.


## See also

Commands

collect

inputlookup

lookup

inputcsv

mcollect

meventcollect

outputcsv

outputtext
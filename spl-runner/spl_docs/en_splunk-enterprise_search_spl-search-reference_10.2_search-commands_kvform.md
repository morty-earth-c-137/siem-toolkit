
# kvform


## Description

Extracts key-value pairs from events based on a form template that describes how to extract the values.




> **Note: For Splunk Cloud Platform, you must create a private app to extract key-value pairs from events. If you are a Splunk Cloud administrator with experience creating private apps, see Manage private apps in your Splunk Cloud Platform deployment in the Splunk Cloud Admin Manual . If you have not created private apps, contact your Splunk account representative for help with this customization.**



## Syntax

kvform [form=&lt;string&gt;] [field=&lt;field&gt;]


### Optional arguments

form

Syntax: form=&lt;string&gt;

Description: Specify a .form file located in a $SPLUNK_HOME/etc/apps/\*/forms/ directory.

field

Syntax: field=&lt;field_name&gt;

Description: Uses the field name to look for .form files that correspond to the field values for that field name. For example, your Splunk deployment uses the splunkd and mongod sourcetypes. If you specify field=sourcetype , the kvform command looks for the splunkd.form and mongod.form in the $SPLUNK_HOME/etc/apps/\*/forms/ directory.

Default: sourcetype


## Usage

Before you can use the kvform command, you must:

- Create the forms directory in the appropriate application path. For example $SPLUNK_HOME/etc/apps/&lt;app_name&gt;/forms .

- Create the .form files and add the files to the forms directory.


### Format for the .form files

A .form file is essentially a text file of all static parts of a form. It might be interspersed with named references to regular expressions of the type found in the transforms.conf file.

An example .form file might look like this:

CODE

Copy

Students Name: [[string:student_name]]
Age: [[int:age]] Zip: [[int:zip]]


```spl

Students Name: [[string:student_name]]
Age: [[int:age]] Zip: [[int:zip]]

```



### Specifying a form

If the form argument is specified, the kvform command uses the &lt;form_name&gt;.form file found in the Splunk configuration forms directory. For example, if form=sales_order , the kvform command looks for a sales_order.form file in the $SPLUNK_HOME/etc/apps/&lt;app_name&gt;/forms directory for all apps. All the events processed are matched against the form, trying to extract values.


### Specifying a field

If you specify the field argument, the the kvform command looks for forms in the forms directory that correspond to the values for that field. For example, if you specify field=error_code , and an event has the field value error_code=404 , the command looks for a form called 404.form in the $SPLUNK_HOME/etc/apps/&lt;app_name&gt;/forms directory.


### Default value

If no form or field argument is specified, the kvform command uses the default value for the field argument, which is sourcetype . The kvform command looks for &lt;sourcetype_value&gt;.form files to extract values.


## Examples


### 1. Extract values using a specific form

Use a specific form to extract values from.

CODE

Copy

... | kvform form=sales_order


```spl

... | kvform form=sales_order

```



### 2. Extract values using a field name

Specify field=sourcetype to extract values from forms such as splunkd.form and mongod.form . If there is a form for a source type, values are extracted from that form. If one of the source types is access_combined but there is no access_combined.form file, that source type is ignored.

CODE

Copy

... | kvform field=sourcetype


```spl

... | kvform field=sourcetype

```



### 3. Extract values using the eventtype field

CODE

Copy

... | kvform field=eventtype


```spl

... | kvform field=eventtype

```



## See also

Commands

extract

multikv

rex

xmlkv
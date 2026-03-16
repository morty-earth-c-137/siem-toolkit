
# fromjson


## Description

Converts JSON-formatted objects into multivalue fields. If you give the fromjson command a single field name that points to proper JSON objects, fromjson returns keys as fields and key values as field values.


## Syntax

Required syntax is in bold .

| fromjson&lt;string&gt;

[ prefix=&lt;string&gt;]


### Optional arguments

prefix

Syntax: prefix=&lt;string&gt;

Description: Prepends a string to the fields that fromjson extracts from a JSON-formatted object. For example, including prefix=my_ in the search adds my_ to the beginning of field names in the results.



Default: none


## Usage

The fromjson command is a streaming command , which means that it turns JSON-formatted objects into fields as each JSON object is received. See Types of commands .


## Examples


### 1. Expand a JSON object to create new fields

Use the fromjson command to expand a JSON-formatted object and return the values in the search result. This example creates two new fields called name and age , and outputs the corresponding values in the search results.

CODE

Copy

| makeresults | eval object=json_object("name", "Albert", "age", 63) | fromjson object


```spl

| makeresults | eval object=json_object("name", "Albert", "age", 63) | fromjson object

```


The results look like this.


| _time | age | name | object |
| --- | --- | --- | --- |
| 2020-11-09 17:01:22 | 63 | Albert | {"name":"Albert", "age":63} |



### 2. Prepend the name of extracted fields

You can use the optional argument prefix to prepend a string to fields extracted from a JSON-formatted object. This example creates two new fields called json_name and json_age .

CODE

Copy

| makeresults | eval object=json_object("name", "Albert", "age", 63) | fromjson object prefix=my_


```spl

| makeresults | eval object=json_object("name", "Albert", "age", 63) | fromjson object prefix=my_

```


The results look something like this.


| _time | my_age | my_name | object |
| --- | --- | --- | --- |
| 2020-11-09 17:01:22 | 63 | Albert | {"name":"Albert", "age":63} |



### 3. Expand nested JSON objects

When you use fromjson to expand JSON-formatted objects into multivalue fields, you can retain the formatting of JSON objects by nesting them within the main object. In the following example, the object called json_obj with the key-value pair "school" and "city", is nested within another JSON object called object .

CODE

Copy

| makeresults | eval object=json_object("age", 19, "name", "Sally", "new", false(), "classes", json_array("math", "history", "science"), "another_json_object", json_object("school", "city"), "null", null)| fromjson object


```spl

| makeresults | eval object=json_object("age", 19, "name", "Sally", "new", false(), "classes", json_array("math", "history", "science"), "another_json_object", json_object("school", "city"), "null", null)| fromjson object

```


The results look something like this.


| _time | age | another_json_obj | classes | name | new | object |
| --- | --- | --- | --- | --- | --- | --- |
| 2020-11-09 17:01:22 | 19 | {"school":"city"} | mathhistoryscience | Sally | false | {"age":19,"name":"Sally","new":false,"classes":["math","history","science"],"another_json_object":{"school":"city"},"null":null} |



## See also

Commands

tojson

Evaluation functions

JSON functions
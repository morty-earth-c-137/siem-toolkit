
# JSON functions

The following table describes the functions that are available for you to use to create or manipulate JSON objects:


| Description | JSON function |
| --- | --- |
| Creates a new JSON object from key-value pairs. | json_object |
| Evaluates whether a value can be parsed as JSON. If the value is JSON, the function returns the value. Otherwise, the function returns null. | json |
| Appends elements to the contents of a valid JSON object. | json_append |
| Creates a JSON array using a list of values. | json_array |
| Maps the elements of a JSON array to a multivalued field. | json_array_to_mv |
| Removes one or more keys and their corresponding values from the specified JSON object. | json_delete |
| Converts a value to an array of JSON objects with key and value fields. | json_entries |
| Extends the contents of a valid JSON object with the values of an array. | json_extend |
| Returns either a JSON array or a Splunk software native type value from a field and zero or more paths. | json_extract |
| Returns Splunk software native type values from a piece of JSON by matching literal strings in the event and extracting them as keys. | json_extract_exact |
| Returns TRUE if the field value is a JSON key in the provided JSON object. | json_has_key_exact |
| Returns the keys from the key-value pairs in a JSON object. The keys are returned as a JSON array. | json_keys |
| Inserts or overwrites values for a JSON node with the values provided and return an updated JSON object. | json_set |
| Generates or overwrites a JSON object using the key-value pairs specified. | json_set_exact |
| Evaluates whether a JSON object uses valid JSON syntax and returns either TRUE or FALSE. | json_valid |



## json_object(&lt;members&gt;)

Creates a new JSON object from members of key-value pairs.


### Usage

If you specify a string for a &lt;key&gt; or &lt;value&gt; , you must enclose the string in double quotation marks. A &lt;key&gt; must be a string. A &lt;value&gt; can be a string, number, Boolean, null, multivalue field, array, or another JSON object.

You can use this function with the eval and where commands, and as part of evaluation expressions with other commands.


### Examples

These examples show different ways to use the json_object function to create JSON objects in your events.


### 1. Create a basic JSON object

The following example creates a basic JSON object { "name": "maria" } .

CODE

Copy

... | eval name = json_object("name", "maria")


```spl

... | eval name = json_object("name", "maria")

```



### 2. Create a JSON object using a multivalue field

The following example creates a multivalue field called firstnames that uses the key name and contains the values "maria" and "arun". The JSON object created is { "name": ["maria", "arun"] } .

CODE

Copy

... | eval firstnames = json_object("name", json_array("maria", "arun"))


```spl

... | eval firstnames = json_object("name", json_array("maria", "arun"))

```



### 3. Create a JSON object using a JSON array

The following example creates a JSON object that uses a JSON array for the values.

CODE

Copy

... | eval  locations = json_object("cities", json_array("London", "Sydney", "Berlin", "Santiago"))


```spl

... | eval  locations = json_object("cities", json_array("London", "Sydney", "Berlin", "Santiago"))

```


The result is the JSON object { "cities": ["London", "Sydney", "Berlin", "Santiago"] } .


### 4. Create a nested JSON object

The following example creates a nested JSON object that uses other JSON objects and a multivalue or JSON array field called gamelist .

CODE

Copy

...| eval gamelist = json_array("Pandemic", "Forbidden Island", "Castle Panic"), games = json_object("category", json_object("boardgames", json_object("cooperative", gamelist)))


```spl

...| eval gamelist = json_array("Pandemic", "Forbidden Island", "Castle Panic"), games = json_object("category", json_object("boardgames", json_object("cooperative", gamelist)))

```


The result is this JSON object:

JSON

Copy

{
  "games": {
    "category": {
      "boardgames": {
        "cooperative": [ "Pandemic", "Forbidden Island", "Castle Panic" ]
      }
    }
  }
}


```spl

{
  "games": {
    "category": {
      "boardgames": {
        "cooperative": [ "Pandemic", "Forbidden Island", "Castle Panic" ]
      }
    }
  }
}

```



## json(&lt;value&gt;)

Evaluates whether a value can be parsed as JSON. If the value is in a valid JSON format, the function returns the value. Otherwise, the function returns null.


### Usage

A &lt;value&gt; can be any kind of value such as string, number, Boolean, null, or JSON array or object.


### Examples


### 1. Identify a JSON value

This example shows how you can use the json function to confirm that a value is JSON. The following search verifies that {"animal" : "pony"} is a JSON value by returning its value, {"animal":"pony"} .

CODE

Copy

... | eval animals = json_object("animal", "pony"), result = json(animals)


```spl

... | eval animals = json_object("animal", "pony"), result = json(animals)

```


The search results look something like this:


| _time | animals | result |
| --- | --- | --- |
| 2023-02-22 14:39:50 | {"animal": "pony"} | {"animal": "pony"} |



### 2. Compare multiple results to identify JSON values

The following example shows how to use the json function to determine if the values in a field are JSON arrays or objects.

Consider the following search results:


| _time | bridges | city |
| --- | --- | --- |
| 2023-04-26 21:10:45 | ["bridges",{"name":"Tower Bridge"},{"length":"801"},{"name":"Millennium Bridge"},{"length":"1066"}] | London |
| 2023-04-26 21:10:45 | ["bridges",{"name":"Rialto Bridge"},{"length":"157"},{"name":"Bridge of Sighs"},{"length":"36"},{"name":"Ponte della Paglia"}] | Venice |
| 2023-04-26 21:10:45 | Golden Gate Bridge | San Francisco |


When you add the json evaluation function to the following search, the results in the bridgesAsJson field identifies which values in the bridges field are JSON values:

CODE

Copy

... | eval bridgesAsJson = json(bridges)


```spl

... | eval bridgesAsJson = json(bridges)

```


When the value is JSON, the value is returned in the bridgesAsJson field. When the value is not JSON, the function returns null. The results look like something like this:


| _time | bridges | bridgesAsJson | city |
| --- | --- | --- | --- |
| 2023-04-26 21:10:45 | ["bridges",{"name":"Tower Bridge"},{"length":"801"},{"name":"Millennium Bridge"},{"length":"1066"}] | [{"name":"Tower Bridge","length":801}, {"name":"Millennium Bridge","length":1066}] | London |
| 2023-04-26 21:10:45 | [{"name":"Rialto Bridge","length":157}, {"name":"Bridge of Sighs","length":36}, {"name":"Ponte della Paglia"}] | [{"name":"Rialto Bridge","length":157}, {"name":"Bridge of Sighs","length":36}, {"name":"Ponte della Paglia"}] | Venice |
| 2023-04-26 21:10:45 | Golden Gate Bridge |  | San Francisco |



## json_append(&lt;json&gt;, &lt;path_value_pairs&gt;)

This function appends values to the ends of indicated arrays within a JSON document. This function provides a JSON eval function equivalent to the multivalue mvappend function.


### Usage

The json_append function always has at least three function inputs: &lt;json&gt; (the name of a valid JSON document such as a JSON object), and at least one &lt;path&gt; and &lt;value&gt; pair.

If &lt;json&gt; does not reference a valid JSON document, such as a JSON object, the function outputs nothing.

The json_append function evaluates &lt;path_value_pairs&gt; from left to right. When a path-value pair is evaluated, the function updates the &lt;json&gt; document. The function then evaluates the next path-value pair against the updated document.

You can use this function with the eval and where commands, and as part of evaluation expressions with other commands.


### Use &lt;path&gt; to designate a JSON document value

Each &lt;path&gt; designates an array or value within the &lt;json&gt; document. The json_append function adds the corresponding &lt;value&gt; to the end of the value designated by the &lt;path&gt; . The following table explains what json_append does depending on what the &lt;path&gt; specifies.


| If&lt;path&gt;specifies... | ...This is whatjson_appenddoes with the corresponding&lt;value&gt; |
| --- | --- |
| An array with one or more values. | json_appendadds the corresponding&lt;value&gt;to the end of that array. |
| An empty array | json_appendadds the corresponding&lt;value&gt;to that array, creating an array with a single value. |
| A scalar or object value | json_appendautowraps the scalar or object value within an array and adds the corresponding&lt;value&gt;to the end of that array. |


The json_append function ignores path-value pairs for which the &lt;path&gt; does not identify any valid value in the JSON document.


### Append arrays as single elements

When the new &lt;value&gt; is an array, json_append appends the array as a single element. For example, if a json_array &lt;path&gt; leads to the array ["a", "b", "c"] and its &lt;value&gt; is the array ["d", "e", "f"] , the result is ["a", "b", "c", ["d", "e", "f"]] .

Appending arrays as single elements separates json_append from json_extend , a similar function that flattens arrays and objects into separate elements as it appends them. When json_extend takes the example in the preceding paragraph, it returns ["a", "b", "c", "d", "e", "f"] .


### Examples

The following examples show how you can use json_append to append values to arrays within a JSON document.


### 1. Add a string to an array

Say you have an object named ponies that contains an array named ponylist : ["Minty", "Rarity", "Buttercup"] . This is the search you would run to append "Fluttershy" to ponylist .

CODE

Copy

... | eval ponies = json_object("ponylist", json_array("Minty", "Rarity", "Buttercup")), 
updatePonies = json_append(ponies, "ponylist", "Fluttershy")


```spl

... | eval ponies = json_object("ponylist", json_array("Minty", "Rarity", "Buttercup")), 
updatePonies = json_append(ponies, "ponylist", "Fluttershy")

```


The output of that eval statement is {"ponylist": ["Minty", "Rarity", "Buttercup", "Fluttershy"]} .


### 2. Append a string to a nested object

This example has a &lt;path&gt; with the value Fluttershy.ponySkills . Fluttershy.ponySkills references an array of an object that is nested within ponyDetails , the source object. The query uses json_append to add a string to the nested object array.

CODE

Copy

... | eval ponyDetails = json_object("Fluttershy", json_object("ponySkills", json_array("running", "jumping"))), ponyDetailsUpdated = json_append(ponyDetails, "Fluttershy.ponySkills", "codebreaking")


```spl

... | eval ponyDetails = json_object("Fluttershy", json_object("ponySkills", json_array("running", "jumping"))), ponyDetailsUpdated = json_append(ponyDetails, "Fluttershy.ponySkills", "codebreaking")

```


The output of this eval statement is ponyDetailsUpdated = {"Fluttershy":{"ponySkills":["running","jumping","codebreaking"]}}


## json_array(&lt;values&gt;)

Creates a JSON array using a list of values.


### Usage

A &lt;value&gt; can be any kind of value such as string, number, or Boolean. You can also use the json_object function to specify values.

You can use this function with the eval and where commands, and as part of evaluation expressions with other commands.


### Examples

These examples show different ways to use the json_array function to create JSON arrays in your events.


### 1. Create a basic JSON array

The following example creates a simple array ["buttercup", "fluttershy", "rarity"] .

CODE

Copy

... | eval ponies = json_array("buttercup", "fluttershy", "rarity")


```spl

... | eval ponies = json_array("buttercup", "fluttershy", "rarity")

```



### 2. Create an JSON array from a string and a JSON object

The following example uses a string dubois and the json_object function for the array values.

CODE

Copy

... | eval surname = json_array("dubois", json_object("name", "patel"))


```spl

... | eval surname = json_array("dubois", json_object("name", "patel"))

```


The result is the JSON array [ "dubois", {"name": "patel}" ] .


## json_array_to_mv(&lt;json_array&gt;, &lt;boolean&gt;)

This function maps the elements of a proper JSON array into a multivalue field.


### Usage

You can use this function with the eval and where commands, and as part of evaluation expressions with other commands.

If the &lt;json array&gt; input to the function is not a valid JSON array, the function outputs nothing.

Use the &lt;boolean&gt; input to specify that the json_array_to_mv function should preserve bracketing quotes on JSON-formatted strings. The &lt;boolean&gt; input defaults to false() .


| Syntax | Description |
| --- | --- |
| json_array_to_mv(&lt;json_array&gt;, false())orjson_array_to_mv(&lt;json_array&gt;) | By default (or when you explicitly set it tofalse()), thejson_array_to_mvfunction removes bracketing quotes from JSON string data types when it converts an array into a multivalue field. |
| json_array_to_mv(&lt;json_array&gt;, true()) | When set totrue(), thejson_array_to_mvfunction preserves bracketing quotes on JSON string data types when it converts an array into a multivalue field. |



### Example

This example demonstrates usage of the json_array_to_mv function to create simple multivalue fields out of JSON data.

The following example creates a simple array: ["Buttercup", "Fluttershy", "Rarity"] . Then it maps that array into a multivalue field named my_little_ponies with the values Buttercup , Fluttershy , and Rarity . The function removes the quote characters when it converts the array elements into field values.

CODE

Copy

... | eval ponies = json_array("Buttercup", "Fluttershy", "Rarity"), my_sweet_ponies = json_array_to_mv(ponies)


```spl

... | eval ponies = json_array("Buttercup", "Fluttershy", "Rarity"), my_sweet_ponies = json_array_to_mv(ponies)

```


If you change this search so it has my_sweet_ponies = json_array_to_mv(ponies,true()) , you get an array with the values "Buttercup" , "Fluttershy" , and "Rarity" . Setting the function to true causes the function to preserve the quote characters when it converts the array elements into field values.


## json_delete(&lt;object&gt;,&lt;keys&gt;)

Use json_delete to remove one or more keys and their corresponding values from the specified JSON object.

The original JSON object is not modified. Instead, a new object is returned.


### Usage

The json_delete function uses two arguments:

- The &lt;object&gt; argument identifies the JSON object from which you want to delete key-value pairs.

- The &lt;keys&gt; argument identifies one or more keys that you want delete. The corresponding values are also deleted.

Array indexing is not supported.

You can use this function with the eval and where commands, and as part of evaluation expressions with other commands. See the eval and where commands.


### Specifying keys

You can specify the &lt;keys&gt; in 2 ways, as shown in the following table:


| Method | Example |
| --- | --- |
| A comma-separated list | json_delete(object, "SSN", "accounts") |
| An array | json_delete(object, ["SSN", "accounts"] |



### Nested keys

You can delete key-value pairs from nested keys. However, deleting key names that contain the dot character ( . ) is not supported. For example, suppose you have the key student.name , which has the value Claudia . Using json_delete(obj, "student.name") looks for the nested object name under the key student , which doesn't exist.


### Examples


### 1. Delete key-value pairs in an object

The following search deletes several key-value pairs from a JSON object. A new JSON object is returned in a field called sales_account .

- This search uses the eval command to create a JSON object literal in a field called object .

- Another eval command is used with the json_delete function to remove several key-value pairs from the JSON object literal, including the values in an array.

JSON

Copy

...| eval object = {"name":"Wei Zhang", "SSN":"123-45-6789", "city":"Seattle", "accounts":["Hagal Quartz", "Caladan Water", "Arrakis Spices"]}
| eval sales_account = json_delete(object, "SSN", "accounts")


```spl

...| eval object = {"name":"Wei Zhang", "SSN":"123-45-6789", "city":"Seattle", "accounts":["Hagal Quartz", "Caladan Water", "Arrakis Spices"]}
| eval sales_account = json_delete(object, "SSN", "accounts")

```


The results look like this:


| object | sales_account |
| --- | --- |
| {"name":"Wei Zhang", "SSN":"123-45-6789", "city":"Seattle", "accounts":["Hagal Quartz", "Caladan Water", "Arrakis Spices"]} | {"name":"Wei Zhang", "city":"Seattle"} |





> **Note: You don't have to use 2 separate eval commands for this search example. You can specify multiple eval command operations separated by commas. For example: ...| eval object = {"name":"Wei Zhang", "SSN":"123-45-6789", "city":"Seattle", "accounts":["Hagal Quartz", "Caladan Water", "Arrakis Spices"]}, sales_account = json_delete(object, "SSN", "accounts")**



### 2. Delete a key-value pair in a nested object

The following search removes a key-value pair from the addresses nested object. A new JSON object is returned in a field called result .

- This search uses the eval command to create a JSON object literal in a field called employee .

- The search then uses another eval command with the json_delete function to remove the email key-value pair from the addresses nested object.

JSON

Copy

...| eval employee = {"name":"Celestino Paulo", "company":"Isthmus Pastimes", "addresses": {"email":"celestino@sample.com", "office":"edificio 890 Avenida Demetrio Panama City Panama"}}
| eval result = json_delete(employee, "addresses.email")


```spl

...| eval employee = {"name":"Celestino Paulo", "company":"Isthmus Pastimes", "addresses": {"email":"celestino@sample.com", "office":"edificio 890 Avenida Demetrio Panama City Panama"}}
| eval result = json_delete(employee, "addresses.email")

```


The results look like this:


| employee | results |
| --- | --- |
| {"name":"Celestino Paulo", "company":"Isthmus Pastimes", "addresses": {"email":"celestino@sample.com", "office":"edificio 890 Avenida Demetrio Panama City Panama"}} | {"name":"Celestino Paulo", "company":"Isthmus Pastimes", "addresses": {"office":"edificio 890 Avenida Demetrio Panama City Panama"}} |



### 3. Delete a key-value pair in a nested object in a pipeline

Consider the following JSON object, which contains Buttercup Games supplier information including a nested object with address information.

JSON

Copy

{"name":"Celestino Paulo", "company":"Isthmus Pastimes", 
   "addresses": {
       "email":"celestino@sample.com", 
       "office":"edificio 890 Avenida Demetrio 
                 Panama City Panama"}
"name":"David Mayer", "company":"Euro Games", 
   "addresses": {
      "email":"david@sample.com", 
      "office":"567 Pariser Platz 2 10117 
                Berlin Germany "}
"name":"Wei Zhang", "company":"Tiger Fun", 
   "addresses": {
       "email":"wei@sample.com", 
       "office":"678 Chome-10-5 Akasaka 
                 Minato City Tokyo 107-8420 Japan"}
"name":"Rutherford Sullivan", "company":"Blarney Games", 
   "addresses": {
       "email":"rutherford@sample.com", 
       "office":"789 Market St Sleveen 
                 Kinsale Co. Cork P17 E068 Ireland"}
}


```spl

{"name":"Celestino Paulo", "company":"Isthmus Pastimes", 
   "addresses": {
       "email":"celestino@sample.com", 
       "office":"edificio 890 Avenida Demetrio 
                 Panama City Panama"}
"name":"David Mayer", "company":"Euro Games", 
   "addresses": {
      "email":"david@sample.com", 
      "office":"567 Pariser Platz 2 10117 
                Berlin Germany "}
"name":"Wei Zhang", "company":"Tiger Fun", 
   "addresses": {
       "email":"wei@sample.com", 
       "office":"678 Chome-10-5 Akasaka 
                 Minato City Tokyo 107-8420 Japan"}
"name":"Rutherford Sullivan", "company":"Blarney Games", 
   "addresses": {
       "email":"rutherford@sample.com", 
       "office":"789 Market St Sleveen 
                 Kinsale Co. Cork P17 E068 Ireland"}
}

```


The following pipeline uses the eval command with the json_delete function to remove the email key-value pair from the addresses nested object. A new JSON object is returned in a field called cleaned .

PYTHON

Copy

$pipeline = from $source | eval cleaned = json_delete(employee, ["addresses.email"]) | into $destination


```spl

$pipeline = from $source | eval cleaned = json_delete(employee, ["addresses.email"]) | into $destination

```



## json_entries(&lt;value&gt;)


### Description

|Returns the key-value entries from the top-level key-value pairs in a JSON object. The entries are returned as a JSON array of JSON objects with fields key and value .


### Usage

You can use this function with the eval , fieldformat , and where commands, and as part of eval expressions.

The &lt;value&gt; argument can be a valid JSON object or the name of a field that contains a valid JSON object.

Use this function in type tests to confirm that the format of an object is what is required and expected.


### Basic example

The following example returns a field named entries containing the array [{"key":"a","value":1},{"key":"b","value":2}] .

JSON

Copy

| makeresults
| eval entries=json_entries("{\"a\": 1, \"b\": 2}")


```spl

| makeresults
| eval entries=json_entries("{\"a\": 1, \"b\": 2}")

```



### Extended example

The employee_record field in these events contains JSON objects.


| _time | employee_record |
| --- | --- |
| 2024-12-17 21:22:43 | {"name":"maria","age":25,"status":"full-time"} |
| 2024-12-17 21:22:43 | {"name":"charlie","age":21,"status":"part-time"} |


The following eval command returns the top-level members of the objects from the employee_record field and stores them in a field named array_format :

CODE

Copy

... | eval array_format = json_entries(employee_record)


```spl

... | eval array_format = json_entries(employee_record)

```


The results look like this:


| _time | array_format | employee_record |
| --- | --- | --- |
| 2024-12-17 21:22:43 | [{"key":"name","value":"maria"},{"key":"age","value":25},{"key":"status","value":"full-time"}] | {"name":"maria","age":25,"status":"full-time"} |
| 2024-12-17 21:22:43 | [{"key":"name","value":"charlie"},{"key":"age","value":21},{"key":"status","value":"part-time"}] | {"name":"charlie","age":21,"status":"part-time"} |



## json_extend(&lt;json&gt;, &lt;path_value_pairs&gt;)

Use json_extend when you want to append multiple values at once to an array. json_extend flattens arrays into their component values and appends those values to the ends of indicated arrays within a valid JSON document.


### Usage

The json_extend function always has at least three function inputs: &lt;json&gt; (the name of a valid JSON document such as a JSON object), and at least one &lt;path&gt; and &lt;value&gt; pair. The &lt;value&gt; must be an array. When given valid inputs, json_extend always outputs an array.

If &lt;json&gt; does not reference a valid JSON document, such as a JSON object, the function outputs nothing.

json_extend evaluates &lt;path_value_pairs&gt; from left to right. When json_extend evaluates a path-value pair, it updates the &lt;json&gt; document. json_extend then evaluates the next path-value pair against the updated document.

You can use json_extend with the eval and where commands, and as part of evaluation expressions with other commands.


### Use &lt;path&gt; to designate a JSON document value

Each &lt;path&gt; designates an array or value within the &lt;json&gt; document. The json_extend function adds the values of the corresponding &lt;array&gt; after the last value of the array designated by the &lt;path&gt; . The following table explains what json_extend does depending on what the &lt;path&gt; specifies.


| If&lt;path&gt;specifies... | ...This is whatjson_extenddoes with the corresponding array values |
| --- | --- |
| An array with one or more values. | json_extendadds the corresponding array values to the end of that array. |
| An empty array | json_extendadds the corresponding array values to that array. |
| A scalar or object value | json_extendautowraps the scalar or object value within an array and adds the corresponding array values to the end of that array. |


json_extend ignores path-value pairs for which the &lt;path&gt; does not identify any valid value in the JSON document.


### How json_extend flattens arrays before it appends them

The json_extend function flattens arrays as it appends them to the specified value. "Flattening" refers to the act of breaking the array down into its component values. For example, if a json_extend &lt;path&gt; leads to the array ["a", "b", "c"] and its &lt;value&gt; is the array ["d", "e", "f"] , the result is ["a", "b", "c", "d", "e", "f"] .

Appending arrays as individual values separates json_extend from json_append , a similar function that appends the &lt;value&gt; as a single element. When json_append takes the example in the preceding paragraph, it returns ["a", "b", "c", ["d", "e", "f"]] .


### Examples

The following examples show how you can use json_extend to append multiple values at once to arrays within a JSON document.


### 1. Extend an array with a set of string values

You start with an object named fakeBandsInMovies that contains an array named fakeMovieBandList : ["The Blues Brothers", "Spinal Tap", "Wyld Stallyns"] . This is the search you would run to extend that list with three more names of fake bands from movies.

CODE

Copy

... | eval fakeBandsInMovies = json_object("fakeMovieBandList", json_array("The Blues Brothers", "Spinal Tap", "Wyld Stallyns")), updateBandList = json_extend(fakeBandsInMovies, "fakeMovieBandList", json_array("The Soggy Bottom Boys", "The Weird Sisters", "The Barden Bellas"))


```spl

... | eval fakeBandsInMovies = json_object("fakeMovieBandList", json_array("The Blues Brothers", "Spinal Tap", "Wyld Stallyns")), updateBandList = json_extend(fakeBandsInMovies, "fakeMovieBandList", json_array("The Soggy Bottom Boys", "The Weird Sisters", "The Barden Bellas"))

```


The output of this eval statement is:

JSON

Copy

{
  "fakeMovieBandList": [
    "The Blues Brothers",
    "Spinal Tap",
    "Wyld Stallyns",
    "The Soggy Bottom Boys",
    "The Weird Sisters",
    "The Barden Bellas"
  ]
}


```spl

{
  "fakeMovieBandList": [
    "The Blues Brothers",
    "Spinal Tap",
    "Wyld Stallyns",
    "The Soggy Bottom Boys",
    "The Weird Sisters",
    "The Barden Bellas"
  ]
}

```



### 2. Extend an array with an object

This example has an object named dndChars that contains an array named characterClasses . You want to update this array with an object from a secondary array. Here is a search you could run to achieve that goal.

CODE

Copy

... | eval dndChars = json_object("characterClasses", json_array("wizard", "rogue", "barbarian")), array2 = json_array(json_object("artifact", "deck of many things")), updatedParty = json_extend(dndChars, "characterClasses", array2)


```spl

... | eval dndChars = json_object("characterClasses", json_array("wizard", "rogue", "barbarian")), array2 = json_array(json_object("artifact", "deck of many things")), updatedParty = json_extend(dndChars, "characterClasses", array2)

```


The output of this eval statement is:

JSON

Copy

{
  "updatedParty": [
    "wizard",
    "rogue",
    "barbarian",
    {
      "artifact": "deck of many things"
    }
  ]
}


```spl

{
  "updatedParty": [
    "wizard",
    "rogue",
    "barbarian",
    {
      "artifact": "deck of many things"
    }
  ]
}

```


Note that when json_extend flattens array2 , it removes the object from the array. Otherwise the output would be:

JSON

Copy

{
  "updatedParty": [
    "wizard",
    "rogue",
    "barbarian",
    {
      "artifact": "deck of many things"
    }
  ]
}


```spl

{
  "updatedParty": [
    "wizard",
    "rogue",
    "barbarian",
    {
      "artifact": "deck of many things"
    }
  ]
}

```



## json_extract(&lt;json&gt;, &lt;paths&gt;)

This function returns a value from a piece of JSON and zero or more paths. The value is returned in either a JSON array, or a Splunk software native type value.


> **Note: If a JSON object contains a value with a special character, such as a period, json_extract can't access it. Use the json_extract_exact function for those situations.**


See json_extract_exact .


### Usage

What is converted or extracted depends on whether you specify a piece of JSON, or JSON and one or more paths.


| Syntax | Description |
| --- | --- |
| json_extract(&lt;json&gt;) | Converts a JSON field to the Splunk software native type. For example:Converts a JSON string to a stringConverts a JSON Boolean to a BooleanConverts a JSON null to a null |
| json_extract(&lt;json&gt;, &lt;path&gt;) | Extracts the value specified by&lt;path&gt;from&lt;json&gt;, and converts the value to the native type. This can be a JSON array if the path leads to an array. |
| json_extract(&lt;json&gt;, &lt;path&gt;, &lt;path&gt;, ...) | Extracts all of the paths from&lt;json&gt;and returns it as a JSON array. |


You can use this function with the eval and where commands, and as part of evaluation expressions with other commands.


### Examples

These examples use this JSON object, which is in a field called cities in an event:

JSON

Copy

{
  "cities": [
    {
      "name": "London",
      "Bridges": [
        { "name": "Tower Bridge", "length": 801 },
        { "name": "Millennium Bridge", "length": 1066 }
      ]
    },
    {
      "name": "Venice",
      "Bridges": [
        { "name": "Rialto Bridge", "length": 157 },
        { "name": "Bridge of Sighs", "length": 36 },
        { "name": "Ponte della Paglia" }
      ]
    },
    {
      "name": "San Francisco",
      "Bridges": [
        { "name": "Golden Gate Bridge", "length": 8981 },
        { "name": "Bay Bridge", "length": 23556 }
      ]
    }
  ]
}


```spl

{
  "cities": [
    {
      "name": "London",
      "Bridges": [
        { "name": "Tower Bridge", "length": 801 },
        { "name": "Millennium Bridge", "length": 1066 }
      ]
    },
    {
      "name": "Venice",
      "Bridges": [
        { "name": "Rialto Bridge", "length": 157 },
        { "name": "Bridge of Sighs", "length": 36 },
        { "name": "Ponte della Paglia" }
      ]
    },
    {
      "name": "San Francisco",
      "Bridges": [
        { "name": "Golden Gate Bridge", "length": 8981 },
        { "name": "Bay Bridge", "length": 23556 }
      ]
    }
  ]
}

```



### 1. Extract the entire JSON object in a field

The following example returns the entire JSON object from the cities field. The cities field contains only one object. The key is the entire object. This extraction can return any type of value.

CODE

Copy

... |eval extracted_cities = json_extract(cities,"{}")


```spl

... |eval extracted_cities = json_extract(cities,"{}")

```


Here are the results of the search:


| Field | Results |
| --- | --- |
| extract_cities | {"cities":[{"name":"London","Bridges":[{"name":"Tower Bridge","length":801},{"name":"Millennium Bridge","length":1066}]},{"name":"Venice","Bridges":[{"name":"Rialto Bridge","length":157},{"name":"Bridge of Sighs","length":36},{"name":"Ponte della Paglia"}]},{"name":"San Francisco","Bridges":[{"name":"Golden Gate Bridge","length":8981},{"name":"Bay Bridge","length":23556}]}]} |



### 2. Extract the first nested JSON object in a field

The following example extracts the information about the city of London from the JSON object. This extraction can return any type of value.

The {&lt;num&gt;} indexing demonstrated in this example search only works when the &lt;path&gt; maps to a JSON array. In this case the {0} maps to the "0" item in the array, which is London. If the example used {1} it would select Venice from the array.

CODE

Copy

... | eval London=json_extract(cities,"{0}")


```spl

... | eval London=json_extract(cities,"{0}")

```


Here are the results of the search:


| Field | Results |
| --- | --- |
| London | {"name":"London","Bridges":[{"name":"Tower Bridge","length":801},{"name":"Millennium Bridge","length":1066}]} |



### 3. Extract the third nested JSON object in a field

The following example extracts the information about the city of San Francisco from the JSON object. This extraction can return any type of value.

CODE

Copy

... | eval San_Francisco=json_extract(cities,"{2}")


```spl

... | eval San_Francisco=json_extract(cities,"{2}")

```


Here are the results of the search:


| Field | Results |
| --- | --- |
| San_Francisco | {"name":"San Francisco","Bridges":[{"name":"Golden Gate Bridge","length":8981},{"name":"Bay Bridge","length":23556}]} |



### 4. Extract a specific key from each nested JSON object in a field

The following example extracts the names of the cities from the JSON object. This extraction can return any type of value.

CODE

Copy

... | eval my_cities=json_extract(cities,"{}.name")


```spl

... | eval my_cities=json_extract(cities,"{}.name")

```


Here are the results of the search:


| Field | Results |
| --- | --- |
| my_cities | ["London","Venice","San Francisco"] |



### 5. Extract a specific set of key-value pairs from each nested JSON object in a field

The following example extracts the information about each bridge from every city from the JSON object. This extraction can return any type of value.

CODE

Copy

... | eval Bridges=json_extract(cities,"{}.Bridges{}")


```spl

... | eval Bridges=json_extract(cities,"{}.Bridges{}")

```


Here are the results of the search:


| Field | Results |
| --- | --- |
| Bridges | [{"name":"Tower Bridge","length":801},{"name":"Millennium Bridge","length":1066},{"name":"Rialto Bridge","length":157},{"name":"Bridge of Sighs","length":36},{"name":"Ponte della Paglia"},{"name":"Golden Gate Bridge","length":8981},{"name":"Bay Bridge","length":23556}] |



### 6. Extract a specific value from each nested JSON object in a field

The following example extracts the names of the bridges from all of the cities from the JSON object. This extraction can return any type of value.

CODE

Copy

... | eval Bridge_names=json_extract(cities,"{}.Bridges{}.name")


```spl

... | eval Bridge_names=json_extract(cities,"{}.Bridges{}.name")

```


Here are the results of the search:


| Field | Results |
| --- | --- |
| Bridge_names | ["Tower Bridge","Millennium Bridge","Rialto Bridge","Bridge of Sighs","Ponte della Paglia","Golden Gate Bridge","Bay Bridge"] |



### 7. Extract a specific key-value pair from a specific nested JSON object in a field

The following example extracts the name and length of the first bridge from the third city from the JSON object. This extraction can return any type of value.

CODE

Copy

... | eval GG_Bridge=json_extract(cities,"{2}.Bridges{0}")


```spl

... | eval GG_Bridge=json_extract(cities,"{2}.Bridges{0}")

```


Here are the results of the search:


| Field | Results |
| --- | --- |
| GG_Bridge | {"name":"Golden Gate Bridge","length":8981} |



### 8. Extract a specific value from a specific nested JSON object in a field

The following example extracts the length of the first bridge from the third city from the JSON object. This extraction can return any type of value.

CODE

Copy

... | eval GG_Bridge_length=json_extract(cities,"{2}.Bridges{0}.length")


```spl

... | eval GG_Bridge_length=json_extract(cities,"{2}.Bridges{0}.length")

```


Here are the results of the search:


| Field | Results |
| --- | --- |
| GG_Bridge_length | 8981 |



## json_extract_exact(&lt;json&gt;, &lt;keys&gt;)

Like the json_extract function, this function returns a Splunk software native type value from a piece of JSON. The main difference between these functions is that the json_extract_exact function does not use paths to locate and extract values, but instead matches literal strings in the event and extracts those strings as keys.

See json_extract .


### Usage

The json_extract_exact function treats strings for key extraction literally. This means that the function does not support explicitly nested paths. You can set paths with nested json_array / json_object function calls.


| Syntax | Description |
| --- | --- |
| json_extract_exact(&lt;json&gt;) | Converts a JSON field to the Splunk software native type. For example:Converts a JSON string to a stringConverts a JSON Boolean to a BooleanConverts a JSON null to a null |
| json_extract_exact(&lt;json&gt;, &lt;string&gt;) | Extracts the key specified by&lt;string&gt;from&lt;json&gt;, and converts the key to the Splunk software native type. This can be a JSON array if the path leads to an array. |
| json_extract_exact(&lt;json&gt;, &lt;string&gt;, &lt;string&gt;, ...) | Extracts all of the strings from&lt;json&gt;and returns them as a JSON array of keys. |


You can use this function with the eval and where commands, and as part of evaluation expressions with other commands.


### Example

Suppose you have a JSON event that looks like this: {"system.splunk.path":"/opt/splunk/"}

If you want to extract system.splunk.path from that event, you can't use the json_extract function because of the period characters. Instead, you would use json_extract_exact , as shown in the following search:

CODE

Copy

... | eval extracted_path=json_extract_exact(splunk_path, "system.splunk.path")


```spl

... | eval extracted_path=json_extract_exact(splunk_path, "system.splunk.path")

```



## json_has_key_exact(&lt;object&gt;, &lt;key&gt;)


### Description

This function evaluates whether a JSON object contains the specified key and returns either TRUE or FALSE.


### Usage

You can use this function with the eval , fieldformat , and where commands, and as part of eval expressions.

The &lt;object&gt; argument identifies the JSON object that you want to check for a specific key. This argument can be a valid JSON object or the name of a field that contains a valid JSON object.

The &lt;key&gt; argument identifies the key that you want to check for in the JSON object. This argument can be a string or the name of a field that contains a string.

You can use this function directly with the where command in searches, but the eval command can't directly accept a Boolean value. You must specify the function inside another function, such as the if function, which can accept a Boolean value as an input.


### Basic examples

The following example returns has key , indicating that the name key exists in the provided JSON object.

CODE

Copy

... | eval test=if(json_has_key_exact(json_object("name", "charlie"), "name"), "has key", "doesn't have key")


```spl

... | eval test=if(json_has_key_exact(json_object("name", "charlie"), "name"), "has key", "doesn't have key")

```


The following example returns has key , indicating that the "charlie.garcia" key exists in the provided JSON object. The function treats the dot character ( . ) in "charlie.garcia" as a string literal, not as a nested object in JSON format.

JSON

Copy

| makeresults
| eval test=if(json_has_key_exact("{\"charlie.garcia\":10}", "charlie.garcia"), "has key", "doesn't have key")


```spl

| makeresults
| eval test=if(json_has_key_exact("{\"charlie.garcia\":10}", "charlie.garcia"), "has key", "doesn't have key")

```



### Extended example

The employee_record field in these events contains JSON objects.


| _time | employee_record |
| --- | --- |
| 2024-12-17 21:22:43 | {"name":"maria","age":25,"status":"full-time"} |
| 2024-12-17 21:22:43 | {"name":"charlie","age":21,"region":"US"} |


The following eval command checks whether the objects in the employee_record field contain the status key, and stores the results in a field named test_results .

CODE

Copy

... | eval test_results=if(json_has_key_exact(employee_record, "status"), "has key", "doesn't have key")


```spl

... | eval test_results=if(json_has_key_exact(employee_record, "status"), "has key", "doesn't have key")

```


The results look like this:


| _time | employee_record | test_results |
| --- | --- | --- |
| 2024-12-17 21:22:43 | {"name":"maria","age":25,"status":"full-time"} | has key |
| 2024-12-17 21:22:43 | {"name":"charlie","age":21,"region":"US"} | doesn't have key |



## json_keys(&lt;json&gt;)

Returns the keys from the key-value pairs in a JSON object. The keys are returned as a JSON array.


### Usage

You can use this function with the eval and where commands, and as part of evaluation expressions with other commands.

The json_keys function cannot be used on JSON arrays.


### Examples


### 1. Return a list of keys from a JSON object

Consider the following JSON object, which is in the bridges field:


| bridges |
| --- |
| {"name": "Clifton Suspension Bridge", "length": 1352, "city": "Bristol", "country": "England"} |


This example extracts the keys from the JSON object in the bridges field:

CODE

Copy

... | eval bridge_keys = json_keys(bridges)


```spl

... | eval bridge_keys = json_keys(bridges)

```


Here are the results of the search:


| bridge_keys |
| --- |
| ["name", "length", "city", "country"] |



### 2. Return a list of keys from multiple JSON objects

Consider the following JSON objects, which are in separate rows in the bridges field:


| bridges |
| --- |
| {"name": "Clifton Suspension Bridge", "length": 1352, "city": "Bristol", "country": "England"} |
| {"name":"Rialto Bridge","length":157, "city": "Venice", "region": "Veneto", "country": "Italy"} |
| {"name": "Helix Bridge", "length": 918, "city": "Singapore", "country": "Singapore"} |
| {"name": "Tilikum Crossing", "length": 1700, "city": "Portland", "state": "Oregon", "country": "United States"} |


This example extracts the keys from the JSON objects in the bridges field:

CODE

Copy

... | eval bridge_keys = json_keys(bridges)


```spl

... | eval bridge_keys = json_keys(bridges)

```


Here are the results of the search:


| bridge_keys |
| --- |
| ["name", "length", "city", "country"] |
| ["name", "length", "city", "region", "country"] |
| ["name", "length", "city", "country"] |
| ["name", "length", "city", "state", "country"] |



## json_set(&lt;json&gt;, &lt;path_value_pairs&gt;)

Inserts or overwrites values for a JSON node with the values provided and returns an updated JSON object.

Similar to the json_set_exact function. See json_set_exact


### Usage

You can use this function with the eval and where commands, and as part of evaluation expressions with other commands.

- If the path contains a list of keys, all of the keys in the chain are created if the keys don't exist.

- If there's a mismatch between the JSON object and the path, the update is skipped and doesn't generate an error. For example, for object {"a": "b"}, json_set(.., "a.c", "d") produces no results since "a" has a string value and "a.c" implies a nested object.

- If the value already exists and is of a matching non-value type, the json_set function overwrites the value by default. A value type match isn't enforced. For example, you can overwrite a number with a string, Boolean, null, and so on.


### Examples

These examples use this JSON object, which is in a field called games in an event:

JSON

Copy

{
  "category": {
    "boardgames": {
      "cooperative": [
        {
          "name": "Pandemic"
        },
        {
          "name": "Forbidden Island"
        },
        {
          "name": "Castle Panic"
        }
      ]
    }
  }
}


```spl

{
  "category": {
    "boardgames": {
      "cooperative": [
        {
          "name": "Pandemic"
        },
        {
          "name": "Forbidden Island"
        },
        {
          "name": "Castle Panic"
        }
      ]
    }
  }
}

```



### 1. Overwrite a value in an existing JSON array

The following example overwrites the value "Castle Panic" in the path [category.boardgames.cooperative] in the JSON object. The value is replaced with "name":"Sherlock Holmes: Consulting Detective" . The results are placed into a new field called my_games .

The position count starts with 0. The third position is 2, which is why the example specifies {2} in the path.

JSON

Copy

... | eval my_games = json_set(games,"category.boardgames.cooperative{2}", "name":"Sherlock Holmes: Consulting Detective")


```spl

... | eval my_games = json_set(games,"category.boardgames.cooperative{2}", "name":"Sherlock Holmes: Consulting Detective")

```


Here are the results of the search:


| Field | Results |
| --- | --- |
| my_games | {"category":{"boardgames":{"cooperative":["name":"Pandemic", "name":"Forbidden Island", "name":"Sherlock Holmes: Consulting Detective"]}}} |



### 2. Insert a list of values in an existing JSON object

The following example inserts a list of popular games ["name":"Settlers of Catan", "name":"Terraforming Mars", "name":"Ticket to Ride"] into the path [category.boardgames.competitive] in the JSON object.

Because the key competitive doesn't exist in the path, the key is created. The json_array function is used to append the value list to the boardgames JSON object.

CODE

Copy

...| eval my_games = json_set(games,"category.boardgames.competitive", json_array(json_object("name", "Settlers of Catan"), json_object("name", "Terraforming Mars"), json_object("name", "Ticket to Ride")))


```spl

...| eval my_games = json_set(games,"category.boardgames.competitive", json_array(json_object("name", "Settlers of Catan"), json_object("name", "Terraforming Mars"), json_object("name", "Ticket to Ride")))

```


Here are the results of the search:


| Field | Results |
| --- | --- |
| my_games | {"category":{"boardgames":{"cooperative":["name":"Pandemic", "name":"Forbidden Island", "name":"Sherlock Holmes: Consulting Detective"],"competitive": ["name":"Settlers of Catan", "name":"Terraforming Mars", "name":"Ticket to Ride"]}}} |


The JSON object now looks like this:

JSON

Copy

{
  "category": {
    "boardgames": {
      "cooperative": [
        {
          "name": "Pandemic"
        },
        {
          "name": "Forbidden Island"
        },
        {
          "name": "Castle Panic"
        }
      ]
    },
    "competitive": [
      {
        "name": "Settlers of Catan"
      },
      {
        "name": "Terraforming Mars"
      },
      {
        "name": "Ticket to Ride"
      }
    ]
  }
}


```spl

{
  "category": {
    "boardgames": {
      "cooperative": [
        {
          "name": "Pandemic"
        },
        {
          "name": "Forbidden Island"
        },
        {
          "name": "Castle Panic"
        }
      ]
    },
    "competitive": [
      {
        "name": "Settlers of Catan"
      },
      {
        "name": "Terraforming Mars"
      },
      {
        "name": "Ticket to Ride"
      }
    ]
  }
}

```



### 3. Insert a set of key-value pairs in an existing JSON object

The following example inserts a set of key-value pairs that specify if the game is available using a Boolean value. These pairs are inserted into the path [category.boardgames.competitive] in the JSON object. The json_array function is used to append the key-value pairs list to the boardgames JSON object.

CODE

Copy

...| eval my_games = json_set(games,"category.boardgames.competitive{}.available", true())


```spl

...| eval my_games = json_set(games,"category.boardgames.competitive{}.available", true())

```


Here are the results of the search:


| Field | Results |
| --- | --- |
| my_games | {"category":{"boardgames":{"cooperative":["name":"Pandemic", "name":"Forbidden Island", "name":"Sherlock Holmes: Consulting Detective"],"competitive": ["name":"Settlers of Catan", "available":true, "name":"Terraforming Mars", "available":true, "name":"Ticket to Ride", "available":true]}}} |


The JSON object now looks like this:

JSON

Copy

{
  "category": {
    "boardgames": {
      "cooperative": [
        {
          "name": "Pandemic"
        },
        {
          "name": "Forbidden Island"
        },
        {
          "name": "Castle Panic"
        }
      ]
    },
    "competitive": [
      {
        "name": "Settlers of Catan",
        "available": true
      },
      {
        "name": "Terraforming Mars",
        "available": true
      },
      {
        "name": "Ticket to Ride",
        "available": true
      }
    ]
  }
}


```spl

{
  "category": {
    "boardgames": {
      "cooperative": [
        {
          "name": "Pandemic"
        },
        {
          "name": "Forbidden Island"
        },
        {
          "name": "Castle Panic"
        }
      ]
    },
    "competitive": [
      {
        "name": "Settlers of Catan",
        "available": true
      },
      {
        "name": "Terraforming Mars",
        "available": true
      },
      {
        "name": "Ticket to Ride",
        "available": true
      }
    ]
  }
}

```


If the Settlers of Catan game is out of stock, you can overwrite the value for the available key with the value false() .

For example:

CODE

Copy

... | eval my_games = json_set(games,"category.boardgames.competitive{0}.available", false())


```spl

... | eval my_games = json_set(games,"category.boardgames.competitive{0}.available", false())

```


Here are the results of the search:


| Field | Results |
| --- | --- |
| my_games | {"category":{"boardgames":{"cooperative":["name":"Pandemic", "name":"Forbidden Island", "name":"Sherlock Holmes: Consulting Detective"],"competitive": ["name":"Settlers of Catan", "available":false, "name":"Terraforming Mars", "available":true, "name":"Ticket to Ride", "available":true]}}} |


The JSON object now looks like this:

JSON

Copy

{
  "category": {
    "boardgames": {
      "cooperative": [
        {
          "name": "Pandemic"
        },
        {
          "name": "Forbidden Island"
        },
        {
          "name": "Castle Panic"
        }
      ]
    },
    "competitive": [
      {
        "name": "Settlers of Catan",
        "available": false
      },
      {
        "name": "Terraforming Mars",
        "available": true
      },
      {
        "name": "Ticket to Ride",
        "available": true
      }
    ]
  }
}


```spl

{
  "category": {
    "boardgames": {
      "cooperative": [
        {
          "name": "Pandemic"
        },
        {
          "name": "Forbidden Island"
        },
        {
          "name": "Castle Panic"
        }
      ]
    },
    "competitive": [
      {
        "name": "Settlers of Catan",
        "available": false
      },
      {
        "name": "Terraforming Mars",
        "available": true
      },
      {
        "name": "Ticket to Ride",
        "available": true
      }
    ]
  }
}

```



## json_set_exact(&lt;json&gt;, &lt;key_value_pairs&gt;)

Generates or overwrites a JSON object using the key-value pairs that you specify.

Similar to the json_set function. See json_set


### Usage

You can use the json_set_exact function with the eval and where commands, and as part of evaluation expressions with other commands.

- The json_set_exact function interprets the keys as literal strings, including special characters. This function does not interpret strings separated by period characters as keys for nested objects.

- If you supply multiple key-value pairs to json_set_exact , the function outputs an array.

- The json_set_exact function does not support or expect paths. You can set paths with nested json_array or json_object function calls.


### Example

Suppose you want to have a JSON object that looks like this:

JSON

Copy

{"system.splunk.path":"/opt/splunk"}


```spl

{"system.splunk.path":"/opt/splunk"}

```


To generate this object, you can use the makeresults command and the json_set_exact function as shown in the following search:

CODE

Copy

| makeresults | eval my_object=json_object(), splunk_path=json_set_exact(my_object, "system.splunk.path", "/opt/splunk")


```spl

| makeresults | eval my_object=json_object(), splunk_path=json_set_exact(my_object, "system.splunk.path", "/opt/splunk")

```


You use json_set_exact for this instead of json_set because the json_set function interprets the period characters in {"system.splunk.path"} as nested objects. If you use json_set in the preceding search you get this JSON object:

JSON

Copy

{"system":{"splunk":{"path":"/opt/splunk"}}}


```spl

{"system":{"splunk":{"path":"/opt/splunk"}}}

```


Instead of this object:

JSON

Copy

{"system.splunk.path":"/opt/splunk"}


```spl

{"system.splunk.path":"/opt/splunk"}

```



## json_valid(&lt;json&gt;)

Evaluates whether a piece of JSON uses valid JSON syntax and returns either TRUE or FALSE.


### Usage

You can use this function with the eval and where commands, and as part of evaluation expressions with other commands.


### Example

The following example validates a JSON object { "names": ["maria", "arun"] } in the firstnames field.

Because fields cannot hold Boolean values, the if function is used with the json_valid function to place the string value equivalents of the Boolean values into the isValid field.

CODE

Copy

... | eval IsValid = if(json_valid(firstnames), "true", "false")


```spl

... | eval IsValid = if(json_valid(firstnames), "true", "false")

```



## See also

Function information

Evaluation functions quick reference

Related functions

mv_to_json_array function

Related commands

tojson

fromjson
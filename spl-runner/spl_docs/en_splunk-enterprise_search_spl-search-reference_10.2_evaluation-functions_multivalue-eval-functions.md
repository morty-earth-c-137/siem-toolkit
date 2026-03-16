
# Multivalue eval functions

The following list contains the functions that you can use on multivalue fields or to return multivalue fields.

You can also use the statistical eval functions, max and min , on multivalue fields. See Statistical eval functions .

For information about using string and numeric fields in functions, and nesting functions, see Evaluation functions .


## commands(&lt;value&gt;)


### Description

This function takes a search string, or field that contains a search string, and returns a multivalued field containing a list of the commands used in &lt;value&gt;.


### Usage

This function is generally not recommended for use except for analysis of audit.log events.

You can use this function with the eval , fieldformat , and where commands, and as part of eval expressions.


### Basic example

The following example returns a multivalued field called x, that contains the commands search , stats , and sort which are the commands used in the search string specified.

CODE

Copy

... | eval x=commands("search foo | stats count | sort count")


```spl

... | eval x=commands("search foo | stats count | sort count")

```



## mvappend(&lt;values&gt;)


### Description

This function takes one or more values and returns a single multivalue result that contains all of the values. The values can be strings, multivalue fields, or single value fields.


### Usage

You can use this function with the eval , fieldformat , and where commands, and as part of eval expressions.


### Basic examples

This example shows how to append two values, localhost is a literal string value and srcip is a field name.

CODE

Copy

... | eval fullName=mvappend("localhost", srcip)


```spl

... | eval fullName=mvappend("localhost", srcip)

```


The following example shows how to use nested mvappend functions.

- The inner mvappend function contains two values: localhost is a literal string value and srcip is a field name.

- The outer mvappend function contains three values: the inner mvappend function, destip is a field name, and 192.168.1.1 which is a literal IP address.

The results are placed in a new field called ipaddresses , which contains the array ["localhost", &lt;values_in_scrip&gt;, &lt;values_in_destip&gt;, "192.168.1.1"] .

CODE

Copy

... | eval ipaddresses=mvappend(mvappend("localhost", srcip), destip, "192.168.1.1")


```spl

... | eval ipaddresses=mvappend(mvappend("localhost", srcip), destip, "192.168.1.1")

```


Note that the previous example generates the same results as the following example, which does not use a nested mvappend function:

CODE

Copy

| makeresults | eval ipaddresses=mvappend("localhost", srcip, destip, "192.168.1.1")


```spl

| makeresults | eval ipaddresses=mvappend("localhost", srcip, destip, "192.168.1.1")

```


If the first value in the srcip field is 203.0.113.0 and the first value in the destip field is 203.0.113.255, the results look something like this:


| time | ipaddresses |
| --- | --- |
| 2024-11-19 16:43:31 | localhost203.0.113.0203.0.113.255192.168.1.1 |



## mvcount(&lt;mv&gt;)


### Description

This function takes a field and returns a count of the values in that field for each result. If the field is a multivalue field, this function returns the number of values in that field. If the field contains a single value, this function returns 1 . If the field has no values, this function returns NULL.


### Usage

You can use this function with the eval , fieldformat , and where commands, and as part of eval expressions.


### Basic example

CODE

Copy

... | eval n=mvcount(multifield)


```spl

... | eval n=mvcount(multifield)

```



### Extended example

In the following example, the mvcount() function returns the number of email addresses in the To , From , and Cc fields and saves the addresses in the specified "_count" fields.

CODE

Copy

eventtype="sendmail" 
| eval To_count=mvcount(split(To,"@"))-1 
| eval From_count=mvcount(From) 
| eval Cc_count= mvcount(split(Cc,"@"))-1


```spl

eventtype="sendmail" 
| eval To_count=mvcount(split(To,"@"))-1 
| eval From_count=mvcount(From) 
| eval Cc_count= mvcount(split(Cc,"@"))-1

```


This search takes the values in the To field and uses the split function to separate the email address on the @ symbol. The split function is also used on the Cc field for the same purpose.

If only a single email address exists in the From field, as you would expect, mvcount(From) returns 1. If there is no Cc address, the Cc field might not exist for the event. In that situation mvcount(cc) returns NULL.


## mvdedup(&lt;mv&gt;)


### Description

This function takes a multivalue field and returns a multivalue field with its duplicate values removed.


### Usage

You can use this function with the eval , fieldformat , and where commands, and as part of eval expressions.


### Basic example

CODE

Copy

... | eval s=mvdedup(mvfield)


```spl

... | eval s=mvdedup(mvfield)

```



## mvfilter(&lt;predicate&gt;)


### Description

This function filters a multivalue field based on an arbitrary Boolean expression. The Boolean expression can reference ONLY ONE field at a time.


### Usage

This function will return NULL values of the field as well. If you do not want the NULL values, use one of the following expressions:

- mvfilter(!isnull(&lt;value&gt;))

- mvfilter(isnotnull(&lt;value&gt;))

You can use this function with the eval , fieldformat , and where commands, and as part of eval expressions.


### Basic example

The following example returns all of the values in field email that end in .net or .org .

CODE

Copy

... | eval n=mvfilter(match(email, "\.net$") OR match(email, "\.org$"))


```spl

... | eval n=mvfilter(match(email, "\.net$") OR match(email, "\.org$"))

```



## mvfind(&lt;mv&gt;,&lt;regex&gt;)


### Description

This function tries to find a value in the multivalue field that matches the regular expression. If a match exists, the index of the first matching value is returned (beginning with zero). If no values match, NULL is returned.


### Usage

You can use this function with the eval , fieldformat , and where commands, and as part of eval expressions.


### Basic example

CODE

Copy

... | eval n=mvfind(mymvfield, "err\d+")


```spl

... | eval n=mvfind(mymvfield, "err\d+")

```



## mvindex(&lt;mv&gt;,&lt;start&gt;,&lt;end&gt;)


### Description

This function returns a subset of the multivalue field using the start and end index values.


### Usage

The &lt;mv&gt; argument must be a multivalue field. The &lt;start&gt; and &lt;end&gt; indexes must be numbers.

The &lt;mv&gt; and &lt;start&gt; arguments are required. The &lt;end&gt; argument is optional.

You can use this function with the eval , fieldformat , and where commands, and as part of eval expressions.


### Specifying the start and end indexes

- Indexes start at zero. If you have 5 values in the multivalue field, the first value has an index of 0. The second value has an index of 1, and so on.

- If only the &lt;start&gt; argument is specified, only that value is included in the results.

- When the &lt;end&gt; argument is specified, the range of values from &lt;start&gt; to &lt;end&gt; are included in the results.

- Both the &lt;start&gt; and &lt;end&gt; arguments can be negative. An index of -1 is used to specify the last value in the list.

- If the indexes are out of range or invalid, the result is NULL.


### Examples

Consider the following values in a multivalue field called names :


| Name | alex | celestino | claudia | david | ikraam | nyah | rutherford | wei |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| index number | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |


Because indexes start at zero, the following example returns the value claudia :

CODE

Copy

... | eval my_names=mvindex(names,2)


```spl

... | eval my_names=mvindex(names,2)

```


To return a range of values, specify both a &lt;start&gt; and &lt;end&gt; value. For example, the following search returns the first 4 values in the field. The start value is 0 and the end value is 3 .

CODE

Copy

... | eval my_names=mvindex(names,0,3)


```spl

... | eval my_names=mvindex(names,0,3)

```


The results look like this:


| my_names |
| --- |
| alex,celestino,claudia,david |



### Extended examples

Consider the following values in a multivalue field:


| ponies |
| --- |
| buttercup, dash, flutter, honey, ivory, minty, pinky, rarity |


To return a value from the end of the list of values, the index numbers start with -1 . The negative symbol indicates that the indexing starts from the last value. For example:


| Pony name | buttercup | dash | flutter | honey | ivory | minty | pinky | rarity |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| index number | -8 | -7 | -6 | -5 | -4 | -3 | -2 | -1 |


To return the last value in the list, you specify -1 , which indicates to start at the end of the list and return only one value. For example:

CODE

Copy

... | eval my_ponies=mvindex(ponies,-1)


```spl

... | eval my_ponies=mvindex(ponies,-1)

```


The results look like this:


| my_ponies |
| --- |
| rarity |


To return the 3rd value from the end, you would specify the index number -3 . For example:

CODE

Copy

... | eval my_ponies=mvindex(ponies,-3)


```spl

... | eval my_ponies=mvindex(ponies,-3)

```


The results look like this:


| my_ponies |
| --- |
| minty |


To return a range of values, specify both a &lt;start&gt; and &lt;end&gt; value. For example, the following search returns the last 3 values in the field. The start value is -3 and the end value is -1 .

CODE

Copy

... | eval my_ponies=mvindex(ponies, -3, -1)


```spl

... | eval my_ponies=mvindex(ponies, -3, -1)

```


The results look like this:


| my_ponies |
| --- |
| minty,pinky,rarity |



## mvjoin(&lt;mv&gt;,&lt;delim&gt;)


### Description

This function takes two arguments, a multivalue field and a string delimiter. The function concatenates the individual values within &lt;mv&gt; using the value of &lt;delim&gt; as a separator.


### Usage

You can use this function with the eval , fieldformat , and where commands, and as part of eval expressions.


### Basic examples

You have a multivalue field called "base" that contains the values "1" "2" "3" "4" "5". The values are separated by a space. You want to create a single value field instead, with OR as the delimiter. For example "1 OR 2 OR 3 OR 4 OR 5".

The following search creates the base field with the values. The search then creates the joined field by using the result of the mvjoin function.

CODE

Copy

... | eval base=mvrange(1,6), joined=mvjoin('base'," OR ")


```spl

... | eval base=mvrange(1,6), joined=mvjoin('base'," OR ")

```


The following example joins together the individual values of "myfield" using a semicolon as the delimiter:

CODE

Copy

... | eval n=mvjoin(myfield, ";")


```spl

... | eval n=mvjoin(myfield, ";")

```



## mvmap(&lt;mv&gt;,&lt;expression&gt;)


### Description

This function iterates over the values of a multivalue field, performs an operation using the &lt;expression&gt; on each value, and returns a multivalue field with the list of results.


### Usage

You can use this function with the eval , fieldformat , and where commands, and as part of eval expressions.


### Basic examples

The following example multiplies each value in the results field by 10.

CODE

Copy

... | eval n=mvmap(results, results\*10)


```spl

... | eval n=mvmap(results, results*10)

```


The following example multiplies each value in the results field by threshold , where threshold is a single-valued field.

CODE

Copy

... | eval n=mvmap(results, results\*threshold)


```spl

... | eval n=mvmap(results, results*threshold)

```


The following example multiplies the 2nd and 3rd values in the results field by threshold , where threshold is a single-valued field. This example uses the mvindex function to identify specific values in the results field.

CODE

Copy

... | eval n=mvmap(mvindex(results, 1,2), results\*threshold)


```spl

... | eval n=mvmap(mvindex(results, 1,2), results*threshold)

```



## mvrange(&lt;start&gt;,&lt;end&gt;,&lt;step&gt;)


### Description

This function creates a multivalue field for a range of numbers. This function can contain up to three arguments: a starting number, an ending number (which is excluded from the field), and an optional step increment. If the increment is a timespan such as 7d , the starting and ending numbers are treated as UNIX time.


### Usage

You can use this function with the eval , fieldformat , and where commands, and as part of eval expressions.

The step increment is optional. If the &lt;step&gt; increment is a timespan such as 7d, the starting and ending numbers are treated as UNIX time.

The &lt;end&gt; number is not included from the multivalue field that is created.


### Basic examples

The following example returns a multivalue field with the values 1, 3, 5, 7, 9.

CODE

Copy

... | eval mv=mvrange(1,11,2)


```spl

... | eval mv=mvrange(1,11,2)

```


The following example takes the UNIX timestamp for 1/1/2018 as the start date and the UNIX timestamp for 4/19/2018 as an end date and uses the increment of 7 days.

CODE

Copy

| makeresults | eval mv=mvrange(1514834731,1524134919,"7d")


```spl

| makeresults | eval mv=mvrange(1514834731,1524134919,"7d")

```


This example returns a multivalue field with the UNIX timestamps. The results appear on the Statistics tab and look something like this:


| _time | mv |
| --- | --- |
| 2018-04-10 12:31:03 | 1514834731151543953115160443311516649131151725393115178587311518463531151906833115196731311520277931152087913115214839311522088731152269353115232983311523903131 |



## mvreverse(&lt;value&gt;)


### Description

The mvreverse command reverses the order of the values in a multivalue field.


### Usage

You must first construct a multivalue field in order to use the mvreverse function on that field. The following two examples show how to build a valid multivalue field using the split and mvappend eval functions.

CODE

Copy

| makeresults | eval a=mvreverse(split("1,2,3", ","))


```spl

| makeresults | eval a=mvreverse(split("1,2,3", ","))

```


CODE

Copy

| makeresults | eval b = mvappend("1","2","3"), a=mvreverse(b)


```spl

| makeresults | eval b = mvappend("1","2","3"), a=mvreverse(b)

```



### Examples

The following example reverses the order of the values in the multivalue field myfield .

CODE

Copy

| makeresults
| eval myfield = "one,two,three"
| makemv tokenizer = "([^,]+),?" myfield
| eval new_myfield = mvreverse(myfield)


```spl

| makeresults
| eval myfield = "one,two,three"
| makemv tokenizer = "([^,]+),?" myfield
| eval new_myfield = mvreverse(myfield)

```


The following example reverses the order of the values in the multivalue field myfield by changing "1", "2", "3" to "3", "2", "1" .

CODE

Copy

| makeresults 
| eval myfield = mvreverse(mvappend("1", "2", "3"))


```spl

| makeresults 
| eval myfield = mvreverse(mvappend("1", "2", "3"))

```


The following example reverses the order of the values in multivalue field myfield from "1","2","3" to "3", "2", "1" in multivalue field new_myfield .

CODE

Copy

| makeresults 
| eval myfield = mvappend("1","2","3"), new_myfield=mvreverse(myfield)


```spl

| makeresults 
| eval myfield = mvappend("1","2","3"), new_myfield=mvreverse(myfield)

```



## mvsort(&lt;mv&gt;)


### Description

This function uses a multivalue field and returns a multivalue field with the values sorted lexicographically.


### Usage

You can use this function with the eval , fieldformat , and where commands, and as part of eval expressions.

Lexicographical order sorts items based on the values used to encode the items in computer memory. In Splunk software, this is almost always UTF-8 encoding, which is a superset of ASCII.

- Numbers are sorted before letters. Numbers are sorted based on the first digit. For example, the numbers 10, 9, 70, 100 are sorted lexicographically as 10, 100, 70, 9.

- Uppercase letters are sorted before lowercase letters.

- Symbols are not standard. Some symbols are sorted before numeric values. Other symbols are sorted before or after letters.


### Basic example

CODE

Copy

... | eval s=mvsort(mvfield)


```spl

... | eval s=mvsort(mvfield)

```



## mvzip(&lt;mv_left&gt;,&lt;mv_right&gt;,&lt;delim&gt;)


### Description

This function combines the values in two multivalue fields. The delimiter is used to specify a delimiting character to join the two values.


### Usage

This is similar to the Python zip command.

You can use this function with the eval , fieldformat , and where commands, and as part of eval expressions.

The values are stitched together combining the first value of &lt;mv_left&gt; with the first value of field &lt;mv_right&gt;, then the second with the second, and so on.

The delimiter is optional, but when specified must be enclosed in quotation marks. The default delimiter is a comma ( , ).


### Basic example

CODE

Copy

... | eval nserver=mvzip(hosts,ports)


```spl

... | eval nserver=mvzip(hosts,ports)

```



### Extended example

You can nest several mvzip functions together to create a single multivalued field three_fields from three separate fields. The pipe ( | ) character is used as the separator between the field values.

CODE

Copy

...| eval three_fields=mvzip(mvzip(field1,field2,"|"),field3,"|")


```spl

...| eval three_fields=mvzip(mvzip(field1,field2,"|"),field3,"|")

```


(Thanks to Splunk user cmerriman for this example.)


## mv_to_json_array(&lt;field&gt;, &lt;infer_types&gt;)

This function maps the elements of a multivalue field to a JSON array.


### Usage

You can use this function with the eval and where commands, and as part of evaluation expressions with other commands.

Because the elements of JSON arrays can have many data types (such as string, numeric, Boolean, and null), the mv_to_json_array function lets you specify how it should map the contents of multivalue fields into JSON arrays. You can have the field values simply written to arrays as string data types, or you can have the function infer different JSON data types.

Use the &lt;infer_types&gt; input to specify that the mv_to_json_array function should attempt to infer JSON data types when it converts field values into array elements. The &lt;infer_types&gt; input defaults to false .


| Syntax | Description |
| --- | --- |
| mv_to_json_array(&lt;field&gt;, false())ormv_to_json_array(&lt;field&gt;) | By default, or when you explicitly set it tofalse(), themv_to_json_arrayfunction maps all values in the multivalued field to the JSON array as string data types, whether they are numeric, strings, Boolean values, or any other JSON data type. Themv_to_json_arrayfunction effectively splits the multivalue field on the comma and writes each quote-enclosed value to the array as an element with the string data type. |
| mv_to_json_array(&lt;field&gt;, true()) | When you set themv_to_json_arrayfunction totrue(), the function removes one set of bracketing quote characters from each value it transfers into the JSON array. If the function does not recognize the resulting array element as a proper JSON data type (such as string, numeric, Boolean, or null), the function turns the element into a null data type. |



### Example

This example shows you how the mv_to_json_array function can validate JSON as it generates JSON arrays.

This search creates a multivalue field named ponies .

CODE

Copy

... | eval ponies = mvappend("\"Buttercup\"", "\"Fluttershy\"", "\"Rarity\"", "true", "null"),


```spl

... | eval ponies = mvappend("\"Buttercup\"", "\"Fluttershy\"", "\"Rarity\"", "true", "null"),

```


The array that is created from these values depends on the &lt;infer_types&gt; input.


### Without inferring data types

When &lt;infer_types&gt; is set to false or omitted, the mv_to_json_array function converts the field values into array elements without changing the values.

CODE

Copy

... | eval my_sweet_ponies = mv_to_json_array(ponies, false())


```spl

... | eval my_sweet_ponies = mv_to_json_array(ponies, false())

```


The resulting array looks like this:

["\"Buttercup\"","\"Fluttershy\"","\"Rarity\"","true","null"]


### With inferring data types

When you run this search with infer_values set to true() , the mv_to_json_array function removes the extra quote and backslash escape characters from the field values when the values are converted into array elements.

CODE

Copy

... | eval my_sweet_ponies = mv_to_json_array(ponies, true())


```spl

... | eval my_sweet_ponies = mv_to_json_array(ponies, true())

```


The resulting array looks like this:

["Buttercup","Fluttershy","Rarity",true,null]


## split(&lt;str&gt;,&lt;delim&gt;)


### Description

This function splits the string values on the delimiter and returns the string values as a multivalue field.




> **Note: The split function doesn't have a maximum character limit for input strings or delimiter, provided enough memory is available for searches.**



### Usage

You can use this function with the eval , fieldformat , and where commands, and as part of eval expressions.

Use an empty string ("") to split the original string into one value per character. For example, the following search splits the string into a , b , c , and d .

CODE

Copy

|makeresults 
|eval test="abcd"
|eval results=split(test,"")


```spl

|makeresults 
|eval test="abcd"
|eval results=split(test,"")

```



### Basic example

To illustrate how the split function works, the following search creates an event with a test field that contains a list of string values separated by semicolon characters ( ; ).

CODE

Copy

| makeresults
| eval test="buttercup;rarity;tenderhoof;dash;mcintosh;fleetfoot;mistmane"


```spl

| makeresults
| eval test="buttercup;rarity;tenderhoof;dash;mcintosh;fleetfoot;mistmane"

```


The results look like this:


| _time | test |
| --- | --- |
| 2022-09-20 17:39:56 | buttercup;rarity;tenderhoof;dash;mcintosh;fleetfoot;mistmane |


To split up each of the names in the event into a multivalue field using the semicolon delimiter, you could run a search like this:

CODE

Copy

| makeresults
| eval test="buttercup;rarity;tenderhoof;dash;mcintosh;fleetfoot;mistmane"
| eval ponies=split(test,";")


```spl

| makeresults
| eval test="buttercup;rarity;tenderhoof;dash;mcintosh;fleetfoot;mistmane"
| eval ponies=split(test,";")

```




Now each of the pony names in the


```spl

test

```


event is a field in a multivalue field. The results look something like this:




| _time | ponies | test |
| --- | --- | --- |
| 2022-09-20 18:22:03 | buttercupraritytenderhoofdashmcintoshfleetfootmistmane | buttercup;rarity;tenderhoof;dash;mcintosh;fleetfoot;mistmane |


You can also use a string of contiguous characters in your search like this, which splits the string on "def".

CODE

Copy

|makeresults 
|eval test="1a2b3c4def567890"
|eval results=split(test,"def")


```spl

|makeresults 
|eval test="1a2b3c4def567890"
|eval results=split(test,"def")

```


The results look something like this.


| _time | results | test |
| --- | --- | --- |
| 2023-01-23 12:18:11 | 1a2b3c4567890 | 1a2b3c4def567890 |



### Extended example

The following search is useful for building equivalents to string functions like Oracle INSTR.

CODE

Copy

| makeresults
|eval test="name::value"|eval results=split(test,"::")


```spl

| makeresults
|eval test="name::value"|eval results=split(test,"::")

```


The results look something like this. The length of the first entry (mvindex=0) is the position of the "::" string, plus or minus one.


| _time | results | test |
| --- | --- | --- |
| 2023-01-23 12:18:11 | namevalue | name::value |



## See also

See the following multivalue commands:

- makemv

- mvcombine

- mvexpand

- nomv
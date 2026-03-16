
# Evaluation functions

Use the evaluation functions to evaluate an expression, based on your events, and return a result.


## Quick reference

See the Supported functions and syntax section for a quick reference list of the evaluation functions.


## Commands

You can use evaluation functions with the eval , fieldformat , and where commands, and as part of eval expressions with other commands.


## Usage

- All functions that accept strings can accept literal strings or any field.

- All functions that accept numbers can accept literal numbers or any numeric field.


### String arguments and fields

For most evaluation functions, when a string argument is expected, you can specify either a literal string or a field name. Literal strings must be enclosed in double quotation marks. In other words, when the function syntax specifies a string you can specify any expression that results in a string. For example, you have a field called name that contains the names of your servers. If you want to append the literal string server at the end of the name, you would use dot notation like this in your search: name."server" .​


### Nested functions

You can specify a function as an argument to another function.

In the following example, the cidrmatch function is used as the first argument in the if function.

CODE

Copy

... | eval isLocal=if(cidrmatch("123.132.32.0/25",ip), "local", "not local")


```spl

... | eval isLocal=if(cidrmatch("123.132.32.0/25",ip), "local", "not local")

```


The following example shows how to use the true() function to provide a default to the case function.

CODE

Copy

... | eval error=case(status == 200, "OK", status == 404, "Not found", true(), "Other")


```spl

... | eval error=case(status == 200, "OK", status == 404, "Not found", true(), "Other")

```



## Supported functions and syntax

There are two ways that you can see information about the supported evaluation functions:

- Function list by category

- Alphabetical list of functions


### Function list by category

The following table is a quick reference of the supported evaluation functions, organized by category. This table provides a brief description for each function. Use the links in the table to learn more about each function and to see examples.


| Type of function | Supported functions and syntax | Description |
| --- | --- | --- |
| Bitwise functions | bit_and(&lt;values&gt;) | Bitwise AND function that takes two or more non-negative integers as arguments and sequentially performs logical bitwise AND on them. |
| bit_or(&lt;values&gt;) | Bitwise OR function that takes two or more non-negative integers as arguments and sequentially performs bitwise OR on them. |  |
| bit_not(&lt;value&gt;, &lt;bitmask&gt;) | Bitwise NOT function that takes a non-negative as an argument and inverts every bit in the binary representation of that number. It also takes an optional second argument that acts as a bitmask. |  |
| bit_xor(&lt;values&gt;) | Bitwise XOR function that takes two or more non-negative integers as arguments and sequentially performs bitwise XOR of each of the given arguments. |  |
| bit_shift_left(&lt;value&gt;, &lt;shift_offset&gt;) | Logical left shift function that takes two non-negative integers as arguments and shifts the binary representation of the first integer over to the left by the specified shift amount. |  |
| bit_shift_right(&lt;value&gt;, &lt;shift_offset&gt;) | Logical right shift function that takes two non-negative integers as arguments and shifts the binary representation of the first integer over to the right by the specified shift amount. |  |
| Comparison and Conditional functions | case(&lt;condition&gt;,&lt;value&gt;,...) | Accepts alternating conditions and values. Returns the first value for which the condition evaluates to TRUE. |
| cidrmatch(&lt;cidr&gt;,&lt;ip&gt;) | Returns TRUE when an IP address,&lt;ip&gt;, belongs to a particular CIDR subnet,&lt;cidr&gt;. |  |
| coalesce(&lt;values&gt;) | Takes one or more values and returns the first value that is not NULL. |  |
| false() | Returns FALSE. |  |
| if(&lt;predicate&gt;,&lt;true_value&gt;,&lt;false_value&gt;) | If the&lt;predicate&gt;expression evaluates to TRUE, returns the&lt;true_value&gt;, otherwise the function returns the&lt;false_value&gt;. |  |
| in(&lt;field&gt;,&lt;list&gt;) | Returns TRUE if one of the values in the list matches a value that you specify. |  |
| like(&lt;str&gt;,&lt;pattern&gt;) | Returns TRUE only if&lt;str&gt;matches&lt;pattern&gt;. |  |
| lookup(&lt;lookup_table&gt;, &lt;json_object&gt;, &lt;json_array&gt;) | Performs a CSV lookup. Returns the output field or fields in the form of a JSON object.Note:Thelookup()function is available only to Splunk Enterprise users. |  |
| match(&lt;str&gt;, &lt;regex&gt;) | Returns TRUE if the regular expression&lt;regex&gt;finds a match against any substring of the string value&lt;str&gt;. Otherwise returns FALSE. |  |
| null() | This function takes no arguments and returns NULL. |  |
| nullif(&lt;field1&gt;,&lt;field2&gt;) | Compares the values in two fields and returns NULL if the value in&lt;field1&gt;is equal to the value in&lt;field2&gt;. Otherwise returns the value in&lt;field1&gt;. |  |
| searchmatch(&lt;search_str&gt;) | Returns TRUE if the event matches the search string. |  |
| true() | Returns TRUE. |  |
| validate(&lt;condition&gt;, &lt;value&gt;,...) | Takes a list of conditions and values and returns the value that corresponds to the condition that evaluates to FALSE. This function defaults to NULL if all conditions evaluate to TRUE. This function is the opposite of thecasefunction. |  |
| Conversion functions | ipmask(&lt;mask&gt;,&lt;ip&gt;) | Generates a new masked IP address by applying a mask to an IP address using a bitwiseANDoperation. |
| printf(&lt;format&gt;,&lt;arguments&gt;) | Creates a formatted string based on a format description that you provide. |  |
| toarray(&lt;value&gt;) | Converts a value to an array value. |  |
| tobool(&lt;value&gt;) | Converts a value to a Boolean value. |  |
| todouble(&lt;value&gt;, &lt;base&gt;) | Converts a value to the equivalent double value of the field, if any. The second argument specifies the numeric base used to convert strings. |  |
| toint(&lt;value&gt;, &lt;base&gt;) | Converts a value to the equivalent integer value of the field, if any. The second argument specifies the numeric base used to convert strings. |  |
| tomv(&lt;value&gt;) | Converts a value to a multivalue. |  |
| tonumber(&lt;str&gt;,&lt;base&gt;) | Converts a string to a number. |  |
| toobject(&lt;value&gt;) | Converts a value to the equivalent object value of the field, if any. |  |
| tostring(&lt;value&gt;,&lt;format&gt;) | Converts the input, such as a number or a Boolean value, to a string. |  |
| Cryptographic functions | md5(&lt;str&gt;) | Computes the md5 hash for the string value. |
| sha1(&lt;str&gt;) | Computes the sha1 hash for the string value. |  |
| sha256(&lt;str&gt;) | Computes the sha256 hash for the string value. |  |
| sha512(&lt;str&gt;) | Computes the sha512 hash for the string value. |  |
| Date and Time functions | now() | Returns the time that the search was started when run as an ad-hoc search. If used with a scheduled search, returns the time that the search was scheduled to run, which might not be the time that the scheduled search actual runs. |
| relative_time(&lt;time&gt;,&lt;specifier&gt;) | Adjusts the time by a relative time specifier. |  |
| strftime(&lt;time&gt;,&lt;format&gt;) | Takes a UNIX time and renders it into a human readable format. |  |
| strptime(&lt;str&gt;,&lt;format&gt;) | Takes a human readable time and renders it into UNIX time. |  |
| time() | The time that eval function was computed. The time will be different for each event, based on when the event was processed. |  |
| Informational functions | isarray(&lt;value&gt;) | Returns TRUE if the field value is an array. |
| isbool(&lt;value&gt;) | Returns TRUE if the field value is Boolean. |  |
| isdouble(&lt;value&gt;) | Returns TRUE if the field value is a double value. |  |
| isint(&lt;value&gt;) | Returns TRUE if the field value is an integer. |  |
| ismv(&lt;value&gt;) | Returns TRUE if the field value is a multivalue. |  |
| isnotnull(&lt;value&gt;) | Returns TRUE if the field value is not NULL. |  |
| isnull(&lt;value&gt;) | Returns TRUE if the field value is NULL. |  |
| isnum(&lt;value&gt;) | Returns TRUE if the field value is a number. |  |
| isobject(&lt;value&gt;) | Returns TRUE if the field value is an object. |  |
| isstr(&lt;value&gt;) | Returns TRUE if the field value is a string. |  |
| typeof(&lt;value&gt;) | Returns a string that indicates the field type, such as Number, String, Boolean, and so forth |  |
| JSON functions | json_object(&lt;members&gt;) | Creates a new JSON object from members of key-value pairs. |
| json(&lt;value&gt;) | Evaluates whether a value can be parsed as JSON. If the value is JSON, the function returns the value. Otherwise, the function returns null. |  |
| json_append(&lt;json&gt;, &lt;path_value_pairs&gt;) | Appends values to the ends of indicated arrays within a JSON document. |  |
| json_array(&lt;values&gt;) | Creates a JSON array using a list of values. |  |
| json_array_to_mv(&lt;json_array&gt;, &lt;boolean&gt;) | Maps the elements of a proper JSON array into a multivalue field. |  |
| json_delete(&lt;object&gt;,&lt;keys&gt;) | Removes one or more keys and their corresponding values from the specified JSON object. |  |
| json_entries(&lt;value&gt;) | Returns the key-value entries from the top-level key-value pairs in a JSON object. The entries are returned as a JSON array of JSON objects with fieldskeyandvalue. |  |
| json_extend(&lt;json&gt;, &lt;path_value_pairs&gt;) | Flattens arrays into their component values and appends those values to the ends of indicated arrays within a valid JSON document. |  |
| json_extract(&lt;json&gt;, &lt;paths&gt;) | This function returns a value from a piece JSON and zero or more paths. The value is returned in either a JSON array, or a Splunk software native type value. |  |
| json_extract_exact(&lt;json&gt;,&lt;keys&gt;) | Returns Splunk software native type values from a piece of JSON by matching literal strings in the event and extracting them as keys. |  |
| json_has_key_exact(&lt;object&gt;, &lt;key&gt;) | Evaluates whether a JSON object contains the specified key and returns either TRUE or FALSE. |  |
| json_keys(&lt;json&gt;) | Returns the keys from the key-value pairs in a JSON object as a JSON array. |  |
| json_set(&lt;json&gt;, &lt;path_value_pairs&gt;) | Inserts or overwrites values for a JSON node with the values provided and returns an updated JSON object. |  |
| json_set_exact(&lt;json&gt;,&lt;key_value_pairs&gt;) | Uses provided key-value pairs to generate or overwrite a JSON object. |  |
| json_valid(&lt;json&gt;) | Evaluates whether piece of JSON uses valid JSON syntax and returns either TRUE or FALSE. |  |
| Mathematical functions | abs(&lt;num&gt;) | Returns the absolute value. |
| ceiling(&lt;num&gt;) | Rounds the value up to the next highest integer. |  |
| exact(&lt;expression&gt;) | Returns the result of a numeric eval calculation with a larger amount of precision in the formatted output. |  |
| exp(&lt;num&gt;) | Returns the exponential functioneN. |  |
| floor(&lt;num&gt;) | Rounds the value down to the next lowest integer. |  |
| ln(&lt;num&gt;) | Returns the natural logarithm. |  |
| log(&lt;num&gt;,&lt;base&gt;) | Returns the logarithm of &lt;num&gt; using &lt;base&gt; as the base. If &lt;base&gt; is omitted, base 10 is used. |  |
| pi() | Returns the constantpito 11 digits of precision. |  |
| pow(&lt;num&gt;,&lt;exp&gt;) | Returns &lt;num&gt; to the power of &lt;exp&gt;,&lt;num&gt;&lt;exp&gt;. |  |
| round(&lt;num&gt;,&lt;precision&gt;) | Returns &lt;num&gt; rounded to the amount of decimal places specified by &lt;precision&gt;. The default is to round to an integer. |  |
| sigfig(&lt;num&gt;) | Rounds &lt;num&gt; to the appropriate number of significant figures. |  |
| sqrt(&lt;num&gt;) | Returns the square root of the value. |  |
| sum(&lt;num&gt;,...) | Returns the sum of numerical values as an integer. |  |
| Multivalue eval functions | commands(&lt;value&gt;) | Returns a multivalued field that contains a list of the commands used in &lt;value&gt;. |
| mvappend(&lt;values&gt;) | Returns a multivalue result based on all of values specified. |  |
| mvcount(&lt;mv&gt;) | Returns the count of the number of values in the specified field. |  |
| mvdedup(&lt;mv&gt;) | Removes all of the duplicate values from a multivalue field. |  |
| mvfilter(&lt;predicate&gt;) | Filters a multivalue field based on an arbitrary Boolean expression. |  |
| mvfind(&lt;mv&gt;,&lt;regex&gt;) | Finds the index of a value in a multivalue field that matches the regular expression. |  |
| mvindex(&lt;mv&gt;,&lt;start&gt;,&lt;end&gt;) | Returns a subset of the multivalue field using the start and end index values. |  |
| mvjoin(&lt;mv&gt;,&lt;delim&gt;) | Takes all of the values in a multivalue field and appends the values together using a delimiter. |  |
| mvmap(&lt;mv&gt;,&lt;expression&gt;) | This function iterates over the values of a multivalue field, performs an operation using the &lt;expression&gt; on each value, and returns a multivalue field with the list of results. |  |
| mvrange(&lt;start&gt;,&lt;end&gt;,&lt;step&gt;) | Creates a multivalue field based on a range of specified numbers. |  |
| mvsort(&lt;mv&gt;) | Returns the values of a multivalue field sorted lexicographically. |  |
| mvzip(&lt;mv_left&gt;,&lt;mv_right&gt;,&lt;delim&gt;) | Combines the values in two multivalue fields. The delimiter is used to specify a delimiting character to join the two values. |  |
| mv_to_json_array(&lt;field&gt;, &lt;inver_types&gt;) | Maps the elements of a multivalue field to a JSON array. |  |
| split(&lt;str&gt;,&lt;delim&gt;) | Splits the string values on the delimiter and returns the string values as a multivalue field. |  |
| Statistical eval functions | avg(&lt;values&gt;) | Returns the average of numerical values as an integer. |
| max(&lt;values&gt;) | Returns the maximum of a set of string or numeric values. |  |
| min(&lt;values&gt;) | Returns the minimum of a set of string or numeric values. |  |
| random() | Returns a pseudo-random integer ranging from zero to 231-1. |  |
| Text functions | len(&lt;str&gt;) | Returns the count of the number of characters, not bytes, in the string. |
| lower(&lt;str&gt;) | Converts the string to lowercase. |  |
| ltrim(&lt;str&gt;,&lt;trim_chars&gt;) | Removes characters from the left side of a string. |  |
| replace(&lt;str&gt;,&lt;regex&gt;,&lt;replacement&gt;) | Substitutes the replacement string for every occurrence of the regular expression in the string. |  |
| rtrim(&lt;str&gt;,&lt;trim_chars&gt;) | Removes the trim characters from the right side of the string. |  |
| spath(&lt;value&gt;,&lt;path&gt;) | Extracts information from the structured data formats XML and JSON. |  |
| substr(&lt;str&gt;,&lt;start&gt;,&lt;length&gt;) | Returns a substring of a string, beginning at the start index. The length of the substring specifies the number of character to return. |  |
| trim(&lt;str&gt;,&lt;trim_chars&gt;) | Trim characters from both sides of a string. |  |
| upper(&lt;str&gt;) | Returns the string in uppercase. |  |
| urldecode(&lt;url&gt;) | Replaces URL escaped characters with the original characters. |  |
| Trigonometry and Hyperbolic functions | acos(X) | Computes the arc cosine of X. |
| acosh(X) | Computes the arc hyperbolic cosine of X. |  |
| asin(X) | Computes the arc sine of X. |  |
| asinh(X) | Computes the arc hyperbolic sine of X. |  |
| atan(X) | Computes the arc tangent of X. |  |
| atan2(X,Y) | Computes the arc tangent of X,Y. |  |
| atanh(X) | Computes the arc hyperbolic tangent of X. |  |
| cos(X) | Computes the cosine of an angle of X radians. |  |
| cosh(X) | Computes the hyperbolic cosine of X radians. |  |
| hypot(X,Y) | Computes the hypotenuse of a triangle. |  |
| sin(X) | Computes the sine of X. |  |
| sinh(X) | Computes the hyperbolic sine of X. |  |
| tan(X) | Computes the tangent of X. |  |
| tanh(X) | Computes the hyperbolic tangent of X. |  |



### Alphabetical list of functions

The following table is a quick reference of the supported evaluation functions, organized alphabetically. This table provides a brief description for each function. Use the links in the table to learn more about each function and to see examples.


| Supported functions and syntax | Description | Type of function |
| --- | --- | --- |
| abs(&lt;num&gt;) | Returns the absolute value. | Mathematical functions |
| acos(X) | Computes the arc cosine of X. | Trigonometry and Hyperbolic functions |
| acosh(X) | Computes the arc hyperbolic cosine of X. | Trigonometry and Hyperbolic functions |
| asin(X) | Computes the arc sine of X. | Trigonometry and Hyperbolic functions |
| asinh(X) | Computes the arc hyperbolic sine of X. | Trigonometry and Hyperbolic functions |
| atan(X) | Computes the arc tangent of X. | Trigonometry and Hyperbolic functions |
| atan2(X,Y) | Computes the arc tangent of X,Y. | Trigonometry and Hyperbolic functions |
| atanh(X) | Computes the arc hyperbolic tangent of X. | Trigonometry and Hyperbolic functions |
| avg(&lt;values&gt;) | Returns the average of numerical values as an integer. | Statistical eval functions |
| bit_and(&lt;values&gt;) | Bitwise AND function that takes two or more non-negative integers as arguments and sequentially performs logical bitwise AND on them. | Bitwise functions |
| bit_or(&lt;values&gt;) | Bitwise OR function that takes two or more non-negative integers as arguments and sequentially performs bitwise OR on them. | Bitwise functions |
| bit_not(&lt;value&gt;, &lt;bitmask&gt;) | Bitwise NOT function that takes a non-negative as an argument and inverts every bit in the binary representation of that number. It also takes an optional second argument that acts as a bitmask. | Bitwise functions |
| bit_xor(&lt;values&gt;) | Bitwise XOR function that takes two or more non-negative integers as arguments and sequentially performs bitwise XOR of each of the given arguments. | Bitwise functions |
| bit_shift_left(&lt;value&gt;, &lt;shift_offset&gt;) | Logical left shift function that takes two non-negative integers as arguments and shifts the binary representation of the first integer over to the left by the specified shift amount. | Bitwise functions |
| bit_shift_right(&lt;value&gt;, &lt;shift_offset&gt;) | Logical right shift function that takes two non-negative integers as arguments and shifts the binary representation of the first integer over to the right by the specified shift amount. | Bitwise functions |
| case(&lt;condition&gt;,&lt;value,...) | Accepts alternating conditions and values. Returns the first value for which the condition evaluates to TRUE. | Comparison and Conditional functions |
| cidrmatch(&lt;cidr&gt;,&lt;ip&gt;) | Returns TRUE when an IP address,&lt;ip&gt;, belongs to a particular CIDR subnet,&lt;cidr&gt;. | Comparison and Conditional functions |
| ceiling(&lt;num&gt;) | Rounds the value up to the next highest integer. | Mathematical functions |
| coalesce(&lt;values&gt;) | Takes one or more values and returns the first value that is not NULL. | Comparison and Conditional functions |
| commands(&lt;value&gt;) | Returns a multivalued field that contains a list of the commands used in &lt;value&gt;. | Multivalue eval functions |
| cos(X) | Computes the cosine of an angle of X radians. | Trigonometry and Hyperbolic functions |
| cosh(X) | Computes the hyperbolic cosine of X radians. | Trigonometry and Hyperbolic functions |
| exact(&lt;expression&gt;) | Returns the result of a numeric eval calculation with a larger amount of precision in the formatted output. | Mathematical functions |
| exp(&lt;num&gt;) | Returns the exponential functioneN. | Mathematical functions |
| false() | Returns FALSE. | Comparison and Conditional functions |
| floor(&lt;num&gt;) | Rounds the value down to the next lowest integer. | Mathematical functions |
| hypot(X,Y) | Computes the hypotenuse of a triangle. | Trigonometry and Hyperbolic functions |
| if(&lt;predicate&gt;,&lt;true_value&gt;,&lt;false_value&gt;) | If the&lt;predicate&gt;expression evaluates to TRUE, returns the&lt;true_value&gt;, otherwise the function returns the&lt;false_value&gt;. | Comparison and Conditional functions |
| in(&lt;field&gt;,&lt;list&gt;) | Returns TRUE if one of the values in the list matches a value that you specify. | Comparison and Conditional functions |
| ipmask(&lt;mask&gt;,&lt;ip&gt;) | The function generates a new masked IP address by applying a mask to an IP address using a bitwiseANDoperation. | Conversion functions |
| isarray(&lt;value&gt;) | Returns TRUE if the field value is an array. | Informational functions |
| isbool(&lt;value&gt;) | Returns TRUE if the field value is Boolean. | Informational functions |
| isdouble(&lt;value&gt;) | Returns TRUE if the field value is a double value. | Informational functions |
| isint(&lt;value&gt;) | Returns TRUE if the field value is an integer. | Informational functions |
| ismv(&lt;value&gt;) | Returns TRUE if the field value is a multivalue. | Informational functions |
| isnotnull(&lt;value&gt;) | Returns TRUE if the field value is not NULL. | Informational functions |
| isnull(&lt;value&gt;) | Returns TRUE if the field value is NULL. | Informational functions |
| isnum(&lt;value&gt;) | Returns TRUE if the field value is a number. | Informational functions |
| isobject(&lt;value&gt;) | Returns TRUE if the field value is an object. | Informational functions |
| isstr(&lt;value&gt;) | Returns TRUE if the field value is a string. | Informational functions |
| json(&lt;value&gt;) | Evaluates whether a value can be parsed as JSON. If the value is JSON, the function returns the value. Otherwise, the function returns null. | JSON functions |
| json_append(&lt;json&gt;, &lt;path_value_pairs&gt;) | Appends values to the ends of indicated arrays within a JSON document. | JSON functions |
| json_array(&lt;values&gt;) | Creates a JSON array using a list of values. | JSON functions |
| json_array_to_mv(&lt;json_array&gt;, &lt;boolean&gt;) | Maps the elements of a proper JSON array into a multivalue field. | JSON functions |
| json_delete(&lt;object&gt;,&lt;keys&gt;) | Removes one or more keys and their corresponding values from the specified JSON object. | JSON functions |
| json_entries(&lt;value&gt;) | Returns the key-value entries from the top-level key-value pairs in a JSON object. The entries are returned as a JSON array of JSON objects with fieldskeyandvalue. | JSON functions |
| json_extend(&lt;json&gt;, &lt;path_value_pairs&gt;) | Flattens arrays into their component values and appends those values to the ends of indicated arrays within a valid JSON document. | JSON functions |
| json_extract(&lt;json&gt;, &lt;paths&gt;) | Returns a value from a piece JSON and zero or more paths. The value is returned in either a JSON array, or a Splunk software native type value. | JSON functions |
| json_extract_exact(&lt;json&gt;,&lt;keys&gt;) | Returns Splunk software native type values from a piece of JSON by matching literal strings in the event and extracting them as keys. | JSON functions |
| json_has_key_exact(&lt;object&gt;, &lt;key&gt;) | Returns TRUE if the field value is a JSON key in the provided JSON object. | JSON functions |
| json_keys(&lt;json&gt;) | Returns the keys from the key-value pairs in a JSON object. The keys are returned as a JSON array. | JSON functions |
| json_object(&lt;members&gt;) | Creates a new JSON object from members of key-value pairs. | JSON functions |
| json_set(&lt;json&gt;, &lt;path_value_pairs&gt;) | Inserts or overwrites values for a JSON node with the values provided and returns an updated JSON object. | JSON functions |
| json_set_exact(&lt;json&gt;,&lt;key_value_pairs&gt;) | Uses provided key-value pairs to generate or overwrite a JSON object. | JSON functions |
| json_valid(&lt;json&gt;) | Evaluates whether piece of JSON uses valid JSON syntax and returns either TRUE or FALSE. | JSON functions |
| len(X) | Returns the count of the number of characters (not bytes) in the string. | Text functions |
| like(&lt;str&gt;,&lt;pattern&gt;)) | Returns TRUE only if&lt;str&gt;matches&lt;pattern&gt;. | Comparison and Conditional functions |
| ln(&lt;num&gt;) | Returns the natural logarithm. | Mathematical functions |
| log(&lt;num&gt;,&lt;base&gt;) | Returns the logarithm of &lt;num&gt; using &lt;base&gt; as the base. If &lt;base&gt; is omitted, base 10 is used. | Mathematical functions |
| lookup(&lt;lookup_table&gt;, &lt;json_object&gt;, &lt;json_array&gt;) | Performs a CSV lookup. Returns the output field or fields in the form of a JSON object.Note:Thelookup()function is available only to Splunk Enterprise users. | Comparison and Conditional functions |
| len(&lt;str&gt;) | Returns the count of the number of characters, not bytes, in the string. | Text functions |
| lower(&lt;str&gt;) | Converts the string to lowercase. | Text functions |
| ltrim(&lt;str&gt;,&lt;trim_chars&gt;) | Removes characters from the left side of a string. | Text functions |
| match(&lt;str&gt;, &lt;regex&gt;) | Returns TRUE if the regular expression&lt;regex&gt;finds a match against any substring of the string value&lt;str&gt;. Otherwise returns FALSE. | Comparison and Conditional functions |
| max(&lt;values&gt; | Returns the maximum of a set of string or numeric values. | Statistical eval functions |
| md5(&lt;str&gt;) | Computes the md5 hash for the string value. | Cryptographic functions |
| min(&lt;values&gt;) | Returns the minimum of a set of string or numeric values. | Statistical eval functions |
| mvappend(&lt;values) | Returns a multivalue result based on all of values specified. | Multivalue eval functions |
| mvcount(&lt;mv&gt;) | Returns the count of the number of values in the specified field. | Multivalue eval functions |
| mvdedup(&lt;mv&gt;) | Removes all of the duplicate values from a multivalue field. | Multivalue eval functions |
| mvfilter(&lt;predicate&gt;) | Filters a multivalue field based on an arbitrary Boolean expression. | Multivalue eval functions |
| mvfind(&lt;mv&gt;,&lt;regex&gt;) | Finds the index of a value in a multivalue field that matches the regular expression. | Multivalue eval functions |
| mvindex(&lt;mv&gt;,&lt;start&gt;,&lt;end&gt;) | Returns a subset of the multivalue field using the start and end index values. | Multivalue eval functions |
| mvjoin(&lt;mv&gt;,&lt;delim&gt;) | Takes all of the values in a multivalue field and appends the values together using a delimiter. | Multivalue eval functions |
| mvmap(&lt;mv&gt;,&lt;expression&gt;) | This function iterates over the values of a multivalue field, performs an operation using the &lt;expression&gt; on each value, and returns a multivalue field with the list of results. | Multivalue eval functions |
| mvrange(&lt;start&gt;,&lt;end&gt;,&lt;step&gt;) | Creates a multivalue field based on a range of specified numbers. | Multivalue eval functions |
| mvsort(&lt;mv&gt;) | Returns the values of a multivalue field sorted lexicographically. | Multivalue eval functions |
| mvzip(&lt;mv_left&gt;,&lt;mv_right&gt;,&lt;delim&gt;) | Combines the values in two multivalue fields. The delimiter is used to specify a delimiting character to join the two values. | Multivalue eval functions |
| mv_to_json_array(&lt;field&gt;, &lt;infer_types&gt;) | Maps the elements of a multivalue field to a JSON array. | JSON functions |
| now() | Returns the time that the search was started when run as an ad-hoc search. If used with a scheduled search, returns the time that the search was scheduled to run, which might not be the time that the scheduled search actual runs. | Date and Time functions |
| null() | This function takes no arguments and returns NULL. | Comparison and Conditional functions |
| nullif(&lt;field1&gt;,&lt;field2&gt;) | Compares the values in two fields and returns NULL if the value in&lt;field1&gt;is equal to the value in&lt;field2&gt;. Otherwise returns the value in&lt;field1&gt;. | Comparison and Conditional functions |
| pi() | Returns the constantpito 11 digits of precision. | Mathematical functions |
| pow(&lt;num&gt;,&lt;exp&gt;) | Returns &lt;num&gt; to the power of &lt;exp&gt;,&lt;num&gt;&lt;exp&gt;. | Mathematical functions |
| printf(&lt;format&gt;,&lt;arguments&gt;) | Creates a formatted string based on a format description that you provide. | Conversion functions |
| random() | Returns a pseudo-random integer ranging from zero to 231-1. | Statistical eval functions |
| relative_time(&lt;time&gt;,&lt;specifier&gt;) | Adjusts the time by a relative time specifier. | Date and Time functions |
| replace(&lt;str&gt;,&lt;regex&gt;,&lt;replacement&gt;) | Substitutes the replacement string for every occurrence of the regular expression in the string. | Text functions |
| round(&lt;num&gt;,&lt;precision&gt;) | Returns &lt;num&gt; rounded to the amount of decimal places specified by &lt;precision&gt;. The default is to round to an integer. | Mathematical functions |
| rtrim(&lt;str&gt;,&lt;trim_chars&gt;) | Removes the trim characters from the right side of the string. | Text functions |
| searchmatch(&lt;search_str&gt;) | Returns TRUE if the event matches the search string. | Comparison and Conditional functions |
| sha1(&lt;str&gt;) | Computes the sha1 hash for the string value. | Cryptographic functions |
| sha256(&lt;str&gt;) | Computes the sha256 hash for the string value. | Cryptographic functions |
| sha512(&lt;stri&gt;) | Computes the sha512 hash for the string value. | Cryptographic functions |
| sigfig(&lt;num&gt;) | Rounds &lt;num&gt; to the appropriate number of significant figures. | Mathematical functions |
| sin(X) | Computes the sine of X. | Trigonometry and Hyperbolic functions |
| sinh(X) | Computes the hyperbolic sine of X. | Trigonometry and Hyperbolic functions |
| spath(&lt;value&gt;,&lt;path&gt;) | Extracts information from the structured data formats XML and JSON. | Text functions |
| split(&lt;str&gt;,&lt;delim&gt;) | Splits the string values on the delimiter and returns the string values as a multivalue field. | Multivalue eval functions |
| sqrt(&lt;num&gt;) | Returns the square root of the value. | Mathematical functions |
| strftime(&lt;time&gt;,&lt;format&gt;) | Takes a UNIX time and renders it into a human readable format. | Date and Time functions |
| strptime(&lt;str&gt;,&lt;format&gt;) | Takes a human readable time and renders it into UNIX time. | Date and Time functions |
| substr(&lt;str&gt;,&lt;start&gt;,&lt;length&gt;) | Returns a substring of a string, beginning at the start index. The length of the substring specifies the number of character to return. | Text functions |
| sum(&lt;num&gt;,...) | Returns the sum of numerical values as an integer. | Mathematical functions |
| tan(X) | Computes the tangent of X. | Trigonometry and Hyperbolic functions |
| tanh(X) | Computes the hyperbolic tangent of X. | Trigonometry and Hyperbolic functions |
| time() | The time that eval function was computed. The time will be different for each event, based on when the event was processed. | Date and Time functions |
| toarray(&lt;value&gt;) | Converts a value to an array value. | Conversion functions |
| tobool(&lt;value&gt;) | Converts a value to a Boolean value. | Conversion functions |
| todouble(&lt;field&gt;, &lt;base&gt;) | Converts a value to the equivalent double value of the field, if any. The second argument specifies the numeric base used to convert strings. | Conversion functions |
| toint(&lt;value&gt;, &lt;base&gt;) | Converts a value to the equivalent integer value of the field, if any. The second argument specifies the numeric base used to convert strings. | Conversion functions |
| tomv(&lt;value&gt;) | Converts a value to a multivalue. | Conversion functions |
| tonumber(&lt;str&gt;,&lt;base&gt;) | Converts a string to a number. | Conversion functions |
| toobject(&lt;value&gt;) | Converts a value to the equivalent object value of the field, if any. | Conversion functions |
| tostring(&lt;value&gt;,&lt;format&gt;) | Converts the input, such as a number or a Boolean value, to a string. | Conversion functions |
| trim(&lt;str&gt;,&lt;trim_chars&gt;) | Trim characters from both sides of a string. | Text functions |
| true() | Returns TRUE. | Comparison and Conditional functions |
| typeof(&lt;value&gt;) | Returns a string that indicates the field type, such as Number, String, Boolean, and so forth. | Informational functions |
| upper(&lt;str&gt;) | Returns the string in uppercase. | Text functions |
| urldecode(&lt;url&gt;) | Replaces URL escaped characters with the original characters. | Text functions |
| validate(&lt;condition&gt;, &lt;value&gt;,...) | Takes a list of conditions and values and returns the value that corresponds to the condition that evaluates to FALSE. This function defaults to NULL if all conditions evaluate to TRUE. This function is the opposite of thecasefunction. | Comparison and Conditional functions |



## See also

Topics:

Statistical and charting functions



Commands:

eval

fieldformat

where



# Conversion functions

The following list contains the functions that you can use to mask IP addresses and convert numbers to strings and strings to numbers.

For information about using string and numeric fields in functions, and nesting functions, see Evaluation functions .


## ipmask(&lt;mask&gt;,&lt;ip&gt;)


### Description

This function generates a new masked IP address by applying a mask to an IP address through a bitwise AND operation. You can use this function to simplify the isolation of an IPv4 address octet without splitting the IP address.


### Usage

The mask must be a valid IPv4 address. The IP must be a valid IPv4 address or a field name where the field value is a valid IPv4 address.

A valid IPv4 address is a quad-dotted notation of four decimal integers, each ranging from 0 to 255.

For the mask argument, you can specify one of the default subnet masks such as 255.255.255.0 .

You can use this function with the eval command, and as part of eval expressions.


### Basic examples

The following example shows how to use the ipmask function with the eval command:

CODE

Copy

... | eval maskedIP = ipmask("255.255.255.0", "10.20.30.120")


```spl

... | eval maskedIP = ipmask("255.255.255.0", "10.20.30.120")

```


The output of this example is 10.20.30.0 .



The following example shows how to use the


```spl

ipmask

```


function in the SELECT clause of the


```spl

from

```


command:



CODE

Copy

... | eval maskedIP = ipmask("0.255.0.244", clientip) AS maskedip


```spl

... | eval maskedIP = ipmask("0.255.0.244", clientip) AS maskedip

```


This search masks every IP address in the clientip field and returns the results in an aliased field called maskedip .

The following example shows how to use the ipmask function in the WHERE clause of the from command to filter the events on a specific mask value:

CODE

Copy

...| where ipmask("0.255.0.224", clientip)="10.20.30.120"


```spl

...| where ipmask("0.255.0.224", clientip)="10.20.30.120"

```


In this example, the masked value is 0.20.0.96 .

The following example shows how to use the ipmask function in a pipeline to create a new field with the masked values:

PYTHON

Copy

$pipeline = from $source | eval maskedIP = ipmask("255.0.255.0", clientip) | fields -clientip | into $destination


```spl

$pipeline = from $source | eval maskedIP = ipmask("255.0.255.0", clientip) | fields -clientip | into $destination

```



## printf(&lt;format&gt;,&lt;arguments&gt;)


### Description

This function builds a string value, based on a string format and the values specified. You can specify zero or more values. The values can be strings, numbers, computations, or fields.

The SPL printf function is similar to the C sprintf() function and similar functions in other languages such as Python, Perl, and Ruby.


### Usage

You can use this function with the eval , fieldformat , and where commands, and as part of eval expressions.

format

Description: The format is a character string that can include one or more format conversion specifiers. Each conversion specifier can include optional components such as flag characters, width specifications, and precision specifications. The format must be enclosed in quotation marks.

Syntax: "(%[flags][width][.precision]&lt;conversion_specifier&gt;)..."

arguments

Description: The arguments are optional and can include the width, precision, and the value to format. The value can be a string, number, or field name.

Syntax: [width][.precision][value]


### Supported conversion specifiers

The following table describes the supported conversion specifiers.


| Conversion specifier | Alias | Description | Examples |
| --- | --- | --- | --- |
| %a or %A |  | Floating point number in hexadecimal format | This example returns the value ofpito 3 decimal points, in hexadecimal format.printf("%.3A",pi())which returns0X1.922P+1 |
| %c |  | Single Unicode code point | This example returns the unicode code point for 65 and the first letter of the string "Foo".printf("%c,%c",65,"Foo")which returnsA,F |
| %d | %i | Signed decimal integer | This example returns the positive or negative integer values, including any signs specified with those values.printf("%d,%i,%d",-2,+4,30)which returns-2,4,30 |
| %e or %E |  | Floating point number, exponential format | This example returns the number 5139 in exponential format with 2 decimal points.printf("%.2e",5139)which returns5.14e+03 |
| %f or %F |  | Floating point number | This example returns the value ofpito 2 decimal points.printf("%.2f",pi())which returns3.14 |
| %g or %G |  | Floating point number. This specifier uses either %e or %f depending on the range of the numbers being formatted. | This example returns the value ofpito 2 decimal points (using the %f specifier) and the number 123 in exponential format with 2 decimal points (using %e specifier).printf("%.2g,%.2g",pi(),123)which returns3.1,1.2e+02 |
| %o |  | Unsigned octal number | This example returns the base-8 number for 255.printf("%o",255)which returns377 |
| %s | %z | String | This example returns the concatenated string values of "foo" and "bar".printf("%s%z", "foo", "bar")which returnsfoobar |
| %u |  | Unsigned, or non-negative, decimal integer | This example returns the integer value of the number in the argument.printf("%u",99)which returns99 |
| %x or %X | %p | Unsigned hexadecimal number (lowercase or uppercase) | This example returns the hexadecimal values that are equivalent to the numbers in the arguments. This example shows both upper and lowercase results when using this specifier.printf("%x,%X,%p",10,10,10)which returnsa,A,A |
| %% |  | Percent sign | This example returns the string value with a percent sign.printf("100%%")which returns100% |



### Flag characters

The following table describes the supported flag characters.


| Flag characters | Description | Examples |
| --- | --- | --- |
| single quote or apostrophe ( ' ) | Adds commas as the thousands separator. | printf("%'d",12345), which returns12,345 |
| dash or minus ( - ) | Left justify. If this flag is not specified, the result keeps its default justification.Theprintffunction supports right justification of results only when it formats that way by default. | printf("%-4d",1)which returns1, which is left justified in the output. |
| zero ( 0 ) | Zero pad | This example returns the value in the argument with leading zeros such that the number has 4 digits.printf("%04d",1), which returns0001 |
| plus ( + ) | Always include the sign ( + or - ). If this flag is not specified, the conversion displays a sign only for negative values. | printf("%+4d",1), which returns+1 |
| &lt;space&gt; | Reserve space for the sign. If the first character of a signed conversion is not a sign or if a signed conversion results in no characters, a &lt;space&gt; is added as a prefixed to the result. If both the &lt;space&gt; and + flags are specified, the &lt;space&gt; flag is ignored. | printf("% -4d",1), which returns1 |
| hash, number, or pound ( # ) | Use an alternate form. For the %o conversion specifier, the # flag increases the precision to force the first digit of the result to be zero. For %x or %X conversion specifiers, a non-zero result has 0x (or 0X) prefixed to it. For %a, %A, %e, %E, %f, %F, %%g , and G conversion specifiers, the result always contains a radix character, even if no digits follow the radix character. Without this flag, a radix character appears in the result of these conversions only if a digit follows it. For %g and %G conversion specifiers, trailing zeros are not removed from the result as they normally are. For other conversion specifiers, the behavior is undefined. | printf("%#x", 1), which returns0x1 |



### Specifying field width

You can use an asterisk ( \* ) with the printf function to return the field width or precision from an argument.

Examples

The following example returns the positive or negative integer values, including any signs specified with those values.



printf("%\*d", 5, 123) which returns 123

The following example returns the floating point number with 1 decimal point.

printf("%.\*f", 1, 1.23) which returns 1.2

The following example returns the value of pi() in exponential format with 2 decimal points.



printf("%\*.\*e", 9, 2, pi()) which returns 3.14e+00

The field width can be expressed using a number or an argument denoted with an asterisk ( \* ) character.


| Field width specifier | Description | Examples |
| --- | --- | --- |
| number | The minimum number of characters to print. If the value to print is shorter than this number, the result is padded with blank spaces. The value is not truncated even if the result is larger. |  |
| \* (asterisk) | The width is not specified in the format string, but as an additional integer value argument preceding the argument that has to be formatted. |  |



### Specifying precision


| Precision | Description |
| --- | --- |
| %d, %i, %o, %u, %x or %X | Precision specifies the minimum number of digits to be return. If the value to be return is shorter than this number, the result is padded with leading zeros. The value is not truncated even if the result is longer. A precision of 0 means that no character is returned for the value 0. |
| %a or %A, %e or %E, %f or %F | This is the number of digits to be returned after the decimal point. The default is 6 . |
| %g or %G | This is the maximum number of significant digits to be returned. |
| %s | This is the maximum number of characters to be returned. By default all characters are printed until the ending null character is encountered. |
| Specifying the period without a precision value | If the period is specified without an explicit value for precision, 0 is assumed. |
| Specifying an asterisk for the precision value, for example.\* | The precision is not specified in the format string, but as an additional integer value argument preceding the argument that has to be formatted. |



### Unsupported conversion specifiers

There are a few conversion specifiers from the C sprintf() function that are not supported, including:

- %C, however %c is supported

- %n

- %S, however %s is supported

- %&lt;num&gt;$ specifier for picking which argument to use


### Basic examples

This example creates a new field called new_field and creates string values based on the values in field_one and field_two . The values are formatted with 4 digits before the decimal and 4 digits after the decimal. The - specifies to left justify the string values. The 30 specifies the width of the field.

CODE

Copy

...| eval new_field=printf("%04.4f %-30s",field_one,field_two)


```spl

...| eval new_field=printf("%04.4f %-30s",field_one,field_two)

```



## toarray(&lt;value&gt;)


### Description

This function takes one argument and returns the equivalent array value of the field, if any. You can use this function to convert a string or multivalue to an array. The toarray function infers the data type of each element as it converts a string or multivalue into an array.


### Usage

You can use this function with the eval , fieldformat , and where commands, and as part of eval expressions.

The value argument can be a string or multivalue, or the name of a field that contains a string or multivalue.

If the value is a string, it must be a list of comma-separated values enclosed in square brackets ( [ ] ), or else the function returns null. For example, this string value is a valid JSON array: ["buttercup", "fluttershy", "rarity"]. .

The following table describes how the toarray function converts specific types of values in search results. The function returns null for all other values.


| Value | Result |
| --- | --- |
| array | The same value. |
| multivalue | mv_to_json_array(&lt;value&gt;, true) |
| string | The string parsed as a JSON array. |



### Basic examples

The following search returns an array called my_array with the value [1,2,3] .

CODE

Copy

| makeresults
| eval my_array=toarray(split("1, 2, 3", ","))


```spl

| makeresults
| eval my_array=toarray(split("1, 2, 3", ","))

```


The following search returns an array called grocery_array with the value ["carrots",1,"potatoes",1.75] .

CODE

Copy

| makeresults
| eval grocery_array=toarray("[\"carrots\", 1.00, \"potatoes\", 1.75]")


```spl

| makeresults
| eval grocery_array=toarray("[\"carrots\", 1.00, \"potatoes\", 1.75]")

```


The following search returns True , indicating that "somefield" isn't an array. The toarray function returns null because "somefield" isn't an array, which in turn, causes the isnull function to return True because the result of the toarray function is null.

CODE

Copy

| makeresults
| eval result = if(isnull(toarray("somefield")), "True", "False")


```spl

| makeresults
| eval result = if(isnull(toarray("somefield")), "True", "False")

```



### Extended example

The test_data field in these events contains multivalues.


| _time | test_data |
| --- | --- |
| 2024-12-10 00:46:39 | 100200300 |
| 2024-12-10 00:46:45 | 456 |


The following eval command converts the multivalues in the test_data field into arrays and stores them in a field named test_array :

CODE

Copy

... | eval test_array = toarray(test_data)


```spl

... | eval test_array = toarray(test_data)

```


The results look like this:


| _time | test_data | test_array |
| --- | --- | --- |
| 2024-12-10 00:46:39 | 100200300 | [100,200,300] |
| 2024-12-10 00:46:45 | 456 | [4,5,6] |



## tobool(&lt;value&gt;)


### Description

This function takes one argument and returns the equivalent Boolean value of the field, if any. You can use this function to convert a string or a number to a Boolean value.


### Usage

You can use this function with the eval , fieldformat , and where commands, and as part of eval expressions.

The value argument can be a string or Boolean, or the name of a field that contains a string or Boolean.

You can use this function directly with the where command in searches, but the eval command can't directly accept a Boolean value. You must specify the function inside another function, such as the if function, which can accept a Boolean value as an input.

The following table describes how the tobool function converts specific types of values in search results. If the value is Boolean, then the result is the same value. The function returns null for all other values.


| Data type | Value | Returned Boolean value |
| --- | --- | --- |
| string | "true" or "True" | true |
|  | "false" or "False" | false |
| number | 0 | false |
|  | Any non-zero number | true |



### Basic examples

Suppose you have data that looks like this:


| _time | categoryId | units |
| --- | --- | --- |
| 2024-11-07 21:25:09 | Dream Crusher | 12 |
| 2024-11-07 21:25:09 | Final Sequel | 0 |
| 2024-11-07 21:25:09 | Grand Theft Scooter | 15 |
| 2024-11-07 21:25:09 | Mediocre Kingdom | 35 |
| 2024-11-07 21:25:09 | Orvil the Wolverine | 1 |


You need to run a search to determine which items are in stock. Because the eval command can't directly accept a Boolean value, your search uses the tobool function as the first argument in the if function, like this:

CODE

Copy

… | eval in_stock=if(tobool(units), "In Stock", "Not in Stock")


```spl

… | eval in_stock=if(tobool(units), "In Stock", "Not in Stock")

```


Your search results look like this:


| _time | categoryId | units | in_stock |
| --- | --- | --- | --- |
| 2024-11-07 21:25:09 | Dream Crusher | 12 | In Stock |
| 2024-11-07 21:25:09 | Final Sequel | 0 | Not in Stock |
| 2024-11-07 21:25:09 | Grand Theft Scooter | 15 | In Stock |
| 2024-11-07 21:25:09 | Mediocre Kingdom | 35 | In Stock |
| 2024-11-07 21:25:09 | Orvil the Wolverine | 1 | In Stock |



## todouble(&lt;value&gt;, &lt;base&gt;)


### Description

This function takes one or two arguments and returns the equivalent double value of the field, if any. The second argument specifies the numeric base used to convert a string to a number using the tonumber(&lt;value&gt;, &lt;base&gt;) function.


### Usage

You can use this function with the eval , fieldformat , and where commands, and as part of eval expressions.

The value argument can be a string or number, or the name of a field that contains a string or number.

The base argument is optional and is used only when the value argument is a string and the function is converted to tonumber(&lt;value&gt;, &lt;base&gt;) . The default base is 10. You can set the base argument to a number between 2 and 36, inclusive.

If the todouble function can't parse a field value to a number, such as if the value contains a leading and trailing space, the function returns null. You can use the trim function with todouble to remove leading or trailing spaces.

If the todouble function can't parse a string to a number, the function returns null. For example, the following search doesn't return any results:

CODE

Copy

| makeresults
| eval result = todouble("number")


```spl

| makeresults
| eval result = todouble("number")

```


The following table describes how the todouble function converts specific types of values in search results. The function returns null for all other values.


| Value | Result |
| --- | --- |
| number | The same value. |
| string | tonumber(&lt;value&gt;, &lt;base&gt;) |



### Basic examples

The following example converts the value 16.00 from a string to a double, and stores the converted value in a field named numbers_double .

CODE

Copy

... | eval numbers_double=todouble("16.00")


```spl

... | eval numbers_double=todouble("16.00")

```


The following example converts the value 5 from a number to a double so that it becomes 5.0 , and then stores the converted value in a field named numbers_double .

CODE

Copy

... | eval numbers_double=todouble(5)


```spl

... | eval numbers_double=todouble(5)

```



## toint(&lt;value&gt;, &lt;base&gt;)


### Description

This function takes one or two arguments and returns the equivalent integer value of the field, if any. The second argument specifies the numeric base used to convert strings.


### Usage

You can use this function with the eval , fieldformat , and where commands, and as part of eval expressions.

The value argument can be a string or number, or the name of a field that contains a string or number. If the value includes decimal places, the toint function rounds the value down to the nearest whole number.

The base argument is optional and is used only when the value argument is a number. The default base is 10. You can set the base argument to a number between 2 and 36, inclusive.

If the toint function can't parse a field value to a number, such as if the value contains a leading and trailing space, the function returns null. You can use the trim function with toint to remove leading or trailing spaces.

The following table describes how the toint function converts specific types of values in search results. The function returns null for all other values.


| Value | Result |
| --- | --- |
| number | The same value. |
| double | floor(&lt;value&gt;) |
| string | floor(tonumber(&lt;value&gt;, &lt;base&gt;)) |



> **Note: Splunk platform supports 53-bit integers with 8 bits of precision. Integers larger than 53 bits are truncated.**



### Basic examples

The following example converts the value 24 from a string to an integer, and stores the converted value in a field named numbers_int .

CODE

Copy

... | eval numbers_int=toint("24")


```spl

... | eval numbers_int=toint("24")

```


The following example converts the value 3.14 from a double to an integer. The toint function rounds the value down to 3 and stores it in a field named numbers_int .

CODE

Copy

...| eval numbers_int=toint(3.14)


```spl

...| eval numbers_int=toint(3.14)

```



## tomv(&lt;value&gt;)


### Description

This function takes one argument and returns the equivalent multivalue of the field, if any. You can use this function to convert a JSON array to a multivalue field.


### Usage

You can use this function with the eval , fieldformat , and where commands, and as part of eval expressions.

The &lt;value&gt; argument can be a valid JSON array or the name of a field that contains a valid JSON array.

The tomv function does not remove the quotation marks from the array values. To remove the quotation marks, use the json_array_to_mv function instead.

The following table describes how the tomv function converts specific types of values in search results. The function returns null for all other values.


| Value | Result |
| --- | --- |
| multivalue | The same value. |
| array | json_array_to_mv(&lt;value&gt;) |
| string | There is no conversion from string. |



### Basic examples

The following example creates an array in the ponies field, converts that array to a multivalue, and then stores the result in a field named mv_ponies :

CODE

Copy

... | eval ponies = json_array("Buttercup", "Fluttershy", "Rarity"), mv_ponies = tomv(ponies)


```spl

... | eval ponies = json_array("Buttercup", "Fluttershy", "Rarity"), mv_ponies = tomv(ponies)

```


The results look like this:


| _time | mv_ponies | ponies |
| --- | --- | --- |
| 2024-12-10 21:20:18 | "Buttercup""Fluttershy""Rarity" | ["Buttercup","Fluttershy","Rarity"] |



### Extended examples

Say you have a field in an event that is a JSON object that you need to convert to a multivalue because you want to call other multivalue functions. You could extract a JSON array from that object and then convert it to a multivalue field using the tomv function. The following example uses a string dubois and the json_object function for the array values.

CODE

Copy

| makeresults
| eval surname = json_array("dubois", json_object("name", "patel")), surname_mv=tomv(surname)


```spl

| makeresults
| eval surname = json_array("dubois", json_object("name", "patel")), surname_mv=tomv(surname)

```


The search results in a multivalue called mv_surname . Your search results look like this:


| _time | mv_surname | surname |
| --- | --- | --- |
| 2024-12-10 21:46:54 | "dubois" | ["dubois",{"name":"patel"}] |
|  | {"name":"patel"} |  |


Here is another example that uses this JSON object, which is in a field called cities in an event:

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


The following search extracts the entire JSON object from the cities field. The cities field contains only one object. The key is the entire object. This extraction can return any type of value.

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


The following search converts the extracted JSON object to a multivalue using the tomv function:

CODE

Copy

... |eval extracted_cities = json_extract(cities,"{}"), mv_cities = tomv(extracted_cities)


```spl

... |eval extracted_cities = json_extract(cities,"{}"), mv_cities = tomv(extracted_cities)

```


The search results look like this:


| Field | Results |
| --- | --- |
| extract_cities | {"cities":[{"name":"London","Bridges":[{"name":"Tower Bridge","length":801},{"name":"Millennium Bridge","length":1066}]},{"name":"Venice","Bridges":[{"name":"Rialto Bridge","length":157},{"name":"Bridge of Sighs","length":36},{"name":"Ponte della Paglia"}]},{"name":"San Francisco","Bridges":[{"name":"Golden Gate Bridge","length":8981},{"name":"Bay Bridge","length":23556}]}]} |
| mv_cities | "name": "London","Bridges": { "name": "Tower Bridge", "length": 801 }, { "name": "Millennium Bridge", "length": 1066 } |
|  | "name": "Venice","Bridges": { "name": "Rialto Bridge", "length": 157 }, { "name": "Bridge of Sighs", "length": 36 }, { "name": "Ponte della Paglia" } |
|  | "name": "San Francisco","Bridges": { "name": "Golden Gate Bridge", "length": 8981 }, { "name": "Bay Bridge", "length": 23556 } |



## tonumber(&lt;str&gt;,&lt;base&gt;)


### Description

This function converts the input string to a number. The string can be a field name or a value.


### Usage

You can use this function with the eval , fieldformat , and where commands, and as part of eval expressions.

The base argument is optional and is used only when the value argument is a string. The default base is 10. You can set the base argument to a number between 2 and 36, inclusive.

If the string contains a decimal point ( . ), then the tonumber function converts the string to a double. Otherwise, the function converts the string to an integer.

If the tonumber function can't parse a field value to a number, for example if the value contains a leading and trailing space, the function returns NULL. Use the trim function to remove leading or trailing spaces.

If the tonumber function can't parse a string to a number, the function returns an error. For example, the following search fails:

CODE

Copy

| makeresults
| eval result=tonumber("seven")


```spl

| makeresults
| eval result=tonumber("seven")

```



> **Note: Splunk platform supports 53 bit integers with 8 bits of precision. Integers larger than 53 bits are truncated.**



### Binary conversion

You can use this function to convert a string representation of a binary number to return the corresponding number in base 10. For example, the result of the following function is 5 :

eval result = tonumber("0101", 2)

This is because the decimal representation of 0101 is 5 .

For information about bitwise functions that you can use with the tonumber function, see Bitwise functions .


### Basic examples

The following example converts the string values for the store_sales field to numbers.

CODE

Copy

... | eval n=tonumber(store_sales)


```spl

... | eval n=tonumber(store_sales)

```


The following example takes the hexadecimal number and uses a base of 16 to return the number "164".

CODE

Copy

... | eval n=tonumber("0A4",16)


```spl

... | eval n=tonumber("0A4",16)

```


The following example trims any leading or trailing spaces from the values in the celsius field before converting it to a number.

CODE

Copy

... | eval temperature=tonumber(trim(celsius))


```spl

... | eval temperature=tonumber(trim(celsius))

```



## toobject(&lt;value&gt;)


### Description

This function takes one argument and returns the equivalent object value of the field, if any. You can use this function to convert a string to a valid JSON object.


### Usage

You can use this function with the eval , fieldformat , and where commands, and as part of eval expressions.

The &lt;value&gt; argument can be a string value or the name of a field that contains a string. The string must be formatted as a valid JSON object.

The following table describes how the toobject function converts specific types of values in search results. The function returns null for all other values.


| Value | Result |
| --- | --- |
| JSON object | The same value. |
| string | The string parsed as a JSON object. |



### Basic examples

The following example converts the string {name: "maria", age:25, status: "full-time"} to a JSON object named employee_record .

JSON

Copy

... | eval employee_record = toobject("{\"name\": \"maria\", \"age\": 25, \"status\": \"full-time\"}")


```spl

... | eval employee_record = toobject("{\"name\": \"maria\", \"age\": 25, \"status\": \"full-time\"}")

```


The results look like this:


| _time | employee_record |
| --- | --- |
| 2024-12-17 19:28:07 | {"name":"maria","age":25,"status":"full-time"} |



## tostring(&lt;value&gt;,&lt;format&gt;)


### Description

This function converts a value to a string. If the value is a number, this function reformats it as a string. If the value is a Boolean value, it returns the corresponding string value, "True" or "False".


### Usage

You can use this function with the eval , fieldformat , and where commands, and as part of eval expressions.

The value argument can be a field name or a value.

Only integers in the range of 0 to 2 53 -1 are accepted as input to the function. For example, tostring("5", "binary") is not supported.

When you use the tostring function with the eval command, the returned values might not sort as expected because they are converted to ASCII. Use the fieldformat command with the tostring function to format the displayed values. The underlying values are not changed by the fieldformat command.

The format argument is optional and is only used when the value argument is a number. The tostring function supports the following formats.


| Format | Description |
| --- | --- |
| "binary" | Converts a number to a binary value. |
| "hex" | Converts the number to a hexadecimal value. |
| "commas" | Formats the number with commas. If the number includes a decimal, the function rounds the number to nearest two decimal places. |
| "duration" | Converts the value in seconds to the readable time format HH:MM:SS. |



### Binary conversion

You can use this function to convert a number to a string of its binary representation. For example, the result of the following function is 1001 , because the binary representation of 9 is 1001 .:

eval result = tostring(9, "binary")

For information about bitwise functions that you can use with the tostring function, see Bitwise functions .


### Basic examples

The following example returns "True 0xF 12,345.68".

CODE

Copy

... | eval n=tostring(1==1) + " " + tostring(15, "hex") + " " + tostring(12345.6789, "commas")


```spl

... | eval n=tostring(1==1) + " " + tostring(15, "hex") + " " + tostring(12345.6789, "commas")

```


The following example returns foo=615 and foo2=00:10:15 . The 615 seconds is converted into minutes and seconds.

CODE

Copy

... | eval foo=615 | eval foo2 = tostring(foo, "duration")


```spl

... | eval foo=615 | eval foo2 = tostring(foo, "duration")

```


The following example formats the column totalSales to display values with a currency symbol and commas. You must use a period between the currency value and the tostring function.

CODE

Copy

... | fieldformat totalSales="$".tostring(totalSales,"commas")


```spl

... | fieldformat totalSales="$".tostring(totalSales,"commas")

```



## See also

Commands

convert

Functions

strptime
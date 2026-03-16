
# Comparison and Conditional functions

The following list contains the functions that you can use to compare values or specify conditional statements.

For information about using string and numeric fields in functions, and nesting functions, see Evaluation functions .

For information about Boolean operators, such as AND and OR, see Boolean operators .


## case(&lt;condition&gt;,&lt;value&gt;,...)


### Description

Accepts alternating conditions and values. Returns the first value for which the condition evaluates to TRUE.

The &lt;condition&gt; arguments are Boolean expressions that are evaluated from first to last. When the first &lt;condition&gt; expression is encountered that evaluates to TRUE, the corresponding &lt;value&gt; argument is returned. The function defaults to NULL if none of the &lt;condition&gt; arguments are true.


### Usage

You can use this function with the eval , fieldformat , and where commands, and as part of eval expressions.


### Basic example


| This example uses the sample data from the Search Tutorial, but should work with any format of Apache Web access log. To try this example on your own Splunk instance, you must download the sample data and follow the instructions toget the tutorial data into Splunk. Use theYesterdaytime range when you run the search. |
| --- |


The following example returns descriptions for the corresponding http status code.

CODE

Copy

sourcetype=access_\* | eval description=case(status==200, "OK", status==404, "Not found", status==500, "Internal Server Error") | table status description


```spl

sourcetype=access_* | eval description=case(status==200, "OK", status==404, "Not found", status==500, "Internal Server Error") | table status description

```


The results appear on the Statistics tab and look like this:


| status | description |
| --- | --- |
| 200 | OK |
| 200 | OK |
| 408 |  |
| 200 | OK |
| 404 | Not found |
| 200 | OK |
| 406 |  |
| 500 | Internal Server Error |
| 200 | OK |


For an example of how to display a default value when that status does not match one of the values specified, see the True function .


### Extended example

This example shows you how to use the case function in two different ways, to create categories and to create a custom sort order.


| This example uses recent earthquake data downloaded from theUSGS Earthquakes website. The data is a comma separated ASCII text file that contains magnitude (mag), coordinates (latitude, longitude), region (place), and so forth, for each earthquake recorded.You can download a current CSV file from theUSGS Earthquake Feedsand upload the file to your Splunk instance if you want follow along with this example. |
| --- |


You want classify earthquakes based on depth. Shallow-focus earthquakes occur at depths less than 70 km. Mid-focus earthquakes occur at depths between 70 and 300 km. Deep-focus earthquakes occur at depths greater than 300 km. We'll use Low, Mid, and Deep for the category names.

CODE

Copy

source=all_month.csv 
| eval Description=case(depth&lt;=70, "Low", depth&gt;70 AND depth&lt;=300, "Mid", 
  depth&gt;300, "Deep") 
| stats count min(mag) max(mag) by Description


```spl

source=all_month.csv 
| eval Description=case(depth<=70, "Low", depth>70 AND depth<=300, "Mid", 
  depth>300, "Deep") 
| stats count min(mag) max(mag) by Description

```


The eval command is used to create a field called Description , which takes the value of "Low", "Mid", or "Deep" based on the Depth of the earthquake. The case() function is used to specify which ranges of the depth fits each description. For example, if the depth is less than 70 km, the earthquake is characterized as a shallow-focus quake; and the resulting Description is Low .

The search also pipes the results of the eval command into the stats command to count the number of earthquakes and display the minimum and maximum magnitudes for each Description.

The results appear on the Statistics tab and look like this:


| Description | count | min(Mag) | max(Mag) |
| --- | --- | --- | --- |
| Deep | 35 | 4.1 | 6.7 |
| Low | 6236 | -0.60 | 7.70 |
| Mid | 635 | 0.8 | 6.3 |


You can sort the results in the Description column by clicking the sort icon in Splunk Web. However in this example the order would be alphabetical returning results in Deep, Low, Mid or Mid, Low, Deep order.

You can also use the case function to sort the results in a custom order, such as Low, Mid, Deep. You create the custom sort order by giving the values a numerical ranking and then sorting based on that ranking.

CODE

Copy

source=all_month.csv 
| eval Description=case(depth&lt;=70, "Low", depth&gt;70 AND depth&lt;=300, "Mid", 
  depth&gt;300, "Deep") 
| stats count min(mag) max(mag) by Description
| eval sort_field=case(Description="Low", 1, Description="Mid", 2, Description="Deep",3) 
| sort sort_field


```spl

source=all_month.csv 
| eval Description=case(depth<=70, "Low", depth>70 AND depth<=300, "Mid", 
  depth>300, "Deep") 
| stats count min(mag) max(mag) by Description
| eval sort_field=case(Description="Low", 1, Description="Mid", 2, Description="Deep",3) 
| sort sort_field

```


The results appear on the Statistics tab and look something like this:


| Description | count | min(Mag) | max(Mag) |
| --- | --- | --- | --- |
| Low | 6236 | -0.60 | 7.70 |
| Mid | 635 | 0.8 | 6.3 |
| Deep | 35 | 4.1 | 6.7 |



## cidrmatch(&lt;cidr&gt;,&lt;ip&gt;)


### Description

This function returns TRUE when an IP address, &lt;ip&gt; , belongs to a particular CIDR subnet, &lt;cidr&gt; .

Both &lt;cidr&gt; and &lt;ip&gt; are string arguments. If you specify a literal string value, instead of a field name, that value must be enclosed in double quotation marks.

The cidrmatch function supports IPv4 and IPv6 addresses and subnets that use CIDR notation.


### Usage

You can use this function with the eval , fieldformat , and where commands, and as part of eval expressions.


### Basic examples

The following example uses the cidrmatch and if functions to set a field, isLocal , to "local" if the field ip matches the subnet. If the ip field does not match the subnet, the isLocal field is set to "not local".

CODE

Copy

... | eval isLocal=if(cidrmatch("123.132.32.0/25",ip), "local", "not local")


```spl

... | eval isLocal=if(cidrmatch("123.132.32.0/25",ip), "local", "not local")

```


The following example uses the cidrmatch function as a filter to remove events that do not match the ip address:

CODE

Copy

... | where cidrmatch("123.132.32.0/25", ip)


```spl

... | where cidrmatch("123.132.32.0/25", ip)

```



### Extended examples for IPv4 addresses

You can use the cidrmatch function to identify CIDR IP addresses by subnet. The following example uses cidrmatch with the eval command to compare an IPv4 address with a subnet that uses CIDR notation to determine whether the IP address is a member of the subnet. If there is a match, the search returns true in a new field called result .

CODE

Copy

| makeresults 
| eval subnet="192.0.2.0/24", ip="192.0.3.0"
| eval result=if(cidrmatch(subnet, ip), "true", "false")


```spl

| makeresults 
| eval subnet="192.0.2.0/24", ip="192.0.3.0"
| eval result=if(cidrmatch(subnet, ip), "true", "false")

```


The IP address is not in the subnet, so search displays false in the result field. The search results look something like this.


| time | ip | result | subnet |
| --- | --- | --- | --- |
| 2020-11-19 16:43:31 | 192.0.3.0 | false | 192.0.2.0/24 |


In the following example, cidrmatch evaluates the IPv4 address 192.0.2.56 to find out if it is in the subnet. This time, instead of using the eval command with the cidrmatch function, we're using the where command, which eliminates any IP addresses that aren't within the subnet. This search compares the CIDR IP address with the subnet and filters the search results by returning the IP address only if it is true.

CODE

Copy

| makeresults 
| eval ip="192.0.2.56" 
| where cidrmatch("192.0.2.0/24", ip)


```spl

| makeresults 
| eval ip="192.0.2.56" 
| where cidrmatch("192.0.2.0/24", ip)

```


The IP address is located within the subnet, so it is displayed in the search results, which look like this.


| time | ip |
| --- | --- |
| 2020-11-19 16:43:31 | 192.0.2.56 |


Note that you can get the same results when using the search command, as shown in this example.

CODE

Copy

| makeresults 
| eval ip="192.0.2.56" 
| search ip="192.0.2.0/24"


```spl

| makeresults 
| eval ip="192.0.2.56" 
| search ip="192.0.2.0/24"

```


The results of the search look like this.


| time | ip |
| --- | --- |
| 2020-11-19 16:43:31 | 192.0.2.56 |



### Extended examples for IPv6 addresses

The following example uses cidrmatch with the eval command to compare an IPv6 address with a subnet that uses CIDR notation to determine whether the IP address is a member of the subnet. If there is a match, search returns true in a new field called result .

CODE

Copy

| makeresults 
| eval subnet="2001:0db8:ffff:ffff:ffff:ffff:ffff:ff00/120", ip="2001:0db8:ffff:ffff:ffff:ffff:ffff:ff99"
| eval result = if(cidrmatch(subnet, ip), "true", "false")


```spl

| makeresults 
| eval subnet="2001:0db8:ffff:ffff:ffff:ffff:ffff:ff00/120", ip="2001:0db8:ffff:ffff:ffff:ffff:ffff:ff99"
| eval result = if(cidrmatch(subnet, ip), "true", "false")

```


The IP address is located within the subnet, so search displays true in the result field. The search results look something like this.


| time | ip | result | subnet |
| --- | --- | --- | --- |
| 2020-11-19 16:43:31 | 2001:0db8:ffff:ffff:ffff:ffff:ffff:ff99 | true | 2001:0db8:ffff:ffff:ffff:ffff:ffff:ff00/120 |


The following example is another way to use cidrmatch to identify which IP addresses are in a subnet. This time, instead of using the eval command with the cidrmatch function, we're using the where command. This search compares the CIDR IPv6 addresses with the specified subnet and filters the search results by returning only the IP addresses that are in the subnet.

CODE

Copy

| makeresults 
| eval ip="2001:0db8:ffff:ffff:ffff:ffff:ffff:ff99"
| where cidrmatch("2001:0db8:ffff:ffff:ffff:ffff:ffff:ff00/120", ip)


```spl

| makeresults 
| eval ip="2001:0db8:ffff:ffff:ffff:ffff:ffff:ff99"
| where cidrmatch("2001:0db8:ffff:ffff:ffff:ffff:ffff:ff00/120", ip)

```


The search results look something like this.


| time | ip |
| --- | --- |
| 2020-11-19 16:43:31 | 2001:0db8:ffff:ffff:ffff:ffff:ffff:ff99 |



### See also

Commands

iplocation

lookup

search


## coalesce(&lt;values&gt;)


### Description

This function takes one or more values and returns the first value that is not NULL.


### Usage

You can use this function with the eval , fieldformat , and where commands, and as part of eval expressions.


### Basic examples

You have a set of events where the IP address is extracted to either clientip or ipaddress . This example defines a new field called ip , that takes the value of either the clientip field or ipaddress field, depending on which field is not NULL (does not exist in that event). If both the clientip and ipaddress field exist in the event, this function returns the first argument, the clientip field.

CODE

Copy

... | eval ip=coalesce(clientip,ipaddress)


```spl

... | eval ip=coalesce(clientip,ipaddress)

```



## false()


### Description

Use this function to return FALSE.

This function enables you to specify a conditional that is obviously false, for example 1==0. You do not specify a field with this function.


### Usage

This function is often used as an argument with other functions.

You can use this function with the eval , fieldformat , and where commands, and as part of eval expressions.


### Basic examples


## if(&lt;predicate&gt;,&lt;true_value&gt;,&lt;false_value&gt;)


### Description

If the &lt;predicate&gt; expression evaluates to TRUE, returns the &lt;true_value&gt; , otherwise the function returns the &lt;false_value&gt; .


### Usage

You can use this function with the eval , fieldformat , and where commands, and as part of eval expressions.

The if function is frequently used in combination with other functions.


### Basic examples

The following example looks at the values of the field error . If error=200 , the function returns err=OK . Otherwise the function returns err=Error .

CODE

Copy

... | eval err=if(error == 200, "OK", "Error")


```spl

... | eval err=if(error == 200, "OK", "Error")

```


The following example uses the cidrmatch and if functions to set a field, isLocal , to "local" if the field ip matches the subnet. If the ip field does not match the subnet, the isLocal field is set to "not local".

CODE

Copy

... | eval isLocal=if(cidrmatch("123.132.32.0/25",ip), "local", "not local")


```spl

... | eval isLocal=if(cidrmatch("123.132.32.0/25",ip), "local", "not local")

```



## in(&lt;field&gt;,&lt;list&gt;)


### Description

The function returns TRUE if one of the values in the list matches a value that you specify.

This function takes a list of comma-separated values.


### Usage

You can use this function with the eval , fieldformat , and where commands, and as part of eval expressions with other commands.

The following syntax is supported:

...| where in(field,"value1","value2", ...)

...| where field in("value1","value2", ...)

...| eval new_field=if(in(field,"value1","value2", ...), "value-if_true","value-if-false")


> **Note: The eval command cannot accept a Boolean value. You must specify the in function inside a function that can accept a Boolean value as input. Those functions are: case , if , and validate .**


The string values must be enclosed in quotation marks. You cannot specify wildcard characters with the values to specify a group of similar values, such as HTTP error codes or CIDR IP address ranges. Use the IN operator instead.

The IN operator is similar to the in function. You can use the IN operator with the search and tstats commands. You can use wildcard characters in the VALUE-LIST with these commands.


### Basic examples

The following example uses the where command to return in=TRUE if one of the values in the status field matches one of the values in the list.

CODE

Copy

... | where status in("400", "401", "403", "404")


```spl

... | where status in("400", "401", "403", "404")

```


The following example uses the in function as the first parameter for the if function. The evaluation expression returns TRUE if the value in the status field matches one of the values in the list.

CODE

Copy

... | eval error=if(in(status, "error", "failure", "severe"),"true","false")


```spl

... | eval error=if(in(status, "error", "failure", "severe"),"true","false")

```


The following example uses the where command to return in=TRUE if the value 203.0.113.255 appears in either the ipaddress or clientip fields.

CODE

Copy

... | where "203.0.113.255" in(ipaddress, clientip)


```spl

... | where "203.0.113.255" in(ipaddress, clientip)

```



### Extended example

The following example combines the in function with the if function to evaluate the status field. The value of true is placed in the new field error if the status field contains one of the values 404, 500, or 503. Then a count is performed of the values in the error field.

CODE

Copy

... | eval error=if(in(status, "404","500","503"),"true","false") | stats count by error


```spl

... | eval error=if(in(status, "404","500","503"),"true","false") | stats count by error

```



### See also

Blogs

Smooth operator | Searching for multiple field values


## like(&lt;str&gt;,&lt;pattern&gt;)


### Description

This function returns TRUE only if &lt;str&gt; matches &lt;pattern&gt; . The match can be an exact match or a match using a wildcard:

- Use the percent ( % ) symbol as a wildcard for matching multiple characters

- Use the underscore ( _ ) character as a wildcard to match a single character

The &lt;str&gt; can be a field name or a string value. The &lt;pattern&gt; must be a string expression enclosed in double quotation marks.


### Usage

You can use this function with the eval , fieldformat , and where commands, and as part of eval expressions.

The following syntax is supported:

...|eval new_field=if(like(&lt;str&gt;, &lt;pattern&gt;)

...| where like(&lt;str&gt;, &lt;pattern&gt;)

...| where &lt;str&gt; LIKE &lt;pattern&gt;


> **Note: The eval command cannot accept a Boolean value. You must specify the like function inside a function that can accept a Boolean value as input. Those functions are: case , if , and validate .**



### Basic examples

The following example returns like=TRUE if the field value starts with foo:

CODE

Copy

... | eval is_a_foo=if(like(field, "foo%"), "yes a foo", "not a foo")


```spl

... | eval is_a_foo=if(like(field, "foo%"), "yes a foo", "not a foo")

```


The following example uses the where command to return like=TRUE if the ipaddress field starts with the value 198. . The percent ( % ) symbol is a wildcard with the like function:

CODE

Copy

... | where like(ipaddress, "198.%")


```spl

... | where like(ipaddress, "198.%")

```



## lookup(&lt;lookup_table&gt;,&lt;json_object&gt;,&lt;json_array&gt;)


### Description

This function performs a CSV lookup. It returns the output field or fields in the form of a JSON object.


> **Note: The lookup() function is available only to Splunk Enterprise users.**



### Syntax

lookup("&lt;lookup_table&gt;", json_object("&lt;input_field&gt;", &lt;match_field&gt;,...), json_array("&lt;output_field&gt;",...))


### Usage

You can use the lookup() function with the eval , fieldformat , and where commands, and as part of eval expressions.

The lookup() function takes an &lt;input_field&gt; from a CSV &lt;lookup_table&gt; , finds events in the search result that have the &lt;match_field&gt; , and then identifies other field-value pairs from from the CSV table that correspond to the input_field and adds them to the matched events in the form of a JSON object.

The lookup() requires a &lt;lookup_table&gt; . You can provide this either a CSV lookup file or CSV lookup definition, enclosed within quotation marks. To provide a file, give the full filename of a CSV lookup file that is stored in the global lookups directory ( $SPLUNK_HOME/etc/system/lookups/ ) or in a lookup directory that matches your current app context, such as $SPLUNK_HOME/etc/users/&lt;user&gt;/&lt;app&gt;/lookups/ .

If the first quoted string does not end in ".csv", the eval processor assumes it is the name of a CSV lookup definition. Specified CSV lookup definitions must be shared globally. CSV lookup definitions cannot be private or shared to a specific app.


> **Note: Specify a lookup definition if you want the various settings associated with the definition to apply, such as limits on matches, case-sensitive match options, and so on.**


A lookup() function can use multiple &lt;input_field&gt; / &lt;match_field&gt; pairs to identify events, and multiple &lt;output_field&gt; values can be applied to those events. Here is an example of valid lookup() syntax with multiple inputs, matches, and outputs.

CODE

Copy

... | eval &lt;string&gt;=lookup("&lt;lookup_table&gt;", json_object("&lt;input_field1&gt;", &lt;match_field1&gt;, "&lt;input_field2&gt;", &lt;match_field2&gt;), json_array("&lt;output_field1&gt;", "&lt;output_field2&gt;", "&lt;output_field3&gt;")


```spl

... | eval <string>=lookup("<lookup_table>", json_object("<input_field1>", <match_field1>, "<input_field2>", <match_field2>), json_array("<output_field1>", "<output_field2>", "<output_field3>")

```


For more information about uploading CSV lookup files and creating CSV lookup definitions, see Define a CSV lookup in Splunk Web in the Knowledge Manager Manual .

The lookup() function uses two JSON functions for eval : json_object and json_array . JSON functions allow the eval processor to efficiently group things together. For more information, see JSON functions in the Search Reference .


### Examples

These examples show different ways to use the lookup() function.


### 1. Simple example that returns a JSON object with an array

This simple makeresults example returns an array that illustrates what status_description values are paired in the http_status.csv lookup table with a status_type of Successful .

This search returns: output={"status_description":["OK","Created","Accepted","Non-Authoritative Information","No Content","Reset Content","Partial Content"]}

CODE

Copy

| makeresults 
| eval type = "Successful" 
| eval output=lookup("http_status.csv", json_object("status_type", type), json_array("status_description"))


```spl

| makeresults 
| eval type = "Successful" 
| eval output=lookup("http_status.csv", json_object("status_type", type), json_array("status_description"))

```



### 2. Example of a search with multiple input and match field pairs

This search uses multiple input and match field pairs to show that an event with type="Successful" and status="200" matches a status_description of OK in the http_status.csv lookup table.

This search returns: output={"status_description":"OK"}

CODE

Copy

| makeresults 
| eval type = "Successful", status="200" 
| eval output=lookup("http_status.csv", json_object("status_type", type, "status", status), json_array("status_description"))


```spl

| makeresults 
| eval type = "Successful", status="200" 
| eval output=lookup("http_status.csv", json_object("status_type", type, "status", status), json_array("status_description"))

```



### 3. Get counts of HTTP status description and type pairs

This example matches values of a status field in a http_status.csv lookup file with values of status fields in the returned events. It then generates JSON objects as values of a status_details field, with the corresponding status_description and status_type field-value pairs, and adds them to the events. Finally, it provides counts of the JSON objects, broken out by object.

Here is an example of a JSON object returned by this search: status_details=JSON:{"status_description":"Created","status_type":"Successful"}

CODE

Copy

index=_internal 
| eval output=lookup("http_status.csv", json_object("status", status), json_array("status_description", "status_type")), status_details="JSON:".output 
| stats count by status_details


```spl

index=_internal 
| eval output=lookup("http_status.csv", json_object("status", status), json_array("status_description", "status_type")), status_details="JSON:".output 
| stats count by status_details

```



### 4. Get counts of the HTTP status description values that have been applied to your events by a HTTP status eval lookup

This example shows how you can nest a lookup function inside another eval function. In this case it is the json_extract JSON function. This extracts status_description field-value pairs from the json_array objects and applies them to corresponding events. The search then returns a count of events with status_description fields, broken out by status_description value.

Here is an example of an extracted status_description value returned by this search. Compare it to the result returned by the third example: status_details=Created

CODE

Copy

index=_internal 
| eval status_details=json_extract(lookup("http_status.csv", json_object("status", status), json_array("status_description")), "status_description") 
| stats count by status_details


```spl

index=_internal 
| eval status_details=json_extract(lookup("http_status.csv", json_object("status", status), json_array("status_description")), "status_description") 
| stats count by status_details

```



## match(&lt;str&gt;, &lt;regex&gt;)


### Description

This function returns TRUE if the regular expression &lt;regex&gt; finds a match against any substring of the string value &lt;str&gt; . Otherwise returns FALSE.


### Usage

The match function is regular expression based. For example use the backslash ( \ ) character to escape a special character, such as a quotation mark. Use the pipe ( | ) character to specify an OR condition.

You can use this function with the eval , fieldformat , and where commands, and as part of eval expressions.


### Basic examples

The following example returns TRUE if, and only if, field matches the basic pattern of an IP address. This examples uses the caret ( ^ ) character and the dollar ( $ ) symbol to perform a full match.

CODE

Copy

... | eval n=if(match(field, "^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"), 1, 0)


```spl

... | eval n=if(match(field, "^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"), 1, 0)

```


The following example uses the match function in an &lt;eval-expression&gt;. The &lt;str&gt; is a calculated field called test . The &lt;regex&gt; is the string yes .

CODE

Copy

...  | eval matches = if(match(test,"yes"), 1, 0)


```spl

...  | eval matches = if(match(test,"yes"), 1, 0)

```


If the value is stored with quotation marks, you must use the backslash ( \ ) character to escape the embedded quotation marks. For example:

CODE

Copy

| makeresults | eval test="\"yes\""  | eval matches = if(match(test, "\"yes\""), 1, 0)


```spl

| makeresults | eval test="\"yes\""  | eval matches = if(match(test, "\"yes\""), 1, 0)

```



## null()


### Description

This function takes no arguments and returns NULL. The evaluation engine uses NULL to represent "no value". Setting a field value to NULL clears the field value.


### Usage

NULL values are field values that are missing in a some results but present in another results.

You can use this function with the eval , fieldformat , and where commands, and as part of eval expressions.


### Basic examples

Suppose you want to calculate the average of the values in a field, but several of the values are zero. If the zeros are placeholders for no value, the zeros will interfere with creating an accurate average. You can use the null function to remove the zeros.


### See also

- You can use the fillnull command to replace NULL values with a specified value.

- You can use the nullif(X,Y) function to compare two fields and return NULL if X = Y.


## nullif(&lt;field1&gt;, &lt;field2&gt;)


### Description

This function compares the values in two fields and returns NULL if the value in &lt;field1&gt; is equal to the value in &lt;field2&gt; . Otherwise the function returns the value in &lt;field1&gt; .


### Usage

You can use this function with the eval , fieldformat , and where commands, and as part of eval expressions.


### Basic example

Using the makeresults command, the following search creates a field called names . Another field called ponies is created based on the names field. The if function is used to change the name buttercup to mistmane in the ponies field.

CODE

Copy

| makeresults
| eval names="buttercup rarity tenderhoof dash"
| makemv delim=" " names
| mvexpand names
| eval ponies = if(names="buttercup", "mistmane", names)


```spl

| makeresults
| eval names="buttercup rarity tenderhoof dash"
| makemv delim=" " names
| mvexpand names
| eval ponies = if(names="buttercup", "mistmane", names)

```


The results look like this:


| _time | names | ponies |
| --- | --- | --- |
| 2022-10-17 14:57:12 | buttercup | mistmane |
| 2022-10-17 14:57:12 | rarity | rarity |
| 2022-10-17 14:57:12 | tenderhoof | tenderhoof |
| 2022-10-17 14:57:12 | dash | dash |


Using the nullif function, you can compare the values in the names and ponies fields. If the values are different, the value from the first field specified are displayed in the compare field. If the values are the same, no value is returned.

CODE

Copy

... eval compare = nullif(names, ponies)


```spl

... eval compare = nullif(names, ponies)

```


The results look like this:


| _time | compare | names | ponies |
| --- | --- | --- | --- |
| 2022-10-17 14:57:12 | buttercup | buttercup | mistmane |
| 2022-10-17 14:57:12 |  | rarity | rarity |
| 2022-10-17 14:57:12 |  | tenderhoof | tenderhoof |
| 2022-10-17 14:57:12 |  | dash | dash |



## searchmatch(&lt;search_str&gt;)


### Description

This function returns TRUE if the event matches the search string.


### Usage

To use the searchmatch function with the eval command, you must use the searchmatch function inside the if function.

You can use this function with the eval , fieldformat , and where commands, and as part of eval expressions.


### Basic examples

The following example uses the makeresults command to create some simple results. The searchmatch function is used to determine if any of the results match the search string "x=hi y=\*" .

CODE

Copy

| makeresults 1 
| eval _raw = "x=hi y=bye" 
| eval x="hi" 
| eval y="bye" 
| eval test=if(searchmatch("x=hi y=\*"), "yes", "no") 
| table _raw test x y


```spl

| makeresults 1 
| eval _raw = "x=hi y=bye" 
| eval x="hi" 
| eval y="bye" 
| eval test=if(searchmatch("x=hi y=*"), "yes", "no") 
| table _raw test x y

```


The result of the if function is yes ; the results match the search string specified with the searchmatch function.


## true()


### Description

Use this function to return TRUE.

This function enables you to specify a condition that is obviously true, for example 1==1. You do not specify a field with this function.


### Usage

This function is often used as an argument with other functions.

You can use this function with the eval , fieldformat , and where commands, and as part of eval expressions.


### Basic examples


| This example uses the sample data from the Search Tutorial, but should work with any format of Apache Web access log. To try this example on your own Splunk instance, you must download the sample data and follow the instructions toget the tutorial data into Splunk. Use theYesterdaytime range when you run the search. |
| --- |


The following example shows how to use the true() function to provide a default value to the case function. If the values in the status field are not 200, or 404, the value used is Other.

CODE

Copy

sourcetype=access_\* | eval description=case(status==200,"OK", status==404, "Not found", true(), "Other") | table status description


```spl

sourcetype=access_* | eval description=case(status==200,"OK", status==404, "Not found", true(), "Other") | table status description

```


The results appear on the Statistics tab and look like this:


| status | description |
| --- | --- |
| 200 | OK |
| 200 | OK |
| 408 | Other |
| 200 | OK |
| 404 | Not found |
| 200 | OK |
| 200 | OK |
| 406 | Other |
| 200 | OK |



## validate(&lt;condition&gt;, &lt;value&gt;,...)


### Description

This function takes a list of conditions and values and returns the value that corresponds to the condition that evaluates to FALSE. This function defaults to NULL if all conditions evaluate to TRUE.

This function is the opposite of the case function.


### Usage

The &lt;condition&gt; arguments must be expressions.

The &lt;value&gt; arguments must be strings. You can use this function with the eval , fieldformat , and where commands, and as part of eval expressions.


### Basic examples

The following example runs a simple check for valid ports.

CODE

Copy

... | eval n=validate(isint(port), "ERROR: Port is not an integer", port &gt;= 1 AND port &lt;= 65535, "ERROR: Port is out of range")


```spl

... | eval n=validate(isint(port), "ERROR: Port is not an integer", port >= 1 AND port <= 65535, "ERROR: Port is out of range")

```

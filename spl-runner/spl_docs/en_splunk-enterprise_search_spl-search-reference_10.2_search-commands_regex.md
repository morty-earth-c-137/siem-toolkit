
# regex


## Description

Removes results that match or do not match the specified regular expression.


## Syntax

The required syntax is in bold .

regex

(&lt;field&gt;=&lt;regex-expression&gt; | &lt;field&gt;!=&lt;regex-expression&gt; | &lt;regex-expression&gt; )


### Required arguments

&lt;regex-expression&gt;

Syntax: "&lt;string&gt;"

Description: An unanchored regular expression. The regular expression must be a Perl Compatible Regular Expression supported by the PCRE library. Quotation marks are required.


### Optional arguments

&lt;field&gt;

Syntax: &lt;field&gt;

Description: Specify the field name from which to match the values against the regular expression.

You can specify that the regex command keeps results that match the expression by using &lt;field&gt;=&lt;regex-expression&gt;. To keep results that do not match, specify &lt;field&gt;!=&lt;regex-expression&gt;.

Default: _raw


## Usage

The regex command is a distributable streaming command. See Command types .

When you use regular expressions in searches, you need to be aware of how characters such as pipe ( | ) and backslash ( \ ) are handled. See SPL and regular expressions in the Search Manual .

Although != is valid within a regex command, NOT is not valid.

For general information about regular expressions, see About Splunk regular expressions in the Knowledge Manager Manual .


### The difference between the regex and rex commands

Use the regex command to remove results that match or do not match the specified regular expression.

Use the rex command to either extract fields using regular expression named groups, or replace or substitute characters in a field using sed expressions.


### Using the regex command with !=

If you use regular expressions in conjunction with the regex command, note that != behaves differently for the regex command than for the search command.

You can use a regex command with != to filter for events that don't have a field value matching the regular expression, or for which the field is null. For example, this search will include events that do not define the field Location .

CODE

Copy

... | regex Location!="Calaveras Farms"


```spl

... | regex Location!="Calaveras Farms"

```


The search command behaves the opposite way. You can use a search command with != to filter for events that don't contain a field matching the search string, and for which the field is defined. For example, this search will not include events that do not define the field Location .

CODE

Copy

... | search Location!="Calaveras Farms"


```spl

... | search Location!="Calaveras Farms"

```


If you use != in the context of the regex command, keep this behavior in mind and make sure you want to include null fields in your results.


## Examples


### 1. Keep only results that contain IP addresses in a non-routable class

This example keeps only search results whose "_raw" field contains IP addresses in the non-routable class A (10.0.0.0/8). This example uses a negative lookbehind assertion at the beginning of the expression.

CODE

Copy

... | regex _raw="(?&lt;!\d)10\.\d{1,3}\.\d{1,3}\.\d{1,3}(?!\d)"


```spl

... | regex _raw="(?<!\d)10\.\d{1,3}\.\d{1,3}\.\d{1,3}(?!\d)"

```



### 2. Keep only the results that match a valid email address

This example keeps only the results that match a valid email address. For example, buttercup@example.com.

CODE

Copy

...| regex  email="^([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})$"


```spl

...| regex  email="^([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})$"

```





> **Note: This regular expression is for example purposes only and isn't a fully RFC-compliant email address validator.**


The following table explains each part of the expression.


| Part of the expression | Description |
| --- | --- |
| ^ | Specifies the beginning of the string. |
| ([a-z0-9_\.-]+) | This is the first group in the expression. Specifies to match one or more lowercase letters, numbers, underscores, dots, or hyphens. The backslash ( \ ) character is used to escape the dot ( . ) character. The dot character is escaped, because a non-escaped dot matches any character. The plus ( + ) sign specifies to match from 1 to unlimited characters in this group. In this example this part of the expression matchesbuttercupin the email address buttercup@example.com. |
| @ | Matches theatsymbol. |
| ([\da-z\.-]+) | This is the second group in the expression. Specifies to match the domain name, which can be one or more lowercase letters, numbers, underscores, dots, or hyphens. This is followed by another escaped dot character. The plus ( + ) sign specifies to match from 1 to unlimited characters in this group. In this example this part of the expression matchesexamplein the email address buttercup@example.com. |
| ([a-z\.]{2,6}) | This is the third group. Specifies to match the top-level domain (TLD), which can be 2 to 6 letters or dots. This group matches all types of TLDs, such as.co.uk,.edu, or.asia. In this example it matches.comin the email address buttercup@example.com. |
| $ | Specifies the end of the string. |



### 3. Filter out zip codes with a specific format

Filter out zip codes that are formatted like a United States zip code or zip+4 code. For example, this search would return a Canadian zip code.

CODE

Copy

... | regex not_usa_zip!="[0-9]{5}(-[0-9]{4})?"


```spl

... | regex not_usa_zip!="[0-9]{5}(-[0-9]{4})?"

```





### 4. Filter events where a field has no value

The search with regex and != in the following example creates 5 events with Country="Canada" and 5 events with City="Toronto", and filters on events where Country does not equal "Canada".

CODE

Copy

| makeresults count=5 | eval Country="Canada"    
| append [
| makeresults count=5 | eval City="Toronto"    
    ] 
| regex Country!="Canada"


```spl

| makeresults count=5 | eval Country="Canada"    
| append [
| makeresults count=5 | eval City="Toronto"    
    ] 
| regex Country!="Canada"

```


This search returns the union of two groups of events: events where the field Country is defined and has a value not equal to "Canada"; and events where the field Country is not defined. As a result, 5 events are displayed for the City field, even though a Country field was not defined for those events. Also, the Country field is displayed, but the values are null. The results look something like this.


| _time | City | Country |
| --- | --- | --- |
| Toronto |  | 2025-11-02 15:48:47 |
| Toronto |  | 2025-11-02 15:48:47 |
| Toronto |  | 2025-11-02 15:48:47 |
| Toronto |  | 2025-11-02 15:48:47 |
| Toronto |  | 2025-11-02 15:48:47 |


In contrast, the search with search and != in the following example doesn't return any events because all of the events with field City where the field Country is null are excluded.

CODE

Copy

| makeresults count=5 | eval Country="Canada"  
| append [
| makeresults count=5 | eval City="Toronto" 
    ] 
| search Country!="Canada"


```spl

| makeresults count=5 | eval Country="Canada"  
| append [
| makeresults count=5 | eval City="Toronto" 
    ] 
| search Country!="Canada"

```



## See also

Commands

rex

search
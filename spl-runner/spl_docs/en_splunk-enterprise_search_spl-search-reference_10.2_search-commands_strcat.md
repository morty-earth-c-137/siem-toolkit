
# strcat


## Description

Concatenates string values from 2 or more fields. Combines together string values and literals into a new field. A destination field name is specified at the end of the strcat command.


## Syntax

strcat [allrequired=&lt;bool&gt;] &lt;source-fields&gt; &lt;dest-field&gt;


### Required arguments

&lt;dest-field&gt;

Syntax: &lt;string&gt;

Description: A destination field to save the concatenated string values in, as defined by the &lt;source-fields&gt; argument. The destination field is always at the end of the series of source fields.

&lt;source-fields&gt;

Syntax: (&lt;field&gt; | &lt;quoted-str&gt;)...

Description: Specify the field names and literal string values that you want to concatenate. Literal values must be enclosed in quotation marks.

quoted-str

Syntax: "&lt;string&gt;"

Description: Quoted string literals.

Examples: "/" or ":"


### Optional arguments

allrequired

Syntax: allrequired=&lt;bool&gt;

Description: Specifies whether or not all source fields need to exist in each event before values are written to the destination field. If allrequired=f , the destination field is always written and source fields that do not exist are treated as empty strings. If allrequired=t , the values are written to destination field only if all source fields exist.

Default: false


## Usage

The strcat command is a distributable streaming command. See Command types .


## Examples


### Example 1:

Add a field called comboIP, which combines the source and destination IP addresses. Separate the addresses with a forward slash character.

CODE

Copy

... | strcat sourceIP "/" destIP comboIP


```spl

... | strcat sourceIP "/" destIP comboIP

```



### Example 2:

Add a field called comboIP, which combines the source and destination IP addresses. Separate the addresses with a forward slash character. Create a chart of the number of occurrences of the field values.

CODE

Copy

host="mailserver" | strcat sourceIP "/" destIP comboIP | chart count by comboIP


```spl

host="mailserver" | strcat sourceIP "/" destIP comboIP | chart count by comboIP

```



### Example 3:

Add a field called address, which combines the host and port values into the format &lt;host&gt;::&lt;port&gt;.

CODE

Copy

... | strcat host "::" port address


```spl

... | strcat host "::" port address

```



## See also

eval

# filldown


## Description

Replaces null values with the last non-null value for a field or set of fields. If no list of fields is given, the filldown command will be applied to all fields. If there are not any previous values for a field, it is left blank (NULL).


## Syntax

filldown &lt;wc-field-list&gt;


### Required arguments

&lt;wc-field-list&gt;

Syntax: &lt;field&gt; ...

Description: A space-delimited list of field names. You can use the asterisk ( \* ) as a wildcard to specify a list of fields with similar names. For example, if you want to specify all fields that start with "value", you can use a wildcard such as value\* .


## Examples


### Example 1:

Filldown null values for all fields.

CODE

Copy

... | filldown


```spl

... | filldown

```



### Example 2:

Filldown null values for the count field only.

CODE

Copy

... | filldown count


```spl

... | filldown count

```



### Example 3:

Filldown null values for the count field and any field that starts with 'score'.

CODE

Copy

... | filldown count score\*


```spl

... | filldown count score*

```



## See also

fillnull
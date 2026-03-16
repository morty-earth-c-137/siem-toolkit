
# iconify


## Description

Causes Splunk Web to display an icon for each different value in the list of fields that you specify.

The iconify command adds a field named _icon to each event. This field is the hash value for the event. Within Splunk Web, a different icon for each unique value in the field is displayed in the events list. If multiple fields are listed, the UI displays a different icon for each unique combination of the field values.


## Syntax

iconify &lt;field-list&gt;


### Required arguments

field-list

Syntax: &lt;field&gt;...

Description: Comma or space-delimited list of fields. You cannot specify a wildcard character in the field list.


## Usage

The iconify command is a distributable streaming command. See Command types .


## Examples


### 1. Display a different icon for each eventtype

CODE

Copy

... | iconify eventtype


```spl

... | iconify eventtype

```



### 2. Display a different icon for unique pairs of field values

Display a different icon for unique pair of clientip and method values.

CODE

Copy

... | iconify clientip method


```spl

... | iconify clientip method

```


Here is how Splunk Web displays the results in your Events List :




## See also

highlight
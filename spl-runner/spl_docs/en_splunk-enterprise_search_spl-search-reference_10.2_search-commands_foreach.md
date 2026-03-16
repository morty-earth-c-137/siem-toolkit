
# foreach


## Description

Use this command to run a subsearch that includes a template to iterate over the following elements:

- Each field in a wildcard field list

- Each value in a single multivalue field

- A single field representing a JSON array

Read use cases from Splunk platform experts about improving Splunk platform searches with the foreach command in the Splunk Lantern Customer Success Center.


## Syntax

The required syntax is in bold .

foreach

mode=(auto_collections | multivalue | json_array | multifield)

&lt;wildcard-field-list&gt; | &lt;field&gt;

[&lt;mode-options&gt;]

&lt;subsearch&gt;

[&lt;subsearch-options&gt;]


### Required arguments

wildcard-field-list

Syntax: &lt;string&gt; ...

Description: A space-delimited wildcard field name or list of wildcard field names that is used to iterate over one or more fields in a search. You can use the asterisk ( \* ) as a wildcard to specify a list of fields with similar names. For example, if you want to specify all fields that start with "value", you can use a wildcard field such as value\* . You can also specify a list of wildcard fields, such as hostA\* hostB\* hostC\* .

You can use this argument only with the multifield mode.

field

Syntax: &lt;string&gt;

Description: A field name that is used when iterating over elements in a multivalue field or JSON array, using the multivalue mode or json_array mode in a search.

subsearch

Syntax: [ subsearch ]

Description: A subsearch that includes a template for replacing the values of the specified fields, which depends on which mode you are using: auto_collections , multivalue , json_array or multifield .

For each field that is matched, the templated subsearch replaces values as follows:


| Option | Default template value | Replacement | Mode |
| --- | --- | --- | --- |
| fieldstr | &lt;&lt;FIELD&gt;&gt; | The whole field name. | multifield |
| matchstr | &lt;&lt;MATCHSTR&gt;&gt; | The part of the field name that matches the wildcard values in the wildcard field. | multifield |
| matchseg1 | &lt;&lt;MATCHSEG1&gt;&gt; | The part of the field name that matches the first wildcard. | multifield |
| matchseg2 | &lt;&lt;MATCHSEG2&gt;&gt; | The part of the field name that matches the second wildcard. | multifield |
| matchseg3 | &lt;&lt;MATCHSEG3&gt;&gt; | The part of the field name that matches the third wildcard. | multifield |
| itemstr | &lt;&lt;ITEM&gt;&gt; | Matches each element in a multivalue field or JSON array. | auto_collections, multivalue, json_array |
| iterstr | &lt;&lt;ITER&gt;&gt; | Matches each number in a multivalue field or JSON array. Use as a placeholder for a zero-based iterator in the multivalue field or JSON array. | auto_collections, multivalue, json_array |



### Optional arguments

mode

Syntax: mode=&lt;mode-name&gt;

Description: Tells the foreach command to iterate over multiple fields, a multivalue field, or a JSON array. If a mode is not specified, the foreach command defaults to the mode for multiple fields, which is the multifield mode.

You can specify one of the following modes for the foreach command:


| Argument | Syntax | Description |
| --- | --- | --- |
| auto_collections | mode=auto_collections | Dynamically iterates over a JSON array or multivalue field depending on which element is present in the search. When you use this mode, you don't need to know whether your functions return JSON arrays or multivalue fields.Theauto_collectionsmode can only be used with theevalcommand. |
| multivalue | mode=multivalue | Iterates over a single supplied multivalue field. Use this mode if your search returns multivalue fields. Add&lt;&lt;ITEM&gt;&gt;to your subsearch as a reference to the iterable object, or add&lt;&lt;ITER&gt;&gt;as a reference to the iterator.Themultivaluemode can only be used with theevalcommand. |
| json_array | mode=json_array | Iterates over a single supplied JSON array. Use this mode withJSON functions. Add&lt;&lt;ITEM&gt;&gt;to your subsearch as a reference to the iterable object, or add&lt;&lt;ITER&gt;&gt;as a reference to the iterator.Thejson_arraymode can only be used with theevalcommand. |
| multifield | mode=multifield | Iterates over a single supplied field name or a list of multiple field names, which can include wildcard characters.This is the default if themodeis not specified.Themultifieldmode can be used with any streaming command. |


mode options

The mode options depend on the mode you use.

Use the following options to iterate over a field or list of fields using the multifield mode. These options are available only with the multifield mode.


| Option | Syntax | Description |
| --- | --- | --- |
| fieldstr | fieldstr=&lt;string&gt; | A customizable string that replaces the&lt;&lt;FIELD&gt;&gt;template value with the name that you specify. The value of thefieldstroption must match the&lt;&lt;FIELD&gt;&gt;template value. For example, if you change the default&lt;&lt;FIELD&gt;&gt;template value toMYFIELD, then you must also change the value offieldstroption toMYFIELD. |
| matchstr | matchstr=&lt;string&gt; | A customizable string that replaces the&lt;&lt;MATCHSTR&gt;&gt;template value with the segment of the field name that matches the wildcard(s) in each field in the list. The value of thematchstroption must match the&lt;&lt;MATCHSTR&gt;&gt;template value. For example, if you change the default&lt;&lt;MATCHSTR&gt;&gt;template value toID, then you must also change the value ofmatchstrtoID.To avoid unpredictable results in searches, do not use thematchstroption with anymatchseg\*options. |
| matchseg1 | matchseg1=&lt;string&gt; | A customizable string that replaces the&lt;&lt;MATCHSEG1&gt;&gt;template value with the segment of the field name that matches the first wildcard in each field in the list. The value of thematchseg1option must match the&lt;&lt;MATCHSEG1&gt;&gt;template value. For example, if you change the default&lt;&lt;MATCHSEG1&gt;&gt;template value toPHONE, then you must also change the value ofmatchseg1toPHONE.To avoid unpredictable results in searches, do not use thematchseg1option with thematchstroption. |
| matchseg2 | matchseg2=&lt;string&gt; | A customizable string that replaces the&lt;&lt;MATCHSEG2&gt;&gt;template value with the segment of the field name that matches the second wildcard in each field in the list. The value of thematchseg2option must match the&lt;&lt;MATCHSEG2&gt;&gt;template value. For example, if you change the default&lt;&lt;MATCHSEG2&gt;&gt;template value toPRICE, then you must also change the value ofmatchseg2toPRICE.To avoid unpredictable results in searches, do not use thematchseg2option together with thematchstroption. |
| matchseg3 | matchseg3=&lt;string&gt; | A customizable string that replaces the&lt;&lt;MATCHSEG3&gt;&gt;template value with the segment of the field name that matches the third wildcard in each field in the list. The value of thematchseg3option must match the&lt;&lt;MATCHSEG3&gt;&gt;template value. For example, if you change the default&lt;&lt;MATCHSEG3&gt;&gt;template value toADDRESS, then you must also change the value ofmatchseg3toADDRESS.To avoid unpredictable results in searches, do not use thematchseg3option together with thematchstroption. |


Use the following options to iterate over multivalue fields or JSON arrays using the multivalue mode, the json_array mode, or the auto_collections mode.


| Option | Syntax | Description |
| --- | --- | --- |
| itemstr | itemstr=&lt;string&gt; | Replaces the&lt;&lt;ITEM&gt;&gt;template value with each element in a multivalue field or JSON array. Theitemstroption lets you redefine the placeholder for the item.The value of theitemstroption must match the&lt;&lt;ITEM&gt;&gt;template value. For example, if you change the default&lt;&lt;ITEM&gt;&gt;template value toNUMBER, then you must also change the value ofitemstrtoNUMBER, like this:CODECopy\| foreach mode=multivalue itemstr=&lt;&lt;NUMBER&gt;&gt; numbers 
    [ eval result = result + &lt;&lt;NUMBER&gt;&gt;]\| foreach mode=multivalue itemstr=&lt;&lt;NUMBER&gt;&gt; numbers 
    [ eval result = result + &lt;&lt;NUMBER&gt;&gt;] |
| iterstr | iterstr=&lt;string&gt; | Replaces the&lt;&lt;&lt;ITER&gt;&gt;template value with the index value in a multivalue field or JSON array. Theiterstroption lets you redefine the placeholder for the iterator, which is the count or index.The value of theiterstroption must match the&lt;&lt;ITER&gt;&gt;template value. For example, if you change the default&lt;&lt;ITER&gt;&gt;template value toNUMBER, then you must also change the value ofiterstrtoNUMBER.For example, consider the following search:CODECopy\| foreach mode=multivalue numbers 
    [ eval result = result + &lt;&lt;ITER&gt;&gt;]\| foreach mode=multivalue numbers 
    [ eval result = result + &lt;&lt;ITER&gt;&gt;]That search is equivalent to this search:CODECopy\| foreach mode=multivalue iterstr=&lt;&lt;NUMBER&gt;&gt; numbers 
    [ eval result = result + &lt;&lt;NUMBER&gt;&gt;]\| foreach mode=multivalue iterstr=&lt;&lt;NUMBER&gt;&gt; numbers 
    [ eval result = result + &lt;&lt;NUMBER&gt;&gt;] |


subsearch options

Syntax: &lt;option-name&gt;

Description:

The subsearch options depend on the mode you use.

You can use the following optional template values in a subsearch when iterating over one or more fields. These template values are available only with the multifield mode.


| Template value | Description |
| --- | --- |
| &lt;&lt;FIELD&gt;&gt; | A customizable string replacement for each field name in the field list. Each time you run a subsearch, this value is used to replace the whole field name in thefieldstroption for each field you specify. For example, if you change the value of&lt;&lt;FIELD&gt;&gt;toMYFIELD, then the value of thefieldstroption is alsoMYFIELD. Your search might look like this:...\|foreach test\* fieldstr=MYFIELD [eval total=total + MYFIELD]. |
| &lt;&lt;MATCHSTR&gt;&gt; | A customizable string replacement that represents wildcards in each matching field name in the list. For example, if the wildcard field that is being matched istest\*and the field name istest8, then the value of&lt;&lt;MATCHSTR&gt;&gt;is 8.To avoid unpredictable results in searches, do not use the&lt;&lt;MATCHSTR&gt;&gt;template value together with any&lt;&lt;MATCHSEG\*&gt;&gt;template values. |
| &lt;&lt;MATCHSEG1&gt;&gt; | A customizable string replacement for thesegmentof the field name that matches the first segment before the first wildcard in each matching field name in the list.To avoid unpredictable results in searches, do not use the&lt;&lt;MATCHSEG1&gt;&gt;template value with the&lt;&lt;MATCHSTR&gt;&gt;template value. |
| &lt;&lt;MATCHSEG2&gt;&gt; | A customizable string replacement for the segment of the field name that matches the second segment before the second wildcard in each matching field name in the list.To avoid unpredictable results in searches, do not use the&lt;&lt;MATCHSEG2&gt;&gt;template value with the &lt;&lt;&lt;MATCHSTR&gt;&gt;template value. |
| &lt;&lt;MATCHSEG3&gt;&gt; | A customizable string replacement for the segment of the field name that matches the third segment before the third wildcard in each matching field name in the list.To avoid unpredictable results in searches, do not use the&lt;&lt;MATCHSEG3&gt;&gt;template value with the&lt;&lt;MATCHSTR&gt;&gt;template value. |


You can use the following optional template values in a subsearch to iterate over elements or numbers in a multivalue field or JSON array. These template values are available with all modes except the multifield mode.


| Template value | Description |
| --- | --- |
| &lt;&lt;ITEM&gt;&gt; | A customizable string that replaces the &lt;&lt;ITEM&gt;&gt; template value with some other string that is substituted with the contents of the multivalue field or JSON array being iterated over. Only a singleevalstatement is permitted in the search pipeline when using this template value with themultivaluemode orjson_arraymode. |
| &lt;&lt;ITER&gt;&gt; | A customizable string that replaces the &lt;&lt;ITER&gt;&gt; template value with some other string that is substituted with the contents of the multivalue field or JSON array being iterated over. Only a singleevalstatement is permitted in the search pipeline when using this template value with themultivaluemode orjson_arraymode. |



## Usage

The foreach command is a streaming command .

You can use the foreach command in the following ways:

- To obtain results across multiple fields in each result row. This is useful, for example, when you need to calculate the average or sum of a value across multiple columns in each row. If you want to iterate over one or more matching fields, use the multifield mode.

- To iterate over multiple values within a single row's field in multivalue fields or JSON arrays. This is useful, for example, when you need to concatenate strings or calculate the average or sum of a set of numbers in a single field across multiple columns in each row in a multivalue field or JSON array. If you want to iterate over a multivalue field, use the multivalue mode. If you want to iterate over a JSON array node, use the json_array mode.

The default &lt;&lt;ITEM&gt;&gt; template value should be used only when the mode is multivalue or json_array .


### Supported commands

The foreach command with mode=multifield supports searches with any streaming command.

The foreach command with all other modes ( mode=auto_collections , mode=multivalue , or mode=json_array ) only supports searches with the eval command.




### Iterating over multiple matching fields containing nonalphanumeric characters

If the field names contain characters other than alphanumeric characters, such as dashes, underscores, or periods, enclose the &lt;&lt;FIELD&gt;&gt; template value in single quotation marks in the right side of the eval command portion of the search to avoid unpredictable results. For example, the following search uses the default foreach multifield mode and adds the values from all of the fields that match myfield_\* .

CODE

Copy

| makeresults
| eval myfield_1 = 5, myfield_2 = 10
| foreach myfield_\* 
       [eval &lt;&lt;FIELD&gt;&gt; = '&lt;&lt;FIELD&gt;&gt;' + &lt;&lt;MATCHSTR&gt;&gt;]


```spl

| makeresults
| eval myfield_1 = 5, myfield_2 = 10
| foreach myfield_* 
       [eval <<FIELD>> = '<<FIELD>>' + <<MATCHSTR>>]

```


The search results look something like this:


| _time | myfield_1 | myfield_2 |
| --- | --- | --- |
| 2023-3-14 15:55:50 | 6 | 12 |


The &lt;&lt;FIELD&gt;&gt; template value in the foreach subsearch is just a string replacement of the field named myfield_\* . The eval expression does not recognize field names with nonalphanumeric characters unless the field names are surrounded by single quotation marks. For the eval expression to work, the &lt;&lt;FIELD&gt;&gt; template value must be surrounded by single quotation marks.


### Support for multiple eval statements

If you need to include multiple eval statements with the foreach command, use the default multifield mode. Multiple eval statements are not supported in foreach searches that use multivalue mode or JSON array mode. As a result, your searches on multivalue fields or JSON arrays must contain only a single eval statement in the pipeline. However, your eval statement can include as many assignments as you want.

For example, the following multivalue search with multiple eval assignments completes successfully because there is only one eval statement, which means there aren't any piped commands following the eval command.

CODE

Copy

| makeresults
| eval mv=mvappend("5", "15"), total = 0, count = 0
| foreach mode=multivalue mv
     [eval total = total + &lt;&lt;ITEM&gt;&gt;, count = count + 1]


```spl

| makeresults
| eval mv=mvappend("5", "15"), total = 0, count = 0
| foreach mode=multivalue mv
     [eval total = total + <<ITEM>>, count = count + 1]

```


The search results look something like this.


| _time | count | mv | total |
| --- | --- | --- | --- |
| 2022-03-29 19:52:38 | 2 | 515 | 20 |



### Wildcards are not supported in multivalue fields or JSON arrays

Unlike multifield mode, the modes for multivalue fields and JSON arrays don't support wildcards in search expressions. Instead, these modes treat a wildcard as part of the field name. For example, the following search includes a field called mv\* , which looks like a wildcarded field.

CODE

Copy

| makeresults 
| eval mv1=mvappend("1", "2"), mv2=mvappend("3", "4"), mv\*=mvappend("100", "300"), total = 0
| foreach mode=multivalue mv\* 
     [eval total = total + &lt;&lt;ITEM&gt;&gt;]


```spl

| makeresults 
| eval mv1=mvappend("1", "2"), mv2=mvappend("3", "4"), mv*=mvappend("100", "300"), total = 0
| foreach mode=multivalue mv* 
     [eval total = total + <<ITEM>>]

```




However, multivalue and JSON array modes don't recognize the wildcard and add up all of the fields containing


```spl

mv

```


. As a result, the search results for multivalue mode look something like this:




| _time | mv\* | mv1 | mv2 | total |
| --- | --- | --- | --- | --- |
| 2022-4-20 15:55:50 | 100300 | 12 | 34 | 400 |



### Elements of the same type in multivalue fields or JSON arrays

Elements in a subsearch and the eval expression must be of the same type as either strings or numbers. For example, the following search correctly adds up the three numbers in the JSON array because all of the elements are numbers.

CODE

Copy

| foreach json_array(1, 2, 3) 
     [eval total = total + &lt;&lt;ITEM&gt;&gt;]


```spl

| foreach json_array(1, 2, 3) 
     [eval total = total + <<ITEM>>]

```


However, the following search results in an error because adding a number to a string isn't allowed.

CODE

Copy

| foreach json_array(1, 2, "hello") 
     [eval total = total + &lt;&lt;ITEM&gt;&gt;]


```spl

| foreach json_array(1, 2, "hello") 
     [eval total = total + <<ITEM>>]

```



## Examples


### 1. Generate a total for each row in search results

Suppose you have events that contain the following data:


| categoryId | www1 | www2 |
| --- | --- | --- |
| ACCESSORIES | 1000 | 500 |
| SIMULATION | 3000 | 750 |
| ARCADE | 800 |  |
| STRATEGY | 400 | 200 |


Use the foreach command with the default multifield mode to iterate over each field that starts with www and generate a total for each row in the search results.

CODE

Copy

...| eval total=0
| foreach www\* 
     [eval total=total + &lt;&lt;FIELD&gt;&gt;]


```spl

...| eval total=0
| foreach www* 
     [eval total=total + <<FIELD>>]

```


The results look like this:


| categoryId | www1 | www2 | total |
| --- | --- | --- | --- |
| ACCESSORIES | 1000 | 500 | 1500 |
| SIMULATION | 3000 | 750 | 3750 |
| ARCADE | 800 |  | 800 |
| STRATEGY | 400 | 200 | 600 |



### 2. Add the values from all fields that start with similar names

The following search adds the values from all of the fields that start with similar names and match the wildcard field test\* . It uses the foreach command with the default multifield mode

CODE

Copy

| makeresults
| eval total=0, test1=1, test2=2, test3=3 
| foreach test\* 
     [eval total=total + &lt;&lt;FIELD&gt;&gt;]


```spl

| makeresults
| eval total=0, test1=1, test2=2, test3=3 
| foreach test* 
     [eval total=total + <<FIELD>>]

```


The results of the search look something like this.


| _time | test1 | test2 | test3 | total |
| --- | --- | --- | --- | --- |
| 2022-4-20 15:55:50 | 1 | 2 | 3 | 6 |


- This search creates one result using the makeresults command.

- The search then uses the eval command to create the fields total , test1 , test2 , and test3 with corresponding values.

- The foreach command is used to perform the subsearch for every field that starts with "test". Each time the subsearch is run, the previous total is added to the value of the test field to calculate the new total. The final total after all of the test fields are processed is 6.

The following table shows how the subsearch iterates over each test field. The table shows the beginning value of the total field each time the subsearch is run and the calculated total based on the value for the test field.


| Subsearch iteration | test field | total field start value | test field value | calculation of total field |
| --- | --- | --- | --- | --- |
| 1 | test1 | 0 | 1 | 0+1=1 |
| 2 | test2 | 1 | 2 | 1+2=3 |
| 3 | test3 | 3 | 3 | 3+3=6 |



### 3. Iterate over fields using the eval and foreach commands

The eval command and foreach command can be used in similar ways. For example, this search uses the eval command:

CODE

Copy

| makeresults
| eval name="name" | eval price="price" | eval category="category"


```spl

| makeresults
| eval name="name" | eval price="price" | eval category="category"

```


It is equivalent to this search that uses the foreach command with the default multifield mode:

CODE

Copy

| makeresults 
| foreach name price category 
     [eval &lt;&lt;FIELD&gt;&gt; = "&lt;&lt;FIELD&gt;&gt;"]


```spl

| makeresults 
| foreach name price category 
     [eval <<FIELD>> = "<<FIELD>>"]

```


The results of both searches look something like this:


| _time | category | name | price |
| --- | --- | --- | --- |
| 2022-4-20 15:55:50 | category | name | price |



### 4. Monitor license usage

Use the foreach command to monitor license usage.

First run the following search on the license manager to return the daily license usage per source type in bytes:

CODE

Copy

index=_internal source=\*license_usage.log type!="\*Summary" earliest=-30d
| timechart span=1d sum(b) AS daily_bytes by st


```spl

index=_internal source=*license_usage.log type!="*Summary" earliest=-30d
| timechart span=1d sum(b) AS daily_bytes by st

```


The search results for one user across several days looks something like this:


| _time | csv | universal_data_json |
| --- | --- | --- |
| 2022-04-03 | 8308923 | 36069628 |
| 2022-04-04 | 7290647 | 48851560 |
| 2022-04-05 | 7676935 | 12542231 |
| 2022-04-06 | 3016517 | 17521059 |


You can also use the foreach command with the default multifield mode to calculate the daily license usage in gigabytes for each field:

CODE

Copy

index=_internal source=\*license_usage.log type!="\*Summary" earliest=-30d
| timechart span=1d sum(b) AS daily_bytes by st
| foreach \* [eval &lt;&lt;FIELD&gt;&gt;='&lt;&lt;FIELD&gt;&gt;'/1024/1024/1024]


```spl

index=_internal source=*license_usage.log type!="*Summary" earliest=-30d
| timechart span=1d sum(b) AS daily_bytes by st
| foreach * [eval <<FIELD>>='<<FIELD>>'/1024/1024/1024]

```


This time the search results look something like this:


| _time | csv | universal_data_json |
| --- | --- | --- |
| 2022-04-03 | 0.2335968237849277853 | 0.6309081468478106 |
| 2022-04-04 | 0.9703636813411461080 | 0.4818287762321547 |
| 2022-04-05 | 0.3825212419915378210 | 0.9126501722671725 |
| 2022-04-06 | 0.0028093503788113594 | 0.0163177577778697 |



### 5. Use the MATCHSTR template value

In this example, the &lt;&lt;FIELD&gt;&gt; template value is a placeholder for test , and the &lt;&lt;MATCHSTR&gt;&gt; template value represents the wildcarded value that follows test in each field name in the eval expression. This example uses the default multifield mode.

CODE

Copy

| makeresults
| eval test1 = 5, test2 = 10
| foreach test\* [eval &lt;&lt;FIELD&gt;&gt; = &lt;&lt;FIELD&gt;&gt; + &lt;&lt;MATCHSTR&gt;&gt;]


```spl

| makeresults
| eval test1 = 5, test2 = 10
| foreach test* [eval <<FIELD>> = <<FIELD>> + <<MATCHSTR>>]

```


The results look something like this:


| _time | test1 | test2 |
| --- | --- | --- |
| 2022-03-28 15:43:39 | 6 | 12 |


The value of each field is added to the value that replaces the wildcard in the field name. For example, for the test1 field, 5 + 1 = 6.


### 6. Use the MATCHSEG1 and MATCHSEG2 template values

This example uses the default multifield mode. The matchseg1 and matchseg2 options are used to add each field value to the two values represented by the wildcard in the corresponding &lt;&lt;MATCHSEG1&gt;&gt; and &lt;&lt;MATCHSEG2&gt;&gt; template values.

CODE

Copy

| makeresults
| eval test1ab2=5, test2ab3=10
| foreach test\*ab\* fieldstr=MYFIELD matchseg1=SEG1 matchseg2=SEG2 
     [eval MYFIELD = MYFIELD + SEG1 + SEG2]


```spl

| makeresults
| eval test1ab2=5, test2ab3=10
| foreach test*ab* fieldstr=MYFIELD matchseg1=SEG1 matchseg2=SEG2 
     [eval MYFIELD = MYFIELD + SEG1 + SEG2]

```


Let's take a closer look at the syntax for the test1ab2=5 eval expression:

- The wildcard field is test\*ab\* .

- The &lt;&lt;FIELD&gt;&gt; template value called MYFIELD is test1ab2=5 .

- The field value is 5.

- The &lt;&lt;MATCHSEG1&gt;&gt; template value called SEG1 is 1.

- The &lt;&lt;MATCHSEG2&gt;&gt; template value called SEG2 is 2.

The results of the search look something like this:


| _time | test1ab2 | test2ab3 |
| --- | --- | --- |
| 2022-03-28 17:10:56 | 8 | 15 |


The value of the test1ab2 field in the search results is 8 because 5 + 1 + 2 = 8.


### 7. Add values in a multivalue field using the auto_collections mode

In this example using the auto_collections mode, &lt;&lt;ITEM&gt;&gt; is a placeholder for each number in the multivalue field, which is added to the total.

CODE

Copy

| makeresults 
| eval mvfield=mvappend("1", "2", "3"), total=0 
| foreach mode=auto_collections
     [eval total = total + &lt;&lt;ITEM&gt;&gt;] 
| table mvfield, total


```spl

| makeresults 
| eval mvfield=mvappend("1", "2", "3"), total=0 
| foreach mode=auto_collections
     [eval total = total + <<ITEM>>] 
| table mvfield, total

```


The results of the search look something like this.


| _time | mvfield | total |
| --- | --- | --- |
| 2024-4-20 15:55:50 | 123 | 6 |


The previous search produces similar results as the following eval search, which also displays the total, but without listing each of the values that make up the total.

CODE

Copy

| makeresults
| eval total = 0
| eval total = total + 1 
| eval total = total + 2 
| eval total = total + 3


```spl

| makeresults
| eval total = 0
| eval total = total + 1 
| eval total = total + 2 
| eval total = total + 3

```


The search results look like this:


| _time | total |
| --- | --- |
| 2024-4-20 15:55:50 | 6 |



### 8. Calculate grade averages using multivalue fields

To find the average of a set of student grades using the multivalue mode, you could run this search:

CODE

Copy

| makeresults 
| eval teacher="James", student_grades=mvappend("50", "100", "30"), sum = 0, count = 0
| foreach mode=multivalue student_grades
    [eval sum = sum + &lt;&lt;ITEM&gt;&gt;, count = count + 1]
| eval average = sum / count


```spl

| makeresults 
| eval teacher="James", student_grades=mvappend("50", "100", "30"), sum = 0, count = 0
| foreach mode=multivalue student_grades
    [eval sum = sum + <<ITEM>>, count = count + 1]
| eval average = sum / count

```


The search results look something like this:


| _time | average | count | student_grades | sum | teacher |
| --- | --- | --- | --- | --- | --- |
| 2022-03-21 16:02:30 | 60 | 3 | 5010030 | 180 | James |



### 9. Add values in a JSON array

If you want to do something simple like add up each element in a JSON array, you could run a search like this:

CODE

Copy

| makeresults 
| eval jsonfield=json_array(1, 2, 3), total=0 
| foreach mode=json_array jsonfield 
     [eval total = total + &lt;&lt;ITEM&gt;&gt;] 
| table jsonfield, total


```spl

| makeresults 
| eval jsonfield=json_array(1, 2, 3), total=0 
| foreach mode=json_array jsonfield 
     [eval total = total + <<ITEM>>] 
| table jsonfield, total

```


The search results look like this:


| jsonfield | total |
| --- | --- |
| [1, 2, 3] | 6 |



### 10. Categorize employees by manager using multivalue fields

You can create lists of employee names and organize them by manager using the eval command or the foreach command. This is an example of a search on employees and their manager using the eval command:

CODE

Copy

| makeresults 
| eval manager="Rutherford", employees=mvappend("Alex", "Claudia", "David")
| fields - _time


```spl

| makeresults 
| eval manager="Rutherford", employees=mvappend("Alex", "Claudia", "David")
| fields - _time

```


The results of the eval search look something like this.


| employees | manager |
| --- | --- |
| AlexClaudiaDavid | Rutherford |


To create multivalue fields of employee names and organize them by manager, you can run a similar search using multivalue fields with the foreach command:

CODE

Copy

| makeresults 
| eval manager="Rutherford", employees=mvappend("Alex", "Claudia", "David"), employees_array=json_array()
| foreach mode=multivalue employees 
     [eval employees_array=json_append(employees_array, "", &lt;&lt;ITEM&gt;&gt;)]
| fields - _time


```spl

| makeresults 
| eval manager="Rutherford", employees=mvappend("Alex", "Claudia", "David"), employees_array=json_array()
| foreach mode=multivalue employees 
     [eval employees_array=json_append(employees_array, "", <<ITEM>>)]
| fields - _time

```


The search results this time look like this:


| employees | employees_array | manager |
| --- | --- | --- |
| AlexClaudiaDavid | ["Alex", "Claudia", "David"] | Rutherford |



### 11. Add values to a JSON array

Now let's take the names of the employees in a multivalue field and append them to a JSON array. In this search, the employees_array is empty.

CODE

Copy

| makeresults 
| eval manager="Rutherford", employees=mvappend("Alex", "Claudia", "David"), employees_array=json_array()
| fields - _time


```spl

| makeresults 
| eval manager="Rutherford", employees=mvappend("Alex", "Claudia", "David"), employees_array=json_array()
| fields - _time

```


The search results look like this:


| employees | employees_array | manager |
| --- | --- | --- |
| AlexClaudiaDavid | [ ] | Rutherford |


To copy all the values from the multivalue field into json_array() , use foreach to iterate over the employees values and append each of the employee names to the array, like this search:

CODE

Copy

| makeresults 
| eval manager="Rutherford", employees=mvappend("Alex", "Claudia", "David"), employees_array=json_array()
| foreach mode=multivalue employees 
     [eval employees_array=json_append(employees_array, "", &lt;&lt;ITEM&gt;&gt;)]
| fields - _time


```spl

| makeresults 
| eval manager="Rutherford", employees=mvappend("Alex", "Claudia", "David"), employees_array=json_array()
| foreach mode=multivalue employees 
     [eval employees_array=json_append(employees_array, "", <<ITEM>>)]
| fields - _time

```


Now the search results look like this:


| employees | employees_array | manager |
| --- | --- | --- |
| AlexClaudiaDavid | ["Alex", "Claudia", "David"] | Rutherford |


The foreach command just copied over each of the employees' names to the JSON array.


### 12. Extracting values from a JSON array

What if you want to extract values for given key names from a JSON array and do something with them? For example, the following search extracts a list of employee IDs from a JSON array of employees and puts them in a new field called ID_array that you can use for other operations.

CODE

Copy

| makeresults 
| eval manager="Rutherford", employees=mvappend("Alex", "Claudia", "David"), ID_array=json_array(), IDs=json_object("Alex", 4125, "Claudia", 2538, "David", 3957)
| foreach mode=multivalue employees 
     [eval ID_array=json_append(ID_array, "", json_extract(IDs, &lt;&lt;ITEM&gt;&gt;))]
| fields - _time


```spl

| makeresults 
| eval manager="Rutherford", employees=mvappend("Alex", "Claudia", "David"), ID_array=json_array(), IDs=json_object("Alex", 4125, "Claudia", 2538, "David", 3957)
| foreach mode=multivalue employees 
     [eval ID_array=json_append(ID_array, "", json_extract(IDs, <<ITEM>>))]
| fields - _time

```


The results of this search look something like this:


| ID_array | IDs | employees | manager |
| --- | --- | --- | --- |
| [4125,2538,3957] | {"Alex":4125,"Claudia":2538,"David":3957} | AlexClaudiaDavid | Rutherford |



### 13. Multiplying elements in a JSON array

You can use the foreach command to multiply numbers and append to a JSON array in searches like this:

CODE

Copy

| makeresults 
| eval price=json_array(1,2,3,4), double_price=json_array()
| foreach mode=json_array price 
    [eval double_price = json_append(double_price, "",  &lt;&lt;ITEM&gt;&gt; \* 2)]


```spl

| makeresults 
| eval price=json_array(1,2,3,4), double_price=json_array()
| foreach mode=json_array price 
    [eval double_price = json_append(double_price, "",  <<ITEM>> * 2)]

```


The results look something like this:


| _time | double_price | price |
| --- | --- | --- |
| 2022-03-21 16:24:49 | [2,4,6,8] | [1,2,3,4] |


This search doubles each value in the array in price and then adds the values to a new array called double_price .


### 14. Calculating weights

To find the weights of values in a JSON array called grades , you could run a search like this:

CODE

Copy

| makeresults 
| eval grades=json_array(1,2,3,4), weight=json_array()
| eval sum = 0
| foreach mode=json_array grades 
    [eval sum = sum + &lt;&lt;ITEM&gt;&gt;]
| foreach mode=json_array grades
    [eval weight = json_append(weight, "", &lt;&lt;ITEM&gt;&gt; / sum)]


```spl

| makeresults 
| eval grades=json_array(1,2,3,4), weight=json_array()
| eval sum = 0
| foreach mode=json_array grades 
    [eval sum = sum + <<ITEM>>]
| foreach mode=json_array grades
    [eval weight = json_append(weight, "", <<ITEM>> / sum)]

```


The search results look something like this:


| _time | grades | sum | weight |
| --- | --- | --- | --- |
| 2022-03-31 12:58:16 | [1,2,3,4] | 10 | [0.1,0.2,0.3,0.4] |



### 15. Iterate over multivalue fields and concatenate the values

The following example iterates over multivalue fields and concatenates the values, so that each letter is added to the index value in the search results.

CODE

Copy

|makeresults
|fields - _time
|eval word=split("ABCDE",""), nums=split("01234","")
|foreach word mode=multivalue [eval word_and_num=mvappend(word_and_num, &lt;&lt;ITEM&gt;&gt;.mvindex(nums, &lt;&lt;ITER&gt;&gt;))]


```spl

|makeresults
|fields - _time
|eval word=split("ABCDE",""), nums=split("01234","")
|foreach word mode=multivalue [eval word_and_num=mvappend(word_and_num, <<ITEM>>.mvindex(nums, <<ITER>>))]

```


The search results look like this:


| nums | word | word_and_num |
| --- | --- | --- |
| 0 | A | A0 |
| 1 | B | B1 |
| 2 | C | C2 |
| 3 | D | D3 |
| 4 | E | E4 |



## See also

Commands

eval , map

Related information

Evaluate and manipulate fields with multiple values

JSON functions
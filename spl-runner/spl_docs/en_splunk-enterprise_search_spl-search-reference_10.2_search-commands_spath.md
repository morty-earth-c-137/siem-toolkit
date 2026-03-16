
# spath


## Description

The spath command enables you to extract information from the structured data formats XML and JSON. The command stores this information in one or more fields. The command also highlights the syntax in the displayed events list.

You can also use the spath() function with the eval command. For more information, see the evaluation functions .


## Syntax

spath [input=&lt;field&gt;] [output=&lt;field&gt;] [path=&lt;datapath&gt; | &lt;datapath&gt;]


### Optional arguments

input

Syntax: input=&lt;field&gt;

Description: The field to read in and extract values from.

Default: _raw

output

Syntax: output=&lt;field&gt;

Description: If specified, the value extracted from the path is written to this field name.

Default: If you do not specify an output argument, the value for the path argument becomes the field name for the extracted value.

path

Syntax: path=&lt;datapath&gt; | &lt;datapath&gt;

Description: The location path to the value that you want to extract. The location path can be specified as path=&lt;datapath&gt; or as just datapath . If you do not specify the path= , the first unlabeled argument is used as the location path. A location path is composed of one or more location steps, separated by periods. An example of this is vendorProductSet.product.desc . A location step is composed of a field name and an optional index surrounded by curly brackets. The index can be an integer, to refer to the position of the data in an array (this differs between JSON and XML), or a string, to refer to an XML attribute. If the index refers to an XML attribute, specify the attribute name with an @ symbol.


## Usage

The spath command is a distributable streaming command. See Command types .


### Location path omitted

When used with no path argument, the spath command runs in "auto-extract" mode. By default, when the spath command is in "auto-extract" mode, it finds and extracts all the fields from the first 5,000 characters in the input field. These fields default to _raw if another input source is not specified. If a path is provided, the value of this path is extracted to a field named by the path or to a field specified by the output argument, if the output argument is provided.


### A location path contains one or more location steps

A location path contains one or more location steps, each of which has a context that is specified by the location steps that precede it. The context for the top-level location step is implicitly the top-level node of the entire XML or JSON document.


### The location step is composed of a field name and an optional array index

The location step is composed of a field name and an optional array index indicated by curly brackets around an integer or a string.

Array indices mean different things in XML and JSON. For example, JSON uses zero-based indexing. In JSON, product.desc{3} refers to the fourth element of the desc child of the product element. In XML, this same path refers to the third desc child of product .


### Using wildcards in place of an array index

The spath command lets you use wildcards to take the place of an array index in JSON. Now, you can use the location path entities.hashtags{}.text to get the text for all of the hashtags, as opposed to specifying entities.hashtags{0}.text , entities.hashtags{1}.text , and so on. The referenced path, here entities.hashtags , has to refer to an array for this to make sense. Otherwise, you get an error just like with regular array indices.

This also works with XML. For example, catalog.book and catalog.book{} are equivalent. Both get you all the books in the catalog.


### Overriding the spath extraction character limit

By default, the spath command extracts all the fields from the first 5,000 characters in the input field. If your events are longer than 5,000 characters and you want to extract all of the fields, you can override the extraction character limit for all searches that use the spath command. To change this character limit for all spath searches, change the extraction_cutoff setting in the limits.conf file to a larger value.

If you change the default extraction_cutoff setting, you must also change the setting to the same value in all limits.conf files across all search head and indexer tiers.

Splunk Cloud Platform

To change the limits.conf extraction_cutoff setting, use one of the following methods:

- The Configure limits page in Splunk Web. For more information, see Configure limits using Splunk Web in the Splunk Cloud Platform Admin Manual .

- The Admin Config Service (ACS) command line interface (CLI). For more information, see Administer Splunk Cloud Platform using the ACS CLI in the Splunk Cloud Platform Admin Config Service Manual .

- The Admin Config Service (ACS) API. For more information, see Manage limits.conf configurations in Splunk Cloud Platform in the Splunk Cloud Platform Admin Config Service Manual .

Splunk Enterprise

To change the extraction_cutoff setting, follow these steps.

Prerequisites

- Only users with file system access, such as system administrators, can edit configuration files.

- Review the steps in How to edit a configuration file in the Splunk Enterprise Admin Manual .


> **CAUTION: Never change or copy the configuration files in the default directory. The files in the default directory must remain intact and in their original location. Make changes to the files in the local directory.**


Steps

- Open or create a local limits.conf file at $SPLUNK_HOME/etc/system/local if you are using \*nix, or %SPLUNK_HOME%\etc\system\local if you are using Windows.

- In the [spath] stanza, add the line extraction_cutoff = &lt;value&gt; set to the value you want as the extraction cutoff.

- If your deployment includes search head or indexer clusters, repeat the previous steps on every indexer peer node or search head cluster member. See Use the deployer to distribute apps and configuration updates in Splunk Enterprise Distributed Search and Update common peer configurations and apps in Splunk Enterprise Managing Indexers and Clusters of Indexers for information about changing the limits.conf setting across search head and indexer clusters.


### JSON data used with the spath command must be well-formed

To use the spath command to extract JSON data, ensure that the JSON data is well-formed. For example, string literals other than the literal strings true , false and null must be enclosed in double quotation marks ( " ). For a full reference on the JSON data format, see the JSON Data Interchange Syntax standard at https://www.ecma-international.org/publications-and-standards/standards/ecma-404/ .


### Alternatives to the spath command

If you are using autokv or index-time field extractions, the path extractions are performed for you at index time.

You do not need to explicitly use the spath command to provide a path.

If you are using indexed_extractions=JSON or KV_MODE=JSON in the props.conf file, then you don't need to use the spath command.


## Basic examples


### 1. Specify an output field and path

This example shows how to specify an output field and path.

CODE

Copy

... | spath output=myfield path=vendorProductSet.product.desc


```spl

... | spath output=myfield path=vendorProductSet.product.desc

```



### 2. Specify just the &lt;datapath&gt;

For the path argument, you can specify the location path with or without the path= . In this example the &lt;datapath&gt; is server.name .

CODE

Copy

... | spath output=myfield server.name


```spl

... | spath output=myfield server.name

```



### 3. Specify an output field and path based on an array

For example, you have this array.

JSON

Copy

{ 
   "vendorProductSet" : [1,2]
}


```spl

{ 
   "vendorProductSet" : [1,2]
}

```


To specify the output field and path, use this syntax.

CODE

Copy

... | spath output=myfield path=vendorProductSet{1}


```spl

... | spath output=myfield path=vendorProductSet{1}

```



### 4. Specify an output field and a path that uses a nested array

For example, you have this nested array.

JSON

Copy

{
   "vendorProductSet" : {
      "product" : [
         {"desc" : 1},
         {"locDesc" : 2}
      ]
   }
}


```spl

{
   "vendorProductSet" : {
      "product" : [
         {"desc" : 1},
         {"locDesc" : 2}
      ]
   }
}

```


To specify the output and path from this nested array, use this syntax.

CODE

Copy

... | spath output=myfield path=vendorProductSet.product{}.locDesc


```spl

... | spath output=myfield path=vendorProductSet.product{}.locDesc

```



### 5. Specify the output field and a path for an XML attribute

Use the @ symbol to specify an XML attribute. Consider the following XML list of books and authors.

XML

Copy

&lt;?xml version="1.0"&gt;
&lt;purchases&gt;
   &lt;book&gt;
         &lt;author&gt;Martin, George R.R.&lt;/author&gt;
         &lt;title yearPublished=1996&gt;A Game of Thrones&lt;/title&gt;
         &lt;title yearPublished=1998&gt;A Clash of Kings&lt;/title&gt;
  &lt;/book&gt;
   &lt;book&gt;
         &lt;author&gt;Clarke, Susanna&lt;/author&gt;
         &lt;title yearPublished=2004&gt;Jonathan Strange and Mr. Norrell&lt;/title&gt;
   &lt;/book&gt;
   &lt;book&gt;
         &lt;author&gt;Kay, Guy Gavriel&lt;/author&gt;
         &lt;title yearPublished=1990&gt;Tigana&lt;/title&gt;
   &lt;/book&gt;
   &lt;book&gt;
         &lt;author&gt;Bujold, Lois McMasters&lt;/author&gt;
         &lt;title yearPublished=1986&gt;The Warrior's Apprentice&lt;/title&gt;
   &lt;/book&gt;
&lt;/purchases&gt;


```spl

<?xml version="1.0">
<purchases>
   <book>
         <author>Martin, George R.R.</author>
         <title yearPublished=1996>A Game of Thrones</title>
         <title yearPublished=1998>A Clash of Kings</title>
  </book>
   <book>
         <author>Clarke, Susanna</author>
         <title yearPublished=2004>Jonathan Strange and Mr. Norrell</title>
   </book>
   <book>
         <author>Kay, Guy Gavriel</author>
         <title yearPublished=1990>Tigana</title>
   </book>
   <book>
         <author>Bujold, Lois McMasters</author>
         <title yearPublished=1986>The Warrior's Apprentice</title>
   </book>
</purchases>

```


Use this search to return the path for the book and the year it was published.

CODE

Copy

... | spath output=dates path=purchases.book.title{@yearPublished} | table dates


```spl

... | spath output=dates path=purchases.book.title{@yearPublished} | table dates

```


In this example, the output is a single multivalue result that lists all of the years the books were published.


## Extended examples


### 1: GitHub

As an administrator of a number of large Git repositories, you want to:

- See who has committed the most changes and to which repository

- Produce a list of the commits submitted for each user

Suppose you are Indexing JSON data using the GitHub PushEvent webhook. You can use the spath command to extract fields called repository, commit_author, and commit_id:

CODE

Copy

... | spath output=repository path=repository.url


```spl

... | spath output=repository path=repository.url

```


CODE

Copy

... | spath output=commit_author path=commits{}.author.name


```spl

... | spath output=commit_author path=commits{}.author.name

```


CODE

Copy

... | spath output=commit_id path=commits{}.id


```spl

... | spath output=commit_id path=commits{}.id

```


To see who has committed the most changes to a repository, run the search.

CODE

Copy

... | top commit_author by repository


```spl

... | top commit_author by repository

```


To see the list of commits by each user, run this search.

CODE

Copy

... | stats values(commit_id) by commit_author


```spl

... | stats values(commit_id) by commit_author

```



### 2: Extract a subset of a XML attribute

This example shows how to extract values from XML attributes and elements.

CODE

Copy

&lt;vendorProductSet vendorID="2"&gt;
            &lt;product productID="17" units="mm" &gt;
                &lt;prodName nameGroup="custom"&gt;
                    &lt;locName locale="all"&gt;APLI 01209&lt;/locName&gt;
                &lt;/prodName&gt;
                &lt;desc descGroup="custom"&gt;
                    &lt;locDesc locale="es"&gt;Precios&lt;/locDesc&gt;
                    &lt;locDesc locale="fr"&gt;Prix&lt;/locDesc&gt;
                    &lt;locDesc locale="de"&gt;Preise&lt;/locDesc&gt;
                    &lt;locDesc locale="ca"&gt;Preus&lt;/locDesc&gt;
                    &lt;locDesc locale="pt"&gt;Preços&lt;/locDesc&gt; 
                &lt;/desc&gt;
           &lt;/product&gt;


```spl

<vendorProductSet vendorID="2">
            <product productID="17" units="mm" >
                <prodName nameGroup="custom">
                    <locName locale="all">APLI 01209</locName>
                </prodName>
                <desc descGroup="custom">
                    <locDesc locale="es">Precios</locDesc>
                    <locDesc locale="fr">Prix</locDesc>
                    <locDesc locale="de">Preise</locDesc>
                    <locDesc locale="ca">Preus</locDesc>
                    <locDesc locale="pt">Preços</locDesc> 
                </desc>
           </product>

```


To extract the values of the locDesc elements (Precios, Prix, Preise, etc.), use:

CODE

Copy

... | spath output=locDesc path=vendorProductSet.product.desc.locDesc


```spl

... | spath output=locDesc path=vendorProductSet.product.desc.locDesc

```


To extract the value of the locale attribute (es, fr, de, etc.), use:

CODE

Copy

... | spath output=locDesc.locale  path=vendorProductSet.product.desc.locDesc{@locale}


```spl

... | spath output=locDesc.locale  path=vendorProductSet.product.desc.locDesc{@locale}

```


To extract the attribute of the 4th locDesc (ca), use:

CODE

Copy

... | spath path=vendorProductSet.product.desc.locDesc{4}{@locale}


```spl

... | spath path=vendorProductSet.product.desc.locDesc{4}{@locale}

```



### 3: Extract and expand JSON events with multi-valued fields

The mvexpand command only works on one multivalued field. This example walks through how to expand a JSON event that has more than one multivalued field into individual events for each field value. For example, given this event with sourcetype=json :

JSON

Copy

{
   "widget": {
       "text": [ 
        {
           "data": "Click here",
           "size": 36
        },
       {
          "data": "Learn more",
          "size": 37
       },
       {
          "data": "Help",
          "size": 38
       },
       ]
   }
}


```spl

{
   "widget": {
       "text": [ 
        {
           "data": "Click here",
           "size": 36
        },
       {
          "data": "Learn more",
          "size": 37
       },
       {
          "data": "Help",
          "size": 38
       },
       ]
   }
}

```


First, start with a search to extract the fields from the JSON. Because no path argument is specified, the spath command runs in "auto-extract" mode and extracts all of the fields from the first 5,000 characters in the input field. The fields are then renamed and placed in a table.

CODE

Copy

sourcetype=json | spath | rename widget.text.size AS size, widget.text.data AS data | table _time,size,data


```spl

sourcetype=json | spath | rename widget.text.size AS size, widget.text.data AS data | table _time,size,data

```


CODE

Copy

_time            size    data
--------------------------- ---- -----------
2018-10-18 14:45:46.000 BST   36 Click here
                              37 Learn more
                              38 Help


```spl

_time            size    data
--------------------------- ---- -----------
2018-10-18 14:45:46.000 BST   36 Click here
                              37 Learn more
                              38 Help

```


Then, use the eval function, mvzip(), to create a new multivalued field named x, with the values of the size and data:

CODE

Copy

sourcetype=json | spath | rename widget.text.size AS size, widget.text.data AS data | eval x=mvzip(data,size) | table _time,data,size,x


```spl

sourcetype=json | spath | rename widget.text.size AS size, widget.text.data AS data | eval x=mvzip(data,size) | table _time,data,size,x

```


CODE

Copy

_time                data    size        x
--------------------------- ----------- ----- --------------
2018-10-18 14:45:46.000 BST Click here   36   Click here,36
                            Learn more   37   Learn more,37
                            Help         38   Help,38


```spl

_time                data    size        x
--------------------------- ----------- ----- --------------
2018-10-18 14:45:46.000 BST Click here   36   Click here,36
                            Learn more   37   Learn more,37
                            Help         38   Help,38

```


Now, use the mvexpand command to create individual events based on x and the eval function mvindex() to redefine the values for data and size.

CODE

Copy

sourcetype=json | spath | rename widget.text.size AS size, widget.text.data AS data | eval x=mvzip(data,size)| mvexpand x |  eval x = split(x,",") | eval data=mvindex(x,0) | eval size=mvindex(x,1) | table _time,data, size


```spl

sourcetype=json | spath | rename widget.text.size AS size, widget.text.data AS data | eval x=mvzip(data,size)| mvexpand x |  eval x = split(x,",") | eval data=mvindex(x,0) | eval size=mvindex(x,1) | table _time,data, size

```


CODE

Copy

_time                data   size
--------------------------- ---------- ----
2018-10-18 14:45:46.000 BST Click here  36
2018-10-18 14:45:46.000 BST Learn more  37
2018-10-18 14:45:46.000 BST Help        38


```spl

_time                data   size
--------------------------- ---------- ----
2018-10-18 14:45:46.000 BST Click here  36
2018-10-18 14:45:46.000 BST Learn more  37
2018-10-18 14:45:46.000 BST Help        38

```




(Thanks to Splunk user G. Zaimi for this example.)




## See also

extract , kvform , multikv , regex , rex , xmlkv , xpath
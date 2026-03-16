
# extract


## Description

Extracts field-value pairs from the search results. The extract command works only on the _raw field. If you want to extract from another field, you must perform some field renaming before you run the extract command.


## Syntax

The required syntax is in bold .

extract

[&lt;extract-options&gt;... ]

[&lt;extractor-name&gt;...]


### Required arguments

None.


### Optional arguments

&lt;extract-options&gt;

Syntax: auto=f | clean_keys=&lt;bool&gt; | kvdelim=&lt;string&gt; | limit=&lt;int&gt; | maxchars=&lt;int&gt; | mv_add=&lt;bool&gt; | pairdelim=&lt;string&gt; | reload=&lt;bool&gt; | segment=&lt;bool&gt;

Description: Options for defining the extraction. See the Extract_options section in this topic.

&lt;extractor-name&gt;

Syntax: &lt;string&gt;

Description: A stanza in the transforms.conf file. This is used when the props.conf file does not explicitly cause an extraction for this source, sourcetype, or host.


### Extract options

auto

Syntax: auto=f

Description: Specifies whether automatic key-value field extraction is turned off. When you include auto=f in a search with the extract command, you are explicitly telling Splunk software not to perform automatic key-value field extraction by default on the _raw field for that specific search. Using this option gives you more granular control over how fields are extracted.

Default: None.

clean_keys

Syntax: clean_keys=&lt;bool&gt;

Description: Specifies whether to clean keys. Overrides CLEAN_KEYS in the transforms.conf file.

Default: The value specified in the CLEAN_KEYS in the transforms.conf file.

kvdelim

Syntax: kvdelim=&lt;string&gt;

Description: A list of character delimiters that separate the key from the value. If the delimiter appears in the value, that value is not extracted. For example, if the delimiter is a colon ( : ) and a key-value pair is Referer: https://buttercupgames.com , the key-value pair is not extracted.

limit

Syntax: limit=&lt;int&gt;

Description: Specifies how many automatic key-value pairs to extract.

Default: 50

maxchars

Syntax: maxchars=&lt;int&gt;

Description: Specifies how many characters to look into the event.

Default: 10240

mv_add

Syntax: mv_add=&lt;bool&gt;

Description: Specifies whether to create multivalued fields. Overrides the value for the MV_ADD parameter in the transforms.conf file.

Default: false

pairdelim

Syntax: pairdelim=&lt;string&gt;

Description: A list of character delimiters that separate the key-value pairs from each other.

reload

Syntax: reload=&lt;bool&gt;

Description: Specifies whether to force reloading of the props.conf and transforms.conf files.

Default: false

segment

Syntax: segment=&lt;bool&gt;

Description: Specifies whether to note the locations of the key-value pairs with the results.

Default: false


## Usage

The extract command is a distributable streaming command . See Command types .


### Alias

The alias for the extract command is kv .


## Examples


### 1. Specify the delimiters to use for the field and value extractions

Extract field-value pairs that are delimited by the pipe ( | ) or semicolon ( ; ) characters. Extract values of the fields that are delimited by the equal ( = ) or colon ( : ) characters. The delimiters are individual characters. In this example the "=" or ":" character is used to delimit the key value. Similarly, a "|" or ";" is used to delimit the field-value pair itself.

CODE

Copy

... | extract pairdelim="|;", kvdelim="=:"


```spl

... | extract pairdelim="|;", kvdelim="=:"

```



### 2. Extract field-value pairs and reload the field extraction settings

Extract field-value pairs and reload field extraction settings from disk.

CODE

Copy

... | extract reload=true


```spl

... | extract reload=true

```



### 3. Rename a field to _raw to extract from that field

Rename the _raw field to a temporary name. Rename the field you want to extract from, to _raw . In this example the field name is uri_query .

CODE

Copy

... | rename _raw AS temp uri_query AS _raw | extract pairdelim="?&" kvdelim="=" | rename _raw AS uri_query temp AS _raw


```spl

... | rename _raw AS temp uri_query AS _raw | extract pairdelim="?&" kvdelim="=" | rename _raw AS uri_query temp AS _raw

```



### 4. Extract field-value pairs from a stanza in the transforms.conf file

Extract field-value pairs that are defined in the my-access-extractions stanza in the transforms.conf file.

CODE

Copy

... | extract my-access-extractions


```spl

... | extract my-access-extractions

```


The transforms.conf stanza for this example looks something like this.

CODE

Copy

[my-access-extractions]
REGEX=\[(?!(?:headerName|headerValue))([^\s\=]+)\=([^\]]+)\]
FORMAT=$1::$2


```spl

[my-access-extractions]
REGEX=\[(?!(?:headerName|headerValue))([^\s\=]+)\=([^\]]+)\]
FORMAT=$1::$2

```



## See also

kvform , multikv , rex , spath , xmlkv , xpath
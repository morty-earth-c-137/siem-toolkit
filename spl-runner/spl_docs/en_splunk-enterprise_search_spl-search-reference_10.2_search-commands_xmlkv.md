
# xmlkv


## Description

The xmlkv command automatically extracts key-value pairs from XML-formatted data.

For JSON-formatted data, use the spath command.


## Syntax

The required syntax is in bold .

xmlkv

[&lt;field&gt;]

maxinputs=&lt;int&gt;


### Required arguments

None.


### Optional arguments

field

Syntax: &lt;field&gt;

Description: The field from which to extract the key and value pairs.

Default: The _raw field.

maxinputs

Syntax: maxinputs=&lt;int&gt;

Description: Sets the maximum number of events or search results that can be passed as inputs into the xmlkv command per invocation of the command. The xmlkv command is invoked repeatedly in increments according to the maxinputs argument until the search is complete and all of the results have been displayed. Do not change the value of maxinputs unless you know what you are doing.

Default: 50000


## Usage

The xmlkv command is a distributable streaming command. See Command types .


### Keys and values in XML elements

From the following XML, name is the key and Settlers of Catan is the value in the first element.

CODE

Copy

&lt;game&gt;
   &lt;name&gt;Settlers of Catan&lt;/name&gt;
   &lt;category&gt;competitive&lt;/category&gt;
&lt;/game&gt;
&lt;game&gt;
   &lt;name&gt;Ticket to Ride&lt;/name&gt;
   &lt;category&gt;competitive&lt;/category&gt;
&lt;/game&gt;


```spl

<game>
   <name>Settlers of Catan</name>
   <category>competitive</category>
</game>
<game>
   <name>Ticket to Ride</name>
   <category>competitive</category>
</game>

```



## Examples


### 1. Automatically extract key-value pairs

Extract key-value pairs from XML tags in the _raw field. Processes a maximum of 50000 events.

CODE

Copy

... | xmlkv


```spl

... | xmlkv

```



### 2. Extract key-value pairs in a specific number of increments

Extract the key-value pairs from events or search results in increments of 10,000 per invocation of the xmlkv command until the search has finished and all of the results are displayed.

CODE

Copy

... | xmlkv maxinputs=10000


```spl

... | xmlkv maxinputs=10000

```



## See also

Commands

extract

kvform

multikv

rex

spath

xpath
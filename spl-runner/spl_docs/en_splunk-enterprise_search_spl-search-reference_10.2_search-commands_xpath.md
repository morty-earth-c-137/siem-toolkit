
# xpath


## Description

Extracts the xpath value from field and sets the outfield attribute.


> **Note: Due to limitations with XML extraction, the xpath command returns empty results when input XML strings have prologue headers, such as xml version or DOCTYPE. As a result, use the spath command instead of the xpath command when extracting XML content.**



### Syntax

xpath [outfield=&lt;field&gt;] &lt;xpath-string&gt; [field=&lt;field&gt;] [default=&lt;string&gt;]


### Required arguments

xpath-string

Syntax: &lt;string&gt;

Description: Specifies the XPath reference.


### Optional arguments

field

Syntax: field=&lt;field&gt;

Description: The field to find and extract the referenced xpath value from.

Default: _raw

outfield

Syntax: outfield=&lt;field&gt;

Description: The field to write, or output, the xpath value to.

Default: xpath

default

Syntax: default=&lt;string&gt;

Description: If the attribute referenced in xpath doesn't exist, this specifies what to write to the outfield . If this isn't defined, there is no default value.


## Usage

The xpath command is a distributable streaming command. See Command types .

The xpath command supports the syntax described in the Python Standard Library 19.7.2.2. Supported XPath syntax .


## Examples


### 1. Extract values from a single element in _raw XML events

You want to extract values from a single element in _raw XML events and write those values to a specific field.

The _raw XML events look like this:

CODE

Copy

&lt;foo&gt;
      &lt;bar nickname="spock"&gt;
      &lt;/bar&gt;
   &lt;/foo&gt;
   &lt;foo&gt;
      &lt;bar nickname="scotty"&gt;
      &lt;/bar&gt;
   &lt;/foo&gt;
   &lt;foo&gt;
      &lt;bar nickname="bones"&gt;
      &lt;/bar&gt;
   &lt;/foo&gt;


```spl

<foo>
      <bar nickname="spock">
      </bar>
   </foo>
   <foo>
      <bar nickname="scotty">
      </bar>
   </foo>
   <foo>
      <bar nickname="bones">
      </bar>
   </foo>

```


Extract the nickname values from _raw XML events. Output those values to the name field.

CODE

Copy

sourcetype="xml" | xpath outfield=name "//bar/@nickname"


```spl

sourcetype="xml" | xpath outfield=name "//bar/@nickname"

```



### 2. Extract multiple values from _raw XML events

Extract multiple values from _raw XML events

The _raw XML events look like this:

CODE

Copy

&lt;DataSet xmlns=""&gt;
        &lt;identity_id&gt;3017669&lt;/identity_id&gt;
        &lt;instrument_id&gt;912383KM1&lt;/instrument_id&gt;
        &lt;transaction_code&gt;SEL&lt;/transaction_code&gt;
        &lt;sname&gt;BARC&lt;/sname&gt;
        &lt;currency_code&gt;USA&lt;/currency_code&gt;
   &lt;/DataSet&gt; 

   &lt;DataSet xmlns=""&gt;
        &lt;identity_id&gt;1037669&lt;/identity_id&gt;
        &lt;instrument_id&gt;219383KM1&lt;/instrument_id&gt;
        &lt;transaction_code&gt;SEL&lt;/transaction_code&gt;
        &lt;sname&gt;TARC&lt;/sname&gt;
        &lt;currency_code&gt;USA&lt;/currency_code&gt;
   &lt;/DataSet&gt;


```spl

<DataSet xmlns="">
        <identity_id>3017669</identity_id>
        <instrument_id>912383KM1</instrument_id>
        <transaction_code>SEL</transaction_code>
        <sname>BARC</sname>
        <currency_code>USA</currency_code>
   </DataSet> 

   <DataSet xmlns="">
        <identity_id>1037669</identity_id>
        <instrument_id>219383KM1</instrument_id>
        <transaction_code>SEL</transaction_code>
        <sname>TARC</sname>
        <currency_code>USA</currency_code>
   </DataSet>

```


Extract the values from the identity_id element from the _raw XML events:

CODE

Copy

... | xpath outfield=identity_id "//DataSet/identity_id"


```spl

... | xpath outfield=identity_id "//DataSet/identity_id"

```


This search returns two results: identity_id=3017669 and identity_id=1037669 .



To extract a combination of two elements,


```spl

sname

```


with a specific value and


```spl

instrument_id

```


, use this search:



CODE

Copy

... | xpath outfield=instrument_id "//DataSet[sname='BARC']/instrument_id"


```spl

... | xpath outfield=instrument_id "//DataSet[sname='BARC']/instrument_id"

```


Because you specify sname='BARC' , this search returns one result: instrument_id=912383KM1 .


### 3. Testing extractions from XML events

You can use the makeresults command to test xpath extractions.

You must add field=xml to the end of your search. For example:

CODE

Copy

| makeresults
| eval xml="&lt;DataSet xmlns=\"\"&gt;
        &lt;identity_id&gt;1037669&lt;/identity_id&gt;
        &lt;instrument_id&gt;219383KM1&lt;/instrument_id&gt;
        &lt;transaction_code&gt;SEL&lt;/transaction_code&gt;
        &lt;sname&gt;TARC&lt;/sname&gt;
        &lt;currency_code&gt;USA&lt;/currency_code&gt;
   &lt;/DataSet&gt;"
| xpath outfield=identity_id "//DataSet/identity_id" field=xml


```spl

| makeresults
| eval xml="<DataSet xmlns=\"\">
        <identity_id>1037669</identity_id>
        <instrument_id>219383KM1</instrument_id>
        <transaction_code>SEL</transaction_code>
        <sname>TARC</sname>
        <currency_code>USA</currency_code>
   </DataSet>"
| xpath outfield=identity_id "//DataSet/identity_id" field=xml

```



## See also

extract , kvform , multikv , rex , spath , xmlkv
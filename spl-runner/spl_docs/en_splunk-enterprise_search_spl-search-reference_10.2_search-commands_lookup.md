
# lookup


## Description

Use the lookup command to invoke field value lookups.

For information about the types of lookups you can define, see About lookups in the Knowledge Manager Manual .

The lookup command supports IPv4 and IPv6 addresses and subnets that use CIDR notation.


## Syntax

The required syntax is in bold .

lookup

[local=&lt;bool&gt;]

[update=&lt;bool&gt;]

&lt;lookup-table-name&gt;

( &lt;lookup-field&gt; [AS &lt;event-field&gt;] )...

[ OUTPUT | OUTPUTNEW (&lt;lookup-destfield&gt; [AS &lt;event-destfield&gt;] )... ]


> Note: The lookup command can accept multiple lookup and event fields and destfields . For example:

CODE

Copy

...| lookup &lt;lookup-table-name&gt; &lt;lookup-field1&gt; AS &lt;event-field1&gt;, &lt;lookup-field2&gt; AS &lt;event-field2&gt; OUTPUTNEW &lt;lookup-destfield1&gt; AS &lt;event-destfield1&gt;, &lt;lookup-destfield2&gt; AS &lt;event-destfield2&gt;


```spl

...| lookup <lookup-table-name> <lookup-field1> AS <event-field1>, <lookup-field2> AS <event-field2> OUTPUTNEW <lookup-destfield1> AS <event-destfield1>, <lookup-destfield2> AS <event-destfield2>

```



### Required arguments

&lt;lookup-table-name&gt;

Syntax: &lt;string&gt;

Description: Can be either the name of a CSV file that you want to use as the lookup, or the name of a stanza in the transforms.conf file that specifies the location of the lookup table file.


### Optional arguments

local

Syntax: local=&lt;bool&gt;

Description: If local=true , forces the lookup to run on the search head and not on any remote peers.

Default: false

update

Syntax: update=&lt;bool&gt;

Description: If the lookup table is modified on disk while the search is running, real-time searches do not automatically reflect the update. To do this, specify update=true . This does not apply to searches that are not real-time searches. This implies that local=true.

Default: false

&lt;lookup-field&gt;

Syntax: &lt;string&gt;

Description: Refers to a field in the lookup table to match against the events. You can specify multiple &lt;lookup-field&gt; values.

&lt;event-field&gt;

Syntax: &lt;string&gt;

Description: Refers to a field in the events from which to acquire the value to match in the lookup table. You can specify multiple &lt;event-field&gt; values.

Default: The value of the &lt;lookup-field&gt;.

&lt;lookup-destfield&gt;

Syntax: &lt;string&gt;

Description: Refers to a field in the lookup table to be copied into the events. You can specify multiple &lt;lookup-destfield&gt; values.

&lt;event-destfield&gt;

Syntax: &lt;string&gt;

Description: A field in the events. You can specify multiple &lt;event-destfield&gt; values.

Default: The value of the &lt;lookup-destfield&gt; argument.


## Usage

The lookup command is a distributable streaming command when local=false , which is the default setting. See Command types .

When using the lookup command, if an OUTPUT or OUTPUTNEW clause is not specified, all of the fields in the lookup table that are not the match fields are used as output fields. If the OUTPUT clause is specified, the output lookup fields overwrite existing fields. If the OUTPUTNEW clause is specified, the lookup is not performed for events in which the output fields already exist.


### Avoid lookup reference cycles

When you set up the OUTPUT or OUTPUTNEW clause for your lookup, avoid accidentally creating lookup reference cycles, where you intentionally or accidentally reuse the same field names among the match fields and the output fields of a lookup search.

For example, if you run a lookup search where type is both the match field and the output field, you are creating a lookup reference cycle. You can accidentally create a lookup reference cycle when you fail to specify an OUTPUT or OUTPUTNEW clause for lookup .

For more information about lookup reference cycles see Define an automatic lookup in Splunk Web in the Knowledge Manager Manual .


### Optimizing your lookup search

If you are using the lookup command in the same pipeline as a transforming command , and it is possible to retain the field you will lookup on after the transforming command, do the lookup after the transforming command. For example, run:

CODE

Copy

sourcetype=access_\* | stats count by status | lookup status_desc status OUTPUT description


```spl

sourcetype=access_* | stats count by status | lookup status_desc status OUTPUT description

```


and not:

CODE

Copy

sourcetype=access_\* | lookup status_desc status OUTPUT description | stats count by description


```spl

sourcetype=access_* | lookup status_desc status OUTPUT description | stats count by description

```


The lookup in the first search is faster because it only needs to match the results of the stats command and not all the Web access events.


## Run lookup in federated searches

If you are running federated searches over standard mode Splunk platform federated providers , and you want to use the lookup command to enrich the results of a federated search, see Run federated searches over lookups in Federated Search .

For an overview of federated search for Splunk, see About Federated Search for Splunk in Federated Search .


### Configure a lookup to run on the local federated search head

In a standard mode federated search, you can force a lookup command to be processed locally on the federated search head by applying local=true to it. If you do not set local=true , Splunk software will optimize processing of the lookup command on the federated search head and the remote search head depending on the specific conditions of the search.

If the lookup definition and lookup tables expected by the lookup are not present on the search heads on which it is processed, Splunk Web displays an error message when the search runs. See Manage knowledge objects for standard mode federated providers in Federated Search .


## Basic example


### 1. Lookup users and return the corresponding group the user belongs to

Suppose you have a lookup table specified in a stanza named usertogroup in the transforms.conf file. This lookup table contains (at least) two fields, user and group . Your events contain a field called local_user . For each event, the following search checks to see if the value in the field local_user has a corresponding value in the user field in the lookup table. For any entries that match, the value of the group field in the lookup table is written to the field user_group in the event.

CODE

Copy

... | lookup usertogroup user as local_user OUTPUT group as user_group


```spl

... | lookup usertogroup user as local_user OUTPUT group as user_group

```



## Extended example


### 1. Lookup price and vendor information and return the count for each product sold by a vendor


| This example uses the tutorialdata.zip file from the Search Tutorial. You can download this file and add it to your Splunk deployment. Seeupload the tutorial data. Additionally, this example uses theprices.csvand thevendors.csvfiles. To follow along with this example in your Splunk deployment, download these CSV files and complete the steps in theUse field lookupssection of the Search Tutorial for both theprices.csvand thevendors.csvfiles. When you create the lookup definition for thevendors.csvfile, name the lookupvendors_lookup. You can skip the step in the tutorial that makes the lookups automatic. |
| --- |


This example calculates the count of each product sold by each vendor.

The prices.csv file contains the product names, price, and code. For example:


| productId | product_name | price | sale_price | Code |
| --- | --- | --- | --- | --- |
| DB-SG-G01 | Mediocre Kingdoms | 24.99 | 19.99 | A |
| DC-SG-G02 | Dream Crusher | 39.99 | 24.99 | B |
| FS-SG-G03 | Final Sequel | 24.99 | 16.99 | C |
| WC-SH-G04 | World of Cheese | 24.99 | 19.99 | D |


The vendors.csv file contains vendor information, such as vendor name, city, and ID. For example:


| Vendor | VendorCity | VendorID | VendorLatitude | VendorLongitude | Vendor StateProvince | Vendor Country | Weight |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Anchorage Gaming | Anchorage | 1001 | 61.17440033 | -149.9960022 | Alaska | United States | 3 |
| Games of Salt Lake | Salt Lake City | 1002 | 40.78839874 | -111.9779968 | Utah | United States | 3 |
| New Jack Games | New York | 1003 | 40.63980103 | -73.77890015 | New York | United States | 4 |
| Seals Gaming | San Francisco | 1004 | 37.61899948 | -122.375 | California | United States | 5 |


The search will query the vendor_sales.log file, which is part of the tutorialdata.zip file. The vendor_sales.log file contains the VendorID, Code, and AcctID fields. For example:


| Entries in the vendor_sales.log file |
| --- |
| [13/Mar/2018:18:24:02] VendorID=5036 Code=B AcctID=6024298300471575 |
| [13/Mar/2018:18:23:46] VendorID=7026 Code=C AcctID=8702194102896748 |
| [13/Mar/2018:18:23:31] VendorID=1043 Code=B AcctID=2063718909897951 |
| [13/Mar/2018:18:22:59] VendorID=1243 Code=F AcctID=8768831614147676 |


The following search calculates the count of each product sold by each vendor and uses the time range All time .

CODE

Copy

sourcetype=vendor_\* | stats count by Code VendorID | lookup prices_lookup Code OUTPUTNEW product_name


```spl

sourcetype=vendor_* | stats count by Code VendorID | lookup prices_lookup Code OUTPUTNEW product_name

```


- The stats command calculates the count by Code and VendorID.

- The lookup command uses the prices_lookup to match the Code field in each event and return the product names.

The search results are displayed on displayed on the Statistics tab.



You can extend the search to display more information about the vendor by using the vendors_lookup.



Use the table command to return only the fields that you need. In this example you want the product_name , VendorID , and count fields. Use the vendors_lookup file to output all the fields in the vendors.csv file that match the VendorID in each event.

CODE

Copy

sourcetype=vendor_\* | stats  count by Code VendorID | lookup prices_lookup Code OUTPUTNEW product_name | table product_name VendorID count | lookup vendors_lookup VendorID


```spl

sourcetype=vendor_* | stats  count by Code VendorID | lookup prices_lookup Code OUTPUTNEW product_name | table product_name VendorID count | lookup vendors_lookup VendorID

```


The revised search results are displayed on the Statistics tab.



To expand the search to display the results on a map, see the geostats command.


### 2. IPv6 CIDR match in Splunk Web

In this example, CSV lookups are used to determine whether a specified IPv6 address is in a CIDR subnet. You can follow along with the example by performing these steps in Splunk Web. See Define a CSV lookup in Splunk Web .

Prerequisites

- Your role must have the upload_lookup_files capability to upload lookup table files in Splunk Web. See Define roles with capabilities in Splunk Enterprise "Securing the Splunk Platform".

- A CSV lookup table file called ipv6test.csv that contains the following text. ip,expected 2001:0db8:ffff:ffff:ffff:ffff:ffff:ff00/120,true The ip field in the lookup table contains the subnet value, not the IP address.

Steps

You have to define a CSV lookup before you can match an IP address to a subnet.

- Select Settings &gt; Lookups to go to the Lookups manager page.

- Click Add new next to Lookup table files .

- Select a Destination app from the drop-down list.

- Click Choose File to look for the ipv6test.csv file to upload.

- Enter ipv6test.csv as the destination filename. This is the name the lookup table file will have on the Splunk server.

- Click Save .

- In the Lookup table list, click Permissions in the Sharing column of the ipv6test lookup you want to share.

- In the Permissions dialog box, under Object should appear in , select All apps to share globally. If you want the lookup to be specific to this app only, select This app only .

- Click Save .

- Select Settings &gt; Lookups .

- Click Add new next to Lookup definitions .

- Select a Destination app from the drop-down list.

- Give your lookup definition a unique Name , like ipv6test.

- Select File-based as the lookup Type .

- Select ipv6test.csv as the Lookup file from the drop-down list.

- Select the Advanced options check box.

- Enter a Match type of CIDR(ip) .

- Click Save .

- In the Lookup definitions list, click Permissions in the Sharing column of the ipv6test lookup definition you want to share.

- In the Permissions dialog box, under Object should appear in , select All apps to share globally. If you want the lookup to be specific to this app only, select This app only . Note: Permissions for lookup table files must be at the same level or higher than those of the lookup definitions that use those files.

- Click Save .

In the Search app, run the following search to match the IP address to the subnet.

CODE

Copy

| makeresults 
| eval ip="2001:0db8:ffff:ffff:ffff:ffff:ffff:ff99" 
| lookup ipv6test ip OUTPUT expected


```spl

| makeresults 
| eval ip="2001:0db8:ffff:ffff:ffff:ffff:ffff:ff99" 
| lookup ipv6test ip OUTPUT expected

```


The IP address is in the subnet, so the search displays


```spl

true

```


in the


```spl

expected

```


field. The search results look something like this.


| time | expected | ip |
| --- | --- | --- |
| 2020-11-19 16:43:31 | true | 2001:0db8:ffff:ffff:ffff:ffff:ffff:ff99 |



## See also

Commands



appendcols

inputlookup

outputlookup

iplocation

search

Functions

cidrmatch

Related information



About lookups in the Knowledge Manager Manual
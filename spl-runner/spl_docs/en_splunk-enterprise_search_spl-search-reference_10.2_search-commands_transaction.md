
# transaction


## Description

The transaction command finds transactions based on events that meet various constraints. Transactions are made up of the raw text (the _raw field) of each member, the time and date fields of the earliest member, as well as the union of all other fields of each member.

Additionally, the transaction command adds two fields to the raw events, duration and eventcount . The values in the duration field show the difference between the timestamps for the first and last events in the transaction. The values in the eventcount field show the number of events in the transaction.

See About transactions in the Search Manual .


## Syntax

The required syntax is in bold .

transaction

[&lt;field-list&gt;]

[name=&lt;transaction-name&gt;]

[&lt;txn_definition-options&gt;...]

[&lt;memcontrol-options&gt;...]

[&lt;rendering-options&gt;...]


### Required arguments

None.


### Optional arguments

field-list

Syntax: &lt;field&gt; ...

Description: One or more field names. The events are grouped into transactions, based on the unique values in the fields. For example, suppose two fields are specified: client_ip and host . For each client_ip value, a separate transaction is returned for each unique host value for that client_ip .

memcontrol-options

Syntax: &lt;maxopentxn&gt; | &lt;maxopenevents&gt; | &lt;keepevicted&gt;

Description: These options control the memory usage for your transactions. They are not required, but you can use 0 or more of the options to define your transaction. See Memory control options .

name

Syntax: name=&lt;transaction-name&gt;

Description: Specify the stanza name of a transaction that is configured in the transactiontypes.conf file. This runs the search using the settings defined in this stanza of the configuration file. If you provide other transaction definition options (such as maxpause) in this search, they overrule the settings in the configuration file.

rendering-options

Syntax: &lt;delim&gt; | &lt;mvlist&gt; | &lt;mvraw&gt; | &lt;nullstr&gt;

Description: These options control the multivalue rendering for your transactions. They are not required, but you can use 0 or more of the options to define your transaction. See Multivalue rendering options .

txn_definition-options

Syntax: &lt;maxspan&gt; | &lt;maxpause&gt; | &lt;maxevents&gt; | &lt;startswith&gt; | &lt;endswith&gt; | &lt;connected&gt; | &lt;unifyends&gt; | &lt;keeporphans&gt;

Description: Specify the transaction definition options to define your transactions. You can use multiple options to define your transaction.


### Txn definition options

connected

Syntax: connected=&lt;bool&gt;

Description: Only relevant if a field or fields list is specified. If an event contains fields required by the transaction, but none of these fields have been instantiated in the transaction (added with a previous event), this opens a new transaction (connected=true) or adds the event to the transaction (connected=false).

If the default value for this argument is changed, the default for the unifyends argument will also change to the same value. For example, if connected=false , then unifyends=false .

Default: true

endswith

Syntax: endswith=&lt;filter-string&gt;

Description: A search or eval expression which, if satisfied by an event, marks the end of a transaction.

keeporphans

Syntax: keeporphans=true | false

Description: Specify whether the transaction command should output the results that are not part of any transactions. The results that are passed through as "orphans" are distinguished from transaction events with a _txn_orphan field, which has a value of 1 for orphan results.

Default: false

maxspan

Syntax: maxspan=&lt;int&gt;[s | m | h | d]

Description: Specifies the maximum length of time in seconds, minutes, hours, or days that the events can span, which is the maximum total time between the earliest and latest events in a transaction. The events in the transaction must span less than the integer specified for maxspan . Events that exceed the maxspan limit are treated as part of a separate transaction. If the value is negative, the maxspan constraint is deactivated and there is no limit.



Events must be sorted in descending chronological order before the maxspan argument is used. See the related example later in this topic.

Default: -1 (no limit)

maxpause

Syntax: maxpause=&lt;int&gt;[s | m | h | d]

Description: Specifies the maximum length of time in seconds, minutes, hours, or days for the pause between consecutive events in a transaction, which is the maximum total time between events. If the value is negative, the maxpause constraint is deactivated and there is no limit.



Events must be sorted in descending chronological order before the maxpause argument is used. See the related example later in this topic.

Default: -1 (no limit)

maxevents

Syntax: maxevents=&lt;int&gt;

Description: The maximum number of events in a transaction. This constraint is deactivated if the value is negative.

Default: 1000

startswith

Syntax: startswith=&lt;filter-string&gt;

Description: A search or eval filtering expression which if satisfied by an event marks the beginning of a new transaction.

unifyends

Syntax: unifyends= true | false

Description: Whether to force events that match startswith/endswith constraint(s) to also match at least one of the fields used to unify events into a transaction.

The default value for this argument is the same as the connected argument. For example, if connected=false , then unifyends=false .

Default: true, set to the same default value as the connected argument


### Filter string options

These options are used with the startswith and endswith arguments.

&lt;filter-string&gt;

Syntax: &lt;search-expression&gt; | (&lt;quoted-search-expression&gt;) | eval(&lt;eval-expression&gt;)

Description: A search or eval filtering expression which if satisfied by an event marks the end of a transaction.

&lt;search-expression&gt;

Description: A valid search expression that does not contain quotes.

&lt;quoted-search-expression&gt;

Description: A valid search expression that contains quotes.

&lt;eval-expression&gt;

Description: A valid eval expression that evaluates to a Boolean.


### Memory control options

If you have Splunk Cloud Platform, Splunk Support administers these settings in the limits.conf file on your behalf.

keepevicted

Syntax: keepevicted=&lt;bool&gt;

Description: Whether to output evicted transactions. Evicted transactions can be distinguished from non-evicted transactions by checking the value of the closed_txn field. The closed_txn field is set to 0 , or false, for evicted transactions and 1 , or true for non-evicted, or closed, transactions. The closed_txn field is set to 1 if one of the following conditions is specified: maxevents , maxspan , maxpause , startswith . For startswith , because the transaction command sees events in reverse chronological order, it closes a transaction when it satisfies the start condition. If none of these conditions is specified, all transactions are output even though all transactions will have closed_txn set to 0 . A transaction can also be evicted when the memory limitations are reached.

Default: false or 0

maxopenevents

Syntax: maxopenevents=&lt;int&gt;

Description: Specifies the maximum number of events (which are) part of open transactions before transaction eviction starts happening, using LRU policy.

Default: The default value for this argument is read from the transactions stanza in the limits.conf file.

maxopentxn

Syntax: maxopentxn=&lt;int&gt;

Description: Specifies the maximum number of not yet closed transactions to keep in the open pool before starting to evict transactions, using LRU policy.

Default: The default value for this argument is read from the transactions stanza in the limits.conf file.


### Multivalue rendering options

delim

Syntax: delim=&lt;string&gt;

Description: Specify a character to separate multiple values. When used in conjunction with the mvraw=t argument, represents a string used to delimit the values in the _raw field.

Default: " " (whitespace)

mvlist

Syntax: mvlist= true | false | &lt;field-list&gt;

Description: Flag that controls how multivalued fields are processed. When set to mvlist=true , the multivalued fields in the transaction are a list of the original events ordered in arrival order. When set to mvlist=false , the multivalued fields in the transaction are a set of unique field values ordered alphabetically. If a comma or space delimited list of fields is provided, only those fields are rendered as lists.

Default: false

mvraw

Syntax: mvraw=&lt;bool&gt;

Description: Used to specify whether the _raw field of the transaction search result should be a multivalued field.

Default: false

nullstr

Syntax: nullstr=&lt;string&gt;

Description: A string value to use when rendering missing field values as part of multivalued fields in a transaction. This option applies only to fields that are rendered as lists.

Default: NULL


## Usage

The transaction command is a centralized streaming command. See Command types .

In the output, the events in a transaction are grouped together as multiple values in the Events field. Each event in a transaction starts on a new line by default.

If there are more than 5 events in a transaction, the remaining events in the transaction are collapsed. A message appears at the end of the transaction which gives you the option to show all of the events in the transaction.


### Specifying multiple fields

The Splunk software does not necessarily interpret the transaction defined by multiple fields as a conjunction ( field1 AND field2 AND field3 ) or a disjunction ( field1 OR field2 OR field3 ) of those fields. If there is a transitive relationship between the fields in the fields list and if the related events appear in the correct sequence, each with a different timestamp, transaction command will try to use it. For example, if you searched for

CODE

Copy

... | transaction host cookie


```spl

... | transaction host cookie

```


You might see the following events grouped into a transaction:

CODE

Copy

event=1 host=a
event=2 host=a cookie=b
event=3 cookie=b


```spl

event=1 host=a
event=2 host=a cookie=b
event=3 cookie=b

```



### Descending chronological order required

The transaction command requires that the incoming events be in descending chronological order. Some commands, such as eval , might change the order or time labeling of events. If one of these commands precedes the transaction command, your search returns an error unless you include a sort command in your search. The sort command must occur immediately before the transaction command to reorder the search results in descending chronological order.


## Basic Examples


### 1. Transactions with the same host, time range, and pause

Group search results that have the same host and cookie value, occur within 30 seconds, and do not have a pause of more than 5 seconds between the events.

CODE

Copy

... | transaction host cookie maxspan=30s maxpause=5s


```spl

... | transaction host cookie maxspan=30s maxpause=5s

```



### 2. Transactions with the same "from" value, time range, and pause

Group search results that have the same value of "from", with a maximum span of 30 seconds, and a pause between events no greater than 5 seconds into a transaction.

PYTHON

Copy

... | transaction from maxspan=30s maxpause=5s


```spl

... | transaction from maxspan=30s maxpause=5s

```



### 3. Transactions with the same field values

You have events that include an alert_level. You want to create transactions where the level is equal. Using the streamstats command, you can remember the value of the alert level for the current and previous event. Using the transaction command, you can create a new transaction if the alert level is different. Output specific fields to table.

CODE

Copy

... | streamstats window=2 current=t latest(alert_level) AS last earliest(alert_level) AS first | transaction endswith=eval(first!=last) | table _time duration first last alert_level eventcount


```spl

... | streamstats window=2 current=t latest(alert_level) AS last earliest(alert_level) AS first | transaction endswith=eval(first!=last) | table _time duration first last alert_level eventcount

```



## Extended Examples


### 1. Transactions of Web access events based on IP address


| This example uses the sample data from the Search Tutorial but should work with any format of Apache web access log. To try this example on your own Splunk instance, you must download the sample data and follow the instructions toget the tutorial data into Splunk. Use the time rangeYesterdaywhen you run the search. |
| --- |


Define a transaction based on Web access events that share the same IP address. The first and last events in the transaction should be no more than thirty seconds apart and each event should not be longer than five seconds apart.

CODE

Copy

sourcetype=access_\* | transaction clientip maxspan=30s maxpause=5s


```spl

sourcetype=access_* | transaction clientip maxspan=30s maxpause=5s

```


This produces the following events list. The clientip for each event in the transaction is highlighted.



This search groups events together based on the IP addresses accessing the server and the time constraints. The search results might have multiple values for some fields, such as


```spl

host

```


and


```spl

source

```


. For example, requests from a single IP could come from multiple hosts if multiple people are shopping from the same office. For more information, read the topic

About transactions

in the

Knowledge Manager Manual

.




### 2. Transaction of Web access events based on host and client IP


| This example uses the sample data from the Search Tutorial but should work with any format of Apache web access log. To try this example on your own Splunk instance, you must download the sample data and follow the instructions toget the tutorial data into Splunk. Use the time rangeYesterdaywhen you run the search. |
| --- |


Define a transaction based on Web access events that have a unique combination of host and clientip values. The first and last events in the transaction should be no more than thirty seconds apart and each event should not be longer than five seconds apart.

CODE

Copy

sourcetype=access_\* | transaction clientip host maxspan=30s maxpause=5s


```spl

sourcetype=access_* | transaction clientip host maxspan=30s maxpause=5s

```


This search produces the following events list.



Each of these events have a distinct combination of the IP address (


```spl

clientip

```


) values and


```spl

host

```


values within the limits of the time constraints specified in the search.




### 3. Purchase transactions based on IP address and time range


| This example uses the sample data from the Search Tutorial but should work with any format of Apache web access log. To try this example on your own Splunk instance, you must download the sample data and follow the instructions toget the tutorial data into Splunk. Use the time rangeYesterdaywhen you run the search. |
| --- |


This search defines a purchase transaction as 3 events from one IP address which occur in a 10 minute span of time.

CODE

Copy

sourcetype=access_\* action=purchase | transaction clientip maxspan=10m maxevents=3


```spl

sourcetype=access_* action=purchase | transaction clientip maxspan=10m maxevents=3

```


This search defines a purchase event based on Web access events that have the action=purchase value. These results are then piped into the transaction command. This search identifies purchase transactions by events that share the same clientip , where each session lasts no longer than 10 minutes, and includes no more than 3 events.

This search produces the following events list:




### 4. Email transactions based on maxevents and endswith


| This example uses sample email data. You should be able to run this search on any email data by replacing thesourcetype=cisco:esawith thesourcetypevalue and themailfromfield with email address field name in your data. For example, the email might beTo,From, orCc). |
| --- |


This example defines an email transaction as a group of up to 10 events. Each event contains the same value for the mid (message ID), icid (incoming connection ID), and dcid (delivery connection ID). The last event in the transaction contains a Message done string.

CODE

Copy

sourcetype="cisco:esa" | transaction mid dcid icid maxevents=10 endswith="Message done"


```spl

sourcetype="cisco:esa" | transaction mid dcid icid maxevents=10 endswith="Message done"

```


This search produces the following list of events:



By default, only the first 5 events in a transaction are shown. The first transaction contains 7 events and the last event is hidden. The second and third transactions show the

Message done

string in the last event in the transaction.




### 5. Email transactions based on maxevents, maxspan, and mvlist


| This example uses sample email data. You should be able to run this search on any email data by replacing thesourcetype=cisco:esawith thesourcetypevalue and themailfromfield with email address field name in your data. For example, the email might beTo,From, orCc). |
| --- |


This example defines an email transaction as a group of up to 10 events. Each event contains the same value for the mid (message ID), icid (incoming connection ID), and dcid (delivery connection ID). The first and last events in the transaction should be no more than thirty seconds apart.

CODE

Copy

sourcetype="cisco:esa" | transaction mid dcid icid maxevents=10 maxspan=30s mvlist=true


```spl

sourcetype="cisco:esa" | transaction mid dcid icid maxevents=10 maxspan=30s mvlist=true

```


By default, the values of multivalue fields are suppressed in search results with the default setting for mvlist , which is false. Specifying mvlist=true in this search displays all of the values of the selected fields. This produces the following events list:



Here you can see that each transaction has a duration that is less than thirty seconds. Also, if there is more than one value for a field, each of the values is listed.




### 6. Transactions with the same session ID and IP address


| This example uses the sample data from the Search Tutorial but should work with any format of Apache web access log. To try this example on your own Splunk instance, you must download the sample data and follow the instructions toget the tutorial data into Splunk. Use the time rangeAll timewhen you run the search. |
| --- |


Define a transaction as a group of events that have the same session ID, JSESSIONID , and come from the same IP address, clientip , and where the first event contains the string, "view", and the last event contains the string, "purchase".

CODE

Copy

sourcetype=access_\* | transaction JSESSIONID clientip startswith="view" endswith="purchase" | where duration&gt;0


```spl

sourcetype=access_* | transaction JSESSIONID clientip startswith="view" endswith="purchase" | where duration>0

```


The search defines the first event in the transaction as events that include the string, "view", using the startswith="view" argument. The endswith="purchase" argument does the same for the last event in the transaction.

This example then pipes the transactions into the where command and the duration field to filter out all of the transactions that took less than a second to complete. The where filter cannot be applied before the transaction command because the duration field is added by the transaction command.



You might be curious about why the transactions took a long time, so viewing these events might help you to troubleshoot.

You won't see it in this data, but some transactions might take a long time because the user is updating and removing items from their shopping cart before they completes the purchase. Additionally, this search is run over all events. There is no filtering before the transaction command. Anytime you can filter the search before the first pipe, the faster the search runs.


### 7. Sort order when using maxspan and maxpause

Pay careful attention to the sort order of your events when using the maxspan and maxpause arguments with the transaction command because searches with events sorted in ascending chronological order return incorrect results.

For example, the following search returns expected results because the search uses | sort -_time to sort events in descending chronological order before the maxspan argument is used:

CODE

Copy

|makeresults count=10
|streamstats count
|eval _time=now()+10\*count, user="nobody"
|sort -_time
|transaction user maxspan=11s


```spl

|makeresults count=10
|streamstats count
|eval _time=now()+10*count, user="nobody"
|sort -_time
|transaction user maxspan=11s

```


The results look like this:


| _raw | _time | closed_txn | count | duration | eventcount | field_match_sum | linecount | user |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | 2024-07-16 16:10:30 | 1 | 109 | 10 | 2 | 2 | 2 | nobody |
|  | 2024-07-16 16:10:10 | 1 | 78 | 10 | 2 | 2 | 2 | nobody |
|  | 2024-07-16 16:09:50 | 1 | 56 | 10 | 2 | 2 | 2 | nobody |
|  | 2024-07-16 16:09:30 | 1 | 34 | 10 | 2 | 2 | 2 | nobody |
|  | 2024-07-16 16:09:10 | 0 | 12 | 10 | 2 | 2 | 2 | nobody |


In contrast, the following search doesn't generate the correct results because events are sorted in ascending chronological order by default before the maxspan argument is used:

CODE

Copy

|makeresults count=20
|streamstats count
|eval _time=now()+10\*count, user="nobody"
|transaction user maxspan=11s


```spl

|makeresults count=20
|streamstats count
|eval _time=now()+10*count, user="nobody"
|transaction user maxspan=11s

```


The results look like this:


| _raw | _time | closed_txn | count | duration | eventcount | field_match_sum | linecount | user |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | 2024-07-16 16:09:17 | 0 | 11023456789 | 90 | 10 | 10 | 10 | nobody |



## See also

Reference

About transactions

Commands

stats

concurrency


## Answers

Have questions? Visit Splunk Answers and see what questions and answers the Splunk community has using the transaction command .
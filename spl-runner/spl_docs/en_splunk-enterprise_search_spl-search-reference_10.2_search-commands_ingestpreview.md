
# ingestpreview

The ingestpreview command previews ingest-time configuration settings without having to ingest or import data.


## Description

The ingestpreview command previews ingest-time configuration settings without having to ingest or import data.

The ingestpreview command previews ingest-time configuration settings without having to ingest or import data. The ingestpreview command takes incoming search results, generates mock ingestion events from those results, and supplies those mock events to the specified ingestion processor, which then outputs the processed events. This lets you quickly author ingest-time configurations without having to upload or index real data. For example, you can iterate or debug an INGEST_EVAL or REGEX transform, as well as troubleshoot configurations in props.conf and transforms.conf.


## Syntax

Syntax for using the ingestpreview command.

The required syntax is in bold .

ingestpreview

[generate_helper_fields=&lt;boolean&gt;]

[ingest_processor=&lt;string&gt;]

[meta_mode=&lt;string&gt;]

[props:&lt;key&gt;=&lt;value&gt;]...

[show_inputs=&lt;boolean&gt;]

[transforms:&lt;key&gt;=&lt;value&gt;]...


### Required arguments

None.


### Optional arguments

generate_helper_fields

Syntax: generate_helper_fields=&lt;boolean&gt;

Description:

Generates the following three additional fields:


| Field | Description |
| --- | --- |
| TRANSFORMS.CONF | Generates the exact settings you can copy and paste into transforms.conf. Settings might differ from those you supply to this search command because of character escaping rule discrepancies between the search language and configuration files. |
| PROPS.CONF | Generates the exact settings you can copy and paste into props.conf. Settings might differ from those you supply to this search command because of character escaping rule discrepancies between the search language and configuration files. |
| WARNS.ERRS | Displays any errors or warnings reported by the processor to help further troubleshoot settings. |


Default: true

ingest_processor

Syntax: ingest_processor=&lt;string&gt;

Description:

The target ingest-time processor accepts one of the following values:


| Option | Description |
| --- | --- |
| regexreplacement | Use for regex replacement. |
| metrics | Use for statsd or collectd data. |
| metricschema | Use for logs to metrics. |


Default: regexreplacement

meta_mode

Syntax: meta_mode=&lt;string&gt;

Description:

Controls how the


```spl

ingestpreview

```


command displays the resulting _meta key. The _meta key contains the map of indexed time field/value pairs. The command always generates a _meta field if it is present in the results. However, Splunk Web will not show this by default since it is a field that starts with an underscore ( _ ). You can set


```spl

meta_mode

```


to one of the following options:


| Option | Description |
| --- | --- |
| Unhide | Creates an alias to the _meta field namedMETAso it is visible in Splunk Web. This is equivalent to using\|eval META=_meta. |
| Expand | Allows each indexed time field/value pair to become a separate field. Each field will be prefixed withMETA.. |
| All | Performs bothexpandandunhidebehaviors. |
| None | Doesn't performexpandorunhidebehaviors. |


Default: unhide

props

Syntax: props:&lt;key&gt;=&lt;value&gt;

Description:

Supply one or more settings for props using this syntax. For example, to configure a statsd event using METRICS_PROTOCOL, specify


```spl

props:METRICS_PROTOCOL=statsd

```


.


> **Note: If field values contain spaces or special characters, you can wrap the values in parentheses or double quotes. The command strips the outer set of these characters before processing the arguments.**


show_inputs

Syntax: show_inputs=&lt;boolean&gt;

Description: If set to true , the command generates INPUT.\* fields for each input field with the original value before transformation. This is helpful for determining the difference between the input and output for a particular field.

transforms

Syntax: transforms:&lt;key&gt;=&lt;value&gt;

Description:

Supply one or more settings for transforms using this syntax. For example, to configure the REGEX setting in transforms.conf, specify


```spl

transforms:REGEX=<your regex>

```


.


> **Note: If field values contain spaces or special characters, you can wrap the values in parentheses or double quotes. The command strips the outer set of these characters before processing the arguments.**



## Examples

Examples for the ingestpreview command.




### 1. Create a meta field and set it to Hello World

Run INGEST_EVAL that creates a meta field, myfield and sets it to Hello World .

CODE

Copy

| makeresults count | fields - count | ingestpreview transforms:INGEST_EVAL=(myfield="Hello World")


```spl

| makeresults count | fields - count | ingestpreview transforms:INGEST_EVAL=(myfield="Hello World")

```



### 2. Run a REGEX transform that changes myfield if _raw matches

Run a REGEX transform that changes myfield if _raw matches. Note that double quotes are used on the REGEX parameter to deal with spaces.

CODE

Copy

| makeresults count| fields - count | eval _raw="raw with open(parenthesis)close" | eval myfield="original_value" | ingestpreview transforms:REGEX="with open\(parenthesis\)close" transforms:WRITE_META=true transforms:FORMAT="$0 myfield::new_value"


```spl

| makeresults count| fields - count | eval _raw="raw with open(parenthesis)close" | eval myfield="original_value" | ingestpreview transforms:REGEX="with open\(parenthesis\)close" transforms:WRITE_META=true transforms:FORMAT="$0 myfield::new_value"

```



### 3. Test dimension extraction (ipv4) for statsd data

Uses ingest_processor=metrics to test dimension extraction (ipv4) for statsd data.

JSON

Copy

| makeresults count| fields - count | eval _raw="cpu.idle.10.3.4.134:1.2342|g" | ingestpreview ingest_processor=metrics props:METRICS_PROTOCOL=statsd props:NO_BINARY_CHECK=true props:SHOULD_LINEMERGE=false transforms:REGEX=((?&lt;ipv4&gt;\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})) transforms:REMOVE_DIMS_FROM_METRIC_NAME=true | eval metric_value=_value


```spl

| makeresults count| fields - count | eval _raw="cpu.idle.10.3.4.134:1.2342|g" | ingestpreview ingest_processor=metrics props:METRICS_PROTOCOL=statsd props:NO_BINARY_CHECK=true props:SHOULD_LINEMERGE=false transforms:REGEX=((?<ipv4>\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})) transforms:REMOVE_DIMS_FROM_METRIC_NAME=true | eval metric_value=_value

```



### 4. Build a metrics event out of sample data

Uses ingest_processor=metricschema to build a metrics event out of sample data. This search first builds a raw event, then mimics the metadata from the field extractions, and then runs the ingestpreview command to display the mock metrics event.

CODE

Copy

| makeresults | eval _raw="2021-01-03T10:35:12-0800 dns_name=contrarian.local severity=informational http_status=200 response_ms=244" | extract auto=f field_extraction | eval _meta="dns_name::contrarian.local severity::informational http_status::200 response_ms::244" | ingestpreview ingest_processor=metricschema generate_helper_fields=true meta_mode=all transforms:METRIC-SCHEMA-MEASURES="NUMS_EXCEPT http_status"


```spl

| makeresults | eval _raw="2021-01-03T10:35:12-0800 dns_name=contrarian.local severity=informational http_status=200 response_ms=244" | extract auto=f field_extraction | eval _meta="dns_name::contrarian.local severity::informational http_status::200 response_ms::244" | ingestpreview ingest_processor=metricschema generate_helper_fields=true meta_mode=all transforms:METRIC-SCHEMA-MEASURES="NUMS_EXCEPT http_status"

```

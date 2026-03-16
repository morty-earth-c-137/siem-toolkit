
# bucketdir


## Description

Replaces a field value with higher-level grouping, such as replacing filenames with directories.

Returns the maxcount events, by taking the incoming events and rolling up multiple sources into directories, by preferring directories that have many files but few events. The field with the path is PATHFIELD (e.g., source), and strings are broken up by a separator character. The default pathfield=source; sizefield=totalCount; maxcount=20; countfield=totalCount; sep="/" or "\\", depending on the operation system.


## Syntax

bucketdir pathfield=&lt;field&gt; sizefield=&lt;field&gt; [maxcount=&lt;int&gt;] [countfield=&lt;field&gt;] [sep=&lt;char&gt;]


### Required arguments

pathfield

Syntax: pathfield=&lt;field&gt;

Description: Specify a field name that has a path value.

sizefield

Syntax: sizefield=&lt;field&gt;

Description: Specify a numeric field that defines the size of bucket.


### Optional arguments

countfield

Syntax: countfield=&lt;field&gt;

Description: Specify a numeric field that describes the count of events.

maxcount

Syntax: maxcount=&lt;int&gt;

Description: Specify the total number of events to bucket.

sep

Syntax: &lt;char&gt;

Description: The separating character. Specify either a forward slash "/" or double back slashes "\\", depending on the operating system.


## Usage

The bucketdir command is a streaming command. It is distributable streaming by default, but centralized streaming if the local setting specified for the command in the commands.conf file is set to true. See Command types .


## Examples


### Example 1:

Return 10 best sources and directories.

CODE

Copy

... | top source | bucketdir pathfield=source sizefield=count maxcount=10


```spl

... | top source | bucketdir pathfield=source sizefield=count maxcount=10

```



## See also

cluster , dedup

# makecontinuous


## Description

Makes a field on the x-axis numerically continuous by adding empty buckets for periods where there is no data and quantifying the periods where there is data. This x-axis field can then be invoked by the chart and timechart commands.


## Syntax

The required syntax is in bold .

makecontinuous

&lt;field&gt;

[&lt;bin-options&gt;...]


### Required arguments

&lt;bins-options&gt;

Datatype: bins | span | start-end

Description: Discretization options. See "Bins options" for details.


### Optional arguments

&lt;field&gt;

Datatype: &lt;field&gt;

Description: Specify a field name.


### Bins options

bins

Syntax: bins=&lt;int&gt;

Description: Sets the maximum number of bins to discretize into.

span

Syntax: &lt;log-span&gt; | &lt;span-length&gt;

Description: Sets the size of each bin, using a span length based on time or log-based span.

&lt;start-end&gt;

Syntax: end=&lt;num&gt; | start=&lt;num&gt;

Description: Sets the minimum and maximum extents for numerical bins. Data outside of the [start, end] range is discarded.


### Span options

&lt;log-span&gt;

Syntax: [&lt;num&gt;]log[&lt;num&gt;]

Description: Sets to log-based span. The first number is a coefficient. The second number is the base. If the first number is supplied, it must be a real number &gt;= 1.0 and &lt; base. Base, if supplied, must be real number &gt; 1.0, meaning it must be strictly greater than 1.

span-length

Syntax: &lt;span&gt;[&lt;timescale&gt;]

Description: A span length based on time.

&lt;span&gt;

Syntax: &lt;int&gt;

Description: The span of each bin. If using a timescale, this is used as a time range. If not, this is an absolute bin "length."

&lt;timescale&gt;

Syntax: &lt;sec&gt; | &lt;min&gt; | &lt;hr&gt; | &lt;day&gt; | &lt;month&gt; | &lt;subseconds&gt;

Description: Time scale units.


| Time scale | Syntax | Description |
| --- | --- | --- |
| &lt;sec&gt; | s \| sec \| secs \| second \| seconds | Time scale in seconds. |
| &lt;min&gt; | m \| min \| mins \| minute \| minutes | Time scale in minutes. |
| &lt;hr&gt; | h \| hr \| hrs \| hour \| hours | Time scale in hours. |
| &lt;day&gt; | d \| day \| days | Time scale in days. |
| &lt;month&gt; | mon \| month \| months | Time scale in months. |
| &lt;subseconds&gt; | us \| ms \| cs \| ds | Time scale in microseconds (us), milliseconds (ms), centiseconds (cs), or deciseconds (ds) |



## Usage

The makecontinuous command is a transforming command . See Command types .


## Examples


### Example 1:

Make the _time field continuous with a span of 10 minutes.

CODE

Copy

... | makecontinuous _time span=10m


```spl

... | makecontinuous _time span=10m

```



## See also

chart , timechart
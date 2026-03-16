
# kmeans


## Description

Partitions the events into k clusters, with each cluster defined by its mean value. Each event belongs to the cluster with the nearest mean value. Performs k-means clustering on the list of fields that you specify. If no fields are specified, performs the clustering on all numeric fields. Events in the same cluster are moved next to each other. You have the option to display the cluster number for each event.


## Syntax

kmeans [ kmeans-options ...] [ field-list ]


### Required arguments

None.


### Optional arguments

field-list

Syntax: &lt;field&gt; ...

Description: Specify a space separated list of the exact fields to use for the join.

Default: If no fields are specified, uses all numerical fields that are common to both result sets. Skips events with non-numerical fields.

kmeans-options

Syntax: &lt;reps&gt; | &lt;iters&gt; | &lt;t&gt; | &lt;k&gt; | &lt;cnumfield&gt; | &lt;distype&gt; | &lt;showcentroid&gt;

Description: Options for the kmeans command.


### kmeans options

reps

Syntax: reps=&lt;int&gt;

Description: Specify the number of times to repeat kmeans using random starting clusters.

Default: 10

iters

Syntax: maxiters=&lt;int&gt;

Description: Specify the maximum number of iterations allowed before failing to converge.

Default: 10000

t

Syntax: t=&lt;num&gt;

Description: Specify the algorithm convergence tolerance.

Default: 0

k

Syntax: k=&lt;int&gt; | &lt;int&gt;-&lt;int&gt;

Description: Specify as a scalar integer value or a range of integers. When provided as single number, selects the number of clusters to use. This produces events annotated by the cluster label. When expressed as a range, clustering is done for each of the cluster counts in the range and a summary of the results is produced. These results express the size of the clusters, and a 'distortion' field which represents how well the data fits those selected clusters. Values must be greater than 1 and less than maxkvalue (see Limits section).

Default: k=2

cnumfield

Syntax: cfield=&lt;field&gt;

Description: Names the field to annotate the results with the cluster number for each event.

Default: CLUSTERNUM

distype

Syntax: dt= ( l1 | l1norm | cityblock | cb ) | ( l2 | l2norm | sq | sqeuclidean ) | ( cos | cosine )

Description: Specify the distance metric to use. The l1 , l1norm , and cb distance metrics are synonyms for cityblock . The l2 , l2norm , and sq distance metrics are synonyms for sqeuclidean or sqEuclidean . The cos distance metric is a synonym for cosine .

Default: sqeucildean

showcentroid

Syntax: showcentroid= true | false

Description: Specify whether to expose the centroid centers in the search results (showcentroid=true) or not.

Default: true


## Usage


### Limits

The number of clusters to collect the values into -- k -- is not permitted to exceed maxkvalue. The maxkvalue is specified in the limits.conf file, in the [kmeans] stanza. The maxkvalue default is 1000.

When a range is given for the k option, the total distance between the beginning and ending cluster counts is not permitted to exceed maxkrange. The maxkrange is specified in the limits.conf file, in the [kmeans] stanza. The maxkrange default is 100.

The above limits are designed to avoid the computation work becoming unreasonably expensive.

The total number of values which are clustered by the algorithm (typically the number of input results) is limited by the maxdatapoints parameter in the [kmeans] stanza of limits.conf . If this limit is exceeded at runtime, a warning message displays in Splunk Web. This defaults to 100000000 or 100 million. This maxdatapoints limit is designed to avoid exhausting memory.


## Examples

Example 1: Group search results into 4 clusters based on the values of the "date_hour" and "date_minute" fields.

CODE

Copy

... | kmeans k=4 date_hour date_minute


```spl

... | kmeans k=4 date_hour date_minute

```


Example 2: Group results into 2 clusters based on the values of all numerical fields.

CODE

Copy

... | kmeans


```spl

... | kmeans

```



## See also

anomalies , anomalousvalue , cluster , outlier ,
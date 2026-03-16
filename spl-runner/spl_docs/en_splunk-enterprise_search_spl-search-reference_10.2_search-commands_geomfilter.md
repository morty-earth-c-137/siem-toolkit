
# geomfilter


## Description

Use the geomfilter command to specify points of a bounding box for clipping choropleth maps.

For more information about choropleth maps, see "Mapping data" in the Dashboards and Visualizations Manual.


## Syntax

geomfilter [min_x=&lt;float&gt;] [min_y=&lt;float&gt;] [max_x=&lt;float&gt;] [max_y=&lt;float&gt;]


### Optional arguments

min_x

Syntax: min_x=&lt;float&gt;

Description: The x coordinate of the bounding box's bottom-left corner, in the range [-180, 180].

Default: -180

min_y

Syntax: min_y=&lt;float&gt;

Description: The y coordinate of the bounding box's bottom-left corner, in the range [-90, 90].

Default: -90

max_x

Syntax: max_x=&lt;float&gt;

Description: The x coordinate of the bounding box's up-right corner, in the range [-180, 180].

Default: 180

max_y

Syntax: max_y=&lt;float&gt;

Description: The y coordinate of the bounding box's up-right corner, in the range [-90, 90].

Default: max_y=90




## Usage

The geomfilter command accepts two points that specify a bounding box for clipping choropleth maps. Points that fall outside of the bounding box will be filtered out.


## Examples

Example 1: This example uses the default bounding box, which will clip the entire map.

CODE

Copy

...| geomfilter


```spl

...| geomfilter

```




Example 2:

This example clips half of the whole map.



CODE

Copy

...| geomfilter min_x=-90 min_y=-90 max_x=90 max_y=90


```spl

...| geomfilter min_x=-90 min_y=-90 max_x=90 max_y=90

```



## See also

geom

# abstract


## Description

Produces an abstract, a summary or brief representation, of the text of the search results. The original text is replaced by the summary.

The abstract is produced by a scoring mechanism. Events that are larger than the selected maxlines , those with more textual terms and more terms on adjacent lines, are preferred over events with fewer terms. If a line has a search term, its neighboring lines also partially match, and might be returned to provide context. When there are gaps between the selected lines, lines are prefixed with an ellipsis (...).

If the text of an event has fewer lines or an equal number of lines as maxlines , no change occurs.


## Syntax

The required syntax is in bold .

abstract

[maxterms=&lt;int&gt;]

[maxlines=&lt;int&gt;]


### Optional arguments

maxterms

Syntax: maxterms=&lt;int&gt;

Description: The maximum number of terms to match. Accepted values are 1 to 1000.

Default: 1000

maxlines

Syntax: maxlines=&lt;int&gt;

Description: The maximum number of lines to match. Accepted values are 1 to 500.

Default: 10


## Examples


### Specify the number of lines to return

Show a summary of up to 5 lines for each search result.

CODE

Copy

... | abstract maxlines=5


```spl

... | abstract maxlines=5

```



### Specify the number of terms to return

Consider the following events:


| Time | Event |
| --- | --- |
| 1/4/236:22:16.000 PM | 91.205.189.15 - - [04/Jan/2023:18:22:16] "GET /oldlink?itemId=EST-14&JSESSIONID=SD6SL7FF7ADFF53113 HTTP 1.1" 200 1665 "http://www.buttercupgames.com/oldlink?itemId=EST-14" "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.46 Safari/536.5" 159 |
| 1/3/2311:08:57.000 PM | 194.146.236.22 - - [03/Jan/2023:23:08:57] "POST /cart.do?action=addtocart&itemId=EST-15&productId=WC-SH-T02&JSESSIONID=SD4SL1FF2ADFF47548 HTTP 1.1" 200 1493 "http://www.buttercupgames.com/product.screen?productId=WC-SH-T02" "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5" 848 |


If you specify maxterms=20 the results look like this:


| Time | Event |
| --- | --- |
| 1/4/236:22:16.000 PM | 91.205.189.15 - - [04/Jan/2023:18 |
| 1/3/2311:08:57.000 PM | 194.146.236.22 - - [03/Jan/2023:23 |


The "terms" are identified as shown in the following table:


| Number | Event 1 term | Event 2 term |
| --- | --- | --- |
| 1 | 91 | 194 |
| 2 | . | . |
| 3 | 205 | 146 |
| 4 | . | . |
| 5 | 189 | 236 |
| 6 | . | . |
| 7 | 15 | 22 |
| 8 |  |  |
| 9 | - | - |
| 10 |  |  |
| 11 | - | - |
| 12 |  |  |
| 13 | [ | [ |
| 14 | 04 | 03 |
| 15 | / | / |
| 16 | Jan | Jan |
| 17 | / | / |
| 18 | 2023 | 2023 |
| 19 | : | : |
| 20 | 18 | 23 |



## See also

highlight

# nomv


## Description

Converts values of the specified multivalue field into one single value. Separates the values using a new line "\n delimiter.

Overrides the configurations for the multivalue field that are set in the fields.conf file.


## Syntax

nomv &lt;field&gt;


### Required arguments

field

Syntax: &lt;field&gt;

Description: The name of a multivalue field.


## Usage

The nomv command is a distributable streaming command. See Command types .

You can use evaluation functions and statistical functions on multivalue fields or to return multivalue fields.


## Examples


### Example 1:

For sendmail events, combine the values of the senders field into a single value. Display the top 10 values.

CODE

Copy

eventtype="sendmail" | nomv senders | top senders


```spl

eventtype="sendmail" | nomv senders | top senders

```



## See also

Commands:

makemv

mvcombine

mvexpand

convert



Functions:

Multivalue eval functions

Multivalue stats and chart functions

split


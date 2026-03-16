
# highlight


## Description

Highlights specified terms in the events list. Matches a string or list of strings and highlights them in the display in Splunk Web . The matching is not case sensitive.


## Syntax

highlight &lt;string&gt;...


### Required arguments

&lt;string&gt;

Syntax: &lt;string&gt; ...

Description: A space-separated list of strings to highlight in the results. The list you specify is not case-sensitive. Any combination of uppercase and lowercase letters that match the string are highlighted.


## Usage

The highlight command is a distributable streaming command. See Command types .

The string that you specify must be a field value. The string cannot be a field name.

You must use the highlight command in a search that keeps the raw events and displays output on the Events tab. You cannot use the highlight command with commands, such as stats which produce calculated or generated results.


## Examples


### Example 1:

Highlight the terms "login" and "logout".

CODE

Copy

... | highlight login,logout


```spl

... | highlight login,logout

```



### Example 2:

Highlight the phrase "Access Denied".

CODE

Copy

... | highlight "access denied"


```spl

... | highlight "access denied"

```



## See also

rangemap
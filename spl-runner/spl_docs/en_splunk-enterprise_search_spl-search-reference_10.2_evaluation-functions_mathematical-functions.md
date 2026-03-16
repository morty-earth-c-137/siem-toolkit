
# Mathematical functions

The following list contains the functions that you can use to perform mathematical calculations.

- For information about using string and numeric fields in functions, and nesting functions, see Evaluation functions .

- For the list of mathematical operators you can use with these functions, see "Operators" in the Usage section of the eval command.


## abs(&lt;num&gt;)


### Description

This function takes a number and returns its absolute value.


### Usage

You can use this function with the eval , fieldformat , and where commands, and as part of eval expressions.


### Basic example

The following example creates a field called absnum , whose values are the absolute values of the numeric field number .

CODE

Copy

... | eval absnum=abs(number)


```spl

... | eval absnum=abs(number)

```



## ceiling(&lt;num&gt;) or ceil(&lt;num&gt;)


### Description

This function rounds a number up to the next highest integer.


### Usage

You can use this function with the eval , fieldformat , and where commands, and as part of eval expressions.

You can use the abbreviation ceil instead of the full name of the function.


### Basic example

The following example returns n=2.

CODE

Copy

... | eval n=ceil(1.9)


```spl

... | eval n=ceil(1.9)

```



## exact(&lt;expression&gt;)


### Description

This function renders the result of a numeric expression with a larger amount of precision in the formatted output.


### Usage

You can use this function with the eval , fieldformat , and where commands, and as part of eval expressions.


### Basic example

CODE

Copy

... | eval n=exact(3.14 \* num)


```spl

... | eval n=exact(3.14 * num)

```



## exp(&lt;num&gt;)


### Description

This function takes a number and returns the exponential function e N .


### Usage

You can use this function with the eval , fieldformat , and where commands, and as part of eval expressions.


### Basic example

The following example returns y=e 3 .

CODE

Copy

... | eval y=exp(3)


```spl

... | eval y=exp(3)

```



## floor(&lt;num&gt;)


### Description

This function rounds a number down to the nearest whole integer.


### Usage

You can use this function with the eval , fieldformat , and where commands, and as part of eval expressions.


### Basic example

The following example returns 1.

CODE

Copy

... | eval n=floor(1.9)


```spl

... | eval n=floor(1.9)

```



## ln(&lt;num&gt;)


### Description

This function takes a number and returns the natural logarithm.


### Usage

You can use this function with the eval , fieldformat , and where commands, and as part of eval expressions.


### Basic example

The following example returns the natural logarithm of the values of bytes.

CODE

Copy

... | eval lnBytes=ln(bytes)


```spl

... | eval lnBytes=ln(bytes)

```



## log(&lt;num&gt;,&lt;base&gt;)


### Description

This function takes either one or two numeric arguments and returns the logarithm of the first argument &lt;num&gt; using the second argument &lt;base&gt;. If the second argument &lt;base&gt; is omitted, this function evaluates the logarithm of number with base 10.


### Usage

You can use this function with the eval , fieldformat , and where commands, and as part of eval expressions.


### Basic example

CODE

Copy

... | eval num=log(number,2)


```spl

... | eval num=log(number,2)

```



## pi()


### Description

This function takes no arguments and returns the constant pi to 11 digits of precision.


### Usage

You can use this function with the eval , fieldformat , and where commands, and as part of eval expressions.


### Basic example

The following example calculates the area of a circle, which is pi() multiplied by the radius to the power of 2.

CODE

Copy

... | eval area_circle=pi()\*pow(radius,2)


```spl

... | eval area_circle=pi()*pow(radius,2)

```



## pow(&lt;num&gt;,&lt;exp&gt;)


### Description

This function takes two numeric arguments &lt;num&gt; and &lt;exp&gt; and returns &lt;num&gt; &lt;base&gt; , &lt;num&gt; to the power of &lt;base&gt;.


### Usage

You can use this function with the eval , fieldformat , and where commands, and as part of eval expressions.


### Basic example

The following example calculates the area of a circle, which is pi() multiplied by the radius to the power of 2.

CODE

Copy

... | eval area_circle=pi()\*pow(radius,2)


```spl

... | eval area_circle=pi()*pow(radius,2)

```



## round(&lt;num&gt;,&lt;precision&gt;)


### Description

This function takes one or two numeric arguments &lt;num&gt; and &lt;precision&gt;, returning &lt;num&gt; rounded up to the amount of decimal places specified by &lt;precision&gt;. The default is to round up to an integer.


### Usage

You can use this function with the eval , fieldformat , and where commands, and as part of eval expressions.

You cannot specify a negative number for the decimal places.


### Basic examples

The following example returns n=4.

CODE

Copy

... | eval n=round(3.5)


```spl

... | eval n=round(3.5)

```


The following example returns n=2.56.

CODE

Copy

... | eval n=round(2.555, 2)


```spl

... | eval n=round(2.555, 2)

```



## sigfig(&lt;num&gt;)


### Description

This function takes one argument, a number, and rounds that number to the appropriate number of significant figures.


### Usage

You can use this function with the eval , fieldformat , and where commands, and as part of eval expressions.

The computation for sigfig is based on the type of calculation that generates the number.

- For multiplication and division, the result should have the minimum number of significant figures of all of the operands.

- For addition and subtraction, the result should have the same number of decimal places as the least precise number of all of the operands.

For example, the numbers 123.0 and 4.567 contain different precision with the decimal places. The first number is less precise because it has 1 decimal place. The second number is more precise because it has 3 decimal places.

If the calculation is 123.0 + 4.567 = 127.567, then the sigfig function returns the fewest number of decimal places. In this example only one decimal place is returned. Because the numbers to the right of the last significant figure are greater than 5, the result returned is 127.6


### Basic examples

Example 1 : The following example shows how the sigfig function works. The calculation 1.00\*1111 returns the value n=1111 , but the following search using the sigfig function returns n=1110 .

CODE

Copy

... | eval n=sigfig(1.00\*1111)


```spl

... | eval n=sigfig(1.00*1111)

```


In this example, 1.00 has 3 significant figures and 1111 has 4 significant figures. In this example, the minimum number of significant figures for all operands is 3. Using the sigfig function, the final result is rounded to 3 digits, returning n=1110 and not 1111.

Example 2 : There are situations where the results of a calculation can return a different accuracy to the very far right of the decimal point. For example, the following search calculates the average of 100 values:

CODE

Copy

| makeresults count=100 | eval test=3.99 | stats avg(test)


```spl

| makeresults count=100 | eval test=3.99 | stats avg(test)

```


The result of this calculation is:


| avg(test) |
| --- |
| 3.9900000000000055 |


When the count is changed to 10000, the results are different:

CODE

Copy

| makeresults count=10000 | eval test=3.99 | stats avg(test)


```spl

| makeresults count=10000 | eval test=3.99 | stats avg(test)

```


The result of this calculation is:


| avg(test) |
| --- |
| 3.990000000000215 |


This occurs because numbers are treated as double-precision floating-point numbers.

To mitigate this issue, you can use the sigfig function to specify the number of significant figures you want returned.

However, first you need to make a change to the stats command portion of the search. You need to change the name of the field avg(test) to remove the parenthesis. For example stats avg(test) AS test . The sigfig function expects either a number or a field name for X. The sigfig function cannot accept a field name that looks like another function, in this case avg .

To specify the number of decimal places you want returned, you multiply the field name by 1 and use zeros to specify the number of decimal places. If you want 4 decimal places returned, you would multiply the field name by 1.0000. To return 2 decimal places, multiply by 1.00, as shown in the following example:

CODE

Copy

| makeresults count=10000 | eval test=3.99 | stats avg(test) AS test | eval new_test=sigfig(test\*1.00)


```spl

| makeresults count=10000 | eval test=3.99 | stats avg(test) AS test | eval new_test=sigfig(test*1.00)

```


The result of this calculation is:


| test |
| --- |
| 3.99 |



## sqrt(&lt;num&gt;)


### Description

This function takes one numeric argument &lt;num&gt; and returns its square root.


### Usage

You can use this function with the eval , fieldformat , and where commands, and as part of eval expressions.


### Basic example

The following example returns 3:

CODE

Copy

... | eval n=sqrt(9)


```spl

... | eval n=sqrt(9)

```



## sum(&lt;num&gt;,...)


### Description

This function takes an arbitrary number of arguments and returns the sum of numerical values as an integer. Each argument must be either a field (single or multi value) or an expression that evaluates to a number. At least one numeric argument is required. When the function is applied to a multivalue field, each numeric value of the field is included in the total. The eval command ignores arguments that don't exist in an event or can't be converted to a number.


### Usage

You can use this function with the eval , fieldformat , and where commands, and as part of eval expressions.


### Basic examples

Example 1 : The following example creates a field called a with value 5.0, a field called b with value 9, and a field called x with value 14 that is the sum of a and b . A field is not created for c and it is not included in the sum because a value was not declared for that argument.

CODE

Copy

... | eval a = 5.0, b = "9", x = sum(a, b, c)


```spl

... | eval a = 5.0, b = "9", x = sum(a, b, c)

```


Example 2 : The following example calculates the sum of three numbers and returns c=6.

CODE

Copy

... | eval c=sum(1, 2, 3)


```spl

... | eval c=sum(1, 2, 3)

```


However, the following example returns an error because one of the arguments in the function is a string.

CODE

Copy

... | eval c=sum(1, 2, "3")


```spl

... | eval c=sum(1, 2, "3")

```


To use a quoted string as a number within the function, you must convert the number to an integer, as shown in the following example that returns c=6.

CODE

Copy

... | eval c=sum(1, 2, tonumber("3"))


```spl

... | eval c=sum(1, 2, tonumber("3"))

```


Example 3 : In this example, a field with a value that is a string results in a field called a with value 1, and a field called c with value 6,

CODE

Copy

... | eval a="1", c=sum(a, 2, 3)


```spl

... | eval a="1", c=sum(a, 2, 3)

```


Example 4 : When an argument is a field, the eval command retrieves the value and attempts to treat it as a number, even if it is a string. The following example creates a field called a with value somedata, and a field called c with value 5.

CODE

Copy

... | eval a="somedata", c=sum(a, 2, 3)


```spl

... | eval a="somedata", c=sum(a, 2, 3)

```


However, the following example returns an error because the string argument is specified directly within the function.

CODE

Copy

... | eval c=sum("somedata", 2, 3)


```spl

... | eval c=sum("somedata", 2, 3)

```

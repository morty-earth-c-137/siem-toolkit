
# Bitwise functions

You can use the following bitwise functions to manipulate fields within searches at the bit level.

- bit_and(&lt;values&gt;)

- bit_or(&lt;values&gt;)

- bit_not(&lt;value&gt;, &lt;bitmask&gt;)

- bit_xor(&lt;values&gt;)

- bit_shift_left(&lt;value&gt;, &lt;shift_offset&gt;)

- bit_shift_right(&lt;value&gt;, &lt;shift_offset&gt;)

These functions add bitwise functionality directly to the Splunk Search Processing Language (SPL), so you can perform operations such as capture a flag or apply masks on values without having to use Python workarounds.




> **Note: Only nonnegative integers in the range of 0 to 2 53 -1 are accepted as input to bitwise functions. This means that numbers that are negative or greater than 53 bits return null.**


To convert a string representation of a binary number to a decimal number, see tonumber(NUMSTR,BASE) . To convert a number to a string version of its binary representation, see tostring(X,Y) .



Read use cases from Splunk platform experts about improving Splunk platform searches with bitwise operators in Splunk Lantern Customer Success Center.


## bit_and(&lt;values&gt;)


### Description

This function takes two or more nonnegative integers as arguments and sequentially performs logical bitwise AND operations on them. Each argument must be in the range of 0 to 2 53 -1.


### Usage

This function takes an arbitrary number of comma-separated arguments and returns the result of a logical AND operation on each pair of corresponding bits. For example, the result of the following search is 8 .

CODE

Copy

| makeresults | eval result = bit_and(12, 9)


```spl

| makeresults | eval result = bit_and(12, 9)

```


This is because the result of the bitwise AND operation is 1000, which is the number 8. See the following table for more information about the sequence of operations in this bitwise function.




| Operation | Binary string | Result |
| --- | --- | --- |
| 12 | 1100 |  |
| 9 | 1001 |  |
| bit_and(12, 9) | 1000 | 8 |



## bit_or(&lt;values&gt;)


### Description

This function takes two or more nonnegative integers as arguments and sequentially performs bitwise OR operations on them. Each argument must be in the range of 0 to 2 53 -1.


### Usage

This function takes an arbitrary number of comma-separated arguments and returns the result of a logical OR operation on each pair of corresponding bits. For example, the result of the following search is 6 .

CODE

Copy

| makeresults | eval result = bit_or(4, 2)


```spl

| makeresults | eval result = bit_or(4, 2)

```


This is because the result of the bitwise OR operation is 0110, which is the number 6. See the following table for more information about the sequence of operations in this bitwise function.




| Operation | Binary string | Result |
| --- | --- | --- |
| 4 | 0100 |  |
| 2 | 0010 |  |
| bit_or(4, 2) | 0110 | 6 |



## bit_not(&lt;value&gt;, &lt;bitmask&gt;)


### Description

This function takes a nonnegative integer as an argument and inverts every bit in the binary representation of that number. This function also takes an optional second argument with a default value of 2 53 -1 that acts as a bitmask that is used in an AND operation with the result of the first operation. You can think of the bitmask as the value up to which you want to print the result.

Both arguments must be in the range of 0 to 2 53 -1 or the operation returns null.


### Usage

You might want to use an optional integer bitmask as the second argument in a bit_not function to limit the number of leading 1s in the result. The bitmask truncates the result by performing a silent bitwise AND on the result of a bitwise NOT operation. The number of bits specified as the bitmask indicates the number of bits you want to see in the results. For example, if the bitmask argument is "1111" , the first four bits of the binary results are displayed. Consider the following search, which specifies a four-bit bitmask:

CODE

Copy

| makeresults | eval long_result = bit_not(9), short_result = bit_not(9, tonumber("1111", 2)) | eval long_binary = tostring(long_result, "binary"), short_binary = tostring(short_result, "binary")


```spl

| makeresults | eval long_result = bit_not(9), short_result = bit_not(9, tonumber("1111", 2)) | eval long_binary = tostring(long_result, "binary"), short_binary = tostring(short_result, "binary")

```


The results look something like this:


| _time | long_binary | long_result | short_binary | short_result |
| --- | --- | --- | --- | --- |
| 2022-09-05 11:12:53 | 11111111111111111111111111111111111111111111111110110 | 9007199254740982 | 110 | 6 |


The short_binary result is 110 instead of a long string of bits like the long_binary results. You might wonder why the result is only three bits, and not four bits, since you specified "1111" in the bitmask. The binary result is actually 0110 , but the leading 0 is not displayed.

You can take a closer look at what is happening in the sequence of bitwise operations using the following table as a guide. First, the bitmask is set to the bitwise NOT of 0, by default. Then, the result of bit_not(9) is "bitwise ANDed" with 15, which is the bitmask resulting from tonumber("1111", 2) . The result of bit_not(9,15) is 110 in binary and 6 in decimal.


| Operation | Binary string | Result |
| --- | --- | --- |
| 0 | 00000 00000000 00000000 00000000 00000000 00000000 00000000 |  |
| bit_not(0) | 11111 11111111 11111111 11111111 11111111 11111111 11111111 |  |
| 9 | 00000 00000000 00000000 00000000 00000000 00000000 00001001 |  |
| bit_not(9) | 11111 11111111 11111111 11111111 11111111 11111111 11110110 |  |
| 15 | 00000 00000000 00000000 00000000 00000000 00000000 00001111 |  |
| bit_not(9, 15) | 00000 00000000 00000000 00000000 00000000 00000000 00000110 | 110 in binary6 in decimal |



## bit_xor(&lt;values&gt;)


### Description

This function takes two or more nonnegative integers as arguments and sequentially performs bitwise XOR operations on each of the given arguments. Each argument must be in the range of 0 to 2 53 -1.


### Usage

This function takes an arbitrary number of comma-separated arguments and returns the result of a logical XOR operation on each pair of corresponding bits. For example, the result of the following function is 1 .

CODE

Copy

| makeresults | eval result = bit_xor(3, 2)


```spl

| makeresults | eval result = bit_xor(3, 2)

```


This is because the result of the bitwise XOR operation is 0001, which is the number 1. See the following table for more information about the sequence of operations in this bitwise function.




| Operation | Binary string | Result |
| --- | --- | --- |
| 3 | 0011 |  |
| 2 | 0010 |  |
| bit_xor(3, 2) | 0001 | 1 |



## bit_shift_left(&lt;value&gt;, &lt;shift_offset&gt;)


### Description

This logical left shift function takes two valid nonnegative integers as arguments and shifts the binary representation of the first integer over to the left by the specified shift offset amount. Shifting left drops the 53rd bit and appends a 0 to the binary representation of the input.

Both arguments must be in the range of 0 to 2 53 -1 or the operation returns null. All results are masked to stay below the 2 53 -1 limit in case of overflows.


### Usage

The shift offset is an integer that specifies the number of times the given integer is shifted to the left. When the bits in a binary digit are shifted to the left, the most-significant bit on the left side is lost and a 0 bit is inserted on the right side of the value. For example, the result of the following search is 4 .

CODE

Copy

| makeresults | eval result = bit_shift_left(2, 1)


```spl

| makeresults | eval result = bit_shift_left(2, 1)

```


This is because the decimal value of 0100 is 4. See the following table for more information about the sequence of operations in this bitwise function.


| Operation | Binary string | Result |
| --- | --- | --- |
| 2 | 0010 |  |
| bit_shift_left(2, 1) | 0100 | 4 |


Because only nonnegative integers in the range of 0 to 2 53 -1 are supported, if values in bit-shift functions are negative or greater than 2 53 -1, such as 2 53 , the function returns null. Also, if the shift offset is greater than 53 bits, the function returns 0. For example, consider the following search.

CODE

Copy

| makeresults | eval result = bit_shift_left(1, 53)


```spl

| makeresults | eval result = bit_shift_left(1, 53)

```


The search results look something like this:


| _time | result |
| --- | --- |
| 2022-08-22 13:39:24 | 0 |


Since the operation results in 54 bits, the 1 on the left drops off and is replaced with 53 zeros, and the value is truncated to 0 when displayed as a search result. After the most significant bit is lost, it is not possible to reverse the operation and recover that bit.

The following table provides examples of left-shift functions to help you understand the results. For the bit_shift_left(3, 52) function, notice that the result is truncated because the bit on the left that is in bold in the binary string is dropped.




| Operation | Binary string | Result |
| --- | --- | --- |
| 3 | 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000011 |  |
| bit_shift_left(3, 1) | 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000110 | 6 |
| bit_shift_left(3, 52) | 110000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 | 4503599627370496 |
| bit_shift_left(3, 57) | 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 | 0 |
| bit_shift_left(3, 253-1) | 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 | 0 |
| bit_shift_left(3, 253) |  | null |
| 67 | 00000000 00000000 00000000 00000000 00000000 00000000 00000000 01000011 |  |
| bit_shift_left(67, 1) | 00000000 00000000 00000000 00000000 00000000 00000000 00000000 10000110 | 134 |
| bit_shift_left(253, 1) |  | null |
| bit_shift_left(3, -2) |  | null |
| bit_shift_right(-3, 1) |  | null |



## bit_shift_right(&lt;value&gt;, &lt;shift_offset&gt;)


### Description

This logical right shift function takes two valid nonnegative integers as arguments and shifts the binary representation of the first integer over to the right by the specified shift offset amount. Shifting right drops the rightmost bit and prepends a 0 to the binary representation of the input.

Both arguments must be in the range of 0 to 2 53 -1 or the operation returns null. All results are masked to stay below the 2 53 -1 limit in case of overflows.


### Usage

The shift offset is an integer that specifies the number of times the given integer is shifted to the right. For example, the result of the following function is 2 .

CODE

Copy

| makeresults | eval result = bit_shift_right(4, 1)


```spl

| makeresults | eval result = bit_shift_right(4, 1)

```


This is because the binary representation of the decimal number 4 is 0100, which is 0010 when shifted left by 1. The decimal value of 0010 is 2.

Like the bit_shift_left function, the bit_shift_right function supports only nonnegative integers in the range of 0 to 2 53 -1. As a result, values in bit-shift operations that are negative or greater than 53 bits or 2 53 return null.


## Examples


### 1. Compare the results of bitwise functions

Consider the following search, which includes sequential bitwise AND, bitwise OR, and bitwise XOR functions.

CODE

Copy

| makeresults 
| eval AND_result = bit_and(4, 6), OR_result = bit_or(4, 6), XOR_result = bit_xor(4, 6)


```spl

| makeresults 
| eval AND_result = bit_and(4, 6), OR_result = bit_or(4, 6), XOR_result = bit_xor(4, 6)

```


The results look something like this:


| _time | AND_result | OR_result | XOR_result |
| --- | --- | --- | --- |
| 2022-09-02 13:44:21 | 4 | 6 | 2 |



### 2. Compare the results of bit shift functions

Consider the following search, which includes sequential logical left shift and logical right shift functions.

CODE

Copy

| makeresults 
| eval LEFT_result = bit_shift_left(2,1), RIGHT_result = bit_shift_right(2,1)


```spl

| makeresults 
| eval LEFT_result = bit_shift_left(2,1), RIGHT_result = bit_shift_right(2,1)

```


The results look something like this:


| _time | LEFT_result | RIGHT_result |
| --- | --- | --- |
| 2022-09-02 13:44:21 | 4 | 1 |



### 3. Get the binary representation of a value from another function

If you want to see your results in binary, you can use the tostring function to convert an argument to a binary string. See tostring(X,Y) .

The following search converts the result of the bit_shift_left(2,1) to its binary representation, which is 100 .

CODE

Copy

| makeresults 
| eval LEFT_result = bit_shift_left(2,1) 
| eval string = tostring(LEFT_result, "binary")


```spl

| makeresults 
| eval LEFT_result = bit_shift_left(2,1) 
| eval string = tostring(LEFT_result, "binary")

```


The results look something like this:


| _time | LEFT_result | string |
| --- | --- | --- |
| 2022-09-02 11:23:43 | 4 | 100 |



### 4. Apply a bitmask to limit the binary output

Consider this search, which uses the bit_not function to invert the bits in the result.

CODE

Copy

| makeresults 
| eval NOT_result = bit_not(9) 
| eval string = tostring(NOT_result, "binary")


```spl

| makeresults 
| eval NOT_result = bit_not(9) 
| eval string = tostring(NOT_result, "binary")

```


The results look something like this:


| _time | NOT_result | string |
| --- | --- | --- |
| 2022-09-02 09:52:12 | 9007199254740982 | 11111111111111111111111111111111111111111111111110110 |


The binary result in the string field has a lot of leading 1's that are in the way. To limit the output, add a bitmask that specifies that you want to see only three bits in the final result, like this:

CODE

Copy

| makeresults 
| eval NOT_result = bit_not(9, tonumber("111",2)) 
| eval string = tostring(NOT_result, "binary")


```spl

| makeresults 
| eval NOT_result = bit_not(9, tonumber("111",2)) 
| eval string = tostring(NOT_result, "binary")

```


The results look something like this:


| _time | NOT_result | string |
| --- | --- | --- |
| 2022-09-02 09:52:12 | 6 | 110 |


The result is the three-bit binary string 110 instead of a lot of 1s and 0s.


### 5. Using values that are outside the range of supported values

Look at what happens when you use a value as input in a function that falls outside of the range of supported values, which is 0 to 2 53 -1. In the following search, the input to the function is 2 53 -1, the max_supported_value , plus one.

CODE

Copy

| makeresults 
| eval max_supported_val = pow(2, 53)-1 
| eval result = bit_and(max_supported_val + 1, 1)


```spl

| makeresults 
| eval max_supported_val = pow(2, 53)-1 
| eval result = bit_and(max_supported_val + 1, 1)

```


The results look something like this:


| _time | max_supported_val |
| --- | --- |
| 2022-09-04 11:15:19 | 9007199254740991 |


The search returns only the value for max_supported_val and the value for the result field is not displayed. This is because result is outside of the supported range of values, so the function returns null. The function also returns null if you use negative values as input.


### 6. Update a binary string to set flags

You can run the following search to set multiple flags using a variable called flags .

CODE

Copy

| makeresults 
| eval flags = "00010", result = tonumber(flags, 2) 
| eval result = bit_or(result, tonumber("11001", 2)) 
| eval result = tostring(result, "binary")


```spl

| makeresults 
| eval flags = "00010", result = tonumber(flags, 2) 
| eval result = bit_or(result, tonumber("11001", 2)) 
| eval result = tostring(result, "binary")

```


The results look something like this:


| _time | flags | result |
| --- | --- | --- |
| 2022-09-05 12:19:03 | 00010 | 11011 |


You can see that the first, fourth, and fifth bits in 11011 are set.


### 7. Check whether a specific flag in a binary string is set

You can run the following search to check whether the third flag in a variable called flags is set.

CODE

Copy

| makeresults 
| eval flags = "00010", result = tonumber(flags, 2) 
| eval result = bit_and(result, 4) 
| eval result = if(result==0, "false", "true")


```spl

| makeresults 
| eval flags = "00010", result = tonumber(flags, 2) 
| eval result = bit_and(result, 4) 
| eval result = if(result==0, "false", "true")

```


The results look something like this:


| _time | flags | result |
| --- | --- | --- |
| 2022-09-05 09:13:22 | 00010 | 0 |


You can see that the third bit in the flag 00010 is set to 0.


### 8. Determine the matching bits in two binary strings

This search gives you the matching bits in two binary strings. Every bit that matches is displayed as 1 in the search results.

CODE

Copy

| makeresults 
| eval bin_number1 = "10011", bin_number2 = "10001", number1 = tonumber(bin_number1, 2), number2 = tonumber(bin_number2, 2) 
| eval matching_bits = bit_xor(number1, number2) 
| eval matching_bits = bit_not(matching_bits, tonumber("11111",2)) 
| eval matching_bits = tostring(matching_bits, "binary")


```spl

| makeresults 
| eval bin_number1 = "10011", bin_number2 = "10001", number1 = tonumber(bin_number1, 2), number2 = tonumber(bin_number2, 2) 
| eval matching_bits = bit_xor(number1, number2) 
| eval matching_bits = bit_not(matching_bits, tonumber("11111",2)) 
| eval matching_bits = tostring(matching_bits, "binary")

```


The results look something like this:


| _time | bin_number1 | bin_number2 | matching_bits | number1 | number2 |
| --- | --- | --- | --- | --- | --- |
| 2022-09-05 10:15:26 | 10011 | 10001 | 11101 | 19 | 17 |


You can see that the matching bits in 10011 and 10001 are the first, third, fourth, and last bits.


### 9. Append a bit flag to a binary string

The following search uses bit_shift_left and bit_or to add a bit flag of 1 to the binary string 10001 .

CODE

Copy

| makeresults 
| eval flags = "10001", result = tonumber(flags, 2), flag_bool = 1 
| eval result = bit_shift_left(result, 1) 
| eval result = bit_or(result, flag_bool) 
| eval result = tostring(result, "binary")


```spl

| makeresults 
| eval flags = "10001", result = tonumber(flags, 2), flag_bool = 1 
| eval result = bit_shift_left(result, 1) 
| eval result = bit_or(result, flag_bool) 
| eval result = tostring(result, "binary")

```


The results look something like this:


| _time | flags | flag_bool | result |
| --- | --- | --- | --- |
| 2022-09-05 12:19:20 | 10001 | 1 | 100011 |


You appended 10001 , so now the result is 100011 .


### 10. Use nested bitwise operations

You can nest multiple bitwise operations in a single search. For example, say you have a field called StreamId=0x12da3b7514f19ce7 . If you want to perform StreamId &gt;&gt; 8 & 0xFFFFFFFF , which right-shifts the StreamID by 8 and then performs a bitwise AND operation with 0xFFFFFFFF, you can run the following search:

CODE

Copy

| makeresults 
| eval streamId = tonumber("0xa3b7514f19ce7", 16), result = bit_and(bit_shift_right(streamId,8), tonumber("0xFFFFFFFF",16))


```spl

| makeresults 
| eval streamId = tonumber("0xa3b7514f19ce7", 16), result = bit_and(bit_shift_right(streamId,8), tonumber("0xFFFFFFFF",16))

```


The results look something like this:


| _time | result | StreamId |
| --- | --- | --- |
| 2022-09-05 11:21:02 | 1964306844 | 2880123815697639 |

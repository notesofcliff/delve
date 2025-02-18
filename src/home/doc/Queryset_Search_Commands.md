## Queryset Search Commands

The `qs_*` commands are designed to modify a Django QuerySet using methods on that QuerySet. These commands allow you to perform various operations such as filtering, annotating, aggregating, and more. The arguments for these commands are parsed in a special way to allow for complex expressions and function calls.

### Argument Parsing

When you use `qs_*` commands, the arguments are parsed into expressions that Django can understand. This means you can use functions and complex expressions to manipulate your data.

### Special Functions

There are some special functions that are particularly useful for searching, transforming, and visualizing your data:

- `F`: Represents the value of a model field. This is useful for referencing fields in expressions, such as when you want to compare or perform operations on fields.
  ```python
  qs_annotate new_field=F('field_name')
  ```
- `Value`: Wraps a value for use in expressions. This is useful for including static values in your expressions.
  ```python
  qs_annotate value_field=Value('static_value')
  ```
- `Q`: Encapsulates a collection of keyword arguments for complex queries. This is useful for building complex filter conditions.
  ```python
  qs_filter Q(field1__gt=10) || Q(field2__lt=5)
  ```
- `KT`: Represents a key transformation. This is useful for transforming keys in JSON fields.
  ```python
  qs_annotate transformed_key=KT('json_field__key__1__foobar')
  ```

#### Available Functions

Here are some functions you can use in your expressions:

- `Lower`: Converts a string to lowercase.
  ```python
  qs_annotate new_field=Lower(old_field)
  ```
- `Upper`: Converts a string to uppercase.
  ```python
  qs_annotate new_field=Upper(old_field)
  ```
- `Length`: Returns the length of a string.
  ```python
  qs_annotate length_field=Length(old_field)
  ```
- `Trim`: Trims whitespace from both ends of a string.
  ```python
  qs_annotate trimmed_field=Trim(old_field)
  ```
- `Cast`: Casts a value to a specified type.
  ```python
  qs_annotate casted_field=Cast(old_field,IntegerField)
  ```
- `Coalesce`: Returns the first non-null value in a list of expressions.
  ```python
  qs_annotate coalesced_field=Coalesce(field1, field2, Value('default'))
  ```
- `Concat`: Concatenates two or more strings.
  ```python
  qs_annotate concatenated_field=Concat(field1, Value(' '), field2)
  ```
- `Greatest`: Returns the greatest value from a list of expressions.
  ```python
  qs_annotate greatest_field=Greatest(field1, field2)
  ```
- `Least`: Returns the least value from a list of expressions.
  ```python
  qs_annotate least_field=Least(field1, field2)
  ```
- `LPad`: Pads a string on the left with a specified character.
  ```python
  qs_annotate lpad_field=LPad(field, 10, fill_text=Value('O'))
  ```
- `RPad`: Pads a string on the right with a specified character.
  ```python
  qs_annotate rpad_field=RPad(field, 10, fill_text=Value('O'))
  ```
- `LTrim`: Trims whitespace from the left end of a string.
  ```python
  qs_annotate ltrim_field=LTrim(field)
  ```
- `RTrim`: Trims whitespace from the right end of a string.
  ```python
  qs_annotate rtrim_field=RTrim(field)
  ```
- `Substr`: Returns a substring from a string.
  ```python
  qs_annotate substr_field=Substr(field, 1, 5)
  ```
- `Replace`: Replaces occurrences of a substring within a string.
  ```python
  qs_annotate replaced_field=Replace(field, Value('old'), Value('new'))
  ```
- `Reverse`: Reverses a string.
  ```python
  qs_annotate reversed_field=Reverse(field)
  ```
- `Now`: Returns the current date and time.
  ```python
  qs_annotate now_field=Now()
  ```
- `TruncDate`: Truncates a date to the specified precision.
  ```python
  qs_annotate trunc_date_field=TruncDate(field)
  ```
- `TruncMonth`: Truncates a date to the month.
  ```python
  qs_annotate trunc_month_field=TruncMonth(field)
  ```
- `TruncYear`: Truncates a date to the year.
  ```python
  qs_annotate trunc_year_field=TruncYear(field)
  ```
- `StrIndex`: Returns the index of a substring within a string.
  ```python
  qs_annotate str_index_field=StrIndex(field, Value('substring'))
  ```
- `Abs`: Returns the absolute value of a number.
  ```python
  qs_annotate abs_field=Abs(field)
  ```
- `ATan2`: Returns the arctangent of two numbers.
  ```python
  qs_annotate atan2_field=ATan2(field1, field2)
  ```
- `Ceil`: Returns the smallest integer greater than or equal to a number.
  ```python
  qs_annotate ceil_field=Ceil(field)
  ```
- `Cos`: Returns the cosine of a number.
  ```python
  qs_annotate cos_field=Cos(field)
  ```
- `Cot`: Returns the cotangent of a number.
  ```python
  qs_annotate cot_field=Cot(field)
  ```
- `Degrees`: Converts radians to degrees.
  ```python
  qs_annotate degrees_field=Degrees(field)
  ```
- `Exp`: Returns the exponential of a number.
  ```python
  qs_annotate exp_field=Exp(field)
  ```
- `Floor`: Returns the largest integer less than or equal to a number.
  ```python
  qs_annotate floor_field=Floor(field)
  ```
- `Ln`: Returns the natural logarithm of a number.
  ```python
  qs_annotate ln_field=Ln(field)
  ```
- `Log`: Returns the logarithm of a number.
  ```python
  qs_annotate log_field=Log(field)
  ```
- `Mod`: Returns the remainder of a division.
  ```python
  qs_annotate mod_field=Mod(field1, field2)
  ```
- `Pi`: Returns the value of pi.
  ```python
  qs_annotate pi_field=Pi()
  ```
- `Power`: Returns a number raised to a power.
  ```python
  qs_annotate power_field=Power(field, 2)
  ```
- `Radians`: Converts degrees to radians.
  ```python
  qs_annotate radians_field=Radians(field)
  ```
- `Round`: Rounds a number to the nearest integer.
  ```python
  qs_annotate round_field=Round(field)
  ```
- `Sign`: Returns the sign of a number.
  ```python
  qs_annotate sign_field=Sign(field)
  ```
- `Sin`: Returns the sine of a number.
  ```python
  qs_annotate sin_field=Sin(field)
  ```
- `Sqrt`: Returns the square root of a number.
  ```python
  qs_annotate sqrt_field=Sqrt(field)
  ```
- `Tan`: Returns the tangent of a number.
  ```python
  qs_annotate tan_field=Tan(field)
  ```
- `Trunc`: Truncates a date to the specified precision. ()
  ```python
  qs_annotate trunc_field=Trunc(field,kind='minute')
  ```
- `Extract`: Extracts a part of a date.
  ```python
  qs_annotate extract_field=Extract(field, 'year')
  ```
- `ExtractDay`: Extracts the day from a date.
  ```python
  qs_annotate extract_day_field=ExtractDay(field)
  ```
- `ExtractHour`: Extracts the hour from a date.
  ```python
  qs_annotate extract_hour_field=ExtractHour(field)
  ```
- `ExtractMinute`: Extracts the minute from a date.
  ```python
  qs_annotate extract_minute_field=ExtractMinute(field)
  ```
- `ExtractMonth`: Extracts the month from a date.
  ```python
  qs_annotate extract_month_field=ExtractMonth(field)
  ```
- `ExtractQuarter`: Extracts the quarter from a date.
  ```python
  qs_annotate extract_quarter_field=ExtractQuarter(field)
  ```
- `ExtractSecond`: Extracts the second from a date.
  ```python
  qs_annotate extract_second_field=ExtractSecond(field)
  ```
- `ExtractWeek`: Extracts the week from a date.
  ```python
  qs_annotate extract_week_field=ExtractWeek(field)
  ```
- `ExtractWeekDay`: Extracts the weekday from a date.
  ```python
  qs_annotate extract_weekday_field=ExtractWeekDay(field)
  ```
- `ExtractYear`: Extracts the year from a date.
  ```python
  qs_annotate extract_year_field=ExtractYear(field)
  ```

#### Aggregation Functions

You can also use these aggregation functions in your expressions:

- `Sum`: Returns the sum of the values.
  ```python
  qs_aggregate total=Sum(field)
  ```
- `Avg`: Returns the average of the values.
  ```python
  qs_aggregate average=Avg(field)
  ```
- `Count`: Returns the count of the values.
  ```python
  qs_aggregate count=Count(field)
  ```
- `Max`: Returns the maximum value.
  ```python
  qs_aggregate max_value=Max(field)
  ```
- `Min`: Returns the minimum value.
  ```python
  qs_aggregate min_value=Min(field)
  ```
- `StdDev`: Returns the standard deviation of the values.
  ```python
  qs_aggregate stddev=StdDev(field)
  ```
- `Variance`: Returns the variance of the values.
  ```python
  qs_aggregate variance=Variance(field)
  ```

#### Example Usages

Here are some example usages of the `qs_*` commands, starting with the `search` command and using multiple `qs_*` commands to manipulate the result set.

```bash
# Search for events and annotate them with additional fields
search field1=value1 | qs_annotate new_field1=Lower(old_field1) new_field2=Concat(field2, Value('suffix'))

# Search for events, filter them, and then count the results
search field1=value1 | qs_filter field2__gt=10 | qs_count

# Search for events, aggregate them, and then annotate the results
search field1=value1 | qs_aggregate total=Sum(field2) average=Avg(field2) | qs_annotate new_field=F('total') + F('average')

# Search for events and retrieve dates from the queryset
search field1=value1 | qs_dates field=date_field kind=month order=ASC
```

### Notes

The `qs_*` commands use Django's ORM methods to perform the specified operations on the QuerySet. The arguments are parsed into expressions that Django can understand, allowing for complex expressions and function calls to be used in the arguments. This provides powerful and flexible ways to manipulate the result set.

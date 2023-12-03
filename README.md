# PyStream

A simple imperfect implementation of streaming operations in Python using [generators](https://wiki.python.org/moin/Generators) inspired by [fs2](https://fs2.io/#/).

### Quick Start: FizzBuzz

#### Problem
Given an integer n, return a string array answer (1-indexed) where:

- answer[i] == "FizzBuzz" if i is divisible by 3 and 5.
- answer[i] == "Fizz" if i is divisible by 3.
- answer[i] == "Buzz" if i is divisible by 5.
- answer[i] == i (as a string) if none of the above conditions are true.

#### Solution with a Single Function and Stream

Streams are a stream of values in which operations can be commited. We can take the values and pass them through the solution as a function.

```python
from PyStream.stream import Stream

def FizzBuzz(n):
    """
    Solution to FizzBuzz
    """
    if n % 3 == 0 and n % 5 == 0:
        return "FizzBuzz"
    elif n % 3 == 0:
        return "Fizz"
    elif n % 5 == 0:
        return "Buzz"
    return str(n)

# Create Stream of values to test
s = Stream(1, 3, 5, 15, 16)

# Run Stream through function
s = s.through(FizzBuzz)

print(s.to_list()) # ['1', 'Fizz', 'Buzz', 'FizzBuzz', '16']
```

#### Solution with Multiple Functions and Streams
The below snippet shows a solution using multiple functions, a Pipe, and a Stream. The solution is more complex than a single function, but offers customization.


```python
from PyStream.stream import Stream, Pipe

# Functions for testing requirements
fizz = lambda x: "Fizz" if isinstance(x, int) and x % 3 == 0 else x
buzz = lambda x: "Buzz" if isinstance(x, int) and x % 5 == 0 else x
fizzbuzz = lambda x: "FizzBuzz" if isinstance(x, int) and x % 3 == 0 and x % 5 == 0 else x

# Create Pipe and make FizzBuzz using single functions
p = Pipe()
p_fizzbuzz = p.through(fizzbuzz).through(buzz).through(fizz).through(str)

# Create Stream of values to test
s = Stream(1, 3, 5, 15, 16)

# Run Stream through Pipe and convert all values to strings
s = s.through(p_fizzbuzz)

print(s.to_list()) # ['1', 'Fizz', 'Buzz', 'FizzBuzz', '16']
```

# Usage

### Initialization

PyStreams are wrappers for Python [generators](https://wiki.python.org/moin/Generators). Streams emulate generators in many ways. They have two primary methods of initialization. One way is can be treated as any other iterable data type and have values passed directly, unlike generators.

```python
from PyStream.stream import Stream

# Initialize a Stream
s = Stream(0, 1, 2, 3, 4)

# Iterate through a Stream
for item in s:
    print(item)

# 0
# 1
# . . .
# 4
```

The second way they can be initialized is via passing a single generator, interator, or any other iterable as the only argument in initialization. This enables lazy evaluation to be maintained when working with generators.

```python
from PyStream.stream import Stream

# Initialize a Stream with an iterable
s1 = Stream([0, 1, 2, 3, 4])

# Initialize a Stream with an generator
s2 = Stream((x for x in [0, 1, 2, 3, 4]))

# Iterate through the Streams
for i1, i2 in zip(s1, s2):
    print(i1, i2)

# prints
# 0 0
# 1 1
# . . .
# 4 4
```

### Compiling Streams

A Stream acts as a generator when being compiled. It should be noted that like generators all Streams composed of a generator source will share state with the parent. If a parent is iterated the Stream will share that state. The generator base means that they can be iterated through but not indexed. The method works with the `next()` function to get the next value.

```python
from PyStream.stream import Stream

# Initialize a Stream with an iterable
s = Stream([0, 1, 2, 3, 4])

# Iterate via next()
i1 = next(s)
print("Fetched via next():", i1)

# Iterate through the Steam via for
for item in s:
    print("Fetched via for(): ", item)

# prints
# Fetched via next(): 0
# Fetched via for():  1
# . . .
# Fetched via for():  4
```

Along with the builtin methods for iteration Stream has custom methods for compiling the Stream. These include the `to_list()`, `drain()`, and `take()` methods.

#### to_list
`to_list()` will execute the equivalent of running `list()` or a for comprehension on the Stream. It compiles the Stream into a list by iterating of every value.

```python
from PyStream.stream import Stream

# Initialize a Stream with an iterable
s = Stream([0, 1, 2, 3, 4])

# Compile with to_list()
print(s.to_list()) # prints [0, 1, 2, 3, 4]
```

#### drain()
`drain()` compiles the entire Stream by evaluating every iteration but will throw away the output. While this seems like a pointless way to evaluate a Stream in current examples it can be used to evaluate a Stream purely for side effects. 
```python
from PyStream.stream import Stream

# Initialize a Stream with an iterable
s = Stream([0, 1, 2, 3, 4])

# Compile with drain()
print(s.drain()) # prints None
```

#### take()
`take()` works differently than `to_list()` and `drain()` as it does not compile the entire Stream. It instead will evaluate *n* values and return them as a list. This allows for compiling multiple values at once without the need for iteration or compiling the entire Stream.
```python
from PyStream.stream import Stream

# Initialize a Stream with an iterable
s = Stream([0, 1, 2, 3, 4])

# Compile with take()
print(s.take(2)) # prints [0, 1]
print(s.take(2)) # prints [2, 3]
print(s.take(2)) # prints [4]
```

## Operations

Streams offer a few handy operations for compiling generators in custom ways. The true value in Streams is their intuitive system of chaining operations together. The most simple of these methods is `through()`.

#### through()
`through()` is an operation that accepts a function and will execute the function on each element when evaluated. It is equivalent to `map()` in the standard library. The use of operations returns the same Steam with an appended operation on evaluation. The child Stream will maintain the same state as the Parent due to the nature of generators discussed in the **Compiling Streams** section.
```python
from PyStream.stream import Stream

def add_10(n):
    """
    Example function that adds 10 to a number.
    """
    return n + 10

# Initialize a Stream with an iterable
s = Stream([0, 1, 2, 3, 4])

# Stream the values through the add_10() function
s = s.through(add_10)

# Compile with to_list()
print(s.to_list()) # prints [10, 11, 12, 13, 14]
```

All operations can chained to create a pipeline containing multiple operations. 
```python
from PyStream.stream import Stream

def add_10(n):
    """
    Example function that adds 10 to a number.
    """
    return n + 10

# Initialize a Stream with an iterable
s = Stream([0, 1, 2, 3, 4])

# Stream the values through the add_10() function
s = s.through(add_10).through(add_10)

# Compile with to_list()
print(s.to_list()) # prints [20, 21, 22, 23, 24]
```

#### filter()
Like through is an equivalent to `map()` in the standard library `filter()` is equivalent to `filter()` in the standard library. It can be given a statement to evaluate True or False and will filter if True.
```python
from PyStream.stream import Stream

def add_10(n):
    """
    Example function that adds 10 to a number.
    """
    return n + 10

def is_even(n):
    """
    Example function that returns if an even number.
    """
    return n % 2 == 0

# Initialize a Stream with an iterable
s = Stream([0, 1, 2, 3, 4])

# Stream the values through the add_10() function
s = s.through(add_10).filter(is_even)

# Compile with to_list()
print(s.to_list()) # prints [20, 22, 24]
```

### Chunking

A chunk is standard library tuple with a builtin `map()` function. They are initialized the same as a tuple. The `map()` function can then be called on a chunk which will return a compiled chunk with the operation evaluated on each item.

```python
from PyStream.stream import Stream

def add_10(n):
    """
    Example function that adds 10 to a number.
    """
    return n + 10

# Initialize a Chunk
c = Chunk(0, 1, 2, 3, 4)

# Print the base chunk
print(c) # prints (0, 1, 2, 3, 4)

# Map add_10 function to the chunk
c = c.map(add_10)

# Print the resulting chunk
print(c) # prints (10, 11, 12, 13, 14)
```

#### chunk()

Streams by default will execute a operations on each single value passed through. This may be inefficent in certain cases. When batching is desirable Streams may be chunked in batches of `n` items. Operations can then be executed on entire chunks or mapped onto each element of a chunk.
```python
from PyStream.stream import Stream

# Initialize a Stream with an iterable
s = Stream([0, 1, 2, 3, 4])

# Chunk a Stream into batches of 2
s = s.chunk(2)

# Compile with to_list()
print(s.to_list()) # prints [(0, 1), (2, 3), (4)]
```

#### through_map_on_chunk()

Operations like `through()` and `filter()` now will require functions designed to accept chunks. In cases where a function should be mapped onto a chunk the function `through_map_on_chunk()` can be used. This is an easy way to map on to chunks rather than rewriting a function and will become very useful for general use Pipes later.
```python
from PyStream.stream import Stream

def add_10(n):
    """
    Example function that adds 10 to a number.
    """
    return n + 10

# Initialize a Stream with an iterable
s = Stream([0, 1, 2, 3, 4])

# Chunk a Stream into batches of 2 and add_10
s = s.chunk(2).through_map_on_chunk(add_10)

# Compile with to_list()
print(s.to_list()) # prints [(10, 11), (12, 13), (14)]
```

### Forking

Forking a stream acts like a combination of `filter()` and `through()`. It will execute a given action if a given condition is true. Otherwise it will pass the value unchanged. This enables branching of the Stream into more of a DAG than a single sequence of operations.

```python
from PyStream.stream import Stream, Pipe

def add_10(n):
    """
    Example function that adds 10 to a number.
    """
    return n + 10

def times_neg1(n):
    """
    Example function that multiplies by -1 to a number.
    """
    return n * -1

def is_even(n):
    """
    Example function that returns if an even number.
    """
    return n % 2 == 0

# Initialize a pipe
p = Pipe().through(times_neg1)

# Initialize a Stream with an iterable
s = Stream([0, 1, 2, 3, 4])

# Stream the values through a fork that multiplies evens by -1 then add 10 to all.
s = s.fork(is_even, p).through(add_10)

# Compile with to_list()
print(s.to_list()) # prints [10, 11, 8, 13, 6]
```

# Pipes

Streams contain many operations for constructing data streams with ease based on generators. Pipes act as reusable code for Streams. They enable the use of all operations without a predefined source. They cannot use the compilation methods. A Pipe is a Stream without a source.

### Initialization

A Pipe is initialized as a blank slate. It will simply act as an identity function when used. When the Pipe is called it takes the arguments the same as initializing a Stream.
```python
from PyStream.stream import Pipe

# Create pipe
p = Pipe()

# Add source to pipe
s = p(0, 1, 2, 3, 4)

# Compile with to_list()
print(s.to_list()) # prints [0, 1, 2, 3, 4]
```

## Operations

Pipes can be used for any operation a Stream would. This includes `through()`, `filter()`, `chunk()`, and `through_map_on_chunk()`.
```python
from PyStream.stream import Pipe

def add_10(n):
    """
    Example function that adds 10 to a number.
    """
    return n + 10

# Create pipe
p = Pipe()

# Add add_10 operation to be evaluated
p = p.through(add_10)

# Add source to pipe
s = p(0, 1, 2, 3, 4)

# Compile with to_list()
print(s.to_list()) # prints [10, 11, 12, 13, 14]
```

Streams can be used a source for a Pipe. This can be done via passing them through the Pipe as a source or using a pipe as an operation in though for a Stream. 
```python
from PyStream.stream import Stream, Pipe

def add_10(n):
    """
    Example function that adds 10 to a number.
    """
    return n + 10

# Create a Stream
s = Stream(0, 1, 2, 3, 4)

# Create pipe
p = Pipe()

# Add add_10 operation to be evaluated
p = p.through_map_on_chunk(add_10)

# Put Stream through Pipe
s = s.chunk(2).through(p)

# Compile with to_list()
print(s.to_list()) # prints [(10, 11), (12, 13), (14)]
```

The above example shows a use case in which the pipe can be used on single values or chunks to evaluate into the same values in stream or batch format. Pipes are simply reusable Stream operations.

## ToDo
- [ ] Steam is generator based meaning each child of a parent after a transformation retains the same source with a shared state. This is not an issue if known by the user, but can cause bugs if parents and children are both used.
- [ ] Add more sources like cli.
- [ ] Add tests for chunks.

```python
from PyStream.stream import Stream, Pipe

# Functions for testing requirements
fizz = lambda x: "Fizz" if isinstance(x, int) and x % 3 == 0 else x
buzz = lambda x: "Buzz" if isinstance(x, int) and x % 5 == 0 else x
fizzbuzz = lambda x: "FizzBuzz" if isinstance(x, int) and x % 3 == 0 and x % 5 == 0 else x

# Create Pipe and make FizzBuzz using single functions
p = Pipe()
p_fizzbuzz = p.through(fizzbuzz).through(buzz).through(fizz).through(str)

# Create Stream of values to test
s = Stream(1, 3, 5, 15, 16)

# Run Stream through Pipe and convert all values to strings
s = s.through(p_fizzbuzz)

print(s.to_list()) # ['1', 'Fizz', 'Buzz', 'FizzBuzz', '16']
```

# Usage

### Initialization

PyStreams are wrappers for Python [generators](https://wiki.python.org/moin/Generators). Streams emulate generators in many ways. They have two primary methods of initialization. One way is can be treated as any other iterable data type and have values passed directly, unlike generators.

```python
from PyStream.stream import Stream

# Initialize a Stream
s = Stream(0, 1, 2, 3, 4)

# Iterate through a Stream
for item in s:
    print(item)

# 0
# 1
# . . .
# 4
```

The second way they can be initialized is via passing a single generator, interator, or any other iterable as the only argument in initialization. This enables lazy evaluation to be maintained when working with generators.

```python
from PyStream.stream import Stream

# Initialize a Stream with an iterable
s1 = Stream([0, 1, 2, 3, 4])

# Initialize a Stream with an generator
s2 = Stream((x for x in [0, 1, 2, 3, 4]))

# Iterate through the Streams
for i1, i2 in zip(s1, s2):
    print(i1, i2)

# prints
# 0 0
# 1 1
# . . .
# 4 4
```

### Compiling Streams

A Stream acts as a generator when being compiled. It should be noted that like generators all Streams composed of a generator source will share state with the parent. If a parent is iterated the Stream will share that state. The generator base means that they can be iterated through but not indexed. The method works with the `next()` function to get the next value.

```python
from PyStream.stream import Stream

# Initialize a Stream with an iterable
s = Stream([0, 1, 2, 3, 4])

# Iterate via next()
i1 = next(s)
print("Fetched via next():", i1)

# Iterate through the Steam via for
for item in s:
    print("Fetched via for(): ", item)

# prints
# Fetched via next(): 0
# Fetched via for():  1
# . . .
# Fetched via for():  4
```

Along with the builtin methods for iteration Stream has custom methods for compiling the Stream. These include the `to_list()`, `drain()`, and `take()` methods.

#### to_list
`to_list()` will execute the equivalent of running `list()` or a for comprehension on the Stream. It compiles the Stream into a list by iterating of every value.

```python
from PyStream.stream import Stream

# Initialize a Stream with an iterable
s = Stream([0, 1, 2, 3, 4])

# Compile with to_list()
print(s.to_list()) # prints [0, 1, 2, 3, 4]
```

#### drain()
`drain()` compiles the entire Stream by evaluating every iteration but will throw away the output. While this seems like a pointless way to evaluate a Stream in current examples it can be used to evaluate a Stream purely for side effects. 
```python
from PyStream.stream import Stream

# Initialize a Stream with an iterable
s = Stream([0, 1, 2, 3, 4])

# Compile with drain()
print(s.drain()) # prints None
```

#### take()
`take()` works differently than `to_list()` and `drain()` as it does not compile the entire Stream. It instead will evaluate *n* values and return them as a list. This allows for compiling multiple values at once without the need for iteration or compiling the entire Stream.
```python
from PyStream.stream import Stream

# Initialize a Stream with an iterable
s = Stream([0, 1, 2, 3, 4])

# Compile with take()
print(s.take(2)) # prints [0, 1]
print(s.take(2)) # prints [2, 3]
print(s.take(2)) # prints [4]
```

## Operations

Streams offer a few handy operations for compiling generators in custom ways. The true value in Streams is their intuitive system of chaining operations together. The most simple of these methods is `through()`.

#### through()
`through()` is an operation that accepts a function and will execute the function on each element when evaluated. It is equivalent to `map()` in the standard library. The use of operations returns the same Steam with an appended operation on evaluation. The child Stream will maintain the same state as the Parent due to the nature of generators discussed in the **Compiling Streams** section.
```python
from PyStream.stream import Stream

def add_10(n):
    """
    Example function that adds 10 to a number.
    """
    return n + 10

# Initialize a Stream with an iterable
s = Stream([0, 1, 2, 3, 4])

# Stream the values through the add_10() function
s = s.through(add_10)

# Compile with to_list()
print(s.to_list()) # prints [10, 11, 12, 13, 14]
```

All operations can chained to create a pipeline containing multiple operations. 
```python
from PyStream.stream import Stream

def add_10(n):
    """
    Example function that adds 10 to a number.
    """
    return n + 10

# Initialize a Stream with an iterable
s = Stream([0, 1, 2, 3, 4])

# Stream the values through the add_10() function
s = s.through(add_10).through(add_10)

# Compile with to_list()
print(s.to_list()) # prints [20, 21, 22, 23, 24]
```

#### filter()
Like through is an equivalent to `map()` in the standard library `filter()` is equivalent to `filter()` in the standard library. It can be given a statement to evaluate True or False and will filter if True.
```python
from PyStream.stream import Stream

def add_10(n):
    """
    Example function that adds 10 to a number.
    """
    return n + 10

def is_even(n):
    """
    Example function that returns if an even number.
    """
    return n % 2 == 0

# Initialize a Stream with an iterable
s = Stream([0, 1, 2, 3, 4])

# Stream the values through the add_10() function
s = s.through(add_10).filter(is_even)

# Compile with to_list()
print(s.to_list()) # prints [20, 22, 24]
```

### Chunking

A chunk is standard library tuple with a builtin `map()` function. They are initialized the same as a tuple. The `map()` function can then be called on a chunk which will return a compiled chunk with the operation evaluated on each item.

```python
from PyStream.stream import Stream

def add_10(n):
    """
    Example function that adds 10 to a number.
    """
    return n + 10

# Initialize a Chunk
c = Chunk(0, 1, 2, 3, 4)

# Print the base chunk
print(c) # prints (0, 1, 2, 3, 4)

# Map add_10 function to the chunk
c = c.map(add_10)

# Print the resulting chunk
print(c) # prints (10, 11, 12, 13, 14)
```

#### chunk()

Streams by default will execute a operations on each single value passed through. This may be inefficent in certain cases. When batching is desirable Streams may be chunked in batches of `n` items. Operations can then be executed on entire chunks or mapped onto each element of a chunk.
```python
from PyStream.stream import Stream

# Initialize a Stream with an iterable
s = Stream([0, 1, 2, 3, 4])

# Chunk a Stream into batches of 2
s = s.chunk(2)

# Compile with to_list()
print(s.to_list()) # prints [(0, 1), (2, 3), (4)]
```

#### through_map_on_chunk()

Operations like `through()` and `filter()` now will require functions designed to accept chunks. In cases where a function should be mapped onto a chunk the function `through_map_on_chunk()` can be used. This is an easy way to map on to chunks rather than rewriting a function and will become very useful for general use Pipes later.
```python
from PyStream.stream import Stream

def add_10(n):
    """
    Example function that adds 10 to a number.
    """
    return n + 10

# Initialize a Stream with an iterable
s = Stream([0, 1, 2, 3, 4])

# Chunk a Stream into batches of 2 and add_10
s = s.chunk(2).through_map_on_chunk(add_10)

# Compile with to_list()
print(s.to_list()) # prints [(10, 11), (12, 13), (14)]
```

### Forking

Forking a stream acts like a combination of `filter()` and `through()`. It will execute a given action if a given condition is true. Otherwise it will pass the value unchanged. This enables branching of the Stream into more of a DAG than a single sequence of operations.

```python
from PyStream.stream import Stream, Pipe

def add_10(n):
    """
    Example function that adds 10 to a number.
    """
    return n + 10

def times_neg1(n):
    """
    Example function that multiplies by -1 to a number.
    """
    return n * -1

def is_even(n):
    """
    Example function that returns if an even number.
    """
    return n % 2 == 0

# Initialize a pipe
p = Pipe().through(times_neg1)

# Initialize a Stream with an iterable
s = Stream([0, 1, 2, 3, 4])

# Stream the values through a fork that multiplies evens by -1 then add 10 to all.
s = s.fork(is_even, p).through(add_10)

# Compile with to_list()
print(s.to_list()) # prints [10, 11, 8, 13, 6]
```

# Pipes

Streams contain many operations for constructing data streams with ease based on generators. Pipes act as reusable code for Streams. They enable the use of all operations without a predefined source. They cannot use the compilation methods. A Pipe is a Stream without a source.

### Initialization

A Pipe is initialized as a blank slate. It will simply act as an identity function when used. When the Pipe is called it takes the arguments the same as initializing a Stream.
```python
from PyStream.stream import Pipe

# Create pipe
p = Pipe()

# Add source to pipe
s = p(0, 1, 2, 3, 4)

# Compile with to_list()
print(s.to_list()) # prints [0, 1, 2, 3, 4]
```

## Operations

Pipes can be used for any operation a Stream would. This includes `through()`, `filter()`, `chunk()`, and `through_map_on_chunk()`.
```python
from PyStream.stream import Pipe

def add_10(n):
    """
    Example function that adds 10 to a number.
    """
    return n + 10

# Create pipe
p = Pipe()

# Add add_10 operation to be evaluated
p = p.through(add_10)

# Add source to pipe
s = p(0, 1, 2, 3, 4)

# Compile with to_list()
print(s.to_list()) # prints [10, 11, 12, 13, 14]
```

Streams can be used a source for a Pipe. This can be done via passing them through the Pipe as a source or using a pipe as an operation in though for a Stream. 
```python
from PyStream.stream import Stream, Pipe

def add_10(n):
    """
    Example function that adds 10 to a number.
    """
    return n + 10

# Create a Stream
s = Stream(0, 1, 2, 3, 4)

# Create pipe
p = Pipe()

# Add add_10 operation to be evaluated
p = p.through_map_on_chunk(add_10)

# Put Stream through Pipe
s = s.chunk(2).through(p)

# Compile with to_list()
print(s.to_list()) # prints [(10, 11), (12, 13), (14)]
```

The above example shows a use case in which the pipe can be used on single values or chunks to evaluate into the same values in stream or batch format. Pipes are simply reusable Stream operations.

## ToDo
- [ ] Steam is generator based meaning each child of a parent after a transformation retains the same source with a shared state. This is not an issue if known by the user, but can cause bugs if parents and children are both used.
- [ ] Add more sources like cli.
- [ ] Add tests for chunks.

# 從 chap11.ipynb 轉換而來
# 使用 ipynb_to_py.py 腳本自動轉換

# In[0]:
# You can order print and ebook versions of *Think Python 3e* from
# [Bookshop.org](https://bookshop.org/a/98697/9781098155438) and
# [Amazon](https://www.amazon.com/_/dp/1098155432?smid=ATVPDKIKX0DER&_encoding=UTF8&tag=oreilly20-20&_encoding=UTF8&tag=greenteapre01-20&linkCode=ur2&linkId=e2a529f94920295d27ec8a06e757dc7c&camp=1789&creative=9325).

# In[1]:
from os.path import basename, exists

def download(url):
    filename = basename(url)
    if not exists(filename):
        from urllib.request import urlretrieve

        local, _ = urlretrieve(url, filename)
        print("Downloaded " + str(local))
    return filename

download('https://github.com/AllenDowney/ThinkPython/raw/v3/thinkpython.py');
download('https://github.com/AllenDowney/ThinkPython/raw/v3/diagram.py');

import thinkpython

# In[2]:
# # Tuples
# 
# This chapter introduces one more built-in type, the tuple, and then shows how lists, dictionaries, and tuples work together.
# It also presents tuple assignment and a useful feature for functions with variable-length argument lists: the packing and unpacking operators.
# 
# In the exercises, we'll use tuples, along with lists and dictionaries, to solve more word puzzles and implement efficient algorithms.
# 
# One note: There are two ways to pronounce "tuple".
# Some people say "tuh-ple", which rhymes with "supple".
# But in the context of programming, most people say "too-ple", which rhymes with "quadruple".

# In[3]:
# ## Tuples are like lists
# 
# A tuple is a sequence of values. The values can be any type, and they are indexed by integers, so tuples are a lot like lists.
# The important difference is that tuples are immutable.
# 
# To create a tuple, you can write a comma-separated list of values.

# In[4]:
t = 'l', 'u', 'p', 'i', 'n'
type(t)

# In[5]:
# Although it is not necessary, it is common to enclose tuples in parentheses.

# In[6]:
t = ('l', 'u', 'p', 'i', 'n')
type(t)

# In[7]:
# To create a tuple with a single element, you have to include a final comma.

# In[8]:
t1 = 'p',
type(t1)

# In[9]:
# A single value in parentheses is not a tuple.

# In[10]:
t2 = ('p')
type(t2)

# In[11]:
# Another way to create a tuple is the built-in function `tuple`. With no
# argument, it creates an empty tuple.

# In[12]:
t = tuple()
t

# In[13]:
# If the argument is a sequence (string, list or tuple), the result is a
# tuple with the elements of the sequence.

# In[14]:
t = tuple('lupin')
t

# In[15]:
# Because `tuple` is the name of a built-in function, you should avoid using it as a variable name.
# 
# Most list operators also work with tuples.
# For example, the bracket operator indexes an element.

# In[16]:
t[0]

# In[17]:
# And the slice operator selects a range of elements.

# In[18]:
t[1:3]

# In[19]:
# The `+` operator concatenates tuples.

# In[20]:
tuple('lup') + ('i', 'n')

# In[21]:
# And the `*` operator duplicates a tuple a given number of times.

# In[22]:
tuple('spam') * 2 

# In[23]:
# The `sorted` function works with tuples -- but the result is a list, not a tuple.

# In[24]:
sorted(t)

# In[25]:
# The `reversed` function also works with tuples.

# In[26]:
reversed(t)

# In[27]:
# The result is a `reversed` object, which we can convert to a list or tuple.

# In[28]:
tuple(reversed(t))

# In[29]:
# Based on the examples so far, it might seem like tuples are the same as lists.

# In[30]:
# ## But tuples are immutable
# 
# If you try to modify a tuple with the bracket operator, you get a `TypeError`.

# In[31]:
%%expect TypeError
t[0] = 'L'

# In[32]:
# And tuples don't have any of the methods that modify lists, like `append` and `remove`.

# In[33]:
%%expect AttributeError

t.remove('l')

# In[34]:
# Recall that an "attribute" is a variable or method associated with an object -- this error message means that tuples don't have a method named `remove`.
# 
# Because tuples are immutable, they are hashable, which means they can be used as keys in a dictionary.
# For example, the following dictionary contains two tuples as keys that map to integers.

# In[35]:
d = {}
d[1, 2] = 3
d[3, 4] = 7

# In[36]:
# We can look up a tuple in a dictionary like this:

# In[37]:
d[1, 2]

# In[38]:
# Or if we have a variable that refers to a tuple, we can use it as a key.

# In[39]:
t = (3, 4)
d[t]

# In[40]:
# Tuples can also appear as values in a dictionary.

# In[41]:
t = tuple('abc')
d = {'key': t}
d

# In[42]:
# ## Tuple assignment
# 
# You can put a tuple of variables on the left side of an assignment, and a tuple of values on the right.

# In[43]:
a, b = 1, 2

# In[44]:
# The values are assigned to the variables from left to right -- in this example, `a` gets the value `1` and `b` gets the value `2`.
# We can display the results like this:

# In[45]:
a, b

# In[46]:
# More generally, if the left side of an assignment is a tuple, the right side can be any kind of sequence -- string, list or tuple. 
# For example, to split an email address into a user name and a domain, you could write:

# In[47]:
email = 'monty@python.org'
username, domain = email.split('@')

# In[48]:
# The return value from `split` is a list with two elements -- the first element is assigned to `username`, the second to `domain`.

# In[49]:
username, domain

# In[50]:
# The number of variables on the left and the number of values on the
# right have to be the same -- otherwise you get a `ValueError`.

# In[51]:
%%expect ValueError
a, b = 1, 2, 3

# In[52]:
# Tuple assignment is useful if you want to swap the values of two variables.
# With conventional assignments, you have to use a temporary variable, like this:

# In[53]:
temp = a
a = b
b = temp

# In[54]:
# That works, but with tuple assignment we can do the same thing without a temporary variable.

# In[55]:
a, b = b, a

# In[56]:
# This works because all of the expressions on the right side are evaluated before any of the assignments.
# 
# We can also use tuple assignment in a `for` statement.
# For example, to loop through the items in a dictionary, we can use the `items` method.

# In[57]:
d = {'one': 1, 'two': 2}

for item in d.items():
    key, value = item
    print(key, '->', value)

# In[58]:
# Each time through the loop, `item` is assigned a tuple that contains a key and the corresponding value.
# 
# We can write this loop more concisely, like this:

# In[59]:
for key, value in d.items():
    print(key, '->', value)

# In[60]:
# Each time through the loop, a key and the corresponding value are assigned directly to `key` and `value`.

# In[61]:
# ## Tuples as return values
# 
# Strictly speaking, a function can only return one value, but if the
# value is a tuple, the effect is the same as returning multiple values.
# For example, if you want to divide two integers and compute the quotient
# and remainder, it is inefficient to compute `x//y` and then `x%y`. It is
# better to compute them both at the same time.
# 
# The built-in function `divmod` takes two arguments and returns a tuple
# of two values, the quotient and remainder.

# In[62]:
divmod(7, 3)

# In[63]:
# We can use tuple assignment to store the elements of the tuple in two variables. 

# In[64]:
quotient, remainder = divmod(7, 3)
quotient

# In[65]:
remainder

# In[66]:
# Here is an example of a function that returns a tuple.

# In[67]:
def min_max(t):
    return min(t), max(t)

# In[68]:
# `max` and `min` are built-in functions that find the largest and smallest elements of a sequence. 
# `min_max` computes both and returns a tuple of two values.

# In[69]:
min_max([2, 4, 1, 3])

# In[70]:
# We can assign the results to variables like this:

# In[71]:
low, high = min_max([2, 4, 1, 3])
low, high

# In[72]:
# ## Argument packing
# 
# Functions can take a variable number of arguments. 
# A parameter name that begins with the `*` operator **packs** arguments into a tuple.
# For example, the following function takes any number of arguments and computes their arithmetic mean -- that is, their sum divided by the number of arguments. 

# In[73]:
def mean(*args):
    return sum(args) / len(args)

# In[74]:
# The parameter can have any name you like, but `args` is conventional.
# We can call the function like this:

# In[75]:
mean(1, 2, 3)

# In[76]:
# If you have a sequence of values and you want to pass them to a function as multiple arguments, you can use the `*` operator to **unpack** the tuple.
# For example, `divmod` takes exactly two arguments -- if you pass a tuple as a parameter, you get an error.

# In[77]:
%%expect TypeError
t = (7, 3)
divmod(t)

# In[78]:
# Even though the tuple contains two elements, it counts as a single argument.
# But if you unpack the tuple, it is treated as two arguments.

# In[79]:
divmod(*t)

# In[80]:
# Packing and unpacking can be useful if you want to adapt the behavior of an existing function.
# For example, this function takes any number of arguments, removes the lowest and highest, and computes the mean of the rest.

# In[81]:
def trimmed_mean(*args):
    low, high = min_max(args)
    trimmed = list(args)
    trimmed.remove(low)
    trimmed.remove(high)
    return mean(*trimmed)

# In[82]:
# First it uses `min_max` to find the lowest and highest elements.
# Then it converts `args` to a list so it can use the `remove` method.
# Finally it unpacks the list so the elements are passed to `mean` as separate arguments, rather than as a single list.
# 
# Here's an example that shows the effect.

# In[83]:
mean(1, 2, 3, 10)

# In[84]:
trimmed_mean(1, 2, 3, 10)

# In[85]:
# This kind of "trimmed" mean is used in some sports with subjective judging -- like diving and gymnastics -- to reduce the effect of a judge whose score deviates from the others. 

# In[86]:
# ## Zip
# 
# Tuples are useful for looping through the elements of two sequences and performing operations on corresponding elements.
# For example, suppose two teams play a series of seven games, and we record their scores in two lists, one for each team.

# In[87]:
scores1 = [1, 2, 4, 5, 1, 5, 2]
scores2 = [5, 5, 2, 2, 5, 2, 3]

# In[88]:
# Let's see how many games each team won.
# We'll use `zip`, which is a built-in function that takes two or more sequences and returns a **zip object**, so-called because it pairs up the elements of the sequences like the teeth of a zipper.

# In[89]:
zip(scores1, scores2)

# In[90]:
# We can use the zip object to loop through the values in the sequences pairwise.

# In[91]:
for pair in zip(scores1, scores2):
     print(pair)

# In[92]:
# Each time through the loop, `pair` gets assigned a tuple of scores.
# So we can assign the scores to variables, and count the victories for the first team, like this:

# In[93]:
wins = 0
for team1, team2 in zip(scores1, scores2):
    if team1 > team2:
        wins += 1
        
wins

# In[94]:
# Sadly, the first team won only three games and lost the series.
# 
# If you have two lists and you want a list of pairs, you can use `zip` and `list`.

# In[95]:
t = list(zip(scores1, scores2))
t

# In[96]:
# The result is a list of tuples, so we can get the result of the last game like this:

# In[97]:
t[-1]

# In[98]:
# If you have a list of keys and a list of values, you can use `zip` and `dict` to make a dictionary.
# For example, here's how we can make a dictionary that maps from each letter to its position in the alphabet.

# In[99]:
letters = 'abcdefghijklmnopqrstuvwxyz'
numbers = range(len(letters))
letter_map = dict(zip(letters, numbers))

# In[100]:
# Now we can look up a letter and get its index in the alphabet.

# In[101]:
letter_map['a'], letter_map['z']

# In[102]:
# In this mapping, the index of `'a'` is `0` and the index of `'z'` is `25`.
# 
# If you need to loop through the elements of a sequence and their indices, you can use the built-in function `enumerate`.

# In[103]:
enumerate('abc')

# In[104]:
# The result is an **enumerate object** that loops through a sequence of pairs, where each pair contains an index (starting from 0) and an element from the given sequence.

# In[105]:
for index, element in enumerate('abc'):
    print(index, element)

# In[106]:
# ## Comparing and Sorting
# 
# The relational operators work with tuples and other sequences.
# For example, if you use the `<` operator with tuples, it starts by comparing the first element from each sequence.
# If they are equal, it goes on to the next pair of elements, and so on, until it finds a pair that differ. 

# In[107]:
(0, 1, 2) < (0, 3, 4)

# In[108]:
# Subsequent elements are not considered -- even if they are really big.

# In[109]:
(0, 1, 2000000) < (0, 3, 4)

# In[110]:
# This way of comparing tuples is useful for sorting a list of tuples, or finding the minimum or maximum.
# As an example, let's find the most common letter in a word.
# In the previous chapter, we wrote `value_counts`, which takes a string and returns a dictionary that maps from each letter to the number of times it appears.

# In[111]:
def value_counts(string):
    counter = {}
    for letter in string:
        if letter not in counter:
            counter[letter] = 1
        else:
            counter[letter] += 1
    return counter

# In[112]:
# Here is the result for the string `'banana'`.

# In[113]:
counter = value_counts('banana')
counter

# In[114]:
# With only three items, we can easily see that the most frequent letter is `'a'`, which appears three times.
# But if there were more items, it would be useful to sort them automatically.
# 
# We can get the items from `counter` like this.

# In[115]:
items = counter.items()
items

# In[116]:
# The result is a `dict_items` object that behaves like a list of tuples, so we can sort it like this.

# In[117]:
sorted(items)

# In[118]:
# The default behavior is to use the first element from each tuple to sort the list, and use the second element to break ties.
# 
# However, to find the items with the highest counts, we want to use the second element to sort the list.
# We can do that by writing a function that takes a tuple and returns the second element.

# In[119]:
def second_element(t):
    return t[1]

# In[120]:
# Then we can pass that function to `sorted` as an optional argument called `key`, which indicates that this function should be used to compute the **sort key** for each item.

# In[121]:
sorted_items = sorted(items, key=second_element)
sorted_items

# In[122]:
# The sort key determines the order of the items in the list.
# The letter with the lowest count appears first, and the letter with the highest count appears last.
# So we can find the most common letter like this.

# In[123]:
sorted_items[-1]

# In[124]:
# If we only want the maximum, we don't have to sort the list.
# We can use `max`, which also takes `key` as an optional argument.

# In[125]:
max(items, key=second_element)

# In[126]:
# To find the letter with the lowest count, we could use `min` the same way.

# In[127]:
# ## Inverting a dictionary
# 
# Suppose you want to invert a dictionary so you can look up a value and get the corresponding key.
# For example, if you have a word counter that maps from each word to the number of times it appears, you could make a dictionary that maps from integers to the words that appear that number of times.
# 
# But there's a problem -- the keys in a dictionary have to be unique, but the values don't. For example, in a word counter, there could be many words with the same count.
# 
# So one way to invert a dictionary is to create a new dictionary where the values are lists of keys from the original.
# As an example, let's count the letters in `parrot`.

# In[128]:
d =  value_counts('parrot')
d

# In[129]:
# If we invert this dictionary, the result should be `{1: ['p', 'a', 'o', 't'], 2: ['r']}`, which indicates that the letters that appear once are `'p'`, `'a'`, `'o'`, and `'t'`, and the letter than appears twice is `'r'`.
# 
# The following function takes a dictionary and returns its inverse as a new dictionary.

# In[130]:
def invert_dict(d):
    new = {}
    for key, value in d.items():
        if value not in new:
            new[value] = [key]
        else:
            new[value].append(key)
    return new

# In[131]:
# The `for` statement loops through the keys and values in `d`.
# If the value is not already in the new dictionary, it is added and associated with a list that contains a single element.
# Otherwise it is appended to the existing list.
# 
# We can test it like this:

# In[132]:
invert_dict(d)

# In[133]:
# And we get the result we expected.
# 
# This is the first example we've seen where the values in the dictionary are lists.
# We will see more!

# In[134]:
# ## Debugging
# 
# Lists, dictionaries and tuples are **data structures**.
# In this chapter we are starting to see compound data structures, like lists of tuples, or dictionaries that contain tuples as keys and lists as values.
# Compound data structures are useful, but they are prone to errors caused when a data structure has the wrong type, size, or structure.
# For example, if a function expects a list of integers and you give it a plain old integer
# (not in a list), it probably won't work.
# 
# To help debug these kinds of errors, I wrote a module called `structshape` that provides a function, also called `structshape`, that takes any kind of data structure as an argument and returns a string that summarizes its structure.
# You can download it from
# <https://raw.githubusercontent.com/AllenDowney/ThinkPython/v3/structshape.py>.

# In[135]:
download('https://raw.githubusercontent.com/AllenDowney/ThinkPython/v3/structshape.py');

# In[136]:
# We can import it like this.

# In[137]:
from structshape import structshape

# In[138]:
# Here's an example with a simple list.

# In[139]:
t = [1, 2, 3]
structshape(t)

# In[140]:
# Here's a list of lists.

# In[141]:
t2 = [[1,2], [3,4], [5,6]]
structshape(t2)

# In[142]:
# If the elements of the list are not the same type, `structshape` groups
# them by type.

# In[143]:
t3 = [1, 2, 3, 4.0, '5', '6', [7], [8], 9]
structshape(t3)

# In[144]:
# Here's a list of tuples.

# In[145]:
s = 'abc'
lt = list(zip(t, s))
structshape(lt)

# In[146]:
# And here's a dictionary with three items that map integers to strings.

# In[147]:
d = dict(lt) 
structshape(d)

# In[148]:
# If you are having trouble keeping track of your data structures,
# `structshape` can help.

# In[149]:
# ## Glossary
# 
# **pack:**
# Collect multiple arguments into a tuple.
# 
# **unpack:**
# Treat a tuple (or other sequence) as multiple arguments.
# 
# **zip object:**
# The result of calling the built-in function `zip`, can be used to loop through a sequence of tuples.
# 
# **enumerate object:**
# The result of calling the built-in function `enumerate`, can be used to loop through a sequence of tuples.
# 
# **sort key:**
# A value, or function that computes a value, used to sort the elements of a collection.
# 
# **data structure:**
# A collection of values, organized to perform certain operations efficiently.

# In[150]:
# ## Exercises

# In[151]:
# This cell tells Jupyter to provide detailed debugging information
# when a runtime error occurs. Run it before working on the exercises.

%xmode Verbose

# In[152]:
# ### Ask a virtual assistant
# 
# The exercises in this chapter might be more difficult than exercises in previous chapters, so I encourage you to get help from a virtual assistant.
# When you pose more difficult questions, you might find that the answers are not correct on the first attempt, so this is a chance to practice crafting good prompts and following up with good refinements.
# 
# One strategy you might consider is to break a big problems into pieces that can be solved with simple functions.
# Ask the virtual assistant to write the functions and test them.
# Then, once they are working, ask for a solution to the original problem.
# 
# For some of the exercises below, I make suggestions about which data structures and algorithms to use.
# You might find these suggestions useful when you work on the problems, but they are also good prompts to pass along to a virtual assistant.

# In[153]:
# ### Exercise
# 
# In this chapter I said that tuples can be used as keys in dictionaries because they are hashable, and they are hashable because they are immutable.
# But that is not always true.
# 
# If a tuple contains a mutable value, like a list or a dictionary, the tuple is no longer hashable because it contains elements that are not hashable. As an example, here's a tuple that contains two lists of integers.

# In[154]:
list0 = [1, 2, 3]
list1 = [4, 5]

t = (list0, list1)
t

# In[155]:
# Write a line of code that appends the value `6` to the end of the second list in `t`. If you display `t`, the result should be `([1, 2, 3], [4, 5, 6])`.

# In[156]:
t[1].append(6)
t

# In[157]:
# Try to create a dictionary that maps from `t` to a string, and confirm that you get a `TypeError`.

# In[158]:
%%expect TypeError

d = {t: 'this tuple contains two lists'}

# In[159]:
# For more on this topic, ask a virtual assistant, "Are Python tuples always hashable?"

# In[160]:
# ### Exercise
# 
# In this chapter we made a dictionary that maps from each letter to its index in the alphabet.

# In[161]:
letters = 'abcdefghijklmnopqrstuvwxyz'
numbers = range(len(letters))
letter_map = dict(zip(letters, numbers))

# In[162]:
# For example, the index of `'a'` is `0`.

# In[163]:
letter_map['a']

# In[164]:
# To go in the other direction, we can use list indexing.
# For example, the letter at index `1` is `'b'`.

# In[165]:
letters[1]

# In[166]:
# We can use `letter_map` and `letters` to encode and decode words using a Caesar cipher.
# 
# A Caesar cipher is a weak form of encryption that involves shifting each letter
# by a fixed number of places in the alphabet, wrapping around to the beginning if necessary. For example, `'a'` shifted by 2 is `'c'` and `'z'` shifted by 1 is `'a'`.
# 
# Write a function called `shift_word` that takes as parameters a string and an integer, and returns a new string that contains the letters from the string shifted by the given number of places.
# 
# To test your function, confirm that "cheer" shifted by 7 is "jolly" and "melon" shifted by 16 is "cubed".
# 
# Hints: Use the modulus operator to wrap around from `'z'` back to `'a'`. 
# Loop through the letters of the word, shift each one, and append the result to a list of letters.
# Then use `join` to concatenate the letters into a string.

# In[167]:
# You can use this outline to get started.

# In[168]:
def shift_word(word, n):
    """Shift the letters of `word` by `n` places.
    
    >>> shift_word('cheer', 7)
    'jolly'
    >>> shift_word('melon', 16)
    'cubed'
    """
    return None

# In[169]:
# Solution

def shift_word(word, n):
    """Shift the letters of `word` by `n` places.
    
    >>> shift_word('cheer', 7)
    'jolly'
    >>> shift_word('melon', 16)
    'cubed'
    """
    t = []
    for letter in word:
        index = (letter_map[letter] + n) % 26
        t.append(letters[index])
    return ''.join(t)

# In[170]:
shift_word('cheer', 7)

# In[171]:
shift_word('melon', 16)

# In[172]:
# You can use `doctest` to test your function.

# In[173]:
from doctest import run_docstring_examples

def run_doctests(func):
    run_docstring_examples(func, globals(), name=func.__name__)

run_doctests(shift_word)

# In[174]:
# ### Exercise
# 
# Write a function called `most_frequent_letters` that takes a string and prints the letters in decreasing order of frequency.
# 
# To get the items in decreasing order, you can use `reversed` along with `sorted` or you can pass `reverse=True` as a keyword parameter to `sorted`.

# In[175]:
# You can use this outline of the function to get started.

# In[176]:
def most_frequent_letters(string):
    return None

# In[177]:
# Solution

def most_frequent_letters(string):
    counter = value_counts(string)
    pairs = sorted(counter.items(), key=second_element, reverse=True)
    for key, value in pairs:
        print(key, value)

# In[178]:
# And this example to test your function.

# In[179]:
most_frequent_letters('brontosaurus')

# In[180]:
# Once your function is working, you can use the following code to print the most common letters in *Dracula*, which we can download from Project Gutenberg.

# In[181]:
download('https://www.gutenberg.org/cache/epub/345/pg345.txt');

# In[182]:
string = open('pg345.txt').read()
most_frequent_letters(string)

# In[183]:
# According to Zim's "Codes and Secret Writing", the sequence of letters in decreasing order of frequency in English starts with "ETAONRISH".
# How does this sequence compare with the results from *Dracula*?

# In[184]:
# ### Exercise
# 
# In a previous exercise, we tested whether two strings are anagrams by sorting the letters in both words and checking whether the sorted letters are the same.
# Now let's make the problem a little more challenging.
# 
# We'll write a program that takes a list of words and prints all the sets of words that are anagrams.
# Here is an example of what the output might look like:
# 
#     ['deltas', 'desalt', 'lasted', 'salted', 'slated', 'staled']
#     ['retainers', 'ternaries']
#     ['generating', 'greatening']
#     ['resmelts', 'smelters', 'termless']
# 
# Hint: For each word in the word list, sort the letters and join them back into a string. Make a dictionary that maps from this sorted string to a list of words that are anagrams of it.

# In[185]:
# The following cells download `words.txt` and read the words into a list.

# In[186]:
download('https://raw.githubusercontent.com/AllenDowney/ThinkPython/v3/words.txt');

# In[187]:
word_list = open('words.txt').read().split()

# In[188]:
# Here's the `sort_word` function we've used before.

# In[189]:
def sort_word(word):
    return ''.join(sorted(word))

# In[190]:
# Solution

anagram_dict = {}
for word in word_list:
    key = sort_word(word)
    if key not in anagram_dict:
        anagram_dict[key] = [word]
    else:
        anagram_dict[key].append(word)

# In[191]:
# To find the longest list of anagrams, you can use the following function, which takes a key-value pair where the key is a string and the value is a list of words.
# It returns the length of the list.

# In[192]:
def value_length(pair):
    key, value = pair
    return len(value)

# In[193]:
# We can use this function as a sort key to find the longest lists of anagrams.

# In[194]:
anagram_items = sorted(anagram_dict.items(), key=value_length)
for key, value in anagram_items[-10:]:
    print(value)

# In[195]:
# If you want to know the longest words that have anagrams, you can use the following loop to print some of them.

# In[196]:
longest = 7

for key, value in anagram_items:
    if len(value) > 1:
        word_len = len(value[0])
        if word_len > longest:
            longest = word_len
            print(value)

# In[197]:
# ### Exercise
# 
# Write a function called `word_distance` that takes two words with the same length and returns the number of places where the two words differ.
# 
# Hint: Use `zip` to loop through the corresponding letters of the words.

# In[198]:
# Here's an outline of the function with doctests you can use to check your function.

# In[199]:
def word_distance(word1, word2):
    """Computes the number of places where two word differ.

    >>> word_distance("hello", "hxllo")
    1
    >>> word_distance("ample", "apply")
    2
    >>> word_distance("kitten", "mutton")
    3
    """
    return None

# In[200]:
# Solution

def word_distance(word1, word2):
    """Computes the number of places where two word differ.

    >>> word_distance("hello", "hxllo")
    1
    >>> word_distance("ample", "apply")
    2
    >>> word_distance("kitten", "mutton")
    3
    """
    assert len(word1) == len(word2)

    count = 0
    for c1, c2 in zip(word1, word2):
        if c1 != c2:
            count += 1

    return count

# In[201]:
from doctest import run_docstring_examples

def run_doctests(func):
    run_docstring_examples(func, globals(), name=func.__name__)
    
run_doctests(word_distance)

# In[202]:
# ### Exercise
# 
# "Metathesis" is the transposition of letters in a word.
# Two words form a "metathesis pair" if you can transform one into the other by swapping two letters, like `converse` and `conserve`.
# Write a program that finds all of the metathesis pairs in the word list. 
# 
# Hint: The words in a metathesis pair must be anagrams of each other.
# 
# Credit: This exercise is inspired by an example at <http://puzzlers.org>.

# In[203]:
# Solution

for anagrams in anagram_dict.values():
    for word1 in anagrams:
        for word2 in anagrams:
            if len(word1) >= 10 and word1 < word2 and word_distance(word1, word2) == 2:
                print(word1, word2)

# In[204]:
# ### Exercise
# 
# This is a bonus exercise that is not in the book.
# It is more challenging than the other exercises in this chapter, so you might want to ask a virtual assistant for help, or come back to it after you've read a few more chapters.
# 
# Here's another Car Talk Puzzler
# (<http://www.cartalk.com/content/puzzlers>):
# 
# > What is the longest English word, that remains a valid English word,
# > as you remove its letters one at a time?
# >
# > Now, letters can be removed from either end, or the middle, but you
# > can't rearrange any of the letters. Every time you drop a letter, you
# > wind up with another English word. If you do that, you're eventually
# > going to wind up with one letter and that too is going to be an
# > English word---one that's found in the dictionary. I want to know
# > what's the longest word and how many letters does it have?
# >
# > I'm going to give you a little modest example: Sprite. Ok? You start
# > off with sprite, you take a letter off, one from the interior of the
# > word, take the r away, and we're left with the word spite, then we
# > take the e off the end, we're left with spit, we take the s off, we're
# > left with pit, it, and I.
# 
# Write a program to find all words that can be reduced in this way, and
# then find the longest one.
# 
# This exercise is a little more challenging than most, so here are some
# suggestions:
# 
# 1.  You might want to write a function that takes a word and computes a
#     list of all the words that can be formed by removing one letter.
#     These are the "children" of the word.
# 
# 2.  Recursively, a word is reducible if any of its children are
#     reducible. As a base case, you can consider the empty string
#     reducible.
# 
# 3.  The word list we've been using doesn't contain single letter
#     words. So you might have to add "I" and "a".
# 
# 4.  To improve the performance of your program, you might want to
#     memoize the words that are known to be reducible.

# In[205]:
# Solution

def children(word):
    """Returns a list of all words that can be formed by removing one letter.

    word: string

    Returns: list of strings
    """
    res = []
    for i in range(len(word)):
        child = word[:i] + word[i+1:]
        if child in word_dict:
            res.append(child)
    return res

# In[206]:
# Solution

"""memo is a dictionary that maps from each word that is known
to be reducible to a list of its reducible children. 
It starts with the empty string."""

memo = {}
memo[''] = ['']


def reduce_word(word):
    """If word is reducible, returns a list of its reducible children.

    Also adds an entry to the memo dictionary.

    A string is reducible if it has at least one child that is 
    reducible.  The empty string is also reducible.

    word: string
    """
     # if have already checked this word, return the answer
    if word in memo:
        return memo[word]

    # check each of the children and make a list of the reducible ones
    res = []
    for child in children(word):
        if reduce_word(child):
            res.append(child)

    # memoize and return the result
    memo[word] = res
    return res

# In[207]:
# Solution

def print_trail(word):
    """Prints the sequence of words that reduces this word to the empty string.

    If there is more than one choice, it chooses the first.

    word: string
    """
    if len(word) == 0:
        return
    print(word, end=' ')
    t = reduce_word(word)
    print_trail(t[0])

# In[208]:
# Solution

def all_reducible():
    """Checks all words in the word_dict; returns a list of reducible ones.
    """
    res = []
    for word in word_dict:
        t = reduce_word(word)
        if len(t) > 0:
            res.append(word)
    return res

# In[209]:
# Solution

word_dict = {}
for word in word_list:
    word_dict[word] = 1

# have to add single letter words to the word list;
# also, the empty string is considered a word.
for word in ['a', 'i', '']:
    word_dict[word] = 1

# find the reducible words and sort by length
words = all_reducible()
sorted_words = sorted(words, key=len)

# print the longest words
for word in sorted_words[-10:]:
    print_trail(word)
    print('')

# In[210]:
# [Think Python: 3rd Edition](https://allendowney.github.io/ThinkPython/index.html)
# 
# Copyright 2024 [Allen B. Downey](https://allendowney.com)
# 
# Code license: [MIT License](https://mit-license.org/)
# 
# Text license: [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-nc-sa/4.0/)

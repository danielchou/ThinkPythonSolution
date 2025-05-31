# 從 chap18.ipynb 轉換而來
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
# Here are versions of the `Card`, `Deck`, and `Hand` classes from Chapter 17, which we will use in some examples in this chapter.

# In[3]:
class Card:
    suit_names = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
    rank_names = [None, 'Ace', '2', '3', '4', '5', '6', '7', 
                  '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
    
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        rank_name = Card.rank_names[self.rank]
        suit_name = Card.suit_names[self.suit]
        return f'{rank_name} of {suit_name}' 

# In[4]:
import random

class Deck:
    def __init__(self, cards):
        self.cards = cards
        
    def __str__(self):
        res = []
        for card in self.cards:
            res.append(str(card))
        return '\n'.join(res)
    
    def make_cards():
        cards = []
        for suit in range(4):
            for rank in range(2, 15):
                card = Card(suit, rank)
                cards.append(card)
        return cards
    
    def shuffle(self):
        random.shuffle(self.cards)
        
    def pop_card(self):
        return self.cards.pop()
    
    def add_card(self, card):
        self.cards.append(card)

# In[5]:
class Hand(Deck):
    def __init__(self, label=''):
        self.label = label
        self.cards = []

# In[6]:
# # Python Extras
# 
# One of my goals for this book has been to teach you as little Python as possible. 
# When there were two ways to do something, I picked one and avoided mentioning the other.
# Or sometimes I put the second one into an exercise.
# 
# Now I want to go back for some of the good bits that got left behind.
# Python provides a number of features that are not really necessary -- you can write good code without them -- but with them you can write code that's more concise, readable, or efficient, and sometimes all three.

# In[7]:
# ## Sets
# 
# Python provides a class called `set` that represents a collection of unique elements.
# To create an empty set, we can use the class object like a function.

# In[8]:
s1 = set()
s1

# In[9]:
# We can use the `add` method to add elements.

# In[10]:
s1.add('a')
s1.add('b')
s1

# In[11]:
# Or we can pass any kind of sequence to `set`.

# In[12]:
s2 = set('acd')
s2

# In[13]:
# An element can only appear once in a `set`.
# If you add an element that's already there, it has no effect.

# In[14]:
s1.add('a')
s1

# In[15]:
# Or if you create a set with a sequence that contains duplicates, the result contains only unique elements.

# In[16]:
set('banana')

# In[17]:
# Some of the exercises in this book can be done concisely and efficiently with sets. 
# For example, here is a solution to an exercise in Chapter 11 that uses a dictionary to check whether there are any duplicate elements in a sequence.

# In[18]:
def has_duplicates(t):
    d = {}
    for x in t:
        d[x] = True
    return len(d) < len(t)

# In[19]:
# This version adds the element of `t` as keys in a dictionary, and then checks whether there are fewer keys than elements.
# Using sets, we can write the same function like this.

# In[20]:
def has_duplicates(t):
    s = set(t)
    return len(s) < len(t)

# In[21]:
has_duplicates('abba')

# In[22]:
# An element can only appear in a set once, so if an element in `t` appears more than once, the set will be smaller than `t`.
# If there are no duplicates, the set will be the same size as `t`.
# 
# `set` objects provide methods that perform set operations.
# For example, `union` computes the union of two sets, which is a new set that contains all elements that appear in either set.

# In[23]:
s1.union(s2)

# In[24]:
# Some arithmetic operators work with sets.
# For example, the `-` operator performs set subtraction -- the result is a new set that contains all elements from the first set that are _not_ in the second set.

# In[25]:
s1 - s2

# In[26]:
# In [Chapter 12](section_dictionary_subtraction) we used dictionaries to find the words that appear in a document but not in a word list.
# We used the following function, which takes two dictionaries and returns a new dictionary that contains only the keys from the first that don't appear in the second.

# In[27]:
def subtract(d1, d2):
    res = {}
    for key in d1:
        if key not in d2:
            res[key] = d1[key]
    return res

# In[28]:
# With sets, we don't have to write this function ourselves.
# If `word_counter` is a dictionary that contains the unique words in the document and `word_list` is a list of valid words, we can compute the set difference like this.

# In[29]:
# this cell creates a small example so we can run the following
# cell without loading the actual data

word_counter = {'word': 1}
word_list = ['word']

# In[30]:
set(word_counter) - set(word_list)

# In[31]:
# The result is a set that contains the words in the document that don't appear in the word list.
# 
# The relational operators work with sets.
# For example, `<=` checks whether one set is a subset of another, including the possibility that they are equal.

# In[32]:
set('ab') <= set('abc')

# In[33]:
# With these operators, we can use sets to do some of the exercises in Chapter 7.
# For example, here's a version of `uses_only` that uses a loop.

# In[34]:
def uses_only(word, available):
    for letter in word: 
        if letter not in available:
            return False
    return True

# In[35]:
# `uses_only` checks whether all letters in `word` are in `available`.
# With sets, we can rewrite it like this.

# In[36]:
def uses_only(word, available):
    return set(word) <= set(available)

# In[37]:
# If the letters in `word` are a subset of the letters in `available`, that means that `word` uses only letters in `available`.

# In[38]:
# ## Counters
# 
# A `Counter` is like a set, except that if an element appears more than once, the `Counter` keeps track of how many times it appears.
# If you are familiar with the mathematical idea of a "multiset", a `Counter` is a
# natural way to represent a multiset.
# 
# The `Counter` class is defined in a module called `collections`, so you have to import it.
# Then you can use the class object as a function and pass as an argument a string, list, or any other kind of sequence.

# In[39]:
from collections import Counter

counter = Counter('banana')
counter

# In[40]:
from collections import Counter

t = (1, 1, 1, 2, 2, 3)
counter = Counter(t)
counter

# In[41]:
# A `Counter` object is like a dictionary that maps from each key to the number of times it appears.
# As in dictionaries, the keys have to be hashable.
# 
# Unlike dictionaries, `Counter` objects don't raise an exception if you access an
# element that doesn't appear.
# Instead, they return `0`.

# In[42]:
counter['d']

# In[43]:
# We can use `Counter` objects to solve one of the exercises from Chapter 10, which asks for a function that takes two words and checks whether they are anagrams -- that is, whether the letters from one can be rearranged to spell the other.
# 
# Here's a solution using `Counter` objects.

# In[44]:
def is_anagram(word1, word2):
    return Counter(word1) == Counter(word2)

# In[45]:
# If two words are anagrams, they contain the same letters with the same counts, so their `Counter` objects are equivalent.
# 
# `Counter` provides a method called `most_common` that returns a list of value-frequency pairs, sorted from most common to least.

# In[46]:
counter.most_common()

# In[47]:
# They also provide methods and operators to perform set-like operations, including addition, subtraction, union and intersection.
# For example, the `+` operator combines two `Counter` objects and creates a new `Counter` that contains the keys from both and the sums of the counts.
# 
# We can test it by making a `Counter` with the letters from `'bans'` and adding it to the letters from `'banana'`.

# In[48]:
counter2 = Counter('bans')
counter + counter2

# In[49]:
# You'll have a chance to explore other `Counter` operations in the exercises at the end of this chapter.

# In[50]:
# ## defaultdict
# 
# The `collections` module also provides `defaultdict`, which is like a dictionary except that if you access a key that doesn't exist, it generates a new value automatically.
# 
# When you create a `defaultdict`, you provide a function that's used to create new values.
# A function that create objects is sometimes called a **factory**.
# The built-in functions that create lists, sets, and other types can be used as factories.
# 
# For example, here's a `defaultdict` that creates a new `list` when needed. 

# In[51]:
from collections import defaultdict

d = defaultdict(list)
d

# In[52]:
# Notice that the argument is `list`, which is a class object, not `list()`, which is a function call that creates a new list.
# The factory function doesn't get called unless we access a key that doesn't exist.

# In[53]:
t = d['new key']
t

# In[54]:
# The new list, which we're calling `t`, is also added to the dictionary.
# So if we modify `t`, the change appears in `d`:

# In[55]:
t.append('new value')
d['new key']

# In[56]:
# If you are making a dictionary of lists, you can often write simpler
# code using `defaultdict`. 
# 
# In one of the exercises in [Chapter 11](chapter_tuples), I made a dictionary that maps from a sorted string of letters to the list of words that can be spelled with those letters.
# For example, the string `'opst'` maps to the list `['opts', 'post', 'pots', 'spot', 'stop', 'tops']`.
# Here's the original code.

# In[57]:
def all_anagrams(filename):
    d = {}
    for line in open(filename):
        word = line.strip().lower()
        t = signature(word)
        if t not in d:
            d[t] = [word]
        else:
            d[t].append(word)
    return d

# In[58]:
# And here's a simpler version using a `defaultdict`.

# In[59]:
def all_anagrams(filename):
    d = defaultdict(list)
    for line in open(filename):
        word = line.strip().lower()
        t = signature(word)
        d[t].append(word)
    return d

# In[60]:
# In the exercises at the end of the chapter, you'll have a chance to practice using `defaultdict` objects.

# In[61]:
from collections import defaultdict

d = defaultdict(list)
key = ('into', 'the')
d[key].append('woods')
d[key]

# In[62]:
# ## Conditional expressions
# 
# Conditional statements are often used to choose one of two values, like this:

# In[63]:
import math
x = 5

# In[64]:
if x > 0:
    y = math.log(x)
else:
    y = float('nan')

# In[65]:
y

# In[66]:
# This statement checks whether `x` is positive. If so, it computes its logarithm. 
# If not, `math.log` would raise a ValueError.
# To avoid stopping the program, we generate a `NaN`, which is a special floating-point value that represents "Not a Number".
# 
# We can write this statement more concisely using a **conditional expression**.

# In[67]:
y = math.log(x) if x > 0 else float('nan')

# In[68]:
y

# In[69]:
# You can almost read this line like English: "`y` gets log-`x` if `x` is greater than 0; otherwise it gets `NaN`".
# 
# Recursive functions can sometimes be written concisely using conditional expressions. 
# For example, here is a version of `factorial` with a conditional _statement_.

# In[70]:
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

# In[71]:
# And here's a version with a conditional _expression_.

# In[72]:
def factorial(n):
    return 1 if n == 0 else n * factorial(n-1)

# In[73]:
# Another use of conditional expressions is handling optional arguments.
# For example, here is class definition with an `__init__` method that uses a conditional statement to check a parameter with a default value.

# In[74]:
class Kangaroo:
    def __init__(self, name, contents=None):
        self.name = name
        if contents is None:
            contents = []
        self.contents = contents

# In[75]:
# Here's a version that uses a conditional expression.

# In[76]:
def __init__(self, name, contents=None):
    self.name = name
    self.contents = [] if contents is None else contents 

# In[77]:
# In general, you can replace a conditional statement with a conditional expression if both branches contain a single expression and no statements.

# In[78]:
# ## List comprehensions
# 
# In previous chapters, we've seen a few examples where we start with an empty list and add elements, one at a time, using the `append` method.
# For example, suppose we have a string that contains the title of a movie, and we want to capitalize all of the words.

# In[79]:
title = 'monty python and the holy grail'

# In[80]:
# We can split it into a list of strings, loop through the strings, capitalize them, and append them to a list.

# In[81]:
t = []
for word in title.split():
    t.append(word.capitalize())

' '.join(t)

# In[82]:
# We can do the same thing more concisely using a **list comprehension**:

# In[83]:
t = [word.capitalize() for word in title.split()]

' '.join(t)

# In[84]:
# The bracket operators indicate that we are constructing a new list.
# The expression inside the brackets specifies the elements of the list, and the `for` clause indicates what sequence we are looping through.
# 
# The syntax of a list comprehension might seem strange, because the loop variable -- `word` in this example -- appears in the expression before we get to its definition.
# But you get used to it.
# 
# As another example, in [Chapter 9](section_word_list) we used this loop to read words from a file and append them to a list.

# In[85]:
download('https://raw.githubusercontent.com/AllenDowney/ThinkPython2/master/code/words.txt');

# In[86]:
word_list = []

for line in open('words.txt'):
    word = line.strip()
    word_list.append(word)

# In[87]:
len(word_list)

# In[88]:
# Here's how we can write that as a list comprehension.

# In[89]:
word_list = [line.strip() for line in open('words.txt')]

# In[90]:
len(word_list)

# In[91]:
# A list comprehension can also have an `if` clause that determines which elements are included in the list.
# For example, here's a `for` loop we used in [Chapter 10](section_palindrome_list) to make a list of only the words in `word_list` that are palindromes.

# In[92]:
def is_palindrome(word):
    return list(reversed(word)) == list(word)

# In[93]:
palindromes = []

for word in word_list:
    if is_palindrome(word):
        palindromes.append(word)

# In[94]:
palindromes[:10]

# In[95]:
# Here's how we can do the same thing with an list comprehension.

# In[96]:
palindromes = [word for word in word_list if is_palindrome(word)]

# In[97]:
palindromes[:10]

# In[98]:
# When a list comprehension is used as an argument to a function, we can often omit the brackets.
# For example, suppose we want to add up $1 / 2^n$ for values of $n$ from 0 to 9.
# We can use a list comprehension like this.

# In[99]:
sum([1/2**n for n in range(10)])

# In[100]:
# Or we can leave out the brackets like this.

# In[101]:
sum(1/2**n for n in range(10))

# In[102]:
# In this example, the argument is technically a **generator expression**, not a list comprehension, and it never actually makes a list.
# But other than that, the behavior is the same.
# 
# List comprehensions and generator expressions are concise and easy to read, at least for simple expressions.
# And they are usually faster than the equivalent for loops, sometimes much faster.
# So if you are mad at me for not mentioning them earlier, I understand.
# 
# But, in my defense, list comprehensions are harder to debug because you can't put a print statement inside the loop.
# I suggest you use them only if the computation is simple enough that you are likely to get it
# right the first time.
# Or consider writing and debugging a `for` loop and then converting it to a list comprehension.

# In[103]:
# ## `any` and `all`
# 
# Python provides a built-in function, `any`, that takes a sequence of boolean values and returns `True` if any of the values are `True`.

# In[104]:
any([False, False, True])

# In[105]:
# `any` is often used with generator expressions.

# In[106]:
any(letter == 't' for letter in 'monty')

# In[107]:
# That example isn't very useful because it does the same thing as the `in` operator. 
# But we could use `any` to write concise solutions to some of the exercises in [Chapter 7](chapter_search). For example, we can write `uses_none` like this.

# In[108]:
def uses_none(word, forbidden):
    """Checks whether a word avoids forbidden letters."""
    return not any(letter in forbidden for letter in word)

# In[109]:
uses_none('banana', 'xyz')

# In[110]:
uses_none('apple', 'efg')

# In[111]:
# This function loops through the letters in `word` and checks whether any of them are in `forbidden`.
# Using `any` with a generator expression is efficient because it stops immediately if it finds a `True` value, so it doesn't have to loop through the whole sequence.
# 
# Python provides another built-in function, `all`, that returns `True` if every element of the sequence is `True`.
# We can use it to write a concise version of `uses_all`.

# In[112]:
def uses_all(word, required):
    """Check whether a word uses all required letters."""
    return all(letter in word for letter in required)

# In[113]:
uses_all('banana', 'ban')

# In[114]:
uses_all('apple', 'api')

# In[115]:
# Expressions using `any` and `all` can be concise, efficient, and easy to read.

# In[116]:
# ## Named tuples
# 
# The `collections` module provides a function called `namedtuple` that can be used to create simple classes.
# For example, the `Point` object in [Chapter 16](section_create_point) has only two attributes, `x` and `y`.
# Here's how we defined it.

# In[117]:
class Point:
    """Represents a point in 2-D space."""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __str__(self):
        return f'({self.x}, {self.y})'

# In[118]:
# That's a lot of code to convey a small amount of information.
# `namedtuple` provides a more concise way to define classes like this.

# In[119]:
from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])

# In[120]:
# The first argument is the name of the class you want to create. The
# second is a list of the attributes `Point` objects should have.
# The result is a class object, which is why it is assigned to a capitalized variable name.
# 
# A class created with `namedtuple` provides an `__init__` method that assigns values to the attributes and a `__str__` that displays the object in a readable form.
# So we can create and display a `Point` object like this.

# In[121]:
p = Point(1, 2)
p

# In[122]:
# `Point` also provides an `__eq__` method that checks whether two `Point` objects are equivalent -- that is, whether their attributes are the same.

# In[123]:
p == Point(1, 2)

# In[124]:
# You can access the elements of a named tuple by name or by index.

# In[125]:
p.x, p.y

# In[126]:
p[0], p[1]

# In[127]:
# You can also treat a named tuple as a tuple, as in this assignment.

# In[128]:
x, y = p
x, y

# In[129]:
# But `namedtuple` objects are immutable.
# After the attributes are initialized, they can't be changed.

# In[130]:
%%expect TypeError

p[0] = 3

# In[131]:
%%expect AttributeError

p.x = 3

# In[132]:
# `namedtuple` provides a quick way to define simple classes.
# The drawback is that simple classes don't always stay simple.
# You might decide later that you want to add methods to a named tuple.
# In that case, you can define a new class that inherits from the named tuple.

# In[133]:
class Pointier(Point):
    """This class inherits from Point"""

# In[134]:
# Or at that point you could switch to a conventional class definition.

# In[135]:
# ## Packing keyword arguments
# 
# In [Chapter 11](section_argument_pack), we wrote a function that packs its arguments into a tuple.

# In[136]:
def mean(*args):
    return sum(args) / len(args)

# In[137]:
# You can call this function with any number of arguments.

# In[138]:
mean(1, 2, 3)

# In[139]:
# But the `*` operator doesn't pack keyword arguments.
# So calling this function with a keyword argument causes an error.

# In[140]:
%%expect TypeError

mean(1, 2, start=3)

# In[141]:
# To pack keyword arguments, we can use the `**` operator:

# In[142]:
def mean(*args, **kwargs):
    print(kwargs)
    return sum(args) / len(args)

# In[143]:
# The keyword-packing parameter can have any name, but `kwargs` is a common choice.
# The result is a dictionary that maps from keywords to values.

# In[144]:
mean(1, 2, start=3)

# In[145]:
# In this example, the value of `kwargs` is printed, but otherwise is has no effect.
# 
# But the `**` operator can also be used in an argument list to unpack a dictionary.
# For example, here's a version of `mean` that packs any keyword arguments it gets and then unpacks them as keyword arguments for `sum`.

# In[146]:
def mean(*args, **kwargs):
    return sum(args, **kwargs) / len(args)

# In[147]:
# Now if we call `mean` with `start` as a keyword argument, it gets passed along to sum, which uses it as the starting point of the summation.
# In the following example `start=3` adds `3` to the sum before computing the mean, so the sum is `6` and the result is `3`.

# In[148]:
mean(1, 2, start=3)

# In[149]:
# As another example, if we have a dictionary with keys `x` and `y`, we can use it with the unpack operator to create a `Point` object.

# In[150]:
d = dict(x=1, y=2)
Point(**d)

# In[151]:
# Without the unpack operator, `d` is treated as a single positional argument, so it gets assigned to `x`, and we get a `TypeError` because there's no second argument to assign to `y`.

# In[152]:
%%expect TypeError

d = dict(x=1, y=2)
Point(d)

# In[153]:
# When you are working with functions that have a large number of keyword arguments, it is often useful to create and pass around dictionaries that specify frequently used options.

# In[154]:
def pack_and_print(**kwargs):
    print(kwargs)
    
pack_and_print(a=1, b=2)

# In[155]:
# ## Debugging
# 
# In previous chapters, we used `doctest` to test functions.
# For example, here's a function called `add` that takes two numbers and returns their sum.
# In includes a doctest that checks whether `2 + 2` is `4`.

# In[156]:
def add(a, b):
    '''Add two numbers.
    
    >>> add(2, 2)
    4
    '''
    return a + b

# In[157]:
# This function takes a function object and runs its doctests.

# In[158]:
from doctest import run_docstring_examples

def run_doctests(func):
    run_docstring_examples(func, globals(), name=func.__name__)

# In[159]:
# So we can test `add` like this.

# In[160]:
run_doctests(add)

# In[161]:
# There's no output, which means all tests passed.
# 
# Python provides another tool for running automated tests, called `unittest`.
# It is a little more complicated to use, but here's an example.

# In[162]:
from unittest import TestCase

class TestExample(TestCase):

    def test_add(self):
        result = add(2, 2)
        self.assertEqual(result, 4)

# In[163]:
# First we import `TestCase`, which is a class in the `unittest` module.
# To use it, we have to define a new class that inherits from `TestCase` and provides at least one test method.
# The name of the test method must begin with `test` and should indicate which function it tests.
# 
# In this example, `test_add` tests the `add` function by calling it, saving the result, and invoking `assertEqual`, which is inherited from `TestCase`.
# `assertEqual` takes two arguments and checks whether they are equal.
# 
# In order to run this test method, we have to run a function in `unittest` called `main` and provide several keyword arguments.
# The following function shows the details -- if you are curious, you can ask a virtual assistant to explain how it works.

# In[164]:
import unittest

def run_unittest():
    unittest.main(argv=[''], verbosity=0, exit=False)

# In[165]:
# `run_unittest` does not take `TestExample` as an argument -- instead, it searches for classes that inherit from `TestCase`.
# Then it searches for methods that begin with `test` and runs them.
# This process is called **test discovery**.
# 
# Here's what happens when we call `run_unittest`.

# In[166]:
run_unittest()

# In[167]:
# `unittest.main` reports the number of tests it ran and the results.
# In this case `OK` indicates that the tests passed.
# 
# To see what happens when a test fails, we'll add an incorrect test method to `TestExample`.

# In[168]:
%%add_method_to TestExample

    def test_add_broken(self):
        result = add(2, 2)
        self.assertEqual(result, 100)

# In[169]:
# Here's what happens when we run the tests.

# In[170]:
run_unittest()

# In[171]:
# The report includes the test method that failed and an error message showing where.
# The summary indicates that two tests ran and one failed.
# 
# In the exercises below, I'll suggest some prompts you can use to ask a virtual assistant for more information about `unittest`.

# In[172]:
# ## Glossary
# 
# **factory:**
#  A function used to create objects, often passed as a parameter to a function.
# 
# **conditional expression:**
# An expression that uses a conditional to select one of two values.
# 
# **list comprehension:**
# A concise way to loop through a sequence and create a list.
# 
# **generator expression:**
# Similar to a list comprehension except that it does not create a list.
# 
# **test discovery:**
# A process used to find and run tests.

# In[173]:
# ## Exercises

# In[174]:
# This cell tells Jupyter to provide detailed debugging information
# when a runtime error occurs. Run it before working on the exercises.

%xmode Verbose

# In[175]:
# ### Ask a virtual assistant
# 
# There are a few topics in this chapter you might want to learn about.
# 
# * "What are the methods and operators of Python's set class?"
# 
# * "What are the methods and operators of Python's Counter class?"
# 
# * "What is the difference between a Python list comprehension and a generator expression?"
# 
# * "When should I use Python's `namedtuple` rather than define a new class?"
# 
# * "What are some uses of packing and unpacking keyword arguments?"
# 
# * "How does `unittest` do test discovery?"
# 
# * "Along with `assertEqual`, what are the most commonly used methods in `unittest.TestCase`?"
# 
# * "What are the pros and cons of `doctest` and `unittest`?"
# 
# For the following exercises, consider asking a virtual assistant for help, but as always, remember to test the results.

# In[176]:
# ### Exercise
# 
# One of the exercises in Chapter 7 asks for a function called `uses_none` that takes a word and a string of forbidden letters, and returns `True` if the word does not use any of the letters. Here's a solution.

# In[177]:
def uses_none(word, forbidden):
    for letter in word.lower():
        if letter in forbidden.lower():
            return False
    return True

# In[178]:
# Write a version of this function that uses `set` operations instead of a `for` loop.
# Hint: ask a VA, "How do I compute the intersection of Python sets?"

# In[179]:
# You can use this outline to get started.

# In[180]:
def uses_none(word, forbidden):
    """Checks whether a word avoid forbidden letters.
    
    >>> uses_none('banana', 'xyz')
    True
    >>> uses_none('apple', 'efg')
    False
    >>> uses_none('', 'abc')
    True
    """
    return False

# In[181]:
# Solution

def uses_none(word, forbidden):
    """Checks whether a word avoid forbidden letters.
    
    >>> uses_none('banana', 'xyz')
    True
    >>> uses_none('apple', 'efg')
    False
    >>> uses_none('', 'abc')
    True
    """
    word_set = set(word.lower())
    forbidden_set = set(forbidden.lower())
    return len(word_set & forbidden_set) == 0

# In[182]:
from doctest import run_docstring_examples

def run_doctests(func):
    run_docstring_examples(func, globals(), name=func.__name__)

# In[183]:
run_doctests(uses_none)

# In[184]:
# ### Exercise
# 
# Scrabble is a board game where the objective is to use letter tiles to spell words.
# For example, if we have tiles with the letters `T`, `A`, `B`, `L`, `E`, we can spell `BELT` and `LATE` using a subset of the tiles -- but we can't spell `BEET` because we don't have two `E`s.
# 
# Write a function that takes a string of letters and a word, and checks whether the letters can spell the word, taking into account how many times each letter appears.

# In[185]:
# You can use the following outline to get started.

# In[186]:
def can_spell(letters, word):
    """Check whether the letters can spell the word.
    
    >>> can_spell('table', 'belt')
    True
    >>> can_spell('table', 'late')
    True
    >>> can_spell('table', 'beet')
    False
    """
    return False

# In[187]:
# Solution

def can_spell(letters, word):
    """Check whether the letters can spell the word.
    
    >>> can_spell('table', 'belt')
    True
    >>> can_spell('table', 'late')
    True
    >>> can_spell('table', 'beet')
    False
    """
    return Counter(word) <= Counter(letters)

# In[188]:
run_doctests(can_spell)

# In[189]:
# ### Exercise
# 
# In one of the exercises from [Chapter 17](chapter_inheritance), my solution to `has_straightflush` uses the following method, which partitions a `PokerHand` into a list of four hands, where each hand contains cards of the same suit.

# In[190]:
    def partition(self):
        """Make a list of four hands, each containing only one suit."""
        hands = []
        for i in range(4):
            hands.append(PokerHand())
            
        for card in self.cards:
            hands[card.suit].add_card(card)
            
        return hands

# In[191]:
# Write a simplified version of this function using a `defaultdict`.

# In[192]:
# Here's an outline of the `PokerHand` class and the `partition_suits` function you can use to get started.

# In[193]:
class PokerHand(Hand):
    
    def partition(self):
        return {}

# In[194]:
# Solution

class PokerHand(Hand):
    def partition(self):
        d = defaultdict(PokerHand)

        for card in self.cards:
            d[card.suit].add_card(card)

        return d

# In[195]:
# To test your code, we'll make a deck and shuffle it.

# In[196]:
cards = Deck.make_cards()
deck = Deck(cards)
deck.shuffle()

# In[197]:
# Then create a `PokerHand` and add seven cards to it.

# In[198]:
random_hand = PokerHand('random')

for i in range(7):
    card = deck.pop_card()
    random_hand.add_card(card)
    
print(random_hand)

# In[199]:
# If you invoke `partition` and print the results, each hand should contain cards of one suit only.

# In[200]:
hand_dict = random_hand.partition()

for hand in hand_dict.values():
    print(hand)
    print()

# In[201]:
# ### Exercise
# 
# Here's the function from Chapter 11 that computes Fibonacci numbers.

# In[202]:
def fibonacci(n):
    if n == 0:
        return 0
    
    if n == 1:
        return 1

    return fibonacci(n-1) + fibonacci(n-2)

# In[203]:
# Write a version of this function with a single return statement that use two conditional expressions, one nested inside the other.

# In[204]:
# Solution

def fibonacci(n):
    return 0 if n == 0 else (1 if n == 1 else fibonacci(n-1) + fibonacci(n-2))

# In[205]:
fibonacci(10)    # should be 55

# In[206]:
fibonacci(20)    # should be 6765

# In[207]:
# ### Exercise
# The following is a function that computes the binomial coefficient
# recursively.

# In[208]:
def binomial_coeff(n, k):
    """Compute the binomial coefficient "n choose k".

    n: number of trials
    k: number of successes

    returns: int
    """
    if k == 0:
        return 1
    
    if n == 0:
        return 0

    return binomial_coeff(n-1, k) + binomial_coeff(n-1, k-1)

# In[209]:
# Rewrite the body of the function using nested conditional expressions.
# 
# This function is not very efficient because it ends up computing the same values over and over.
# Make it more efficient by memoizing it, as described in [Chapter 10](section_memos).

# In[210]:
# Solution

def binomial_coeff(n, k, cache={}):
    """Compute the binomial coefficient "n choose k".

    n: number of trials
    k: number of successes

    returns: int
    """
    if (n, k) in cache:
        return cache[n, k]
    
    res = 1 if k == 0 else (0 if n == 0 else 
                            binomial_coeff(n-1, k) + 
                            binomial_coeff(n-1, k-1))
    cache[n, k] = res
    return res

# In[211]:
binomial_coeff(10, 4)    # should be 210

# In[212]:
# ### Exercise
# 
# Here's the `__str__` method from the `Deck` class in [Chapter 17](section_print_deck).

# In[213]:
%%add_method_to Deck

    def __str__(self):
        res = []
        for card in self.cards:
            res.append(str(card))
        return '\n'.join(res)

# In[214]:
# Write a more concise version of this method with a list comprehension or generator expression.

# In[215]:
%%add_method_to Deck

    def __str__(self):            
        return '\n'.join(str(card) for card in self.cards)

# In[216]:
# You can use this example to test your solution.

# In[217]:
cards = Deck.make_cards()
deck = Deck(cards)
print(deck)

# In[218]:

# In[219]:
# [Think Python: 3rd Edition](https://allendowney.github.io/ThinkPython/index.html)
# 
# Copyright 2024 [Allen B. Downey](https://allendowney.com)
# 
# Code license: [MIT License](https://mit-license.org/)
# 
# Text license: [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-nc-sa/4.0/)

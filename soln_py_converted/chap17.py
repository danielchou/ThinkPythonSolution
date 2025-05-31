# 從 chap17.ipynb 轉換而來
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
# # Inheritance
# 
# The language feature most often associated with object-oriented programming is **inheritance**.
# Inheritance is the ability to define a new class that is a modified version of an existing class.
# In this chapter I demonstrate inheritance using classes that represent playing cards, decks of cards, and poker hands.
# If you don't play poker, don't worry -- I'll tell you what you need to know.

# In[3]:
# ## Representing cards
# 
# There are 52 playing cards in a standard deck -- each of them belongs to one of four suits and one of thirteen ranks. 
# The suits are Spades, Hearts, Diamonds, and Clubs.
# The ranks are Ace, 2, 3, 4, 5, 6, 7, 8, 9, 10, Jack, Queen, and King.
# Depending on which game you are playing, an Ace can be higher than King or lower than 2.
# 
# If we want to define a new object to represent a playing card, it is obvious what the attributes should be: `rank` and `suit`.
# It is less obvious what type the attributes should be.
# One possibility is to use strings like `'Spade'` for suits and `'Queen'` for ranks.
# A problem with this implementation is that it would not be easy to compare cards to see which had a higher rank or suit.
# 
# An alternative is to use integers to **encode** the ranks and suits.
# In this context, "encode" means that we are going to define a mapping between numbers and suits, or between numbers and ranks.
# This kind of encoding is not meant to be a secret (that would be "encryption").

# In[4]:
# For example, this table shows the suits and the corresponding integer codes:
# 
# 
# | Suit | Code |
# | --- | --- |
# |  Spades     |   3  |
# |  Hearts     |   2  |
# |  Diamonds   |   1  |
# |  Clubs      |   0  |
# 
# With this encoding, we can compare suits by comparing their codes.

# In[5]:
# To encode the ranks, we'll use the integer `2` to represent the rank `2`, `3` to represent `3`, and so on up to `10`.
# The following table shows the codes for the face cards.
# 
#   
# | Rank | Code |
# | --- | --- |
# |  Jack     |   11  |
# |  Queen   |   12  |
# |  King      |   13  |
# 
# And we can use either `1` or `14` to represent an Ace, depending on whether we want it to be considered lower or higher than the other ranks.
# 
# To represent these encodings, we will use two lists of strings, one with the names of the suits and the other with the names of the ranks.
# 
# Here's a definition for a class that represents a playing card, with these lists of strings as **class variables**, which are variables defined inside a class definition, but not inside a method.

# In[6]:
class Card:
    """Represents a standard playing card."""

    suit_names = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
    rank_names = [None, 'Ace', '2', '3', '4', '5', '6', '7', 
                  '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']

# In[7]:
# The first element of `rank_names` is `None` because there is no card with rank zero. By including `None` as a place-keeper, we get a list with the nice property that the index `2` maps to the string `'2'`, and so on.
# 
# Class variables are associated with the class, rather than an instance of the class, so we can access them like this.

# In[8]:
Card.suit_names

# In[9]:
# We can use `suit_names` to look up a suit and get the corresponding string.

# In[10]:
Card.suit_names[0]

# In[11]:
# And `rank_names` to look up a rank.

# In[12]:
Card.rank_names[11]

# In[13]:
# ## Card attributes
# 
# Here's an `__init__` method for the `Card` class -- it takes `suit` and `rank` as parameters and assigns them to attributes with the same names.

# In[14]:
%%add_method_to Card

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

# In[15]:
# Now we can create a `Card` object like this.

# In[16]:
queen = Card(1, 12)

# In[17]:
# We can use the new instance to access the attributes.

# In[18]:
queen.suit, queen.rank

# In[19]:
# It is also legal to use the instance to access the class variables.

# In[20]:
queen.suit_names

# In[21]:
# But if you use the class, it is clearer that they are class variables, not attributes.

# In[22]:
# ## Printing cards
# 
# Here's a `__str__` method for `Card` objects.

# In[23]:
%%add_method_to Card

    def __str__(self):
        rank_name = Card.rank_names[self.rank]
        suit_name = Card.suit_names[self.suit]
        return f'{rank_name} of {suit_name}' 

# In[24]:
# When we print a `Card`, Python calls the `__str__` method to get a human-readable representation of the card.

# In[25]:
print(queen)

# In[26]:
# The following is a diagram of the `Card` class object and the Card instance.
# `Card` is a class object, so its type is `type`.
# `queen` is an instance of `Card`, so its type is `Card`.
# To save space, I didn't draw the contents of `suit_names` and `rank_names`.

# In[27]:
from diagram import Binding, Value, Frame, Stack

bindings = [Binding(Value(name), draw_value=False)
            for name in ['suit_names', 'rank_names']]
    
frame1 = Frame(bindings, name='type', dy=-0.5, offsetx=0.77)
binding1 = Binding(Value('Card'), frame1)

bindings = [Binding(Value(name), Value(value))
            for name, value in zip(['suit', 'rank'], [1, 11])]
    
frame2 = Frame(bindings, name='Card', dy=-0.3, offsetx=0.33)
binding2 = Binding(Value('queen'), frame2)

stack = Stack([binding1, binding2], dy=-1.2)

# In[28]:
from diagram import diagram, Bbox, make_list, adjust

width, height, x, y = [2.11, 2.14, 0.35, 1.76]
ax = diagram(width, height)
bbox = stack.draw(ax, x, y)

value = make_list([])
bbox2 = value.draw(ax, x+1.66, y)

value = make_list([])
bbox3 = value.draw(ax, x+1.66, y-0.5)

bbox = Bbox.union([bbox, bbox2, bbox3])
#adjust(x, y, bbox)

# In[29]:
# Every `Card` instance has its own `suit` and `rank` attributes, but there is only one `Card` class object, and only one copy of the class variables `suit_names` and `rank_names`.

# In[30]:
# ## Comparing cards
# 
# Suppose we create a second `Card` object with the same suit and rank.

# In[31]:
queen2 = Card(1, 12)
print(queen2)

# In[32]:
# If we use the `==` operator to compare them, it checks whether `queen` and `queen2` refer to the same object.

# In[33]:
queen == queen2

# In[34]:
# They don't, so it returns `False`.
# We can change this behavior by defining the special method `__eq__`.

# In[35]:
%%add_method_to Card

    def __eq__(self, other):
        return self.suit == other.suit and self.rank == other.rank

# In[36]:
# `__eq__` takes two `Card` objects as parameters and returns `True` if they have the same suit and rank, even if they are not the same object.
# In other words, it checks whether they are equivalent, even if they are not identical.
# 
# When we use the `==` operator with `Card` objects, Python calls the `__eq__` method.

# In[37]:
queen == queen2

# In[38]:
# As a second test, let's create a card with the same suit and a different rank.

# In[39]:
six = Card(1, 6)
print(six)

# In[40]:
# We can confirm that `queen` and `six` are not equivalent.

# In[41]:
queen == six

# In[42]:
# If we use the `!=` operator, Python invokes a special method called `__ne__`, if it exists.
# Otherwise it invokes`__eq__` and inverts the result -- so if `__eq__` returns `True`, the result of the `!=` operator is `False`.

# In[43]:
queen != queen2

# In[44]:
queen != six

# In[45]:
# Now suppose we want to compare two cards to see which is bigger.
# If we use one of the relational operators, we get a `TypeError`.

# In[46]:
%%expect TypeError

queen < queen2

# In[47]:
# To change the behavior of the `<` operator, we can define a special method called `__lt__`, which is short for "less than".
# For the sake of this example, let's assume that suit is more important than rank -- so all Spades outrank all Hearts, which outrank all Diamonds, and so on.
# If two cards have the same suit, the one with the higher rank wins.
# 
# To implement this logic, we'll use the following method, which returns a tuple containing a card's suit and rank, in that order.

# In[48]:
%%add_method_to Card

    def to_tuple(self):
        return (self.suit, self.rank)

# In[49]:
# We can use this method to write `__lt__`.

# In[50]:
%%add_method_to Card

    def __lt__(self, other):
        return self.to_tuple() < other.to_tuple()

# In[51]:
# Tuple comparison compares the first elements from each tuple, which represent the suits.
# If they are the same, it compares the second elements, which represent the ranks.
# 
# Now if we use the `<` operator, it invokes the `__lt__` method.

# In[52]:
six < queen

# In[53]:
# If we use the `>` operator, it invokes a special method called `__gt__`, if it exists.
# Otherwise it invokes `__lt__` with the arguments in the opposite order.

# In[54]:
queen < queen2

# In[55]:
queen > queen2

# In[56]:
# Finally, if we use the `<=` operator, it invokes a special method called `__le__`.

# In[57]:
%%add_method_to Card

    def __le__(self, other):
        return self.to_tuple() <= other.to_tuple()

# In[58]:
# So we can check whether one card is less than or equal to another.

# In[59]:
queen <= queen2

# In[60]:
queen <= six

# In[61]:
# If we use the `>=` operator, it uses `__ge__` if it exists. Otherwise, it invokes `__le__` with the arguments in the opposite order.

# In[62]:
queen >= six

# In[63]:
# As we have defined them, these methods are complete in the sense that we can compare any two `Card` objects, and consistent in the sense that results from different operators don't contradict each other.
# With these two properties, we can say that `Card` objects are **totally ordered**.
# And that means, as we'll see soon, that they can be sorted.

# In[64]:
# ## Decks
# 
# Now that we have objects that represent cards, let's define objects that represent decks.
# The following is a class definition for `Deck` with
# an `__init__` method takes a list of `Card` objects as a parameter and assigns it to an attribute called `cards`.

# In[65]:
class Deck:

    def __init__(self, cards):
        self.cards = cards

# In[66]:
# To create a list that contains the 52 cards in a standard deck, we'll use the following static method.

# In[67]:
%%add_method_to Deck

    def make_cards():
        cards = []
        for suit in range(4):
            for rank in range(2, 15):
                card = Card(suit, rank)
                cards.append(card)
        return cards

# In[68]:
# In `make_cards`, the outer loop enumerates the suits from `0` to `3`.
# The inner loop enumerates the ranks from `2` to `14` -- where `14` represents an Ace that outranks a King.
# Each iteration creates a new `Card` with the current suit and rank, and appends it to `cards`.
# 
# Here's how we make a list of cards and a `Deck` object that contains it.

# In[69]:
cards = Deck.make_cards()
deck = Deck(cards)
len(deck.cards)

# In[70]:
# It contains 52 cards, as intended.

# In[71]:
# ## Printing the deck
# 
# Here is a `__str__` method for `Deck`.

# In[72]:
%%add_method_to Deck

    def __str__(self):
        res = []
        for card in self.cards:
            res.append(str(card))
        return '\n'.join(res)

# In[73]:
# This method demonstrates an efficient way to accumulate a large string -- building a list of strings and then using the string method `join`. 
# 
# We'll test this method with a deck that only contains two cards.

# In[74]:
small_deck = Deck([queen, six])

# In[75]:
# If we call `str`, it invokes `__str__`.

# In[76]:
str(small_deck)

# In[77]:
# When Jupyter displays a string, it shows the "representational" form of the string, which represents a newline with the sequence `\n`.
# 
# However, if we print the result, Jupyter shows the "printable" form of the string, which prints the newline as whitespace.

# In[78]:
print(small_deck)

# In[79]:
# So the cards appear on separate lines.

# In[80]:
# ## Add, remove, shuffle and sort
# 
# To deal cards, we would like a method that removes a card from the deck
# and returns it. The list method `pop` provides a convenient way to do
# that.

# In[81]:
%%add_method_to Deck

    def take_card(self):
        return self.cards.pop()

# In[82]:
# Here's how we use it.

# In[83]:
card = deck.take_card()
print(card)

# In[84]:
# We can confirm that there are `51` cards left in the deck.

# In[85]:
len(deck.cards)

# In[86]:
# To add a card, we can use the list method `append`.

# In[87]:
%%add_method_to Deck

    def put_card(self, card):
        self.cards.append(card)

# In[88]:
# As an example, we can put back the card we just popped.

# In[89]:
deck.put_card(card)
len(deck.cards)

# In[90]:
# To shuffle the deck, we can use the `shuffle` function from the `random` module:

# In[91]:
import random

# In[92]:
# This cell initializes the random number generator so we
# always get the same results.

random.seed(3)

# In[93]:
%%add_method_to Deck
            
    def shuffle(self):
        random.shuffle(self.cards)

# In[94]:
# If we shuffle the deck and print the first few cards, we can see that they are in no apparent order.

# In[95]:
deck.shuffle()
for card in deck.cards[:4]:
    print(card)

# In[96]:
# To sort the cards, we can use the list method `sort`, which sorts the elements "in place" -- that is, it modifies the list rather than creating a new list.

# In[97]:
%%add_method_to Deck
            
    def sort(self):
        self.cards.sort()

# In[98]:
# When we invoke `sort`, it uses the `__lt__` method to compare cards.

# In[99]:
deck.sort()

# In[100]:
# If we print the first few cards, we can confirm that they are in increasing order.

# In[101]:
for card in deck.cards[:4]:
    print(card)

# In[102]:
# In this example, `Deck.sort` doesn't do anything other than invoke `list.sort`.
# Passing along responsibility like this is called **delegation**.

# In[103]:
# ## Parents and children
# 
# Inheritance is the ability to define a new class that is a modified version of an existing class.
# As an example, let's say we want a class to represent a "hand", that is, the cards held by one player.
# 
# * A hand is similar to a deck -- both are made up of a collection of cards, and both require operations like adding and removing cards.
# 
# * A hand is also different from a deck -- there are operations we want for hands that don't make sense for a deck. For example, in poker we might compare two hands to see which one wins. In bridge, we might compute a score for a hand in order to make a bid.
# 
# This relationship between classes -- where one is a specialized version of another -- lends itself to inheritance. 
# 
# To define a new class that is based on an existing class, we put the name of the existing class in parentheses.

# In[104]:
class Hand(Deck):
    """Represents a hand of playing cards."""

# In[105]:
# This definition indicates that `Hand` inherits from `Deck`, which means that `Hand` objects can access methods defined in `Deck`, like `take_card` and `put_card`.
# 
# `Hand` also inherits `__init__` from `Deck`, but if we define `__init__` in the `Hand` class, it overrides the one in the `Deck` class.

# In[106]:
%%add_method_to Hand

    def __init__(self, label=''):
        self.label = label
        self.cards = []

# In[107]:
# This version of `__init__` takes an optional string as a parameter, and always starts with an empty list of cards.
# When we create a `Hand`, Python invokes this method, not the one in `Deck` -- which we can confirm by checking that the result has a `label` attribute.

# In[108]:
hand = Hand('player 1')
hand.label

# In[109]:
# To deal a card, we can use `take_card` to remove a card from a `Deck`, and `put_card` to add the card to a `Hand`.

# In[110]:
deck = Deck(cards)
card = deck.take_card()
hand.put_card(card)
print(hand)

# In[111]:
# Let's encapsulate this code in a `Deck` method called `move_cards`.

# In[112]:
%%add_method_to Deck

    def move_cards(self, other, num):
        for i in range(num):
            card = self.take_card()
            other.put_card(card)

# In[113]:
# This method is polymorphic -- that is, it works with more than one type: `self` and `other` can be either a `Hand` or a `Deck`.
# So we can use this method to deal a card from `Deck` to a `Hand`, from one `Hand` to another, or from a `Hand` back to a `Deck`.

# In[114]:
# When a new class inherits from an existing one, the existing one is called the **parent** and the new class is called the **child**. In general:
# 
# * Instances of the child class should have all of the attributes of the parent class, but they can have additional attributes.
# 
# * The child class should have all of the methods of the parent class, but it can have additional methods.
# 
# * If a child class overrides a method from the parent class, the new method should take the same parameters and return a compatible result.
# 
# This set of rules is called the "Liskov substitution principle" after computer scientist Barbara Liskov.
# 
# If you follow these rules, any function or method designed to work with an instance of a parent class, like a `Deck`, will also work with instances of a child class, like `Hand`.
# If you violate these rules, your code will collapse like a house of cards (sorry).

# In[115]:
# ## Specialization
# 
# Let's make a class called `BridgeHand` that represents a hand in bridge -- a widely played card game.
# We'll inherit from `Hand` and add a new method called `high_card_point_count` that evaluates a hand using a "high card point" method, which adds up points for the high cards in the hand.
# 
# Here's a class definition that contains as a class variable a dictionary that maps from card names to their point values.

# In[116]:
class BridgeHand(Hand):
    """Represents a bridge hand."""

    hcp_dict = {
        'Ace': 4,
        'King': 3,
        'Queen': 2,
        'Jack': 1,
    }

# In[117]:
# Given the rank of a card, like `12`, we can use `Card.rank_names` to get the string representation of the rank, and then use `hcp_dict` to get its score.

# In[118]:
rank = 12
rank_name = Card.rank_names[rank]
score = BridgeHand.hcp_dict.get(rank_name, 0)
rank_name, score

# In[119]:
# The following method loops through the cards in a `BridgeHand` and adds up their scores.

# In[120]:
%%add_method_to BridgeHand

    def high_card_point_count(self):
        count = 0
        for card in self.cards:
            rank_name = Card.rank_names[card.rank]
            count += BridgeHand.hcp_dict.get(rank_name, 0)
        return count

# In[121]:
# This cell makes a fresh Deck and 
# initializes the random number generator

cards = Deck.make_cards()
deck = Deck(cards)
random.seed(3)

# In[122]:
# To test it, we'll deal a hand with five cards -- a bridge hand usually has thirteen, but it's  easier to test code with small examples.

# In[123]:
hand = BridgeHand('player 2')

deck.shuffle()
deck.move_cards(hand, 5)
print(hand)

# In[124]:
# And here is the total score for the King and Queen.

# In[125]:
hand.high_card_point_count()

# In[126]:
# `BridgeHand` inherits the variables and methods of `Hand` and adds a class variable and a method that are specific to bridge.
# This way of using inheritance is called **specialization** because it defines a new class that is specialized for a particular use, like playing bridge.

# In[127]:
# ## Debugging
# 
# Inheritance is a useful feature.
# Some programs that would be repetitive without inheritance can be written more concisely with it.
# Also, inheritance can facilitate code reuse, since you can customize the behavior of a parent class without having to modify it.
# In some cases, the inheritance structure reflects the natural structure of the problem, which makes the design easier to understand.
# 
# On the other hand, inheritance can make programs difficult to read.
# When a method is invoked, it is sometimes not clear where to find its definition -- the relevant code may be spread across several modules.
# 
# Any time you are unsure about the flow of execution through your program, the simplest solution is to add print statements at the beginning of the relevant methods.
# If `Deck.shuffle` prints a message that says something like `Running Deck.shuffle`, then as the program runs it traces the flow of execution.
# 
# As an alternative, you could use the following function, which takes an object and a method name (as a string) and returns the class that provides the definition of the method.

# In[128]:
def find_defining_class(obj, method_name):
    """Find the class where the given method is defined."""
    for typ in type(obj).mro():
        if method_name in vars(typ):
            return typ
    return f'Method {method_name} not found.'

# In[129]:
# `find_defining_class` uses the `mro` method to get the list of class objects (types) that will be searched for methods.
# "MRO" stands for "method resolution order", which is the sequence of classes Python searches to "resolve" a method name -- that is, to find the function object the name refers to.
# 
# As an example, let's instantiate a `BridgeHand` and then find the defining class of `shuffle`.

# In[130]:
hand = BridgeHand('player 3')
find_defining_class(hand, 'shuffle')

# In[131]:
# The `shuffle` method for the `BridgeHand` object is the one in `Deck`.

# In[132]:
# ## Glossary
# 
# **inheritance:**
#  The ability to define a new class that is a modified version of a previously defined class.
# 
# **encode:**
#  To represent one set of values using another set of values by constructing a mapping between them.
# 
# **class variable:**
# A variable defined inside a class definition, but not inside any method.
# 
# **totally ordered:**
# A set of objects is totally ordered if we can compare any two elements and the results are consistent.
# 
# **delegation:**
# When one method passes responsibility to another method to do most or all of the work.
# 
# **parent class:**
# A class that is inherited from.
# 
# **child class:**
# A class that inherits from another class.
# 
# **specialization:**
# A way of using inheritance to create a new class that is a specialized version of an existing class.

# In[133]:
# ## Exercises

# In[134]:
# This cell tells Jupyter to provide detailed debugging information
# when a runtime error occurs. Run it before working on the exercises.

%xmode Verbose

# In[135]:
# ### Ask a Virtual Assistant
# 
# When it goes well, object-oriented programming can make programs more readable, testable, and reusable.
# But it can also make programs complicated and hard to maintain.
# As a result, OOP is a topic of controversy -- some people love it, and some people don't.
# 
# To learn more about the topic, ask a virtual assistant:
# 
# * What are some pros and cons of object-oriented programming?
# 
# * What does it mean when people say "favor composition over inheritance"?
# 
# * What is the Liskov substitution principle?
# 
# * Is Python an object-oriented language?
# 
# * What are the requirements for a set to be totally ordered?
# 
# And as always, consider using a virtual assistant to help with the following exercises.

# In[136]:
# ### Exercise
# 
# In contract bridge, a "trick" is a round of play in which each of four players plays one card.
# To represent those cards, we'll define a class that inherits from `Deck`.

# In[137]:
class Trick(Deck):
    """Represents a trick in contract bridge."""

# In[138]:
# As an example, consider this trick, where the first player leads with the 3 of Diamonds, which means that Diamonds are the "led suit".
# The second and third players "follow suit", which means they play a card with the led suit.
# The fourth player plays a card of a different suit, which means they cannot win the trick.
# So the winner of this trick is the third player, because they played the highest card in the led suit.

# In[139]:
cards = [Card(1, 3),
         Card(1, 10),
         Card(1, 12),
         Card(2, 13)]
trick = Trick(cards)
print(trick)

# In[140]:
# Write a `Trick` method called `find_winner` that loops through the cards in the `Trick` and returns the index of the card that wins.
# In the previous example, the index of the winning card is `2`.

# In[141]:
# You can use the following outline to get started.

# In[142]:
%%add_method_to Trick

    def find_winner(self):
        return 0

# In[143]:
%%add_method_to Trick

    def find_winner(self):
        lead = self.cards[0]
        
        top_index = 0
        top_rank = lead.rank
        
        for i, card in enumerate(self.cards):
            if card.suit == lead.suit and card.rank > top_rank:
                top_index = i
                top_rank = card.rank
                
        return top_index

# In[144]:
# If you test your method with the previous example, the index of the winning card should be `2`.

# In[145]:
trick.find_winner()

# In[146]:
# ### Exercise
# 
# The next few exercises ask to you write functions that classify poker hands.
# If you are not familiar with poker, I'll explain what you need to know.
# We'll use the following class to represent poker hands.

# In[147]:
class PokerHand(Hand):
    """Represents a poker hand."""

    def get_suit_counts(self):
        counter = {}
        for card in self.cards:
            key = card.suit
            counter[key] = counter.get(key, 0) + 1
        return counter
    
    def get_rank_counts(self):
        counter = {}
        for card in self.cards:
            key = card.rank
            counter[key] = counter.get(key, 0) + 1
        return counter    

# In[148]:
# `PokerHand` provides two methods that will help with the exercises.
# 
# * `get_suit_counts` loops through the cards in the `PokerHand`, counts the number of cards in each suit, and returns a dictionary that maps from each suit code to the number of times it appears.
# 
# * `get_rank_counts` does the same thing with the ranks of the cards, returning a dictionary that maps from each rank code to the number of times it appears.
# 
# All of the exercises that follow can be done using only the Python features we have learned so far, but some of them are more difficult than most of the previous exercises.
# I encourage you to ask a virtual assistant for help.
# 
# For problems like this, it often works well to ask for general advice about strategies and algorithms.
# Then you can either write the code yourself or ask for code.
# If you ask for code, you might want to provide the relevant class definitions as part of the prompt.

# In[149]:
# As a first exercise, we'll write a method called `has_flush` that checks whether a hand has a "flush" -- that is, whether it contains at least five cards of the same suit.
# 
# In most varieties of poker, a hand contains either five or seven cards, but there are some exotic variations where a hand contains other numbers of cards.
# But regardless of how many cards there are in a hand, the only ones that count are the five that make the best hand.

# In[150]:
# You can use the following outline to get started.

# In[151]:
%%add_method_to PokerHand

    def has_flush(self):
        """Checks whether this hand has a flush."""
        return False

# In[152]:
%%add_method_to PokerHand

    def has_flush(self):
        """Checks whether this hand has a flush."""
        counter = self.get_suit_counts()
        for count in counter.values():
            if count >= 5:
                return True
        return False

# In[153]:
# To test this method, we'll construct a hand with five cards that are all Clubs, so it contains a flush.

# In[154]:
good_hand = PokerHand('good_hand')

suit = 0
for rank in range(10, 15):
    card = Card(suit, rank)
    good_hand.put_card(card)
    
print(good_hand)

# In[155]:
# If we invoke `get_suit_counts`, we can confirm that the rank code `0` appears `5` times.

# In[156]:
good_hand.get_suit_counts()

# In[157]:
# So `has_flush` should return `True`.

# In[158]:
good_hand.has_flush()

# In[159]:
# As a second test, we'll construct a hand with three Clubs and two other suits.

# In[160]:
cards = [Card(0, 2),
         Card(0, 3),
         Card(2, 4),
         Card(3, 5),
         Card(0, 7),
        ]

bad_hand = PokerHand('bad hand')
for card in cards:
    bad_hand.put_card(card)
    
print(bad_hand)

# In[161]:
# So `has_flush` should return `False`.

# In[162]:
bad_hand.has_flush()

# In[163]:
# ### Exercise
# 
# Write a method called `has_straight` that checks whether a hand contains a straight, which is a set of five cards with consecutive ranks.
# For example, if a hand contains ranks `5`, `6`, `7`, `8`, and `9`, it contains a straight.
# 
# An Ace can come before a two or after a King, so `Ace`, `2`, `3`, `4`, `5` is a straight and so is `10`, `Jack`, `Queen`, `King`, `Ace`.
# But a straight cannot "wrap around", so `King`, `Ace`, `2`, `3`, `4` is not a straight.

# In[164]:
# You can use the following outline to get started.
# It includes a few lines of code that count the number of Aces -- represented with the code `1` or `14` -- and store the total in both locations of the counter.

# In[165]:
%%add_method_to PokerHand

    def has_straight(self, n=5):
        """Checks whether this hand has a straight with at least `n` cards."""
        counter = self.get_rank_counts()
        aces = counter.get(1, 0) + counter.get(14, 0)
        counter[1] = aces
        counter[14] = aces
        
        return False

# In[166]:
%%add_method_to PokerHand

    def has_straight(self, n=5):
        """Checks whether this hand has a straight."""
        counter = self.get_rank_counts()
        aces = counter.get(1, 0) + counter.get(14, 0)
        counter[1] = aces
        counter[14] = aces

        in_a_row = 0
        for i in range(1, 15):
            if counter.get(i, 0):
                in_a_row += 1
                if in_a_row == n:
                    return True
            else:
                in_a_row = 0
        return False

# In[167]:
# `good_hand`, which we created for the previous exercise, contains a straight.
# If we use `get_rank_counts`, we can confirm that it has at least one card with each of five consecutive ranks.

# In[168]:
good_hand.get_rank_counts()

# In[169]:
# So `has_straight` should return `True`.

# In[170]:
good_hand.has_straight()

# In[171]:
# `bad_hand` does not contain a straight, so `has_straight` should return `False`.

# In[172]:
bad_hand.has_straight()

# In[173]:
# ### Exercise
# 
# A hand has a straight flush if it contains a set of five cards that are both a straight and a flush -- that is, five cards of the same suit with consecutive ranks.
# Write a `PokerHand` method that checks whether a hand has a straight flush.

# In[174]:
# You can use the following outline to get started.

# In[175]:
%%add_method_to PokerHand

    def has_straightflush(self):
        """Check whether this hand has a straight flush."""
        return False

# In[176]:
%%add_method_to PokerHand

    def partition(self):
        """Make a list of four hands, each containing only one suit."""
        hands = []
        for i in range(4):
            hands.append(PokerHand())
            
        for card in self.cards:
            hands[card.suit].put_card(card)
            
        return hands

# In[177]:
%%add_method_to PokerHand

    def has_straightflush(self):
        """Check whether this hand has a straight flush."""
        for hand in self.partition():
            if hand.has_straight():
                return True
        return False

# In[178]:
# Use the following examples to test your method.

# In[179]:
good_hand.has_straightflush()     # should return True

# In[180]:
bad_hand.has_straightflush()     # should return False

# In[181]:
# Note that it is not enough to check whether a hand has a straight and a flush.
# To see why, consider the following hand.

# In[182]:
from copy import deepcopy

straight_and_flush = deepcopy(bad_hand)
straight_and_flush.put_card(Card(0, 6))
straight_and_flush.put_card(Card(0, 9))
print(straight_and_flush)

# In[183]:
# This hand contains a straight and a flush, but they are not the same five cards.

# In[184]:
 straight_and_flush.has_straight(), straight_and_flush.has_flush()

# In[185]:
# So it does not contain a straight flush.

# In[186]:
straight_and_flush.has_straightflush()    # should return False

# In[187]:
# ### Exercise
# 
# A poker hand has a pair if it contains two or more cards with the same rank.
# Write a `PokerHand` method that checks whether a hand contains a pair.

# In[188]:
# You can use the following outline to get started.

# In[189]:
%%add_method_to PokerHand

    def check_sets(self, *need_list):
        return True

# In[190]:
%%add_method_to PokerHand

    def check_sets(self, *need_list):
        counts = self.get_rank_counts()
        set_list = sorted(counts.values(), reverse=True)
        
        for need, have in zip(need_list, set_list):
            if need > have:
                return False
        return True

# In[191]:
%%add_method_to PokerHand

    def has_pair(self):
        return self.check_sets(2)

# In[192]:
# To test your method, here's a hand that has a pair.

# In[193]:
pair = deepcopy(bad_hand)
pair.put_card(Card(1, 2))
print(pair)

# In[194]:
pair.has_pair()    # should return True

# In[195]:
bad_hand.has_pair()    # should return False

# In[196]:
good_hand.has_pair()   # should return False

# In[197]:
# ### Exercise
# 
# A hand has a full house if it contains three cards of one rank and two cards of another rank.
# Write a `PokerHand` method that checks whether a hand has a full house.

# In[198]:
# You can use the following outline to get started.

# In[199]:
%%add_method_to PokerHand

    def has_full_house(self):
        return False

# In[200]:
%%add_method_to PokerHand

    def has_full_house(self):
        return self.check_sets(3, 2)

# In[201]:
# You can use this hand to test your method.

# In[202]:
boat = deepcopy(pair)
boat.put_card(Card(2, 2))
boat.put_card(Card(2, 3))
print(boat)

# In[203]:
boat.has_full_house()     # should return True

# In[204]:
pair.has_full_house()     # should return False

# In[205]:
good_hand.has_full_house()     # should return False

# In[206]:
# ### Exercise
# 
# This exercise is a cautionary tale about a common error that can be difficult to debug.
# Consider the following class definition.

# In[207]:
class Kangaroo:
    """A Kangaroo is a marsupial."""
    
    def __init__(self, name, contents=[]):
        """Initialize the pouch contents.

        name: string
        contents: initial pouch contents.
        """
        self.name = name
        self.contents = contents

    def __str__(self):
        """Return a string representaion of this Kangaroo.
        """
        t = [ self.name + ' has pouch contents:' ]
        for obj in self.contents:
            s = '    ' + object.__str__(obj)
            t.append(s)
        return '\n'.join(t)

    def put_in_pouch(self, item):
        """Adds a new item to the pouch contents.

        item: object to be added
        """
        self.contents.append(item)

# In[208]:
# `__init__` takes two parameters: `name` is required, but `contents` is optional -- if it's not provided, the default value is an empty list.
# 
# `__str__` returns a string representation of the object that includes the name and the contents of the pouch.
# 
# `put_in_pouch` takes any object and appends it to `contents`.
# 
# Now let's see how this class works.
# We'll create two `Kangaroo` objects with the names `'Kanga'` and `'Roo'`.

# In[209]:
kanga = Kangaroo('Kanga')
roo = Kangaroo('Roo')

# In[210]:
# To Kanga's pouch we'll add two strings and Roo.

# In[211]:
kanga.put_in_pouch('wallet')
kanga.put_in_pouch('car keys')
kanga.put_in_pouch(roo)

# In[212]:
# If we print `kanga`, it seems like everything worked.

# In[213]:
print(kanga)

# In[214]:
# But what happens if we print `roo`?

# In[215]:
print(roo)

# In[216]:
# Roo's pouch contains the same contents as Kanga's, including a reference to `roo`!
# 
# See if you can figure out what went wrong.
# Then ask a virtual assistant, "What's wrong with the following program?" and paste in the definition of `Kangaroo`.

# In[217]:

# In[218]:
# [Think Python: 3rd Edition](https://allendowney.github.io/ThinkPython/index.html)
# 
# Copyright 2024 [Allen B. Downey](https://allendowney.com)
# 
# Code license: [MIT License](https://mit-license.org/)
# 
# Text license: [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-nc-sa/4.0/)

# LTAT.03.001 - Introduction to Computer Programming @ Tartu Univesity - Project
# 11/2018
# This file implements the classes used in the program.

import datetime as dt # Necessary classes for due dates.

class Deck(object):
    # Basically should be really simple: A list of flashcards
    # with a few extra methods.
    def __init__(self, title):
        self.cards = []
        self.title = title
    
    def set_title(self, title):
        self.title = str(title)
    def get_title(self):
        return self.title
    
    def sort(self):
        self.cards.sort()
    
    def get_card(self, i):
        # in: int
        # returns a card itself.
        return self.cards[i]
    
    def get_card_display(self, i):
        # in: int
        # returns a 2-tuple of card back and front
        temp = self.cards[i]
        return (temp.get_front(),temp.get_back())
    
    def edit_card(self, i, performance):
        # in: int, int
        # updates card of given index, should sort after this.
        self.cards[i].card_update(performance)
        self.sort()
        
    def count_due(self):
        # out: int
        self.sort()
        
        n = 0
        time = dt.datetime.now()
        for card in self.cards:
            if card.get_next_due() <= time:
                n += 1
            else: 
                break
        return n
    
    def add_card(self, card):
        # in: Flashcard
        if type(card) == Flashcard:
            self.cards.append(card)
            
    def remove_card(self, card):
        # in: Flashcard
        # finds all cards with same front and back text
        while card in self.cards:
            del self.cards[self.cards.index(card)]
    
    def remove_card_i(self, i):
        # in: int
        # removes card by index
        del self.cards[i]
    def __len__(self):
        # how many cards total
        return len(self.cards)
    def __iter__(self):
        return iter(self.cards)
    
class Flashcard(object):
    # We'll be implementing the SuperMemo 2 algorithm to calculate due dates.
    # Hopefully this class will be extensible.
    def __init__(self, front, back, ease=2.5, streak=0, next_due=dt.datetime.now()):
        '''
         N/A, string, string, float >= 1.3, int, datetime
         Front is what is shown to user, the question, if you will.
         Back is the answer.
         Ease is a float, minimum 1.3. The larger this value is, the
        longer the time between due dates is going to be. Default of 2.5.
         Streak is self explanatory. The higher this is, the
        longer the difference between due dates again. Default of 0.
         Next due will be the date the flashcard is due. The default for this
        is going to be basically creation date.
        '''
        #  Assign the flashcard text.
        self.front = str(front)
        self.back  = str(back)
        self.ease  = ease
        self.streak   = streak
        self.next_due = next_due
    
    # Setting the card text.
    def get_front(self):
        # in: none
        # out: string
        return self.front
    def set_front(self, front):
        # in: string
        # out: none
        self.front = str(front)

    def get_back(self):
        # in: none
        # out: string
        return self.back
    def set_back(self, back):
        # in: string
        # out: none
        self.back = str(back)
    
    def get_ease(self): # used in due date calculation
        # in: none
        # out: float
        return self.ease
    def set_ease(self, ease):
        # in: float/int. using later methods, input bound to be float regardless.
        # out: none
        if ease <= 1.3:
            self.ease = 1.3
        else:
            self.ease = float(ease)
    
    def get_streak(self): # used in due date calculation
        # in: none
        # out: int
        return self.streak
    def set_streak(self, streak):
        # in: int
        # out: none
        if streak >= 0:
            self.streak = int(streak)
        else:
            self.streak = 0
    # Easy use functionality.
    def reset_streak(self): # to be used on incorrect answer
        self.set_streak(0)
    def iter_streak(self):  # to be used on   correct answer
        self.set_streak(self.get_streak() + 1)    
    
    def get_next_due(self):
        # in: none
        # out: dt.datetime
        return self.next_due
    
    def set_next_due(self, next_due): # DEBUG: keeping this one for debug purposes until no longer necessary
        # in: dt.datetime
        # out: none
        self.next_due = next_due
        
    def update_next_due(self, delta):
        # in: float/int, days to push next due forward relative to answer time.
        # out: none
        self.next_due = dt.datetime.now() + dt.timedelta(delta)
        
    def get_all_data(self):
        # in: none
        # out: returns list of all card data [str, str, float, int, datetime]
        return [self.get_front(), self.get_back(), self.get_ease(), self.get_streak(), self.get_next_due()]
    
    def card_update(self, performance):
        # in: integer from 0-5. Performance value assigned by user themselves via some interface.
        # out: none
        # This method implements SM2 and does the heavy lifting.
        # Nothing else should be necessary unless you wish to edit card data -
        # for example, to change the back and front.
        self.set_ease(self.get_ease() + (-0.8 + 0.28*performance + 0.02*performance**2))
        if performance < 3: # Failure states: 0, 1, 2
            self.reset_streak()
            self.update_next_due(1.0) # due in one day if incorrect
        else: # Correct states: 3, 4, 5
            self.iter_streak()
            self.update_next_due(6*self.get_ease()**(self.get_streak()-1))
    
    # Now to set the class magic methods.
    def __str__(self):
        # Conversion into string
        # What to show in the console upon print
        return "Front: \"{}\" Back: \"{}\" Ease: \"{}\" Streak: \"{}\" Due: \"{}\"".format(
            self.get_front(),self.get_back(),self.get_ease(),self.get_streak(),self.get_next_due())
    
    def __repr__(self):
        # Similar. Representation of the data - more or less how to recreate the card.
        return "Flashcard(\"{}\",\"{}\",{},{},{})".format(
            self.get_front(),self.get_back(),self.get_ease(),self.get_streak(),self.get_next_due().__repr__())
        # nasty direct call to magic method
    
    def __eq__(self, other):
        # Defines equality operator ==. We can use this to find duplicate cards.
        # Let's use only the front and back text for these ones.
        # Takes advantage of already existing string comparisons.
        return self.get_front() == other.get_front() and self.get_back() == other.get_back()
    def __ne__(self, other):
        # Defines inequality. Essentially inverse of previous.
        return not (self.get_front() == other.get_front() and self.get_back() == other.get_back())
    
    # more comparison operators
    # These should make it compatible with standard sorting functions
    # so that a list of flashcards can easily be sorted by their due dates
    # with the .sort() method.
    def __lt__(self, other):
        return self.get_next_due() <  other.get_next_due()
    def __gt__(self, other):
        return self.get_next_due() >  other.get_next_due()
    def __le__(self, other):
        return self.get_next_due() <= other.get_next_due()
    def __ge__(self, other):
        return self.get_next_due() >= other.get_next_due()
    # More card types can perhaps be added with inheritance.
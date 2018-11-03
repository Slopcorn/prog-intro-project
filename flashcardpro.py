# LTAT.03.001 - Introduction to Computer Programming @ Tartu Univesity - Project
# 11/2018

import datetime as dt # Necessary classes for due dates.

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
        #  Everything is going to have getter and setter methods
        # with checks built in to prevent disasters happening.
        self.front = str(front)
        self.back  = str(back)
        self.ease  = ease
        self.streak   = streak
        self.next_due = next_due
    
    # These will be simple, all good.
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
        # in: float, days to push next due forward relative to answer time.
        # out: none
        self.next_due = dt.datetime.now() + dt.timedelta(delta)
    '''
        an idea: incorrect card can be delayed by a day by use of certain input instead of automatically.
                 if wrong (performance 0) then set to current, (1, 2) push back a day, else (2-5) use SM2 algo.
    TODO: adding methods to automatically update all necessary card data based on a performance value.
          adding methods to be able to sort the cards by due date. any magic methods that may be of use.
          maybe there is a way to be able to use regular sort functions on a list of cards.
    '''
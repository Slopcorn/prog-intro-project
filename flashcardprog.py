# LTAT.03.001 - Introduction to Computer Programming @ Tartu Univesity - Project
# 11/2018
# This file implements the program functionality on command line.

import flashcardclasses as fc
deck_arr = [] # list of decks to be loaded in

####################################################

def load_data(filename = "data.txt", arr = deck_arr):
    # in: str, list
    # out: None
    # Loads the data from filename.
    file = open(filename, mode="r", encoding="UTF-8")
    data_iter = 0  # card data iterator
    data_list = [] # card data itself
    
    for line in file:
        if line[0] == '\t': # if flashcard data...
            data_iter += 1
        line = line.strip()
        if data_iter != 0: # subpar
            if data_iter < 3: # first two - strings
                data_list.append(line)
            elif data_iter < 4: # ease
                data_list.append(float(line))
            elif data_iter < 5: # streak
                data_list.append(int(line))
            elif data_iter == 5: # due
                data_list.append(fc.dt.datetime.fromtimestamp(float(line)))
                # adding cards to latest deck...
                arr[-1].load_card(fc.Flashcard(data_list[0],data_list[1],data_list[2],data_list[3],data_list[4]))
                data_list = [] # reset data list and iterator for new data
                data_iter = 0
        else: # if not data, add new deck to list.
            arr.append(fc.Deck(line))
    file.close()
    
def save_data(filename = "data.txt", arr = deck_arr):
    # in: str, list
    # out: None
    # Saves the current state decks and cards into filename.
    file = open(filename, mode="w", encoding="UTF-8")
    for deck in deck_arr:
        file.write(deck.get_title() + '\n')
        for card in deck:
            data = card.get_all_data()
            data[-1] = data[-1].timestamp() # unix timestamp
            for elem in data:
                file.write('\t' + str(elem) + '\n')            
    file.close()

def print_all_cards(reload = 0, arr = deck_arr):
    # in: int, list
    # prints all cards we have loaded
    if reload: # if reload is true, we'll load data in again.
        load_data()
    for deck in arr:
        print("Deck name: " + deck.get_title())
        for card in deck:
            print('\t' + str(card))

####################################################
# Try to load the data.
try:
    load_data()
except FileNotFoundError:
    save_data() # creates file should it not exist

####################################################
# Command line interface.
def main_screen():
    opt = {0: "q", 1: decks_screen, 2: study_screen}
    txt = ["Quit", "Decks", "Study"]

    for i in range(len(opt)):
        print("{}: {}".format(str(i), txt[i]))

    n = int(input("Option: "))
    return opt[n]

def decks_screen(arr = deck_arr):
    opt = {0:"q", 1: main_screen, 2: new_deck, 3: delete_deck, 4: edit_deck}
    txt = ["Quit", "Home", "New deck", "Delete deck", "Edit deck"]

    print("Your decks are currently as follows: ")
    for i in range(len(arr)):
        print("{}: {}, due: {}".format(str(i), arr[i].get_title(), arr[i].count_due()))
    
    for i in range(len(opt)):
        print("{}: {}".format(str(i), txt[i]))
    n = int(input("Option: "))
    return opt[n]

def new_deck(arr = deck_arr):
    title = input("Enter a title for your new deck: ")
    arr.append(fc.Deck(title))
    return decks_screen

def delete_deck(arr = deck_arr):
    n = int(input("Enter the number of the deck you wish to delete: "))
    del arr[n]
    return decks_screen

def edit_deck(arr = deck_arr):
    def new_card(deck):
        front = input("Enter front side of card: ")
        back =  input("Enter back side of card: ")
        deck.add_card(front, back)
    def delete_card(deck):
        n = int(input("Enter the number of the card you wish to delete: "))
        deck.remove_card_i(deck, n)
    def edit_card(deck):
        n = int(input("Enter the number of the card you wish to edit: "))
        print("Current card data: {}".format(deck.get_card(n)))

        active_card = deck.get_card(n)

        change_front_choice = input("Do you wish to change the front of the card? y/n: ")
        while change_front_choice.lower() != "y" and change_front_choice.lower() != "n":
            change_front_choice = input("Invalid input. Change the front of the card? y/n: ")
        if change_front_choice.lower() == "y":
            new_front = input("Enter the new front side of the card: ")
            active_card.set_front(new_front)

        change_back_choice = input("Do you wish to change the back of the card? y/n: ")
        while change_back_choice.lower() != "y" and change_back_choice.lower() != "n":
            change_back_choice = input("Invalid input. Change the back of the card? y/n: ")
        if change_back_choice.lower() == "y":
            new_back = input("Enter the new back side of the card: ")
            active_card.set_back(new_back)

        reset_data_choice = input("Do you wish to reset the data of the card? y/n: ")
        while reset_data_choice.lower() != "y" and reset_data_choice.lower() != "n":
            reset_data_choice = input("Invalid input. Reset the data of the card? y/n: ")
        if reset_data_choice.lower() == "y":
            active_card.card_reset()
        deck.replace_card(n, active_card)

    deck_n = int(input("Enter the number of the deck you wish to edit: "))
    active_deck = arr[deck_n]
    
    print_cards = input("Print all cards? y/n: ")
    while print_cards.lower() != "y" and print_cards.lower() != "n":
        print_cards = input("Invalid input. Print all cards? y/n: ")
    if print_cards.lower() == "y":
        for i in range(len(active_deck)):
            active_card = active_deck.get_card(i)
            front = active_card.get_front()
            back  = active_card.get_back()
            print("{}: Front: {}, Back: {}".format(str(i), front, back))
    
    opt = {0:"", 1: main_screen, 2: new_card, 3: delete_card, 4: edit_card}
    txt = ["Back to decks", "Home", "New card", "Delete card", "Edit card"]

    for i in range(len(opt)):
        print("{}: {}".format(str(i), txt[i]))
    n = int(input("Option: "))
    while n != 0:
        if n == 2 or n == 3 or n == 4:
            opt[n](arr[deck_n])
            n = int(input("Option: "))
        if n == 1:
            return opt[n]
    return decks_screen

def study_screen(arr=deck_arr):
    print("Your decks are currently as follows: ")
    for i in range(len(arr)):
        print("{}: {}, due: {}".format(str(i), arr[i].get_title(), arr[i].count_due()))
    n = int(input("Enter the number of the deck you wish to study with or -1 to cancel: "))
    if n == -1:
        return main_screen
    else:
        active_deck = arr[n]
        while active_deck.get_card().is_due():
            data = active_deck.get_card_display()
            print(data[0])
            input("Press enter to reveal back side.")
            print(data[1])
            print("Rate your ease of recall. -1 to quit.")
            performance = int(input("0: Failed, 4: Hard, 5: Medium, 6: Easy : "))
            while performance < -1 or performance > 6:
                performance = int(input("0: Failed, 4: Hard, 5: Medium, 6: Easy : "))
            if performance == -1:
                return study_screen
            active_deck.edit_card(0, performance)
            cont = input("Continue? y/n: ")
            while cont.lower() != "y" and cont.lower() != "n":
                cont = input("Invalid input. Continue? y/n: ")
            if cont.lower() == "n":
                return study_screen
        print("No more cards are due.")
        return study_screen
    
####################################################
# Program loop.
chosen = main_screen
while chosen != "q":
    chosen = chosen()
    save_data()
else:
    save_data()
    print("Goodbye!")
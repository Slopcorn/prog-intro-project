# LTAT.03.001 - Introduction to Computer Programming @ Tartu Univesity - Project
# 11/2018
# This file implements the program functionality on command line.
import flashcardclasses as fc

deck_arr = [] # list of decks to be loaded in

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
                arr[-1].add_card(fc.Flashcard(data_list[0],data_list[1],data_list[2],
                                 data_list[3],data_list[4]))
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
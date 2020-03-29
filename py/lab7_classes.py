#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 15:44:19 2020

@author: root
"""

import random

# =============================================================================
# Deck class
# Intialize each Deck with 52 Cards 
# =============================================================================
class Deck:

    def __init__(self):
        self.ranks = ['2','3','4','5','6','7','8','9','10','Jack','Queen','King','Ace']
        self.values = [2,3,4,5,6,7,8,9,10,11,12,13,14]
        self.suits = ['clubs', 'diamonds', 'hearts', 'spades']
        self.cards = []
        
        x = 0
        for i in range(len(self.suits)):
            for j in range(len(self.values)):
                card = Card(self.ranks[j], self.suits[i], self.values[j], x)
                self.cards.append(card)
                x += 1 

    def draw_card(self):
        card = self.cards[0]
        self.cards.pop(0)
        return card
    
    def return_card(self, card):
        self.cards.append(card)
    
    def shuffle_deck(self):
        random.shuffle(self.cards)
    
    def deck_is_empty(self):
        if len(self.cards) == 0:
            return True
        else:
            return False
        
    def reset_deck(self):
        self.cards = []
        x = 0
        for i in range(len(self.suits)):
            for j in range(len(self.values)):
                card = Card(self.ranks[j], self.suits[i], self.values[j], x)
                self.cards.append(card)
                x += 1  
        self.shuffle_deck()
   

# =============================================================================
# Card class
# Initialize each Card with given values
# =============================================================================
class Card: 
    
    def __init__(self, rank_val, suit_val, value_val, id_val):
        self.rank = rank_val
        self.suit = suit_val
        self.value = value_val
        self.id = id_val       

def score_round(p1_card, p2_card, d1, d2):
    if p1_card.value > p2_card.value:
        d1.return_card(p1_card)
        d1.return_card(p2_card)
        print("player1 won Round " + str(i+1))

    elif p1_card.value < p2_card.value:
        d2.return_card(p1_card)
        d2.return_card(p2_card)
        print("player2 won Round " + str(i+1))

    else:
        d1.return_card(p1_card)
        d2.return_card(p2_card)
        print("Round " + str(i+1) + " was a tie") 
        
    return d1, d2

# =============================================================================
#  Play game   
# =============================================================================

# Initialize round counter and input
i = 0
a =''

# Initialize decks and shuffle
d1 = Deck()
d2 = Deck()
d1.shuffle_deck()
d2.shuffle_deck()

while i < 5:
    a = input("\npress 1 to play card else quit \n")
    if int(a) == 1 :

        print('\nRound : ' + str(i+1) + '\n')
        
        p1_card = d1.draw_card()
        p2_card = d2.draw_card()
        
        print( 'player1 : ' + str(p1_card.rank + ' of ' + str(p1_card.suit)))
        print( 'player2 : ' + str(p2_card.rank + ' of ' + str(p2_card.suit)))
        
        d1, d2 = score_round(p1_card, p2_card, d1, d2)
    
        i += 1
    else:
        quit()
    
p1_score = sum([x.value for x in d1.cards])
p2_score = sum([x.value for x in d2.cards])

print("\nFinal scores:\nPlayer1: " + str(p1_score) + "\nPlayer2: " + str(p2_score))    
   
    
    
    
    
    
    
    
    
    
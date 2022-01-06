from random import *
from flask import render_template

class Card:
    '''Represents each card in the game, 25 instances come together to make the whole board'''
    def __init__(self, name, cardtype, revealed, position):
        self.name = name #name = word
        self.cardtype = cardtype #cardtype = color, death, or blank. 
        self.revealed = revealed #bool
        self.position = position #tuple (row, column)
    
    def __repr__(self):
        return f'Card({self.name}, {self.cardtype}, {self.revealed}, {self.position})'
    
    def __str__(self):
        return f'Card({self.name}, {self.cardtype}, {self.revealed}, {self.position})'

class Team:
    '''Represents each of the teams playing the game, 2 instances are created: blue and red'''
    def __init__(self, color, current_score = 0, winning_score = 8):
        self.color = color
        self.current_score = current_score
        self.winning_score = winning_score
    
    def __repr__(self):
        return self.color
    
    def __str__(self):
        return self.color

def print_cardtypes(cards):
    for n in range(5):
        for m in range(5):
            print(cards[n*5 + m].cardtype, end = '\t'*2)
        print()

def print_cardnames(cards):
    for n in range(5):
        for m in range(5):
            card = cards[n*5 + m]
            if card.revealed:
                #word = f'*{card.name}'
                #word = ''
                word = str(card.cardtype).upper()
            else:
                word = card.name
            endMult = 16 - len(word) #ensures each column is aligned
            print(word, end = ' '*endMult)
        print()

# Create instances for each Team
blue = Team('blue')
red = Team('red')

# Creates the cardtypes for the game, giving 1 team 9 and setting that team as the starting team
cardtypes = [blue]*8 + [red]*8 + ['death'] + ['blank']*7
current_team = choice([blue, red])
current_team.winning_score += 1
cardtypes.append(current_team)
shuffle(cardtypes)

# take the words from the file and create a list
wordfile = open("./words.txt", "r") 
wordlist = [x.strip() for x in wordfile]
shuffle(wordlist)
wordfile.close()

# create list of Cards
cards = []
for row in range(5):
    for column in range(5):
        name = wordlist.pop()
        cardtype = cardtypes.pop()
        card = Card(name, cardtype, False, (row, column))
        cards.append(card)

def gameover(winner, message=''):
    return render_template("gameover.html", winner=str(winner), message=message)

def other_team(team):
    '''Return the other team'''
    if team == blue:
        return red
    elif team == red:
        return blue

def lookup_card(word):
    for card in cards:
        if card.name.lower() == word.lower():
            return card

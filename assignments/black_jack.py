# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = True
outcome = ""
score = 0
in_progress = False

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.hand = []
        # create Hand object

    def __str__(self):
        cardset = []
        message = " "
        for i, v in enumerate(self.hand):
            cardset.append(str(self.hand[i]))
            message += cardset[i] + " "
        return 'Hand contains' + str(message)   # return a string representation of a hand

    def add_card(self, card):
        self.hand.append(card)  # add a card object to a hand

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
      
        values = []
        hand_value = 0
        for card in self.hand:
            a = card.get_rank()
            values.append(VALUES[a])
        aces = False
        for number in values:
            hand_value += number
            
            if number == 1:
                aces = True
                
        if not aces:
            return hand_value
        else:
            if hand_value + 10 <= 21:
                return hand_value +10
            else:
                return hand_value
            
            
    def draw(self, canvas, position):
        global player, dealer, pos_player, pos_dealer
        
        for i in self.hand:
            
            Card.draw(i, canvas, position)
            position[0] += CARD_SIZE[0]
            
        

        
# define deck class 
class Deck:
    def __init__(self):
        self.deck = []
        for i, v in enumerate(SUITS):
            for j, w in enumerate(RANKS):
                self.deck.append(Card(v, w))# create a Deck object

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck)

    def deal_card(self):
        a = self.deck.pop()
        return a    # deal a card object from the deck
    
    def __str__(self):
        cardset = []
        message = " "
        for i, v in enumerate(self.deck):
            cardset.append(str(self.deck[i]))
            message += cardset[i] + " "
        return 'Deck contains' + str(message) # return a string representation of a hand    # return a string representing the deck



#define event handlers for buttons
def deal():
    global outcome, in_play, deck, player, dealer, score, in_progress 
    outcome = ""
    # your code goes here
    if in_progress:
        outcome = "-1 for cheating!"
        score -= 1
    
    in_play = True
    deck = Deck()
    player = Hand()
    dealer = Hand()
    
    deck.shuffle()
    
    for i in range(0, 2):
        a = deck.deal_card()
        player.hand.append(a)
        b = deck.deal_card()
        dealer.hand.append(b)
    
    in_progress = True

def hit():
    global in_play, score, outcome, in_progress
    outcome = ""
    if in_play:
        if player.get_value() <= 21:
            a = deck.deal_card()
            player.hand.append(a)
            if player.get_value() > 21:
                outcome = "Busted!"
                in_progress = False
                in_play = False
                score -= 1

    # if the hand is in play, hit the player
   
    # if busted, assign a message to outcome, update in_play and score
       
def stand():
    global in_play, score, outcome, in_progress
    in_play = False
    if in_progress == False:
        return
    if outcome == "Busted!":
        return
    while dealer.get_value() < 17:
        a = deck.deal_card()
        dealer.hand.append(a)
        if dealer.get_value() > 21:
            outcome = "Dealer busted"
            in_progress = False
            score += 1
            return
        
    if dealer.get_value() >= player.get_value():
        outcome = "You lose!"
        in_progress = False
        score -= 1
    else:
        outcome = "You win!"
        in_progress = False
        score += 1

        # replace with your code below
   
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more

    # assign a message to outcome, update in_play and score

# draw handler    
def draw(canvas):
    global player, dealer, pos_player, pos_dealer, message
    # test to make sure that card.draw works, replace with your code below
    pos_player = [50, 400]
    player.draw(canvas, pos_player)
    pos_dealer = [50, 150]
    dealer.draw(canvas, pos_dealer)

    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [50 + CARD_BACK_SIZE[0] / 2, 150 + CARD_BACK_SIZE[1] / 2], CARD_BACK_SIZE)

    title = canvas.draw_text("Blackjack", [50, 80], 50, 'White')
    Dealer = canvas.draw_text("Dealer", [50, 130], 30, 'White')
    Player = canvas.draw_text("Player", [50, 380], 30, 'White')
    Score = canvas.draw_text(("Score: " + str(score)), [400, 130], 30, 'White')

    if in_play:
        canvas.draw_text("Hit or stand?", [150, 380], 30, 'White')
    else:
        canvas.draw_text("New deal?", [150, 380], 30, 'White')
    
    canvas.draw_text(str(outcome), [400, 300], 30, 'White')


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling

deal()
frame.start()


# remember to review the gradic rubric


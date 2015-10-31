# implementation of card game - Memory

import simplegui
import random
frame_size = (800, 100)
card_width = 50
card_height = 100
deck = []
opened = []
exposed = [False] * 16
turns = 0
message = "Turns = 0" 


# helper function to initialize globals
def new_game():
    global deck, turns, state, exposed
    for i, value in enumerate(exposed):
        exposed[i] = False
    deck1 = range(8)
    deck2 = range(8)
    deck = deck1 + deck2
    random.shuffle(deck)
    state = 0
    turns = 0
    label.set_text(message)
     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global state, exposed, opened, turns
        
    for i, card in enumerate(deck):
        card_x = card_width * i
        if pos[0] > card_x and pos[0] < card_x + card_width:
                
            if not exposed[i]:
                exposed[i] = True
                opened.append(i)
            else:
                return
                
            if state == 0:
                state = 1
            elif state == 1:
                turns += 1
                message = "Turns = " + str(turns)
                label.set_text(message)
                state = 2 
            else:
                state = 1
                if len(opened) > 2:           
                    if deck[opened[-3]] == deck[opened[-2]]:
                        pass  
                    else:
                        exposed[opened[-2]] = False
                        exposed[opened[-3]] = False
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    global pos_card, cards, card_pos, index
    pos_card = [card_width / 2, card_height / 2]
    for i, card in enumerate(deck):
        if exposed[i]:
            canvas.draw_text(str(card), pos_card, 24, "White")
            pos_card[0] += card_width
        else:
            index = 0
            canvas.draw_polygon([(pos_card[0] - card_width / 2, 0), 
                                 (pos_card[0] + card_width / 2, 0), 
                                 (pos_card[0] + card_width / 2, card_height), 
                                 (pos_card[0] - card_width / 2, card_height)], 
                                1, "White", "Green")
            pos_card[0] += card_width

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", frame_size[0], frame_size[1])
frame.add_button("Reset", new_game)
label = frame.add_label(message)

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric

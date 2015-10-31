# Implementation of classic arcade game Pong
# by Alexandra E.

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = -1
RIGHT = 1
# array of pong sounds to be randomly played
SOUNDS = [
    simplegui.load_sound("http://empact.io/pong/1.wav"),
    simplegui.load_sound("http://empact.io/pong/2.wav"),
    simplegui.load_sound("http://empact.io/pong/3.wav"),
    simplegui.load_sound("http://empact.io/pong/4.wav"),
]
fail = simplegui.load_sound("http://empact.io/pong/loser.mp3")

ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [0, 0]
paddle1_X = PAD_WIDTH / 2
paddle1_pos = [HEIGHT / 2 - PAD_HEIGHT / 2, HEIGHT / 2 + PAD_HEIGHT / 2]
paddle2_X = WIDTH - PAD_WIDTH / 2
paddle2_pos = [HEIGHT / 2 - PAD_HEIGHT / 2, HEIGHT / 2 + PAD_HEIGHT / 2]
paddle1_vel = [0, 0]
paddle2_vel = [0, 0]
player1 = 0
player2 = 0

# playing random sound
def play_sound():
    a = random.randrange(0, len(SOUNDS))
    SOUNDS[a].play()

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel 
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    ball_vel[0] = direction * random.randrange(2, 5)
    ball_vel[1] = -random.randrange(2, 5)

# define event handlers
def new_game():
    global player1, player2
    player1 = 0
    player2 = 0
    spawn_ball(RIGHT)

def try_collide():
    global ball_vel, player1, player2

    paddle_pos = None
    winner = None
    direction = None

    if ball_pos[0] - BALL_RADIUS <= PAD_WIDTH: # try left gutter
        paddle_pos = paddle1_pos
        winner = 2
        direction = RIGHT
    elif ball_pos[0] + BALL_RADIUS >= WIDTH - PAD_WIDTH: # try right gutter
        paddle_pos = paddle2_pos
        winner = 1
        direction = LEFT
    else:
        return

    if (ball_pos[1] + BALL_RADIUS >= paddle_pos[0] and ball_pos[1] - BALL_RADIUS <= paddle_pos[1]):
        ball_vel[0] = -ball_vel[0] * 0.1 - ball_vel[0]
        play_sound()
    else:
        fail.play()
        if winner == 1:
            player1 += 1
        else:
            player2 += 1
        spawn_ball(direction) 


def draw(canvas):
    global player1, player2
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # bounce off top and bottom
    if (ball_pos[1] - BALL_RADIUS <=0) or (ball_pos[1] + BALL_RADIUS >= HEIGHT):
        ball_vel[1] = -ball_vel[1]
        play_sound()
        
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "White", "White")
    
    # update paddle's vertical position, keep paddle on the screen
    for paddle_pos in (paddle1_pos, paddle2_pos):
        if paddle_pos[0] <= 0:
            paddle_pos[0] = 0
            paddle_pos[1] = PAD_HEIGHT
        if paddle_pos[1] >= HEIGHT:
            paddle_pos[0] = HEIGHT - PAD_HEIGHT
            paddle_pos[1] = HEIGHT
    
    # draw paddles
    paddle1_pos[0] += paddle1_vel[1]
    paddle1_pos[1] += paddle1_vel[1]
    paddle2_pos[0] += paddle2_vel[1]
    paddle2_pos[1] += paddle2_vel[1]
    
    canvas.draw_line([paddle1_X, paddle1_pos[0]], [paddle1_X, paddle1_pos[1]], PAD_WIDTH - 1, "White")
    canvas.draw_line([paddle2_X, paddle2_pos[0]], [paddle2_X, paddle2_pos[1]], PAD_WIDTH - 1, "White")
    
    # determine whether paddle and ball collide    
    try_collide()
        
    # draw scores
    canvas.draw_text(str(player1), [WIDTH / 4, HEIGHT / 8], 40, "White")
    canvas.draw_text(str(player2), [WIDTH - WIDTH / 4, HEIGHT / 8], 40, "White")
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    acc = 5
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel[1] -= acc
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel[1] += acc
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel[1] -= acc
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel[1] += acc

def keyup(key):
    global paddle1_vel, paddle2_vel
    paddle1_vel[1] = 0
    paddle2_vel[1] = 0

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.add_button("Restart", new_game, 200)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

# start frame
new_game()
frame.start()

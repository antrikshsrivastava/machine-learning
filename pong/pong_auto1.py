# Implementation of classic arcade game Pong
  
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random
  
# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400      
BALL_RADIUS = 5
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

MULTIPLIER = 2
max_bounces = 3
genome = 0
generation = 0
# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH/2, HEIGHT/2];    
    ball_vel = [MULTIPLIER * random.randrange(120, 240), MULTIPLIER * random.randrange(60, 180)]
    if (direction == RIGHT):  
        ball_vel[1] = -ball_vel[1]  
    if (direction == LEFT):  
        ball_vel[0] = -ball_vel[0]  
        ball_vel[1] = -ball_vel[1] 
  
# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel, bounce1, bounce2  # these are numbers
    global score1, score2  # these are ints
    paddle1_pos = HEIGHT / 2 
    paddle2_pos = HEIGHT / 2 
    paddle1_vel = 0 
    paddle2_vel = 0 
    score1 = 0 
    score2 = 0
    bounce1 = 0
    bounce2 = 0
  
    if score1 >= score2:  
        spawn_ball(LEFT)  
    else:  
        spawn_ball(RIGHT)
        

  
def draw(canvas):
    global generation, genome
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, bounce1, bounce2, total_bounces_nn, total_bounces_stupid_ai
    p2_vel = stupidai2(paddle2_pos+PAD_HEIGHT/2,ball_pos[1])
    print "[Generation: " + str(generation) + ", Genome: " + str(genome) + "] - Input: " + str(paddle2_pos+PAD_HEIGHT/2) + ", " + str("{0:.2f}".format(ball_pos[1])) + "->" + "{0:.2f}".format(p2_vel[0])
    if (p2_vel[0] < 0.5):
        paddle2_vel = MULTIPLIER * -6
    else:
        paddle2_vel = MULTIPLIER * 6
    paddle2_vel = (p2_vel[0] - 0.5) * MULTIPLIER * 12

    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
  
    #check ball left or right
    if (ball_pos[1] <= BALL_RADIUS) or (ball_pos[1] >= HEIGHT-BALL_RADIUS):    
        ball_vel[1] = -ball_vel[1]  
  
    if ball_pos[0] <= BALL_RADIUS:    
        if paddle1_pos - HALF_PAD_HEIGHT <= ball_pos[1]<=paddle1_pos + HALF_PAD_HEIGHT:    
            ball_vel[0] = -ball_vel[0]    
            ball_vel[0] = ball_vel[0]*1.1   
            ball_vel[1] = ball_vel[1]*1.1
            bounce1 += 1
            total_bounces_stupid_ai += 1
        else:    
            spawn_ball(RIGHT)    
            score2 += 1
            paddle1_pos = HEIGHT / 2
            paddle2_pos = HEIGHT / 2
            bounce2 += 1
  
  
    elif ball_pos[0] >= WIDTH-BALL_RADIUS:    
        if paddle2_pos - HALF_PAD_HEIGHT <= ball_pos[1] <= paddle2_pos + HALF_PAD_HEIGHT:    
            ball_vel[0] = -ball_vel[0]    
            ball_vel[0] = ball_vel[0]*1.1   
            ball_vel[1] = ball_vel[1]*1.1
            total_bounces_nn += 1
        else:    
            spawn_ball(LEFT)    
            score1 += 1
            paddle1_pos = HEIGHT / 2
            paddle2_pos = HEIGHT / 2

    ball_pos[0]+=ball_vel[0]/60   
    ball_pos[1]+=ball_vel[1]/60
    # draw ball
    canvas.draw_circle(ball_pos, 20, 1, "Green", "White")
    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos = ball_pos[1]
    if HALF_PAD_HEIGHT <= paddle1_pos + paddle1_vel <= HEIGHT - HALF_PAD_HEIGHT:  
        #paddle1_pos += paddle1_vel
        pass
    if HALF_PAD_HEIGHT <= paddle2_pos + paddle2_vel <= HEIGHT - HALF_PAD_HEIGHT:  
        paddle2_pos += paddle2_vel 
    # draw paddles
    canvas.draw_line([HALF_PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT],   
                [HALF_PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT],   
                PAD_WIDTH, "White")
    canvas.draw_line([WIDTH - HALF_PAD_WIDTH, paddle2_pos + HALF_PAD_HEIGHT],   
                [WIDTH - HALF_PAD_WIDTH, paddle2_pos - HALF_PAD_HEIGHT],   
                PAD_WIDTH, "White") 
    # draw scores
    canvas.draw_text(str(score1)+"  :  "+str(score2),   
                (WIDTH / 2 - 36, 40), 36, "Yellow")
    
    if total_bounces_nn > max_bounces or total_bounces_stupid_ai > max_bounces:
        frame.stop()
        

  
def keydown(key):
    global paddle1_vel, paddle2_vel, MULTIPLIER
    vel = 6
    if key == simplegui.KEY_MAP['s']:    
        paddle1_vel = vel    
    elif key == simplegui.KEY_MAP['w']:    
        paddle1_vel = -vel    
    elif key == simplegui.KEY_MAP['up']:    
        paddle2_vel = -vel    
    elif key == simplegui.KEY_MAP['down']:    
        paddle2_vel = vel
    # To slow down game
    elif key == simplegui.KEY_MAP['o']:
        if (MULTIPLIER >= 2):
            MULTIPLIER = MULTIPLIER / 2
    # To speed up game
    elif key == simplegui.KEY_MAP['p']:
        MULTIPLIER = MULTIPLIER * 2
    # To skip to next generation
    elif key == simplegui.KEY_MAP['l']:
        frame.stop()
  
 #Stop motion paddle       
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['s']:    
        paddle1_vel = 0   
    elif key == simplegui.KEY_MAP['w']:    
        paddle1_vel = 0   
    elif key == simplegui.KEY_MAP['up']:    
        paddle2_vel = 0   
    elif key == simplegui.KEY_MAP['down']:    
        paddle2_vel = 0 
  
def button_handler():   
    global score1,score2
    score1=0
    score2=0
    spawn_ball(RIGHT)
# create frame




stupidai1 = lambda y1,y2: 1 if y1 < y2 else -1
  
# start frame
def play(n, maximum_bounces, this_generation, this_genome):
    global stupidai2
    global frame
    global max_bounces
    global total_bounces_nn, total_bounces_stupid_ai
    global generation, genome
    generation = this_generation
    genome = this_genome
    total_bounces_nn = 0
    total_bounces_stupid_ai = 0
    max_bounces = maximum_bounces
    frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
    stupidai2 = n
    frame.set_draw_handler(draw)
    frame.set_keydown_handler(keydown)
    frame.set_keyup_handler(keyup)
    frame.add_button("New Game",button_handler)
    new_game()
    frame.start()


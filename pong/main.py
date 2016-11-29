try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

# Implementation of classic arcade game Pong
import random
import math

# initialize globals - pos and vel encode vertical info for paddles

WIDTH = 600  # Game area width. (Canvas width)
HEIGHT = 400  # Game area height. (Canvas height)

BALL_RADIUS = 10  # Radius of the ball in play. Note, not a diameter.

PAD_WIDTH = 8  # Width of the game paddle.
PAD_HEIGHT = 80  # Height of the game paddle.

# DEBUG = True      				# Turn on debugging lines and variable outputting.
DEBUG = False
# MAGICAL = True					# what is this?
MAGICAL = False

RIGHT_GUTTER = WIDTH - PAD_WIDTH  # Gutter = the area beyond the paddle.
LEFT_GUTTER = PAD_WIDTH  # Left gutter is simple enough.
ball_pos = [WIDTH / 2, HEIGHT / 2]  # Ball starts out in the center.
ball_vel = [0, 0]  # Ball velocity in multipliers (-1, 1) rather than absolute speed.

keys = simplegui.KEY_MAP  # For the sake of conciseness.
playing = False  # The game can be paused and will be paused after each match.

paddle1_pos = 0  # Left paddle's Y position
paddle2_pos = 0  # Right paddle's Y position

paddle1_vel = 0  # For me to be able to update paddles in the same function as everything else.
paddle2_vel = 0  # Again, in multipliers rather than absolute speed.

score1 = 0  # Score variables. Left paddle here.
score2 = 0  # Right paddle here :)

maxspeed = 2  # Try setting this to more than 10. I dare you.
default_maxspeed = 2  # Speed is reset to 2 by this.
SPEED_INCREMENT = 0.1  # Speed is incremented by 10% every paddle touch :L
do_speed_increment = True  # If we use speed incrementing, required for the course.

next_player = random.randint(0, 1) == 0  # First player is randomly picked.


## Sets ball initial velocity.
def ball_init(right):
    global ball_pos, ball_vel
    ball_vel[1] = -1
    if right:
        ball_vel[0] = 1
    else:
        ball_vel[0] = -1


## Game update function. Not drawing!
def update(c):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, playing
    global paddle1_vel, paddle2_vel, maxspeed
    ## This is where it gets crazy.

    ## Paddle bounds checks
    if paddle1_pos < 0: paddle1_pos = 0
    if paddle2_pos < 0: paddle2_pos = 0
    if paddle1_pos + PAD_HEIGHT >= HEIGHT: paddle1_pos = HEIGHT - PAD_HEIGHT - 1
    if paddle2_pos + PAD_HEIGHT >= HEIGHT: paddle2_pos = HEIGHT - PAD_HEIGHT - 1

    # ?!?!?
    if MAGICAL:
        paddle2_vel = stupidai(paddle2_pos + PAD_HEIGHT / 2, ball_pos[1])

    ## Paddle positioning and placement
    paddle1_pos = paddle1_pos + maxspeed * paddle1_vel
    paddle2_pos = paddle2_pos + maxspeed * paddle2_vel

    ## Ball:
    ## 1.  Bounds checks (red side walls)
    if (ball_pos[1] - BALL_RADIUS <= 0 or
                    ball_pos[1] + BALL_RADIUS >= HEIGHT):
        ball_vel[1] = -ball_vel[1]

    ## 2. Paddle bounce.
    if ((ball_pos[1] >= paddle2_pos and
                 ball_pos[1] < paddle2_pos + PAD_HEIGHT and
                     ball_pos[0] + BALL_RADIUS >= RIGHT_GUTTER)
        or
            (ball_pos[1] >= paddle1_pos and
                     ball_pos[1] < paddle1_pos + PAD_HEIGHT and
                         ball_pos[0] - BALL_RADIUS <= LEFT_GUTTER)):
        ball_vel[0] = -ball_vel[0]
        if do_speed_increment:
            maxspeed *= 1 + SPEED_INCREMENT

    ## 2.5 Missing the paddle. Reset ball!

    ## Separately for each paddle to set the winner of a game.
    elif ball_pos[0] + BALL_RADIUS >= RIGHT_GUTTER:
        # paddle1 win!
        resetgame(1)

    elif ball_pos[0] - BALL_RADIUS <= LEFT_GUTTER:
        # paddle2 win!
        resetgame(2)

    ## 3. Move the ball
    ball_pos[0] = ball_pos[0] + maxspeed * ball_vel[0]
    ball_pos[1] = ball_pos[1] + maxspeed * ball_vel[1]


def draw(c):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel

    ## There's a pause system now :)
    if playing:
        update(c)

    ## Gutter/Middle lines
    c.draw_line([WIDTH / 2, 0], [WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0], [PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([RIGHT_GUTTER, 0], [RIGHT_GUTTER, HEIGHT], 1, "White")

    ## Left paddle (manual rectangles <3)
    c.draw_polygon(
        [(0, paddle1_pos),
         (LEFT_GUTTER, paddle1_pos),
         (LEFT_GUTTER, paddle1_pos + PAD_HEIGHT),
         (0, paddle1_pos + PAD_HEIGHT)],
        1, "White", "White")

    ## Right paddle
    c.draw_polygon([(WIDTH, paddle2_pos),
                    (RIGHT_GUTTER, paddle2_pos),
                    (RIGHT_GUTTER, paddle2_pos + PAD_HEIGHT),
                    (WIDTH, paddle2_pos + PAD_HEIGHT)],
                   1, "White", "White")

    # draw ball and scores
    c.draw_circle(ball_pos, BALL_RADIUS, 1, "white", "white")

    c.draw_text("%d   %d" % (score1, score2), (WIDTH // 2 - 50, HEIGHT), 48, "silver", "sans-serif")

    if not playing:
        c.draw_text("Click to start game.", (100, 100), 48, "silver", "sans-serif")
    # Debug
    if DEBUG:
        # Informational texts.
        c.draw_text("Paddle 1 Y: %d V: %d" % (paddle1_pos, paddle1_vel), (10, 12), 12, "gray", "sans-serif")
        c.draw_text("Paddle 2 Y: %d V: %d" % (paddle2_pos, paddle2_vel), (10, 24), 12, "gray", "sans-serif")

        c.draw_text("Ball X: %d Y: %d, Vx: %d Vy: %d" % (ball_pos[0], ball_pos[1], ball_vel[0], ball_vel[1]), (10, 36),
                    12, "gray", "sans-serif")

        c.draw_text("score1: %d score2: %d" % (score1, score2), (10, 48), 12, "gray", "sans-serif")
        c.draw_text("game speed: %d" % maxspeed, (10, 60), 12, "gray", "sans-serif")
        c.draw_text("playing: %s" % playing, (10, 72), 12, "gray", "sans-serif")
        # Side collision lines.
        c.draw_line((0, BALL_RADIUS), (WIDTH, BALL_RADIUS), 1, "red")
        c.draw_line((0, HEIGHT - BALL_RADIUS), (WIDTH, HEIGHT - BALL_RADIUS), 1, "red")
        # Paddle collision lines.
        c.draw_line((LEFT_GUTTER + BALL_RADIUS, 0), (LEFT_GUTTER + BALL_RADIUS, HEIGHT), 1, "red")
        c.draw_line((RIGHT_GUTTER - BALL_RADIUS, 0), (RIGHT_GUTTER - BALL_RADIUS, HEIGHT), 1, "red")
        # Okay paddle collision lines
        c.draw_line((LEFT_GUTTER + BALL_RADIUS, paddle1_pos), (LEFT_GUTTER + BALL_RADIUS, paddle1_pos + PAD_HEIGHT), 1,
                    "green")
        c.draw_line((RIGHT_GUTTER - BALL_RADIUS, paddle2_pos), (RIGHT_GUTTER - BALL_RADIUS, paddle2_pos + PAD_HEIGHT),
                    1, "green")


def keydown(key):
    global paddle1_vel, paddle2_vel, playing
    if key == keys["up"]:
        # Right paddle UP!
        paddle2_vel = -1
    elif key == keys["down"]:
        # Right paddle DOWN!
        paddle2_vel = 1
    elif key == keys["w"]:
        # Left paddle UP!
        paddle1_vel = -1
    elif key == keys["s"]:
        paddle1_vel = 1

        # else nothing >_>


def keyup(key):
    global paddle1_vel, paddle2_vel, playing

    if key == keys["up"] or key == keys["down"]:
        paddle2_vel = 0
    elif key == keys["w"] or key == keys["s"]:
        paddle1_vel = 0
    ## Added them here to prevent infinite key spam
    elif key == keys["space"]:
        if playing:
            pausegame()
        else:
            startgame()
    elif key == keys["r"]:
        playing = False
        startgame()
        # else nothing


# Optional argument, because called by mouseclick handler.
def startgame(a=0):
    global playing
    if a:
        resetgame()
    # unpause!
    if not playing:
        playing = True


## Pauses the game.
def pausegame():
    global playing
    if playing:
        playing = False


## Simply restarts the game.
def resetgame(winner=0):
    global ball_pos, ball_vel, playing
    global score1, score2, next_player
    global maxspeed, default_maxspeed, do_speed_increment

    ball_pos = [WIDTH / 2, HEIGHT / 2]
    ball_vel = [0, 0]
    ## Resets max speed.
    if do_speed_increment:
        maxspeed = default_maxspeed

    playing = False
    if winner == 0:
        # Reset button clicked!
        ball_init(next_player)
        startgame()

    ## Win scores. Might want to use the multiplier here, oh how I want to!
    elif winner == 1:
        score1 += 1
        # is the next player the right one? no!
        next_player = False
    elif winner == 2:
        score2 += 1
        # is the next player the right one? yes!
        next_player = True


def reset_game(a=0):
    global score1, score2
    score1 = score2 = 0
    resetgame(0)


## Nothing to see here, move along
stupidai = lambda y1, y2: 1 if y1 < y2 else -1

### create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)

frame.add_button("Start", startgame, 50)
frame.add_button("Pause", pausegame, 50)
frame.add_button("Reset", reset_game, 50)

## Some keys to use.
frame.add_label("Pong")
frame.add_label("Up/down arrow for right paddle.")
frame.add_label("W/S for left paddle.")
frame.add_label("Space to pause/unpause.")

frame.set_draw_handler(draw)

frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(startgame)

# start frame
frame.start()

resetgame()

# Rubric:
# 1.  The ball spawns in the middle of the canvas with either an upward left or an upward right velocity.
# 2.  The ball bounces off of the top and bottom walls correctly.
# 3.  The ball respawns in the middle of the screen when it strikes the left or right gutter but not the paddles
# 4.  The left and right gutters are properly used as the edges.
# 5.  The ball spawns moving towards the player that won the last point.
# 6.  The 'w' and 's' keys correctly control the velocity of the left paddle as described above.
# 7.  The up and down arrows keys correctly control the velocity of the right paddle
# 8.  The edge of each paddle is flush with the gutter.
# 9.  The paddles stay on the canvas at all times
# 10. The ball correctly bounces off the left and right paddles.
# 11. The scoring text is positioned and updated appropriately.
# 12. Reset button that resets the score and restarts the game.

# Thanks for grading <3

# Bonus: Set MAGICAL to True to get some idiotic AI on the right side!
# You'll still play with W/S on the left tho.
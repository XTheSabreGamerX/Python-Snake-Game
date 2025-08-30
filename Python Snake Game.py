# The goal of the game is to control the snake (square) to collect
# circles to increase both the score and the length. If the snake
# hits itself or the surrounding border, it's game over.

import turtle
import random

# ===SETTINGS===
STEP = 20
DELAY_MS = 100
SCORE = 0
HIGH_SCORE = 0

# ===SCREEN SETUP===
wn = turtle.Screen()
wn.title("Matias - 02 Task Performance 1 - Snake Game")
wn.bgcolor("black")
wn.setup(width=800, height=600)
wn.tracer(0)

# ===SCORE DISPLAY===
pen = turtle.Turtle()
pen.speed(0)
pen.color('white')
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write('Score: 0', 'High Score: 0', align='center')

def update_score():
    pen.clear()
    pen.goto(0, 260)
    pen.write(f"Score: {SCORE}  High Score: {HIGH_SCORE}", align="center")

# ===GAME OVER===
pen_gameover = turtle.Turtle()
pen_gameover.speed(0)
pen_gameover.color('red')
pen_gameover.penup()
pen_gameover.hideturtle()

def game_over():
    global SCORE

    # Reset score
    SCORE = 0

    # Move segments off screen
    for s in segments:
        s.goto(1000, 1000)
    segments.clear()

    # Reset head
    head.goto(0, 0)
    head.direction = "stop"

    # Clear and redraw score
    pen.clear()
    pen.goto(0, 260)
    pen.write(f"Score: {SCORE}  High Score: {HIGH_SCORE}", align="center")

    # Show Game Over
    pen_gameover.clear()
    pen_gameover.goto(0, 0)
    pen_gameover.write("GAME OVER", align="center", font=("Courier", 36, "bold"))


# ===DRAW BORDER===
border = turtle.Turtle()
border.speed(0)
border.color('white')
border.pensize(3)
border.penup()
border.goto(-400, 300)
border.pendown()
for _ in range(2):
    border.forward(800)
    border.right(90)
    border.forward(600)
    border.right(90)
border.hideturtle()

# ===FOOD===
food = turtle.Turtle()
food.shape("circle")
food.color("pink")
food.penup()
food.goto(0, 100)

# ===SNAKE HEAD===
head = turtle.Turtle()
head.shape("square")
head.color("lime")
head.penup()
head.goto(0, 0)
head.direction = "stop"

# ===SNAKE BODY===
segments = []

# ===CONTROLS===
def move_up():
    if head.direction != "down":
        head.direction = "up"
        pen_gameover.clear()


def move_down():
    if head.direction != "up":
        head.direction = "down"
        pen_gameover.clear()


def move_left():
    if head.direction != "right":
        head.direction = "left"
        pen_gameover.clear()


def move_right():
    if head.direction != "left":
        head.direction = "right"
        pen_gameover.clear()


wn.listen()  # Bound to both lower and uppercase to ignore case for controls
wn.onkeypress(move_up, "w")
wn.onkeypress(move_up, "W")
wn.onkeypress(move_down, "s")
wn.onkeypress(move_down, "S")
wn.onkeypress(move_left, "a")
wn.onkeypress(move_left, "A")
wn.onkeypress(move_right, "d")
wn.onkeypress(move_right, "D")


# ===MOVEMENT UPDATE===
def move():
    x, y = head.xcor(), head.ycor()
    if head.direction == "up":
        head.sety(y + STEP)
    elif head.direction == "down":
        head.sety(y - STEP)
    elif head.direction == "left":
        head.setx(x - STEP)
    elif head.direction == "right":
        head.setx(x + STEP)


# ===MAIN LOOP===
def game_loop():
    global SCORE, HIGH_SCORE

    # Save head's previous location
    prev_x, prev_y = head.xcor(), head.ycor()
    move()

    # === MOVE BODY SEGMENTS (tail follows head) ===
    for i in range(len(segments)-1, 0, -1):
        x = segments[i-1].xcor()
        y = segments[i-1].ycor()
        segments[i].goto(x, y)

    if len(segments) > 0:
        segments[0].goto(prev_x, prev_y)

    # === CHECK COLLISION WITH FOOD ===
    if head.distance(food) < 20:
        # move food
        x = random.randint(-380, 380)
        y = random.randint(-280, 280)
        food.goto(x, y)

        # Update Score
        SCORE += 100
        if SCORE > HIGH_SCORE:
            HIGH_SCORE = SCORE

        update_score()

        # Create a new segment
        new_segment = turtle.Turtle()
        new_segment.shape('square')
        new_segment.color('green')
        new_segment.penup()

        if len(segments) > 0:
            last_x, last_y = segments[-1].xcor(), segments[-1].ycor()
            new_segment.goto(last_x, last_y)
        else:
            new_segment.goto(prev_x, prev_y)

        segments.append(new_segment)

    # === CHECK COLLISION WITH BODY ===
    for segment in segments:
        if head.distance(segment) < 20:
            game_over()
            break
        
    # ===CHECK COLLISION WITH BORDER===
    if head.xcor() > 390 or head.xcor() < -390 or head.ycor() > 290 or head.ycor() < -290:
        game_over()

    wn.update()
    wn.ontimer(game_loop, DELAY_MS)

game_loop()
wn.mainloop()
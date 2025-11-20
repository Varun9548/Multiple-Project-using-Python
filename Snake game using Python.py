from tkinter import *
import random

GAME_WIDTH = 1000
GAME_HEIGHT = 800
SPEED = 150
SPACE_SIZE = 40
BODY_PARTS = 3
SNAKE_COLOR = "purple"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"

class Snake:
    def __init__(self, canvas):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []
        self.canvas = canvas

        for i in range(BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = self.canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

class Food:
    def __init__(self, canvas):
        self.canvas = canvas
        self.spawn_food()

    def spawn_food(self):
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE - 1)) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE - 1)) * SPACE_SIZE
        self.coordinates = [x, y]
        self.canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

def next_turn(snake, food):
    global direction
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))
    square = snake.canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text="score: {}".format(score))
        snake.canvas.delete("food")
        food.spawn_food()
    else:
        del snake.coordinates[-1]
        snake.canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)

def change_direction(new_direction):
    global direction
    global current_direction
    current_direction = direction
    # Disallow reversing the direction
    if (new_direction == 'up' and current_direction != 'down') or \
       (new_direction == 'down' and current_direction != 'up') or \
       (new_direction == 'left' and current_direction != 'right') or \
       (new_direction == 'right' and current_direction != 'left'):
        direction = new_direction

def check_collisions(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        print("GAME OVER")
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            print("GAME OVER")
            return True

    return False

def game_over():
    Canvas.delete(ALL)
    Canvas.create_text(Canvas.winfo_width() / 2, Canvas.winfo_height() / 2, font=('consolas', 70),
                       text="GAME OVER", fill="red", tag="gameover")

window = Tk()
window.title("Snake Game")
window.resizable(False, False)

score = 0
direction = 'down'
label = Label(window, text="score: {}".format(score), font=('consolas', 40))
label.pack()

Canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
Canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int(screen_width / 2) - (window_width / 2)
y = int(screen_height / 2) - (window_height / 2)

window.geometry(f"{int(window_width)}x{int(window_height)}+{int(x)}+{int(y)}")

snake = Snake(Canvas)
food = Food(Canvas)

next_turn(snake, food)

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

window.mainloop()

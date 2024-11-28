from tkinter import *
from PIL import Image, ImageTk
import random
# Game configuration
GAME_WIDTH = 800
GAME_HEIGHT = 600
SPEED = 150
SPACE_SIZE = 50
BODY_PARTS = 3
BACKGROUND_IMAGE = "background.png"  # Background image
HEALTHY_FOODS = ["apple.png", "banana.png", "carrot.png"]  # Healthy food images
JUNK_FOODS = ["cake.png", "burger.png", "pizza.png"]  # Junk food images
SNAKE_COLOR = "#00FF00"
TEXT_COLOR = "#388BBA"
FOOD_COUNT = 5  # Number of healthy foods to spawn

# Snake class
class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(
                x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake"
            )
            self.squares.append(square)

    def grow(self):
        # Increase the snake's size by 1
        self.body_size += 1

# Healthy Food class
class HealthyFood:
    def __init__(self):
        self.food_items = []
        self.spawn_food()

    def spawn_food(self):
        canvas.delete("food")
        self.food_items = []

        for _ in range(FOOD_COUNT):
            x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
            y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE

            image = canvas.create_image(
                x + SPACE_SIZE // 2,
                y + SPACE_SIZE // 2,
                image=random.choice(healthy_food_images),
                tag="food",
            )
            self.food_items.append(([x, y], image))


# Junk Food (Obstacle) class
class JunkFood:
    def __init__(self):
        self.coordinates = []
        self.images = []
        self.generate_junk_food()

    def generate_junk_food(self):
        canvas.delete("obstacle")
        self.coordinates = []
        self.images = []

        for _ in range(random.randint(5, 10)):  # Random number of obstacles
            x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
            y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE

            self.coordinates.append([x, y])
            image = random.choice(junk_food_images)
            self.images.append(
                canvas.create_image(
                    x + SPACE_SIZE // 2, y + SPACE_SIZE // 2, image=image, tag="obstacle"
                )
            )


# Game logic
def next_turn(snake, food, junk_food):
    global direction, score

    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    # Wrap-around logic (snake passes through walls)
    x %= GAME_WIDTH
    y %= GAME_HEIGHT

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(
        x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR
    )
    snake.squares.insert(0, square)

    # Check if the snake eats any healthy food
    for food_coords, food_item in food.food_items:
        if x == food_coords[0] and y == food_coords[1]:
            score += 1
            label.config(text=f"Score: {score}")
            canvas.delete(food_item)
            food.food_items.remove((food_coords, food_item))

            # Grow the snake after eating healthy food
            snake.grow()

    # If all food is eaten, spawn new foods
    if not food.food_items:
        food.spawn_food()

    # If no food was eaten, remove the tail
    if len(snake.coordinates) > snake.body_size:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    # Check collisions
    if check_self_collision(snake) or check_junk_collision(snake, junk_food):
        game_over()
        return

    # Schedule the next turn
    window.after(SPEED, next_turn, snake, food, junk_food)


def change_direction(new_direction):
    global direction

    if new_direction == "left" and direction != "right":
        direction = new_direction
    elif new_direction == "right" and direction != "left":
        direction = new_direction
    elif new_direction == "up" and direction != "down":
        direction = new_direction
    elif new_direction == "down" and direction != "up":
        direction = new_direction


def check_self_collision(snake):
    x, y = snake.coordinates[0]
    return any(x == part[0] and y == part[1] for part in snake.coordinates[1:])


def check_junk_collision(snake, junk_food):
    x, y = snake.coordinates[0]
    return [x, y] in junk_food.coordinates


def game_over():
    canvas.delete(ALL)
    canvas.create_text(
        GAME_WIDTH / 2,
        GAME_HEIGHT / 2 - 40,
        font=("consolas", 50),
        text="GAME OVER",
        fill="red",
        tag="gameover",
    )
    restart_button.pack(pady=20)


def restart_game():
    global score, direction, snake, food, junk_food
    canvas.delete(ALL)
    canvas.create_image(0, 0, anchor=NW, image=background_image)  # Reset background
    restart_button.pack_forget()

    score = 0
    direction = "down"
    label.config(text=f"Score: {score}")

    snake = Snake()
    food = HealthyFood()
    junk_food = JunkFood()

    next_turn(snake, food, junk_food)


# Main program
window = Tk()
window.title("Snake Game - Health Habiter")
window.resizable(False, False)

score = 0
direction = "down"

label = Label(window, text=f"Score: {score}", font=("consolas", 30), fg=TEXT_COLOR)
label.pack(pady=10)

canvas = Canvas(window, width=GAME_WIDTH, height=GAME_HEIGHT)
canvas.pack()

# Load images
background_image = ImageTk.PhotoImage(Image.open(BACKGROUND_IMAGE).resize((GAME_WIDTH, GAME_HEIGHT)))
healthy_food_images = [
    ImageTk.PhotoImage(Image.open(img).resize((SPACE_SIZE, SPACE_SIZE))) for img in HEALTHY_FOODS
]
junk_food_images = [
    ImageTk.PhotoImage(Image.open(img).resize((SPACE_SIZE, SPACE_SIZE))) for img in JUNK_FOODS
]

# Set background image
canvas.create_image(0, 0, anchor=NW, image=background_image)

# Restart button
restart_button = Button(
    window, text="Restart", font=("consolas", 20), bg="#444444", fg=TEXT_COLOR, command=restart_game
)

# Bind keyboard events for controlling the snake
window.bind("<Left>", lambda event: change_direction("left"))
window.bind("<Right>", lambda event: change_direction("right"))
window.bind("<Up>", lambda event: change_direction("up"))
window.bind("<Down>", lambda event: change_direction("down"))

snake = Snake()
food = HealthyFood()
junk_food = JunkFood()

next_turn(snake, food, junk_food)

window.mainloop()

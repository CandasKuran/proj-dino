import customtkinter as ctk
import random
from PIL import Image, ImageTk

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")
        self.canvas = ctk.CTkCanvas(root, width=400, height=400, bg='black')
        self.canvas.pack()
        
        # Charger les images
        self.snake_image = ImageTk.PhotoImage(Image.open("snake_segment.png").resize((20, 20)))
        self.food_image = ImageTk.PhotoImage(Image.open("food.png").resize((20, 20)))
        
        self.snake = [(20, 20), (20, 30), (20, 40)]
        self.food = self.create_food()
        self.direction = 'Down'
        self.score = 0
        self.game_over = False
        self.draw_snake()
        self.draw_food()
        self.root.bind('<KeyPress>', self.change_direction)
        self.update()

    def create_food(self):
        while True:
            x = random.randint(0, 19) * 20
            y = random.randint(0, 19) * 20
            if (x, y) not in self.snake:
                return (x, y)

    def draw_snake(self):
        self.canvas.delete('snake')
        for segment in self.snake:
            self.canvas.create_image(segment[0], segment[1], anchor='nw', image=self.snake_image, tags='snake')

    def draw_food(self):
        self.canvas.delete('food')
        self.canvas.create_image(self.food[0], self.food[1], anchor='nw', image=self.food_image, tags='food')

    def change_direction(self, event):
        if event.keysym in ['Up', 'Down', 'Left', 'Right']:
            self.direction = event.keysym

    def update(self):
        if not self.game_over:
            self.move_snake()
            self.check_collisions()
            self.draw_snake()
            self.draw_food()
            self.root.after(100, self.update)

    def move_snake(self):
        head_x, head_y = self.snake[-1]
        if self.direction == 'Up':
            new_head = (head_x, head_y - 20)
        elif self.direction == 'Down':
            new_head = (head_x, head_y + 20)
        elif self.direction == 'Left':
            new_head = (head_x - 20, head_y)
        elif self.direction == 'Right':
            new_head = (head_x + 20, head_y)
        self.snake.append(new_head)
        if new_head == self.food:
            self.food = self.create_food()
            self.score += 1
        else:
            self.snake.pop(0)

    def check_collisions(self):
        head_x, head_y = self.snake[-1]
        if head_x < 0 or head_x >= 400 or head_y < 0 or head_y >= 400 or len(self.snake) != len(set(self.snake)):
            self.game_over = True
            self.canvas.create_text(200, 200, text="Game Over", fill="white", font=('Arial', 24))

root = ctk.CTk()
game = SnakeGame(root)
root.mainloop()
#!/usr/bin/env python3
"""
Snake Game - Tkinter GUI
Classic Snake with 10 levels, increasing speed, score & level display.
"""

import tkinter as tk
from tkinter import PhotoImage
import random
import os
import sys


def resource_path(relative_path):
    """Get absolute path to resource (works for dev and for PyInstaller)."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game - 10 Levels")
        self.root.resizable(False, False)
        self.root.configure(bg="#1a1a2e")

        # Load and set logo / window icon
        self.logo_img = None
        try:
            logo_path = resource_path("logo.png")
            self.logo_img = PhotoImage(file=logo_path)
            self.root.iconphoto(True, self.logo_img)
        except Exception:
            pass  # Continue without logo if missing

        # Game settings
        self.GAME_WIDTH = 600
        self.GAME_HEIGHT = 400
        self.SPACE_SIZE = 20
        self.BODY_PARTS = 3
        self.SNAKE_COLOR = "#00ff88"
        self.FOOD_COLOR = "#ff4757"
        self.BG_COLOR = "#0f0f1a"
        self.GRID_COLOR = "#1a1a2e"

        # Level system (1 → 10)
        # Speed in milliseconds (lower = faster)
        self.LEVEL_SPEEDS = {
            1: 120,
            2: 105,
            3: 90,
            4: 80,
            5: 70,
            6: 60,
            7: 50,
            8: 42,
            9: 35,
            10: 28,
        }
        # Points needed to reach each level
        self.LEVEL_THRESHOLDS = {
            1: 0,
            2: 50,
            3: 100,
            4: 160,
            5: 230,
            6: 310,
            7: 400,
            8: 500,
            9: 620,
            10: 760,
        }

        self.score = 0
        self.level = 1
        self.direction = "right"
        self.running = False
        self.SPEED = self.LEVEL_SPEEDS[1]

        # Top info bar (Score + Logo + Level)
        info_frame = tk.Frame(root, bg="#1a1a2e")
        info_frame.pack(pady=(8, 5), fill="x")

        self.score_label = tk.Label(
            info_frame,
            text="Score: 0",
            font=("Consolas", 15, "bold"),
            bg="#1a1a2e",
            fg="#00ff88",
            width=12,
            anchor="w",
        )
        self.score_label.pack(side=tk.LEFT, padx=(15, 0))

        # Logo in the center
        if self.logo_img:
            # Resize logo for the top bar (smaller version)
            self.logo_small = self.logo_img.subsample(2, 2)  # 64x64
            logo_label = tk.Label(info_frame, image=self.logo_small, bg="#1a1a2e")
            logo_label.pack(side=tk.LEFT, expand=True)
        else:
            # Fallback text logo
            tk.Label(
                info_frame,
                text="🐍 SNAKE",
                font=("Consolas", 14, "bold"),
                bg="#1a1a2e",
                fg="#00ff88",
            ).pack(side=tk.LEFT, expand=True)

        self.level_label = tk.Label(
            info_frame,
            text="Level: 1 / 10",
            font=("Consolas", 15, "bold"),
            bg="#1a1a2e",
            fg="#ffa502",
            width=14,
            anchor="e",
        )
        self.level_label.pack(side=tk.RIGHT, padx=(0, 15))

        # Canvas
        self.canvas = tk.Canvas(
            root,
            bg=self.BG_COLOR,
            height=self.GAME_HEIGHT,
            width=self.GAME_WIDTH,
            highlightthickness=0,
        )
        self.canvas.pack(padx=10, pady=5)

        self._draw_grid()

        # Buttons
        btn_frame = tk.Frame(root, bg="#1a1a2e")
        btn_frame.pack(pady=10)

        self.start_btn = tk.Button(
            btn_frame,
            text="▶ Start",
            font=("Consolas", 12, "bold"),
            bg="#00ff88",
            fg="#0f0f1a",
            activebackground="#00cc6a",
            activeforeground="#0f0f1a",
            relief="flat",
            padx=15,
            pady=5,
            command=self.start_game,
        )
        self.start_btn.pack(side=tk.LEFT, padx=5)

        self.restart_btn = tk.Button(
            btn_frame,
            text="↺ Restart",
            font=("Consolas", 12, "bold"),
            bg="#3742fa",
            fg="white",
            activebackground="#2f36c9",
            activeforeground="white",
            relief="flat",
            padx=15,
            pady=5,
            command=self.restart_game,
            state=tk.DISABLED,
        )
        self.restart_btn.pack(side=tk.LEFT, padx=5)

        # Instructions
        instructions = tk.Label(
            root,
            text="Use ← ↑ → ↓  or  W A S D   •   Levels 1–10 (speed increases)",
            font=("Consolas", 10),
            bg="#1a1a2e",
            fg="#a0a0b0",
        )
        instructions.pack(pady=(0, 10))

        # Key bindings
        self.root.bind("<Left>", lambda e: self.change_direction("left"))
        self.root.bind("<Right>", lambda e: self.change_direction("right"))
        self.root.bind("<Up>", lambda e: self.change_direction("up"))
        self.root.bind("<Down>", lambda e: self.change_direction("down"))
        self.root.bind("<a>", lambda e: self.change_direction("left"))
        self.root.bind("<d>", lambda e: self.change_direction("right"))
        self.root.bind("<w>", lambda e: self.change_direction("up"))
        self.root.bind("<s>", lambda e: self.change_direction("down"))

        # Center window
        self.root.update_idletasks()
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (w // 2)
        y = (self.root.winfo_screenheight() // 2) - (h // 2)
        self.root.geometry(f"+{x}+{y}")

        # Start message
        self.canvas.create_text(
            self.GAME_WIDTH // 2,
            self.GAME_HEIGHT // 2 - 20,
            text="Press START to play!",
            fill="#00ff88",
            font=("Consolas", 20, "bold"),
            tags="start_msg",
        )
        self.canvas.create_text(
            self.GAME_WIDTH // 2,
            self.GAME_HEIGHT // 2 + 20,
            text="10 Levels • Speed increases each level",
            fill="#a0a0b0",
            font=("Consolas", 12),
            tags="start_msg",
        )

    def _draw_grid(self):
        for i in range(0, self.GAME_WIDTH, self.SPACE_SIZE):
            self.canvas.create_line(i, 0, i, self.GAME_HEIGHT, fill=self.GRID_COLOR, width=1)
        for i in range(0, self.GAME_HEIGHT, self.SPACE_SIZE):
            self.canvas.create_line(0, i, self.GAME_WIDTH, i, fill=self.GRID_COLOR, width=1)

    def _update_labels(self):
        self.score_label.config(text=f"Score: {self.score}")
        self.level_label.config(text=f"Level: {self.level} / 10")

    def _check_level_up(self):
        """Increase level when score crosses the next threshold (max 10)."""
        if self.level >= 10:
            return

        next_level = self.level + 1
        if self.score >= self.LEVEL_THRESHOLDS[next_level]:
            self.level = next_level
            self.SPEED = self.LEVEL_SPEEDS[self.level]
            self._update_labels()

            # Brief level-up flash
            self.canvas.create_text(
                self.GAME_WIDTH // 2,
                40,
                text=f"LEVEL {self.level}!",
                fill="#ffa502",
                font=("Consolas", 18, "bold"),
                tags="level_up",
            )
            self.root.after(800, lambda: self.canvas.delete("level_up"))

    def start_game(self):
        if self.running:
            return

        self.canvas.delete("start_msg")
        self.canvas.delete("gameover")
        self.canvas.delete("level_up")

        self.running = True
        self.start_btn.config(state=tk.DISABLED)
        self.restart_btn.config(state=tk.NORMAL)

        self.score = 0
        self.level = 1
        self.SPEED = self.LEVEL_SPEEDS[1]
        self.direction = "right"
        self._update_labels()

        # Create snake
        self.snake_positions = []
        start_x = self.SPACE_SIZE * 3
        start_y = self.SPACE_SIZE * 5
        for i in range(self.BODY_PARTS):
            self.snake_positions.append((start_x - i * self.SPACE_SIZE, start_y))

        self.snake_squares = []
        for x, y in self.snake_positions:
            square = self.canvas.create_rectangle(
                x, y, x + self.SPACE_SIZE, y + self.SPACE_SIZE,
                fill=self.SNAKE_COLOR, outline="#00cc6a", width=1
            )
            self.snake_squares.append(square)

        self.food = None
        self.spawn_food()
        self.next_turn()

    def restart_game(self):
        self.running = False
        self.canvas.delete("all")
        self._draw_grid()
        self.start_btn.config(state=tk.NORMAL)
        self.restart_btn.config(state=tk.DISABLED)
        self.score = 0
        self.level = 1
        self.SPEED = self.LEVEL_SPEEDS[1]
        self._update_labels()

        self.canvas.create_text(
            self.GAME_WIDTH // 2,
            self.GAME_HEIGHT // 2 - 20,
            text="Press START to play!",
            fill="#00ff88",
            font=("Consolas", 20, "bold"),
            tags="start_msg",
        )
        self.canvas.create_text(
            self.GAME_WIDTH // 2,
            self.GAME_HEIGHT // 2 + 20,
            text="10 Levels • Speed increases each level",
            fill="#a0a0b0",
            font=("Consolas", 12),
            tags="start_msg",
        )

    def spawn_food(self):
        while True:
            x = random.randint(0, (self.GAME_WIDTH // self.SPACE_SIZE) - 1) * self.SPACE_SIZE
            y = random.randint(0, (self.GAME_HEIGHT // self.SPACE_SIZE) - 1) * self.SPACE_SIZE
            if (x, y) not in self.snake_positions:
                break

        if self.food:
            self.canvas.delete(self.food)

        self.food_pos = (x, y)
        self.food = self.canvas.create_oval(
            x + 2, y + 2, x + self.SPACE_SIZE - 2, y + self.SPACE_SIZE - 2,
            fill=self.FOOD_COLOR, outline="#ff6b81", width=1
        )

    def next_turn(self):
        if not self.running:
            return

        head_x, head_y = self.snake_positions[0]

        if self.direction == "left":
            head_x -= self.SPACE_SIZE
        elif self.direction == "right":
            head_x += self.SPACE_SIZE
        elif self.direction == "up":
            head_y -= self.SPACE_SIZE
        elif self.direction == "down":
            head_y += self.SPACE_SIZE

        new_head = (head_x, head_y)

        if self.check_collisions(new_head):
            self.game_over()
            return

        self.snake_positions.insert(0, new_head)

        square = self.canvas.create_rectangle(
            head_x, head_y, head_x + self.SPACE_SIZE, head_y + self.SPACE_SIZE,
            fill=self.SNAKE_COLOR, outline="#00cc6a", width=1
        )
        self.snake_squares.insert(0, square)

        # Ate food?
        if new_head == self.food_pos:
            self.score += 10
            self._update_labels()
            self._check_level_up()
            self.spawn_food()
        else:
            self.snake_positions.pop()
            self.canvas.delete(self.snake_squares.pop())

        self.root.after(self.SPEED, self.next_turn)

    def change_direction(self, new_direction):
        if not self.running:
            return
        opposites = {"left": "right", "right": "left", "up": "down", "down": "up"}
        if new_direction != opposites.get(self.direction):
            self.direction = new_direction

    def check_collisions(self, head):
        x, y = head
        if x < 0 or x >= self.GAME_WIDTH or y < 0 or y >= self.GAME_HEIGHT:
            return True
        if head in self.snake_positions[1:]:
            return True
        return False

    def game_over(self):
        self.running = False
        self.canvas.create_rectangle(
            60, self.GAME_HEIGHT // 2 - 60,
            self.GAME_WIDTH - 60, self.GAME_HEIGHT // 2 + 60,
            fill="#1a1a2e", outline="#ff4757", width=2, tags="gameover"
        )
        self.canvas.create_text(
            self.GAME_WIDTH // 2,
            self.GAME_HEIGHT // 2 - 25,
            text="GAME OVER",
            fill="#ff4757",
            font=("Consolas", 24, "bold"),
            tags="gameover",
        )
        self.canvas.create_text(
            self.GAME_WIDTH // 2,
            self.GAME_HEIGHT // 2 + 10,
            text=f"Score: {self.score}   •   Level: {self.level}/10",
            fill="#ffffff",
            font=("Consolas", 13),
            tags="gameover",
        )
        self.start_btn.config(state=tk.DISABLED)
        self.restart_btn.config(state=tk.NORMAL)


def main():
    root = tk.Tk()
    SnakeGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()

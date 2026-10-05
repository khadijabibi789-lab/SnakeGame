# Snake Game (Tkinter) – 10 Levels + Logo

A classic Snake game with a modern dark GUI, **10 progressive levels**, and a custom logo.

## Features
- Custom snake logo (window icon + top bar)
- 10 levels (speed increases each level)
- Score + Level display
- Smooth controls (Arrow keys + WASD)
- Game Over screen with final score & level
- Start / Restart buttons

## Level System

| Level | Points needed | Speed |
|-------|---------------|-------|
| 1     | 0             | Slow  |
| 2     | 50            |       |
| 3     | 100           |       |
| 4     | 160           |       |
| 5     | 230           |       |
| 6     | 310           |       |
| 7     | 400           |       |
| 8     | 500           |       |
| 9     | 620           |       |
| 10    | 760           | Fastest |

## Files

| File              | Description                          |
|-------------------|--------------------------------------|
| `snake_game.py`   | Main game + full GUI                 |
| `logo.png`        | Game logo (used as icon + header)    |
| `SnakeGame.spec`  | PyInstaller configuration file       |
| `build.bat`       | Windows build script                 |
| `build.sh`        | Linux / macOS build script           |
| `README.md`       | This file                            |

## Run the game

```bash
python snake_game.py
```

## Create executable

### Windows
```bash
build.bat
```

### Linux / macOS
```bash
chmod +x build.sh
./build.sh
```

The executable will appear in the `dist/` folder.  
(The logo is automatically bundled.)

## Controls
- **Arrow Keys** or **WASD** → Move the snake
- **Start** → Begin game
- **Restart** → Play again after Game Over

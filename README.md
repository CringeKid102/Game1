# Terminal Infiltration

## Overview
Terminal Infiltration is a stealth-based game where players control an agent infiltrating a secure facility. The objective is to complete a series of hacks while avoiding detection from guards and security systems.

## Project Structure
```
terminal-infiltration
├── assets
│   └── videos
│       └── hacking bg.mp4     # Video asset used as the animated background for the game.
├── src
│   ├── Stealth Game.py        # Main game logic, including classes for buttons, guards, and game state.
│   └── main.py                # (optional) Entry point for the game; current runnable script is Stealth Game.py.
├── requirements.txt           # Lists Python dependencies required for the project.
├── .gitignore                 # Specifies files and directories to be ignored by Git.
└── README.md                  # Documentation for the project, including setup instructions and gameplay details.
```

## Setup Instructions
1. Clone the repository:
   ```
   git clone <repository-url>
   cd terminal-infiltration
   ```

2. Install the required dependencies:
   ```
   pip install pygame opencv-python numpy
   ```

   - opencv-python (cv2) is used to decode and read MP4 frames.
   - numpy is used for frame array handling.

3. Ensure the background video exists at:
   - assets/videos/hacking bg.mp4

4. Run the game:
   ```
   python src/Stealth Game.py
   ```

## Gameplay
- Use the terminal to help the agent avoid detection.
- Complete 5 hacks before time runs out.
- Keep the detection level below 100% to succeed.

## Controls
- Click buttons to disable cameras, cut lights, create distractions, or hack systems.
- Monitor the status of guards and your detection level to strategize your moves.

## Video Background
The game now renders a looping MP4 background using the video located at `assets/videos/hacking bg.mp4`. Make sure the file is present and that `opencv-python` and `numpy` are installed for playback.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
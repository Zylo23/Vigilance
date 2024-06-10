# Vigilance Trigger Bot

Vigilance is an advanced trigger bot for detecting and responding to specific color patterns on the screen. This project is designed for educational purposes.

## Table of Contents

- [Vigilance Trigger Bot](#vigilance-trigger-bot)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Installation](#installation)
    - [Prerequisites](#prerequisites)
    - [Setup](#setup)
    - [Requirements](#requirements)
  - [Usage](#usage)
    - [Hotkeys](#hotkeys)
  - [Configuration](#configuration)
  - [License](#license)

## Features

- Detects specific color patterns on the screen
- Supports multiple detection modes with configurable delay
- Hotkey support for toggling bot state and switching modes
- Visual and audio feedback for status changes

## Installation

### Prerequisites

Ensure you have Python installed. This project uses Python 3.7 or higher.

### Setup

1. Clone the repository:

    ```sh
    git clone https://github.com/Zylo23/Vigilance.git
    cd Vigilance
    ```

2. Set up the virtual environment and install dependencies:

    ```sh
    setup.bat
    ```

### Requirements

The required Python packages are listed in `requirements.txt`:

```
colorama
mss
pillow
pyyaml
keyboard
numpy
mouse
```

## Usage

1. Activate the virtual environment and run the bot:

    ```sh
    run.bat
    ```

2. The bot will start running and you can use the specified hotkeys to control it.

### Hotkeys

- `Insert`: Toggle the bot's active state
- `Ctrl + Tab`: Switch detection modes

## Configuration

The configuration file `config.yaml` will be created automatically if it does not exist. You can modify the keys for toggling the bot and switching modes.

Default configuration:

```yaml
hold_key: 'shift'
toggle_key: 'insert'
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

Developed by [Zylo23](https://github.com/Zylo23)

Feel free to contribute to this project by submitting issues or pull requests.
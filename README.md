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
- Hotkey support for toggling bot state, switching modes, and adjusting detection zone size
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
colorama==0.4.6
keyboard==0.13.5
mouse==0.7.1
mss==9.0.1
Pillow==10.3.0
PyYAML==6.0.1
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
- `Ctrl + Up`: Increase detection zone size
- `Ctrl + Down`: Decrease detection zone size

## Configuration

The configuration file `config.yaml` will be created automatically if it does not exist. You can modify the keys for toggling the bot, switching modes, and adjusting the detection zone size.

Default configuration:

```yaml
hold_key: 'shift'
toggle_key: 'insert'
switch_mode_key: 'ctrl + tab'
increase_zone_key: 'ctrl + up'
decrease_zone_key: 'ctrl + down'
zone_size: 5
modes:
  - name: '0.3s Delayer'
    delay: 0.3
  - name: '0.25s Delayer'
    delay: 0.25
  - name: '0.2s Delayer'
    delay: 0.2
  - name: '0.15s Delayer'
    delay: 0.15
  - name: '0.1s Delayer'
    delay: 0.1
  - name: 'No Delay Full-Auto'
    delay: 0
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

Developed by [Zylo23](https://github.com/Zylo23)

Feel free to contribute to this project by submitting issues or pull requests.

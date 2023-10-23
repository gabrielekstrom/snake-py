# snake-py

snake-py is a simple terminal implementation of the classic snake game written in Python. It was written as a school project as part of the course *Tillämpad programmering*.

## Dependencies
* [Python](https://www.python.org/)
* Python `curses` module, [windows-curses](https://pypi.org/project/windows-curses/)

## Running the game

1. Make sure Python is installed. If you are on Windows you will also need to install the [windows-curses](https://pypi.org/project/windows-curses/) module.

2. Run the game
    ```console
    python src/snake.py
    ```

### Installation (Windows only)
1. Create a new Python virtual environment
    ```console
    python -m venv .venv
    ```
2. Activate the virtual environment
    ```console
    .\venv\Scripts\activate.bat
    ```
3. Install the required packages
    ```console
    python -m pip install -r requirements.txt
    ```
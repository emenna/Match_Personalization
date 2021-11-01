# Loper Match Automation

## Windows Setup

### Clone the project
Use git to clone the project, think about installing PyCharm as well (optional).

### Setup your environment
1. [Download Python3](https://www.python.org/downloads/) and follow instructions for install
2. [Download more ram](https://downloadmoreram.com/) (not really)

## Run the program
1. Navigate to the directory where the project is
2. Figure out the absolute path to the school content Excel
3. Figure out the absolute path to the users' directory (where the user Excels are)
4. Run the program ```python3 -m venv loper\cli.py --user_dir_path <user dir> --output_dir . --content_file_path <content file path>```
5. It should write the Excel to the current directory you're in
# Expense Settler
Expense sharing tool

## Features
+ Log each person's expenses in separate CSV files
+ Automatically calculates the amount each person should pay or receive
+ Logs the settlement details in a text file

## SetUp
1. Clone the GitHub repository
```bash
git clone https://github.com/ryu0315360/expense-settler.git
```
2. Navigate to the project folder and install the required Python packages.
```bash
cd path/to/expense-settler
pip install -r requirements.txt
```

## How to Use
1. Prepare CSV files for each participant with their expenses. Each CSV should be named **'<participant_name>.csv'** (i.e. andrew.csv), and contain entries in the following format:
```csv
2023-09-01,Lunch,25,share ## date, content, amount(int), whos
```
2. Place the CSV fils in the same directory as the script
3. Run the script
```bash
python settle.py
```

## TODO
1. more general purpose (date, names..)
2. better data structure. (pandas)

from expense import Expense
from reminder import Reminder

import matplotlib.pyplot as plt
from datetime import datetime

def main():
    file = "expense.csv"
    reminder_file = "reminder.csv"
    budget = 0
    options = ["Enter New Expense", "Summarize", "Set Budget", "Set Reminder", "Exit"]

    #Reminder Sys
    reminders = dict()
    with open(reminder_file, "r") as f:
        lines = f.readlines()

        for line in lines:
            reminder_name, reminder_day = line.split(",")
            if int(reminder_day) in reminders:
                reminders[int(reminder_day)].append(reminder_name)
            else:
                reminders[int(reminder_day)] = [reminder_name]
    
    day = int(datetime.now().day)

    if day in reminders:
        for rem in reminders[day]:
            print(f"{rem} due Today")

    while True:
        
        print("Select Option: ")

        for i, option in enumerate(options):
            print(f"{i+1}.\t{option}")
        
        opt = int(input("Enter Option:\t"))-1

        match opt:
            case 0:
                expense = getExpense()
                parseToCSV(expense, file)
            case 1:
                summarize(file, budget)
            case 2:
                budget = setBudget()
            case 3:
                setReminder()
            case 4:
                break

def getExpense():
    expense_name = input("Name of Expense: ")
    expense_amount = float(input("Enter Expense Amount: "))

    expense_category = [
        "Food",
        "Business",
        "Entertainment",
        "Investment",
        "Home",
        "Misc"
    ]

    while True:
        print("Select a Category: ")

        for i, category in enumerate(expense_category):
            print(f"{i+1}.\t{category}")

        valid_range = f"[1 to {len(expense_category)}]"
        idx = int(input(f"Enter a Category {valid_range}: "))-1

        if idx in range(len(expense_category)):
            new_expense = Expense(name=expense_name, category=expense_category[idx], amount=expense_amount)
            return new_expense
        else:
            print("Invalid Category. Please Enter Valid Category Number.")

def parseToCSV(expense: Expense, file):
    with open(file, "a") as f:
        f.write(f"{expense.name},{expense.category},{expense.amount}\n")

def summarize(file, budget):
    expenses: list[Expense] = []
    with open(file, "r") as f:
        lines = f.readlines()

        for line in lines:
            
            expense_name, expense_category, expense_amount = line.strip().split(",")
            expense_line = Expense(
                name=expense_name,
                category=expense_category,
                amount=float(expense_amount)
            )
            expenses.append(expense_line)
    
    categorize = dict()

    for expense in expenses:
        key = expense.category

        if key in categorize:
            categorize[key] += expense.amount
        else:
            categorize[key] = expense.amount
    
    total_expense = sum([ex.amount for ex in expenses])

    print(f"Total Expense: {total_expense:.2f}")

    remaining = budget-total_expense

    print(f"Remaining: {remaining:.2f}")

    #Bar Graph Category Wise

    plt.bar(list(categorize.keys()), list(categorize.values()), color="#C26B7E", width=0.01 )
    plt.xlabel("Categories")
    plt.ylabel("Amount")
    plt.title("Expense By Category")
    plt.show()

    plt.bar(0, total_expense, color="#587e6d", width=0.92)
    plt.bar(0,remaining, color="#813fed", width=0.92, bottom=total_expense)
    plt.legend(["Expense", "Remaining"])
    plt.title("Total Expense Vs Remaining")
    plt.show()

def setBudget():
    budget = float(input("Enter Budget:\t"))

    return budget

def setReminder():
    file = "reminder.csv"
    name = input("Enter Name of reminder: ")
    day= int(input("Enter Day of reminder: "))
    rem = Reminder(name, day)

    with open(file, "a") as f:
        f.write(f"{rem.name},{rem.date}\n")


if __name__=="__main__":
    main()
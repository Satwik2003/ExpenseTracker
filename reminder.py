class Reminder():
    def __init__(self, name, date):
        self.name = name
        self.date = date
        

    def __repr__(self):
        print(f"{self.name} due today.")

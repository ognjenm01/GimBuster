from datetime import datetime

class ExamTerm:
    def __init__(self, date, time, is_available, timestamp):
        self.date = date
        self.time = time
        self.is_available = is_available
        self.timestamp = timestamp

    def __str__(self):
        return self.date + ", " + self.time + ", " + str(self.is_available) + ", " + str(self.timestamp)
    
    def __eq__(self, other):
        return self.date == other.date and self.time == other.time and self.is_available == other.is_available
    
    def fancyprint(self):
        return self.date + " - " + self.time + " Poslednji put azurirano: " + str(self.timestamp)
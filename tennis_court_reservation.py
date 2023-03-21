import datetime
import json
import csv


class ReservationSystem:

    def __init__(self):
        self.reservations = []


    def get_num_reservations_for_user(self, name, date):
        count = 0
        for reservation in self.reservations:
            if reservation["name"] == name and reservation["date"].date() == date.date():
                count += 1
        return count
        
    
    def is_court_available(self, date, duration):
        end_time = date + duration
        for reservation in self.reservations:
            if date < reservation["date"] + reservation["duration"] and end_time > reservation["date"]:
                return False
            return True
        
    
    def self_closest_available_time(self, date):
        delta = datetime.timedelta(minutes=30)
        while True:
            if self.is_court_available(date, datetime.timedelta(minutes=60)):
                return date.strftime("%A, %d %B %Y, %H:%M")
            date += delta
    

    def get_reservation_for_user(self, name, date):
        for reservation in self.reservations:
            if reservation["name"] == name and reservation["date"] == date:
                return reservation
            return None
    

    def get_reservations_for_day(self, date):
        reservations_for_day = []
        for reservation in self.reservations:
            if reservation["date"].date() == date.date():
                reservations_for_day.append(reservation)
        return reservations_for_day


    def add_reservation(self, name, date, duration):
        if self.get_num_reservations_for_user(name, date) >= 2:
            raise ValueError("Masz już 2 rezerwacje w tym tygodniu")
        
        if date - datetime.datetime.now() < datetime.timedelta(hours = 1):
            raise ValueError("Rezerwacji można dokonać minimum godzinę przed planowanym czasem gry")
        
        if not self.is_court_available(date, duration):
            closest_time = self.self_closest_available_time(date)
            raise ValueError(f"Kort jest zajęty w tym czasie. Najbliższy wolny termin jest {closest_time}.")
        
        self.reservations.append({"name": name, "date": date, "duration": duration})
    
    
    def cancel_reservation(self, name, date):
        reservation = self.get_reservation_for_user(name, date)

        if reservation is None:
            raise ValueError("Nie ma Twojej rezerwacji w tym czasie")
        
        if reservation["date"] - datetime.datetime.now() < datetime.timedelta(hours=1):
            raise ValueError("Rezerwacje można anulować co najmniej godzinę przed czasem gry")

        self.reservations.remove(reservation)


    def print_schedule(self, start_date, end_date):
        current_date = start_date

        while current_date <= end_date:
            reservations_for_day = self.get_reservations_for_day(current_date)
            if reservations_for_day:
                print(current_date.strftime("%A, %d %B %Y"))
                for reservation in reservations_for_day:
                    start_time = reservation["date"].strftime("%H:%M")
                    end_time = (reservation["date"] + reservation["duration"]).strftime("%H:%M")
                    print(f"* {reservation['name']} {start_time} - {end_time}")
            else:
                print(current_date.strftime("%A, %d %B %Y"))
                print("No reservations")
            print()
            current_date += datetime.timedelta(days=1)
    

    def save_schedule(self, start_date, end_date, format, file_name):
        schedule = {"reservations": []}
        current_date = start_date

        while current_date <= end_date:
            reservations_for_day = self.get_reservations_for_day(current_date)
            for reservation in reservations_for_day:
                start_time = reservation["date"].strftime("%H: %M")
                end_time = (reservation["date"] + datetime.timedelta(minutes=reservation["duration"])).strftime("%H: %M")
                reservation_entry = {
                    "name": reservation["name"],
                    "start_time": start_time,
                    "end_time": end_time,
                    "date": current_date.strftime("%Y-%m-%d")}
                schedule["reservations"].append(reservation_entry)
            current_date += datetime.timedelta(days=1)
            
        if format == "json":
            with open(file_name, "w") as file:
                json.dump(schedule, file, indent=4)
        elif format == "csv":
            with open(file_name, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Name", "Date", "Start time", "End time"])
                for reservation in schedule["reservations"]:
                    writer.writerow([reservation["name"], reservation["date"].strftime("%Y-%m-%d"), reservation["start_time"], reservation["end_time"]])
        else:
            print("Niewłaściwy format pliku. Właściwym formatem jest 'json' lub 'csv'.")
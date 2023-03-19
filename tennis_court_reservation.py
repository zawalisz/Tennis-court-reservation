import datetime


class ReservationSystem:

    def __init__(self):
        self.reservations = []


    def add_reservation(self, name, date, duration):
        if self.get_num_reservations_for_user(name, date) >= 2:
            raise ValueError("Masz już 2 rezerwacje w tym tygodniu")
        
        if date - datetime.datetime.now() < datetime.timedelta(hour = 1):
            raise ValueError("Rezerwacji można dokonać minimum godzinę przed planowanym czasem gry")
        
        if not self.is_court_available(date, duration):
            closest_time = self_closest_available_time(date)
            raise ValueError("Kort jest zajęty w tym czasie. Najbliższy wolny termin jest {closest_time}.")
        
        self.reservations.append({"name": name, "date": date, "duration": duration})
    
    
    def cancel_reservation(self, name, date):
        reservation = self.get_reservation_for_user(name, date)

        if reservation is None:
            raise ValueRrror("Nie ma Twojej rezerwacji w tym czasie")
        
        if reservation ["date"] - datatime.datetime.now() < datetime.timedelta(hours=1):
            raise ValueError("Rezerwacje można anulować co najmniej godzinę przed czasem gry")

        self.reservations.remove(reservation)


    def print_shedule(self, start_date, end_date):
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
    

    def save_shedule(self, start_date, end_date, format, file_name):
        shedule = {"reservations": []}
        current_date = start_date
        while current_date <= end_date:
            reservations_for_day = self.get_reservations_for_day(current_date)
            for reservation in reservations_for_day:
                start_time = reservation["date"].strftime("%H: %M")
                end_time = reservation(["date"] + timedelta(minutes=reservation["duration"])).strftime("%H: %M")
                reservation_entry = {"name": reservation["name"], "start_time": start_time, "end_time": end_time, "date": current_date.strftime("%d-%m-%Y")}
                shedule["reservations"].append(reservation_entry)
                current_date += timedelta(days=1)

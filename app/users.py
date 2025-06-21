from datetime import date, datetime
from pathlib import Path
import csv

class User:

    def __init__(self, username, sex, height, birthday):
        self._username = username
        self._sex = sex
        self._height = height
        self._birthdate = birthday  # This will trigger the setter and calculate age
        self.age_in_years = float(self.age[0] + self.age[1])
        if sex == "Male":
            self.minimum_optimal_body_fat_perc = 0.10 * float(self.age_in_years) + 5
            self.maximum_optimal_body_fat_perc = 0.10 * float(self.age_in_years) + 15
        else:
            self.minimum_optimal_body_fat_perc = 0.12 * float(self.age_in_years) + 7
            self.maximum_optimal_body_fat_perc = 0.12 * float(self.age_in_years) + 17
        self.csv_file_name = f"userdata_{username}.csv" # this is a string
        self.calculations_file = Path(self.csv_file_name) # this is an object

    @property
    def username(self):
        return self._username

    @property
    def sex(self):
        return self._sex
    
    @property
    def height(self):
        return self._height
    
    @property
    def birthdate(self):
        return self._birthdate

    @property
    def age(self):
        return User.calculate_age(self._birthdate)

    @username.setter
    def username(self, new_username):
        self._username = new_username
    
    @sex.setter
    def sex(self, new_sex):
        self._sex = new_sex

    @height.setter
    def height(self, new_height):
        self._height = new_height

    @birthdate.setter
    def birthdate(self, new_birthday):
        if isinstance(new_birthday, str):
            new_birthday = datetime.strptime(new_birthday, "%d/%m/%Y").date()
        self._birthdate = new_birthday

    @age.setter
    def age(self, new_age):
        self._birthdate = User.calculate_birthdate(new_age)

    @username.deleter
    def username(self):
        del self._username

    @sex.deleter
    def sex(self):
        del self._sex
    
    @height.deleter
    def height(self):
        del self._height

    @birthdate.deleter
    def birthdate(self):
        del self._birthdate
        del self._age
    
    @staticmethod
    def calculate_age(birthdate):
        if isinstance(birthdate, str):
            birthdate = datetime.strptime(birthdate, "%d/%m/%Y").date()   
        today = date.today()
        years = today.year - birthdate.year
        months = today.month - birthdate.month
        days = today.day - birthdate.day
        # Adjust for negative months or days
        if days < 0:
            months -= 1
            days += 30  # Assuming 30 days in a month for simplicity
        if months < 0:
            years -= 1
            months += 12
        return f"{years}y/{months}m/{days}d"

    @staticmethod
    def calculate_birthdate(age):
        # Split age string into years, months, and days
        age_parts = age.split('/')
        years = int(age_parts[0][:-1])
        months = int(age_parts[1][:-1])
        days = int(age_parts[2][:-1])
        # Calculate birthdate
        today = date.today()
        birthdate = today - timedelta(days=days)
        birthdate = birthdate.replace(year=birthdate.year - years, month=birthdate.month - months)
        return birthdate.strftime("%d/%m/%Y")
    
    def check_and_create_csv(self, calculations):
        """
        Checks if the user's CSV file exists. If not, creates it with the provided calculations as the header.

        Args:
            calculations (list): A list of category names to be used as the header.
        """

        if not self.calculations_file.exists():
            print(f"CSV file '{self.calculations_file}' not found. Creating a new one.")
            with self.calculations_file.open('w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(calculations)
        else:
            print(f"CSV file '{self.calculations_file}' already exists.")

"""
# Example usage
user1 = User("Misa", "Male", 163, "10/04/1984")
print(user1.birthdate)  # 1984-04-10
print(user1.age)  # 40y/0m/0d (if the current date is after April 10, 2024)
print(user1.csv_file_name)
print(user1.calculations_file)
print(user1.age_in_years)
print(user1.minimum_optimal_body_fat_perc)
print(user1.maximum_optimal_body_fat_perc)
"""
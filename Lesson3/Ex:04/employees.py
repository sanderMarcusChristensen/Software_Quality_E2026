from datetime import datetime, date


class Employee:
    
    DEPARTMENTS = [
        "HR",
        "Finance",
        "IT",
        "Sales",
        "General Services"
    ]

    
    EDUCATION_LEVELS = {
        0: "none",
        1: "primary",
        2: "secondary",
        3: "tertiary"
    }

    # ---------- Constructor ----------

    def __init__(
        self,
        cpr,
        first_name,
        last_name,
        department,
        base_salary,
        educational_level,
        date_of_birth,
        date_of_employment,
        country
    ):
        
        self.set_cpr(cpr)
        self.set_first_name(first_name)
        self.set_last_name(last_name)
        self.set_department(department)
        self.set_base_salary(base_salary)
        self.set_educational_level(educational_level)
        self.set_date_of_birth(date_of_birth)
        self.set_date_of_employment(date_of_employment)
        self.set_country(country)

   
    # CPR
    def get_cpr(self):
        return self.__cpr

    def set_cpr(self, cpr):
        # CPR behandles som tekst, fordi det kan begynde med 0
        cpr = str(cpr)

        if len(cpr) != 10 or not cpr.isdigit():
            raise ValueError(
                "CPR must contain exactly 10 numeric digits"
            )

        self.__cpr = cpr

    
    # First name
    def get_first_name(self):
        return self.__first_name

    def set_first_name(self, first_name):
        if not isinstance(first_name, str):
            raise TypeError("First name must be a string")

        if not self.__valid_name(first_name):
            raise ValueError(
                "First name must contain 1-30 alphabetic "
                "characters, spaces or dashes"
            )

        self.__first_name = first_name

    
    # Last name
    def get_last_name(self):
        return self.__last_name

    def set_last_name(self, last_name):
        if not isinstance(last_name, str):
            raise TypeError("Last name must be a string")

        if not self.__valid_name(last_name):
            raise ValueError(
                "Last name must contain 1-30 alphabetic "
                "characters, spaces or dashes"
            )

        self.__last_name = last_name

    # Privat hjælpemetode til validering af navne
    def __valid_name(self, name):
        # Navnet skal indeholde mellem 1 og 30 tegn
        if len(name) < 1 or len(name) > 30:
            return False

        # Fjern tilladte mellemrum og bindestreger,
        # inden vi kontrollerer de resterende tegn
        letters_only = name.replace(" ", "").replace("-", "")

        # Navnet skal indeholde mindst ét bogstav,
        # og alle resterende tegn skal være bogstaver
        return len(letters_only) > 0 and letters_only.isalpha()

    
    # Department
    def get_department(self):
        return self.__department

    def set_department(self, department):
        if department not in self.DEPARTMENTS:
            raise ValueError(
                f"Department must be one of: "
                f"{', '.join(self.DEPARTMENTS)}"
            )

        self.__department = department

  
    # Base salary
    def get_base_salary(self):
        return self.__base_salary

    def set_base_salary(self, base_salary):
        if (
            not isinstance(base_salary, (int, float))
            or isinstance(base_salary, bool)
        ):
            raise TypeError("Base salary must be a number")

        if base_salary < 20000 or base_salary > 100000:
            raise ValueError(
                "Base salary must be between 20000 and 100000 DKK"
            )

        self.__base_salary = base_salary

   
    # Educational level
    def get_educational_level(self):
        # Opgaven kræver, at getteren returnerer navnet
        return self.EDUCATION_LEVELS[self.__educational_level]

    def set_educational_level(self, educational_level):
        if (
            not isinstance(educational_level, int)
            or isinstance(educational_level, bool)
        ):
            raise TypeError(
                "Educational level must be an integer"
            )

        if educational_level not in self.EDUCATION_LEVELS:
            raise ValueError(
                "Educational level must be 0, 1, 2 or 3"
            )

        self.__educational_level = educational_level

    
    # Date of birth
    def get_date_of_birth(self):
        return self.__date_of_birth.strftime("%d/%m/%Y")

    def set_date_of_birth(self, date_of_birth):
        parsed_date = self.__convert_to_date(date_of_birth)
        today = date.today()

        # Beregn medarbejderens alder
        age = today.year - parsed_date.year

        # Hvis personen endnu ikke har haft fødselsdag i år,
        # trækkes ét år fra
        if (today.month, today.day) < (
            parsed_date.month,
            parsed_date.day
        ):
            age -= 1

        if age < 18:
            raise ValueError(
                "Employee must be at least 18 years old"
            )

        self.__date_of_birth = parsed_date

    
    # Date of employment
    def get_date_of_employment(self):
        return self.__date_of_employment.strftime("%d/%m/%Y")

    def set_date_of_employment(self, date_of_employment):
        parsed_date = self.__convert_to_date(date_of_employment)

        if parsed_date > date.today():
            raise ValueError(
                "Date of employment cannot be later "
                "than the present day"
            )

        self.__date_of_employment = parsed_date

    # Privat hjælpemetode til omdannelse af datoer
    def __convert_to_date(self, date_string):
        if not isinstance(date_string, str):
            raise TypeError(
                "Date must be written as a string: dd/MM/yyyy"
            )

        try:
            return datetime.strptime(
                date_string,
                "%d/%m/%Y"
            ).date()

        except ValueError:
            raise ValueError(
                "Date must have the format dd/MM/yyyy"
            )

  
    # Country
  
    def get_country(self):
        return self.__country

    def set_country(self, country):
        if not isinstance(country, str):
            raise TypeError("Country must be a string")

        if not country.strip():
            raise ValueError("Country cannot be empty")

        # Gem uden overflødige mellemrum før og efter navnet
        self.__country = country.strip()

    # Actual salary
    def getSalary(self):
        return (
            self.__base_salary
            + self.__educational_level * 1220
        )

    # Employee discount
    def getDiscount(self):
        today = date.today()

        years_of_employment = (
            today.year - self.__date_of_employment.year
        )

        # Hvis årets ansættelsesdag ikke er passeret endnu,
        # er det seneste ansættelsesår ikke fuldført
        if (today.month, today.day) < (
            self.__date_of_employment.month,
            self.__date_of_employment.day
        ):
            years_of_employment -= 1

        return years_of_employment * 0.5

    # Shipping costs
    def getShippingCosts(self):
       
        country = self.__country.lower()

        if country in ["denmark", "norway", "sweden"]:
            return 0

        if country in ["iceland", "finland"]:
            return 50

        return 100
### Завдання
# У цьому домашньому завданні вам треба:
# 1. Додати функціонал збереження адресної книги на диск та відновлення з диска. 
# Для цього ви можете вибрати будь-який зручний для вас протокол серіалізації/десеріалізації 
# даних та реалізувати методи, які дозволять зберегти всі дані у файл і завантажити їх із файлу.
# 2. Додати користувачеві можливість пошуку вмісту книги контактів, щоб можна було знайти всю 
# інформацію про одного або кількох користувачів за кількома цифрами номера телефону або літерами імені тощо.

# Критерії прийому:
# - Програма не втрачає дані після виходу з програми та відновлює їх з файлу.
# - Програма виводить список користувачів, які мають в імені або номері телефону є збіги із введеним рядком.

from collections import UserDict
from datetime import datetime
import pickle, csv


class Field:
    def __init__(self, value):
        self.value = value
        # print(f'from Field: {self.value}')


class Name(Field):
    # name = True
    pass


class Phone(Field):
    def __init__(self, value):
        self.__value = None
        self.value = value
        super().__init__(self.__value)
    
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):
        # print(value.__class__)
        if (type(value) == int) and (len(str(value)) == 12):
            self.__value = value



class Birthday(Field):
    def __init__(self, value):
        self.__value = None
        self.value = value
        super().__init__(self.__value)
    
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):
        # print(value.__class__)
        if type(value) == datetime:
            self.__value = value


class Record:
    def __init__(self, name: Name, phone: Phone=None, birthday: Birthday=None): #: phone - це не обовязковий агрумент, тому по замовчюванню None
        """в тестах ми заповнюємо класс Record обьектами класів name та phone, тому в цьому конструкторі вже приходять
        не просто строки типу 'Bill', а саме обьекти классу name
        name = Name('Bill')
        phone = Phone('1234567890')
        """
        self.name = name
        self.phone = []
        self.birthday = birthday
        if phone:
            self.phone.append(phone)

    def __str__(self):
        return f"{self.name.value} {[ph.value for ph in self.phone]} {self.birthday.value}"
        
    def add_phone(self, phone):
        phone_number = Phone(phone)
        if phone_number not in self.phone:
            self.phone.append(phone_number)

    def delete_phone(self, phone):
        self.phone.remove(phone)

    def edit_phone(self, old_phone, new_phone):
        index = self.phone.index(old_phone)
        self.phone[index] = new_phone

    def days_to_birthday(self, birthday): #повертає кількість днів до наступного дня народження
        current_date = datetime.now().date()
        if birthday:
            birthday_date = birthday.replace(year=datetime.now().year).date() 
            delta = birthday_date - current_date
            if delta.days >= 0:
                return f'{delta.days} days to birthday'
            else:
                delta = birthday_date.replace(year=datetime.now().year+1) - current_date
                return f'{delta.days} days to birthday'
        else:
            return None


class AddressBook(UserDict):
    N = 2 # чому 2?

    def add_record(self, record: Record):
        self.data[record.name.value] = record
        # {‘Bill’: “Bill 0987777 22.09.2000”} - результат add_record
    
    def find_record(self, value):
        return self.data.get(value)    

    def search(self, value):
        result = []
        for cont in self.data.values():
            for ph in cont.phone:
                if value in str(ph.value):
                    result.append(f'{cont}')
                        
            if value in cont.name.value:
                    result.append(f'{cont}')
        return result if result != [] else f"No results for: {value}"        

    def iterator(self, n) -> list[dict]:
        contact_list = []  # список записів контактів
        if n:
            AddressBook.N = n
        for record in self.data.values():
            contact_list.append(record)
        return self.__next__(contact_list)
    
    def __iter__(self, contact_list: list[dict]):
        n_list = []
        counter = 0
        for contact in contact_list:
            n_list.append(contact)
            counter += 1
            if counter >= AddressBook.N:  # якщо вже створено список із заданої кількості записів
                yield n_list
                n_list.clear()
                counter = 0
        yield n_list

    def __next__(self, contact_list):
        generator = self.__iter__(contact_list)
        page = 1
        while True:
            user_input = input("Press ENTER")
            if user_input == "":
                try:
                    result = next(generator)
                    if result:
                        print(f"{'*' * 20} Page {page} {'*' * 20}")
                        page += 1
                    for var in result:
                        print(var)
                except StopIteration:
                    print(f"{'*' * 20} END {'*' * 20}")
                    break
            else:
                break
    
    def save_to_file(self, filename):
        self.filename = filename
        with open(self.filename, 'wb') as fh:
            pickle.dump(self, fh)

    # def save_to_table(self, filename):
    #     self.filename = filename
    #     with open(filename, 'w', newline='') as fh:
    #         writer = csv.DictWriter(fh, fieldnames='contact')
    #         for contact in self.data.values():
    #             writer.writerow(contact)

    def read_from_file(self, filename):
        self.filename = filename
        with open(self.filename, 'rb') as fh:
            unpacked = pickle.load(fh)
        return unpacked




# ### Checking mentor
if __name__ == "__main__":
    # record contact 1
    name = Name('Bill')
    phone = Phone(123456789012)
    birthday = Birthday(datetime(1990, 8, 3))
    rec = Record(name, phone, birthday)
    ab = AddressBook()
    ab.add_record(rec)
    rec.add_phone(380999876543)
    # print(ab)
    # print(rec)
    # print(type(rec))
    # print(rec.name.value)
    # print([ph.value for ph in rec.phone])
    # print(rec.birthday.value)
    # print(rec.days_to_birthday(datetime(1990, 8, 3)))
    
    # record contac 2
    name2 = Name('Mary')
    phone2 = Phone(987654321012)
    birthday2 = Birthday(datetime(1993, 9, 25))
    rec2 = Record(name2, phone2, birthday2)
    ab.add_record(rec2)
    # print(ab)
    # print(rec2.birthday.value)
    # print(rec2.days_to_birthday(datetime(1993, 9, 25)))
    # print(rec2.phone)

    # ##print(isinstance(ab['Bill'], Record))
    # assert isinstance(ab['Bill'], Record) # оператор assert працює так, він порівнює щось, я якщо це порівняння дає false - він викликає помилку
    # ##print(isinstance(ab['Bill'].name, Name))
    # assert isinstance(ab['Bill'].name, Name) # тут він перевіряє що в книзі контактів під ключем 'Bill' - знаходиться обьект классу Name
    # ##print(isinstance(ab['Bill'].phone, list))
    # assert isinstance(ab['Bill'].phone, list)
    # ##print(isinstance(ab['Bill'].phone[0], Phone))
    # assert isinstance(ab['Bill'].phone[0], Phone)
    # ##print(ab['Bill'].phone[0].value == '1234567890')
    # assert ab['Bill'].phone[0].value == 123456789012

    
    """Додамо контактів для перевірки ітератора"""
    name = Name('Bob')
    phone = Phone(343456789012)
    birthday = Birthday(datetime(1980, 1, 31))
    rec2 = Record(name, phone, birthday)

    name = Name('Tom')
    phone = Phone(433456789015)
    birthday = Birthday(datetime(1992, 12, 13))
    rec3 = Record(name, phone, birthday)

    name = Name('Bard')
    phone = Phone(153455789062)
    birthday = Birthday(datetime(2000, 4, 10))
    rec4 = Record(name, phone, birthday)

    ab.add_record(rec2)
    ab.add_record(rec3)
    ab.add_record(rec4)

    # ab.iterator(n=3)

    # print(ab)
    # ab.save_to_table('mod12_ab_mary.csv')
    # ab.save_to_file('mod12_ab_mary.bin')
    # ab_from_file = ab.read_from_file('mod12_ab_mary.bin')
    # print(ab_from_file)

    """Пошук вмісту книги контактів"""
    # print(ab)
    # print(ab.find_record('Mary'))
    print(ab.search('ar'))

    print('All Ok)')


# cont = {'Bill': 'Bill 0987777 22.09.2000', 'Mary': 'Mary 0995553312 17.06.2002', 'Sasha': 'Sasha 0635678910 22.09.2000'}
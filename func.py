from typing import Dict, List
import json

MSG_CHOOSE = "Выберите пункт из списка. ->"
MSG_ADD = "1. Добавить новую запись."
MSG_SEARCH = "2. Поиск по... (выберите для информации)"
MSG_EXIT = "\t\t0. Выйти из программы."
MSG_SEARCH_VAR = """Поиск...
1. ...по имени.    2. ...по фамилии.
3. ...по телефону. 4. ...по городу
0. Вернуться в передыдущее меню.
"""
MSG_DELETE = "Удалить запись"
MSG_UPDATE = "Обновить запись"
MSG_SORRY = "Извините, еще не готово. "
MSG_GET_FIRST_NAME = "Введите имя: "
MSG_GET_LAST_NAME = "Введите фамилию: "
MSG_GET_PHONE_NUMBER = "Введите номер телефона: "
MSG_GET_CITY = "Введите город: "
MSG_SUCCS_SAVE = "Контакт успешно сохранен. "
MSG_ERROR_KEY = "Не коректный ключ. Попробуйте снова! "
MSG_OPERATIONS = """1. Обновить. \t\t2.Удалить.
                 0. Вернуться в передыдущее меню."""
MSG_NO_SUITABLE = "0. Нету подходящих. "
MSG_CHOOSE_INFO_UPDATE = """Выберите что хитите изменить:
1. First name. \t2. Last name.
3. Phone number.\t 4. City.
0. Выход"""


def phonebook(filename: str):
    while True:
        sm()
        user_input = input(MSG_CHOOSE)

        if user_input == "1":
            add_contact(filename)

        elif user_input == "2":
            search_menu(filename)

        elif user_input == "0":
            break


def sm():
    print(f"{MSG_ADD}\t{MSG_SEARCH}\n"
          f"\t{MSG_EXIT}")


def save_phonebook(data: List[Dict], filename: str):
    with open(filename, 'w') as fw:
        json.dump(data, fw)
    print(MSG_SUCCS_SAVE)


def get_phonebook(filename) -> List[Dict]:
    try:
        with open(filename, 'r') as fr:
            print("Открой и прочти")
        return json.load(fr)
    except:
        print("Не удалось")
        return []


def get_fname() -> str:
    return input(MSG_GET_FIRST_NAME)


def get_lname() -> str:
    return input(MSG_GET_LAST_NAME)


def get_phnumber() -> str:
    return input(MSG_GET_PHONE_NUMBER)


def get_city() -> str:
    return input(MSG_GET_CITY)


def add_contact(filename):
    contacts = get_phonebook(filename)
    contacts.append({"First name": get_fname(),
                     "Last name": get_lname(),
                     "Phone number": get_phnumber(),
                     "City": get_city()})
    save_phonebook(contacts, filename)


def search_menu(filename):
    while True:
        rez = None
        print(MSG_SEARCH_VAR)
        key_search = input(MSG_CHOOSE)
        if key_search == '0':
            break
        elif key_search == '1':
            rez = searchbyfname(get_fname(), filename)
        elif key_search == '2':
            rez = searchbylname(get_lname(), filename)
        elif key_search == '3':
            rez = searchbypnumber(get_phnumber(), filename)
        elif key_search == '4':
            rez = searchbycity(get_city(), filename)
        else:
            print(MSG_ERROR_KEY)
        if rez is not []:
            for i, contact in enumerate(rez):
                print(f"{i + 1}. - {contact}")
            user_input = input(MSG_NO_SUITABLE)
            if not user_input.isdigit():
                print("not digit")
                break
            elif user_input == "0" or int(user_input) not in range(1, len(rez) + 1):
                print("out of len")
                break
            else:
                print(rez[int(user_input) - 1])
                user_input2 = input(MSG_OPERATIONS)

                if not user_input2.isdigit() or user_input == '0':
                    break
                elif user_input2 == '1':
                    update_contact(rez[int(user_input) - 1], filename)
                elif user_input2 == '2':
                    delete_contact(rez[int(user_input) - 1], filename)
                else:
                    break


def __search(key, val, filename) -> List[Dict]:
    contacts = get_phonebook(filename)
    rez = []
    for contact in contacts:
        if val.lower() in contact.get(key).lower():
            rez.append(contact)
    return rez


def searchbyfname(val, filename) -> List[Dict]:
    return __search("First name", val, filename)


def searchbylname(val, filename) -> List[Dict]:
    return __search("Last name", val, filename)


def searchbypnumber(val, filename) -> List[Dict]:
    return __search("Phone number", val, filename)


def searchbycity(val, filename) -> List[Dict]:
    return __search("City", val, filename)


def update_contact(contact: Dict, filename: str):
    contacts = get_phonebook(filename)
    contacts.pop(contacts.index(contact))

    while True:
        print(contact)
        print(MSG_CHOOSE_INFO_UPDATE)
        user_input = input(MSG_CHOOSE)
        if user_input == '1':
            contact["First name"] = get_fname()
        elif user_input == '2':
            contact["Last name"] = get_lname()
        elif user_input == '3':
            contact["Phone number"] = get_phnumber()
        elif user_input == '4':
            contact["City"] = get_city()
        elif user_input == '0':
            break
        else:
            continue

        contacts.append(contact)
        save_phonebook(contacts, filename)


def delete_contact(contact: Dict, filename: str):
    contacts = get_phonebook(filename)
    contacts.pop(contacts.index(contact))
    save_phonebook(contacts, filename)

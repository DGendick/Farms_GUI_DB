# users_data |0 - index |1 - Username |2 - Firstname |3 - Surname |4 - Date of birth |5 - Email |6 - Password |
import os
import getpass
import rating_and_feedback
import bcrypt
from datetime import datetime
user_auth_done = False
curr_user = []
class User:
    def __init__(self, username):
        self.__index = None
        self.__username = username
    
    @property
    def index(self):
        return self.__index
    
    @property
    def username(self):
        return self.__username

    @property
    def firstname(self):
        return self.__firstname
    
    @property
    def surname(self):
        return self.__surname
    
    @property
    def date_of_birth(self):
        return self.__date_of_birth
    
    @property
    def email(self):
        return self.__email
    
    @property
    def password(self):
        return self.__password
    
    @firstname.setter
    def firstname(self,firstname):
        self.__firstname = firstname

    @index.setter
    def index(self,index):
        self.__index = index

    @surname.setter
    def surname(self,surname):
        self.__surname = surname
        

    @date_of_birth.setter
    def date_of_birth(self,date_of_birth):
        self.__date_of_birth = date_of_birth
    
    @email.setter
    def email(self,email):
        self.__email = email
        
    @password.setter
    def password(self,password):
        self.__password = password
    
    #### Классы
    @classmethod
    def register(
            cls,
            file_path,
            username,
            firstname,
            surname,
            dob,
            email,
            password
    ):
        users = []

        if not os.path.exists(file_path):   #Создаем файл если его нет
            if not os.path.exists("users"):
                os.mkdir("users")
            index = 0
            username =  str("Admin")
            ####OOP
            user = User(username)
            user.index = index
            ####OOP
            firstname = str("Dmitrii")
            ####OOP
            user.firstname = firstname
            ####OOP
            surname = str("Gendik")
            ####OOP
            user.surname = surname
            ####OOP
            dob = str("07-10-1996")
            dob = datetime.strptime(dob,"%d-%m-%Y")#(dob, "%Y-%m-%d)
            dob = str(dob.date())
            ####OOP
            user.date_of_birth = dob
            ####OOP
            email = str("dmitriigendik@yandеx.ru")
            ####OOP
            user.email = email
            ###OOP
            password = str(bcrypt.hashpw(b'0000',bcrypt.gensalt()))
            ###OOP
            user.password = password
            ###OOP
            printer = list(user.__dict__.values())

            with open(file_path,'w', encoding='utf-8') as file:
                file.write(f"{','.join(map(str, printer))}\n")
                
        if os.path.exists(file_path):

            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as file:

                users = file.readlines()

        # проверяем существование

        for line in users:

            data = line.strip().split(",")

            if len(data) > 5:

                if data[1] == username:
                    return None, messagebox.showerror(
                "Error",
                "Passwords do not match"
            )


                if data[5] == email:
                    return None, "Email exists"


        # создаём пользователя

        user = cls(username)

        user.index = len(users)

        user.firstname = firstname

        user.surname = surname

        user.date_of_birth = dob

        user.email = email

        user.password = str(
            bcrypt.hashpw(
                password.encode("utf-8"),
                bcrypt.gensalt()
            )
        )

        data = list(
            user.__dict__.values()
        )
        with open(
            file_path,
            "a",
            encoding="utf-8"
        ) as file:

            file.write(
                ",".join(map(str,data))
                + "\n"
            )


        return user, "Success"



    @classmethod
    def authenticate(cls,file_path, username,password,):
        if not os.path.exists(file_path):   #Создаем файл если его нет
                    if not os.path.exists("users"):
                        os.mkdir("users")
                    index = 0
                    username =  str("Admin")
                    ####OOP
                    user = User(username)
                    user.index = index
                    ####OOP
                    firstname = str("Dmitrii")
                    ####OOP
                    user.firstname = firstname
                    ####OOP
                    surname = str("Gendik")
                    ####OOP
                    user.surname = surname
                    ####OOP
                    dob = str("07-10-1996")
                    dob = datetime.strptime(dob,"%d-%m-%Y")#(dob, "%Y-%m-%d)
                    dob = str(dob.date())
                    ####OOP
                    user.date_of_birth = dob
                    ####OOP
                    email = str("dmitriigendik@yandеx.ru")
                    ####OOP
                    user.email = email
                    ###OOP
                    password = str(bcrypt.hashpw(b'0000',bcrypt.gensalt()))
                    ###OOP
                    user.password = password
                    ###OOP
                    printer = list(user.__dict__.values())
        
                    with open(file_path,'w', encoding='utf-8') as file:
                        file.write(f"{','.join(map(str, printer))}\n")
        with open(file_path,'r',encoding='utf-8') as file:
            for line in file:
                data = line.strip().split(",") 
                if data[1] == username and bcrypt.checkpw(password.encode("utf-8"),data[6][2:-1].encode("utf-8")):


                    user = cls(data[1])
                    user.__index = data[0]
                    user.__firstname = data[2]
                    user.__surname = data[3]
                    user.__date_of_birth = data[4]
                    user.__email = data[5]
                    user.__password = data[6]

                    return user
                
                    
            
        return print(f"\nПользователь {username} не найден")

file_path = 'users/useroop.txt'
def auth_oop(user_auth_done, curr_user):
    
    vis_divider = '======================'      #разделитель для меню
    file_path = "users/users_data.csv"
    printer = []
    step = 999
    if not os.path.exists(file_path):   #Создаем файл если его нет
        if not os.path.exists("users"):
            os.mkdir("users")
        index = 0
        username =  str("Admin")
        ####OOP
        user = User(username)
        user.index = index
        ####OOP
        firstname = str("Dmitrii")
        ####OOP
        user.firstname = firstname
        ####OOP
        surname = str("Gendik")
        ####OOP
        user.surname = surname
        ####OOP
        dob = str("07-10-1996")
        dob = datetime.strptime(dob,"%d-%m-%Y")#(dob, "%Y-%m-%d)
        dob = str(dob.date())
        ####OOP
        user.date_of_birth = dob
        ####OOP
        email = str("dmitriigendik@yandеx.ru")
        ####OOP
        user.email = email
        ###OOP
        password = str(bcrypt.hashpw(b'0000',bcrypt.gensalt()))
        ###OOP
        user.password = password
        ###OOP
        printer = list(user.__dict__.values())

        with open(file_path,'w', encoding='utf-8') as file:
            file.write(f"{','.join(map(str, printer))}\n")
    while True:
        match step:
            case 0:
                try:
                    if user == None:
                        return False, []
                    else:
                        return user != None, user.username
                except:
                    return False, []
            case 999: #Меню
                print(vis_divider)
                print("1. Регистрация")
                print("2. Аутентификация")
                if user_auth_done:
                    user = User(curr_user)
                    print("3. Просмотреть оставленные отзывы")
                print("0. Выход")
                print(vis_divider)
                step =  input('Введите интересующую вас операцию > ')
                try:
                    step =  int(step)
                except:
                    print(f"Ошибка! {step} - не является командой")
                    step = 999
            case 1: #Регистрация пользователя
                users_data = open(file_path).read().split("\n")
                users_data_t =[]
                for i in range(len(users_data)):
                    users_data_t.append(users_data[i].split(","))
                users_data = users_data_t
                index = len(users_data) - 1
                
                print(vis_divider)
                print('Регистрация нового пользователя')
                print(vis_divider)
                while True:
                    username =  str(input('Введите логин > '))
                    i = 0
                    user_exist = False
                    for i in range(len(users_data)-1):
                        if users_data[i][1] == username:
                            user_exist = True
                    if user_exist:
                        print('Пользователь с таким логином уже существует. Попробуйте ввести другой\n')
                    else:
                        ####OOP
                        user = User(username)
                        user.index = index
                        break

                firstname = str(input('Введите имя пользователя > ')).capitalize()
                user.firstname = firstname
                surname = str(input('Введите фамилию пользователя > ')).capitalize()
                user.surname = surname
                while True:
                    dob = str(input('Введите дату рождения в формате ДД-ММ-ГГГГ > '))
                    try:
                        dob = datetime.strptime(dob,"%d-%m-%Y")#(dob, "%Y-%m-%d)
                        break
                    except:
                        print(f"Данные введены неверно. Убедитесь, что формат соответствует ДД-ММ-ГГГГ")
                user.date_of_birth = str(dob.date())
                step = 999
                while True:
                    email = str(input('Введите email пользователя > '))
                    i = 0
                    email_exist = False
                    for i in range(len(users_data)-1):
                        if users_data[i][5] == email:
                            email_exist = True
                    if email_exist:
                        print('Пользователь с такам email уже существует. Попробуйте ввести другой\n')
                    else:
                        user.email = email
                        break
                while True:
                    password = str(getpass.getpass(prompt="Введите пароль пользователя >  ")) #str(input('Введите пароль пользователя > '))
                    password_confirm = str(getpass.getpass(prompt="Повторно введите пароль пользователя для подтверждения > "))
                    if password_confirm != password:
                        print('Пароли не совпадают. Пожалуйста повторите попытку\n')
                    else:
                        password = str(bcrypt.hashpw(password.encode("utf-8"),bcrypt.gensalt()))
                        user.password = password
                        break
                
                printer = list(user.__dict__.values())

                with open(file_path,'a', encoding='utf-8') as file:
                    file.write(f"{','.join(map(str, printer))}\n")

                print('Регистрация пройдена успешно\n')
            case 2:
                if user_auth_done == True:
                    return user_auth_done, curr_user                            
                print(vis_divider)
                print('Аутентификация пользователя')
                print(vis_divider)
                username =  str(input('Введите логин > '))
                password = str(getpass.getpass(prompt="Введите пароль пользователя >  "))
                user = User.authenticate(file_path,username,password)
                if user == None:
                    step = 999
                else:
                    print(f"\nС возвращением, {user.username}!")
                    step = 0
            case 3:#удаление отзыва
                if user != None:
                    rating_and_feedback.rating(0,user.username,3)
                    step = 999
                else:
                    print("Для просмотра отзывов выполните аутентификацию")
                    step = 999
            case _:
                print(f"Ошибка! {step} - не является командой")
                step = 999

###Старая функция 
def auth(user_auth_done, curr_user):
    vis_divider = '======================'      #разделитель для меню

    file_path = "users/users_data.csv"
    printer = []
    step = 999

    if not os.path.exists(file_path):   #Создаем файл если его нет
        if not os.path.exists("users"):
            os.mkdir("users")
        index = 0
        printer.append(0)
        username =  str("Admin")
        printer.append(username)
        firstname = str("Dmitrii")
        printer.append(firstname)
        surname = str("Gendik")
        printer.append(surname)
        dob = str("07-10-1996")
        dob = datetime.strptime(dob,"%d-%m-%Y")#(dob, "%Y-%m-%d)
        printer.append(str(dob.date()))
        email = str("dmitriigendik@yandеx.ru")
        printer.append(email)
        password = str(bcrypt.hashpw(b'0000',bcrypt.gensalt()))
        printer.append(password)
        
        with open(file_path,'w', encoding='utf-8') as file:
            file.write(f"{','.join(map(str, printer))}\n")
    while True:
        match step:
            case 0: 
                user_auth_done = False
                curr_user = []
                return user_auth_done, curr_user
            case 999: #Меню
                print(vis_divider)
                print("1. Регистрация")
                print("2. Аутентификация")
                if user_auth_done:
                    print("3. Просмотреть оставленные отзывы")
                print("0. Выход")
                print(vis_divider)
                step =  input('Введите интересующую вас операцию > ')
                try:
                    step =  int(step)
                except:
                    print(f"Ошибка! {step} - не является командой")
                    step = 999
            case 1: #Регистрация пользователя
                users_data = open(file_path).read().split("\n")
                users_data_t =[]
                for i in range(len(users_data)):
                    users_data_t.append(users_data[i].split(","))
                users_data = users_data_t
                index = len(users_data) - 1
                printer.append(index)
                print(vis_divider)
                print('Регистрация нового пользователя')
                print(vis_divider)
                while True:
                    username =  str(input('Введите логин > '))
                    i = 0
                    user_exist = False
                    for i in range(len(users_data)-1):
                        if users_data[i][1] == username:
                            user_exist = True
                    if user_exist:
                        print('Пользователь с таким логином уже существует. Попробуйте ввести другой\n')
                    else:
                        printer.append(username)
                        break

                firstname = str(input('Введите имя пользователя > ')).capitalize()
                printer.append(firstname)
                surname = str(input('Введите фамилию пользователя > ')).capitalize()
                printer.append(surname)
                while True:
                    dob = str(input('Введите дату рождения в формате ДД-ММ-ГГГГ > '))
                    try:
                        dob = datetime.strptime(dob,"%d-%m-%Y")#(dob, "%Y-%m-%d)
                        break
                    except:
                        print(f"Данные введены неверно. Убедитесь, что формат соответствует ДД-ММ-ГГГГ")
                printer.append(str(dob.date()))
                step = 999
                while True:
                    email = str(input('Введите email пользователя > '))
                    i = 0
                    email_exist = False
                    for i in range(len(users_data)-1):
                        if users_data[i][5] == email:
                            email_exist = True
                    if email_exist:
                        print('Пользователь с такам email уже существует. Попробуйте ввести другой\n')
                    else:
                        printer.append(email)
                        break
                while True:
                    password = str(getpass.getpass(prompt="Введите пароль пользователя >  ")) #str(input('Введите пароль пользователя > '))
                    password_confirm = str(getpass.getpass(prompt="Повторно введите пароль пользователя для подтверждения > "))
                    if password_confirm != password:
                        print('Пароли не совпадают. Пожалуйста повторите попытку\n')
                    else:
                        password = str(bcrypt.hashpw(password.encode("utf-8"),bcrypt.gensalt()))
                        printer.append(password)
                        break

                with open(file_path,'a', encoding='utf-8') as file:
                    file.write(f"{','.join(map(str, printer))}\n")

                print('Регистрация пройдена успешно\n')
            case 2: # Аутентификация пользователя
                if user_auth_done == True:
                        return user_auth_done, curr_user                            
                print(vis_divider)
                print('Аутентификация пользователя')
                print(vis_divider)
                while True:
                    printer = []
                    users_data = open(file_path).read().split("\n")
                    users_data_t =[]
                    for i in range(len(users_data)):
                        users_data_t.append(users_data[i].split(","))
                    users_data = users_data_t
                    username =  str(input('Введите логин > '))
                    printer.append(username)
                    password = str(getpass.getpass(prompt="Введите пароль пользователя >  "))
                    printer.append(password)
                    for i in range(len(users_data)-1):
                        if printer[0] == users_data[i][1]:
                            if bcrypt.checkpw(printer[1].encode("utf-8"),users_data[i][6][2:-1].encode("utf-8")):#printer[1] ==users_data[i][6]:

                                user_auth_done = True
                                
                                curr_user = [users_data[i][0],users_data[i][1]]
                                print(f"\nС возвращением, {curr_user[1]}!")
                                step = 999
                                return user_auth_done, curr_user
                                #break
                            else:
                                print(vis_divider)
                                print("Введен неверный пароль")
                                print(vis_divider)
                                print("1. Повторить попытку")
                                print("0. Вернуться в главное меню")

                                cmd = input("> ")

                                if cmd == "1":
                                    step_case_2 = 1
                                    break
                                elif cmd == "0":
                                    step_case_2 = 0
                                    break
                                else:
                                    print(f"Ошибка! {cmd} - не является командой")
                        else:
                            step_case_2 = 2
                    match step_case_2:
                        case 1:
                         ...
                        case 0:
                            break
                        case 2:
                            print(f"\nПользователь {printer[0]} не найден")
                            step = 999
                            break
            case 3:#удаление отзыва
                if user_auth_done:
                    rating_and_feedback.rating(0,curr_user,3)
                    step = 999
                else:
                    print("Для просмотра отзывов выполните аутентификацию")
                    step = 999
            case _:
                print(f"Ошибка! {step} - не является командой")
                step = 999
                            
if __name__ == '__main__':

    user_auth_done = False                           
    auth_oop(user_auth_done, [])                
                            




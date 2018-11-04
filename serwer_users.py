from psycopg2 import connect
from psycopg2 import IntegrityError

from Warsztaty2.clcrypto import check_password
from Warsztaty2.models import User

import argparse
import sys

cnx = connect(database="Workshop2_db", user="postgres", password="coderslab", host="localhost")
cnx.autocommit = True
cursor = cnx.cursor()

parser = argparse.ArgumentParser()  #stworzenie parsera argumentów linii komend. Parser to klasa ArgumentParser() importowana z biblioteki argparse
parser.add_argument("-u", "--username", nargs=1, help="User's name, not unique", dest="username")  #tworzenie kolejnych argumentów czytelnych dla programu
parser.add_argument("-@", "--email", nargs=1, help="User's email, unique", dest="email")  #nargs - odpowiada za możliwość wpisywania danych z linii komend
parser.add_argument("-p", "--password", nargs=1, help="User's password", dest="password")  #help - to komunikat wyświetlony w "helpie" do programu
parser.add_argument("-n", "--new-pass", nargs=1, help="User's new password", dest="new_password")  #dest - to informacja, jak odwołać się do argumentów w kodzie programu
parser.add_argument("-l", "--list", action="store_true", help="Show list of all users")  #action - to informacja, jaką wartość logiczną ma argument, jeśli został wywołany z linii komend
parser.add_argument("-d", "--delete", action="store_true", help="Deletes user's account")  # domyślnie - action ma wartość "False". Po wywołaniu - "True".
parser.add_argument("-e", "--edit", action="store_true", help="Modifies user's account")

args = parser.parse_args()  #stworzenie obiektu args, powstałej jako efektu działania metody parse_args na obiekcie parser

#   # dodawanie usera do bazy użytkowników <--> -u --email -p
if (
    args.username and  #warunki do pierwszego scenariusza. Wywołanie argumentu z username z linii komend zmienia jego stan z "None"
    args.email and
    args.password and
    args.edit is False and
    args.delete is False
   ):
    user = User(cursor)  #stworzenie instancji klasy User - niezbędnej do przechowania danych użytkownika
    user.username = args.username[0]  #pobranie treści argumentu wpisanego z linii komend jako username. Logicznie, to pierwszy element tablicy zwracanej przez metodę username obiektu args.
    user.email = args.email[0]
    if user.set_hashed_password(args.password[0]):  #metoda user_set_hashed_password zwraca true lub false - w zależności od spełniania przez hasło warunków koniecznych minimalnej długości
        try:
            user.save()
            print("Dodano użytkownika!")
        except IntegrityError as error:
            print("Taki e-mail już istnieje w bazie!", error)
    else:
        print("Hasło zbyt krótkie")
        sys.exit()


# edycja hasła użytkownika  <--> --email -p -n -e
if (
    args.email and
    args.password and
    args.new_password and
    args.edit is True
   ):
    try:
        loaded_user = User.load_by_email(cursor, args.email[0])  #wywołanie metody load_by_email , której argumentem jest cursor do bazy SQL oraz podany z linii komend e-mail
        if check_password(args.password[0], loaded_user.hashed_password):  #walidacja hasła
            new_hashed_password = args.new_password[0]
            loaded_user.set_hashed_password(new_hashed_password)
            loaded_user.update_password()  #wywołanie metody "update_password" nadpisującej hasło w bazie danych.
            print("Hasło zmienione!")
        else:
            print("Złe hasło wejścia do bazy!")  #innymi słowy, uzytkownik pomylił swoje hasło.
    except AttributeError as attrerror:
        print("Nie ma takiego użytkownika", attrerror)

# #kasowanie użytkownika po emailu  <--> --email -p -d
if (
    args.email and
    args.password and
    args.delete is True
   ):
    try:
        loaded_user = User.load_by_email(cursor, args.email[0])  #wczytywanie Usera po podanym emailu.
        if check_password(args.password[0], loaded_user.hashed_password):  #walidacja hasła.
            User.delete_user_by_mail(User, cursor, args.email[0])
            print("Skasowano użytkownika o emailu:", args.email[0])
        else:
            print("Złe hasło, nie można skasować")
    except AttributeError:
        print("Nie ma takiego użytkownika!")

# #wczytywanie bazy userów  <--> -l
if args.list is True:  # jeśli z linii komend podano argument "-l", czyli "list".
    for single_user in User.load_all_users(cursor):  #wywołanie metody statycznej "load all users" z klasy User
        print("ID:", single_user._id)
        print("username:", single_user.username)
        print("email:", single_user.email, "\n")


cursor.close()
cnx.close()

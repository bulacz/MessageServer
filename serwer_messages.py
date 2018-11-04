from psycopg2 import connect

from Warsztaty2.models import Message
from Warsztaty2.models import User

import argparse
import datetime
import sys
  #otwarcie połączenia z bazą danych
cnx = connect(database="Workshop2_db", user="postgres", password="coderslab", host="localhost")
cnx.autocommit = True
cursor = cnx.cursor()
  #podanie programowi lidty oczekiwanych argumentów z linii komend
parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", nargs=1, help="User's name, not unique", dest="username")
parser.add_argument("-@", "--email", nargs=1, help="User's email, unique", dest="email")
parser.add_argument("-p", "--password", nargs=1, help="User's password", dest="password")
parser.add_argument("-l", "--list", action="store_true", help="Show list of all messages")
parser.add_argument("-t", "--to", nargs=1, help="Receiver's e-mail", dest="receiver")
parser.add_argument("-s", "--send", nargs=1, default="None", type=str, help="Sends messages", dest="send")
  #stworzenie obiektu Parsera.
args = parser.parse_args()


if (
    args.email and  #warunki pierwszego scenariusza - podano adres e-mail, hasło i zażądano wylistowania wiadomości do użytkownika.
    args.password and
    args.list is True
   ):
    user_email = args.email[0]  # pobranie z linii komend adresu e-mail.
    user_password = args.password[0]  #oraz hasła.
    if User.validate_password(cursor, user_email, user_password) is True:  #jeśli validacja hasła się powiodła (istnieje użytkownik o podanym e-mailu i hasłą się zgadzają)
        Message.load_message_for_user_by_email(cursor, user_email)  #wczytanie wiadomości i ich treści.
        print("Oto wiadomości do Ciebie: \n")
        for single_message in Message.load_message_for_user_by_email(cursor, user_email):
            print("message ID:", single_message.get_message_id)
            print("sent from user (id", single_message.from_id, ") :", single_message.sender_email)
            print("message sent:", single_message.text)
            print("sent on:", single_message.date, "\n----------")
    else:
        print("Niewłaściwy login, lub hasło. Program przerywa działanie")  #działanie, jeśli walidacja hasła się nie powiedzie.
        sys.exit()

if (
    args.email and  #warunki drugiego scneraiusza - podano email, hasło, adres odbiorcy i atrybut send
    args.password and
    args.receiver and
    args.send
   ):
    user_email = args.email[0]
    user_password = args.password[0]
    if User.validate_password(cursor, user_email, user_password) is True:  #walidacja hasła użytkownika:
        sender_user = User.load_by_email(cursor, user_email)  #stworzenie nadawcy - instancji klasy User, właściwej do wskazania ID nadawcy do tabeli messages.
        new_message = Message(cursor)  #stworzenie instancji klasy Message - nowej wiadomości do tabeli Messages
        new_message.sender_id = sender_user.id  #wskazanie kolejnych elementów zapytania SQL dopisującej wiadomość do bazy
        new_message.sender_email = user_email
        new_message.receiver_email = args.receiver[0]
        receiver_user = User.load_by_email(cursor, new_message.receiver_email)  #stworzenie odbiorcy wiadomości - instancji klasy User.
        if receiver_user:  #jeśli udało się powołać odbiorcę - e-mail podany w linii komend jako e-mail adresatata jerst właściwy
            new_message.receiver_id = receiver_user.id
            new_message.text = str(args.send[0])
            new_message.date = datetime.datetime.now()
            if new_message.send_message():  #próba wysłania wiadomości. Metoda send.message zwraca "true", jeśli uda się wysłać, "false", jeśli nie.
                print("Wysłano wiadomość")
            else:
                print("Nie można wysyłać pustej wiadomości")
        else:
            print("Nie znaleziono adresata")
            sys.exit()
    else:
        print("Niewłaściwy login, lub hasło. Program przerywa działanie.")

  #zamknięcie połączenia z bazą danych.
cursor.close()
cnx.close()

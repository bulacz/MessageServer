from psycopg2 import connect

from Warsztaty2.models import User
from Warsztaty2.models import Message


import datetime


cnx = connect(database="Workshop2_db", user="postgres", password="coderslab", host="localhost")
cnx.autocommit = True
cursor = cnx.cursor()

# #dodawanie użytkownika do bazy - działa
# user = User(cursor)
# user.username = "User5"
# user.email = "user5@knownmail.com"
# user.set_hashed_password("haslohaslo")
# user.save()

# #Wczytywanie po istniejącym Id - działa
# id_to_look_for = 1
# print("ID", User.load_by_id(cursor, id_to_look_for).id)
# print("Username:", User.load_by_id(cursor, id_to_look_for).username)
# print("email:", User.load_by_id(cursor, id_to_look_for).email)
# print("pass:", User.load_by_id(cursor, id_to_look_for).hashed_password)

# #Wczytywanie po nieistniejącym ID - działa
# id_to_look_for = 100
# print("ID", User.load_by_id(cursor, id_to_look_for).id)
# print("Username:", User.load_by_id(cursor, id_to_look_for).username)
# print("email:", User.load_by_id(cursor, id_to_look_for).email)
# print("pass:", User.load_by_id(cursor, id_to_look_for).hashed_password)

# # wczytywanie całej bazy -działa
# print(User.load_all_users(cursor))
# for single_user in User.load_all_users(cursor):
#     print("ID:", single_user._id)
#     print("username:", single_user.username)
#     print("email:", single_user.email)
#     print("pass:", single_user._hashed_password, "\n")

# #modyfikowanie użytkownika -działa. Zmiana hasła zwraca inny ciąg znaków.
# id_to_modify = 18
# user_to_modify = User.load_by_id(cursor, id_to_modify)
# print("user_to_modify to", user_to_modify)
# print("User_id", user_to_modify.id)
# print("User name", user_to_modify.username)
# print("User e-mail", user_to_modify.email)
# print("User hashed_pass", user_to_modify.hashed_password)
# user_to_modify.set_hashed_password("really_weak_test_password")
# user_to_modify.save()

# #Kasowanie usera po id = działa
# id_to_delete = 1
# User.delete_user(User, cursor, id_to_delete)


# #dodawanie wiadomości - działa. Sprawdzone.
# test_message = Message(cursor)
# test_message.sender_id = 4
# test_message.receiver_id = 2
# test_message.text = "This is a test message"
# test_message.date = datetime.datetime.now()
# test_message.send_message()

# #wyszukiwanie wiadomości po ID - działa.
# message_id = 1
# print("ID:", Message.load_message_by_id(cursor, message_id).get_message_id)
# print("from:", Message.load_message_by_id(cursor, message_id).from_id)
# print("to:", Message.load_message_by_id(cursor, message_id).to_id)
# print("text:", Message.load_message_by_id(cursor, message_id).text)
# print("date:", Message.load_message_by_id(cursor, message_id).date)

# #wczytywanie wiadomości dla użytkownika o ID - działa.
# user_id = 6
# print("Długość tablicy wiadomości (ilość wiadomości):", len(Message.load_message_for_user(cursor, user_id)))
# for single_message in Message.load_message_for_user(cursor, user_id):
#     print("message ID:", single_message.get_message_id)
#     print("sent from user:", single_message.from_id)
#     print("message sent:", single_message.text)
#     print("sent on:", single_message.date, "\n")

# #wczytywanie wiadomości wysłanych przez użytkownika o zadanym ID - działa
# user_id = 6
# print("Długość tablicy wiadomości (ilość wiadomości):", len(Message.load_message_from_user(cursor, user_id)))
# for single_message in Message.load_message_from_user(cursor, user_id):
#     print("message ID:", single_message.get_message_id)
#     print("sent to user:", single_message.to_id)
#     print("message sent:", single_message.text)
#     print("sent on:", single_message.date, "\n")

# #Wczytywanie wszystkich wiadomości - działa
# print("Długość tablicy wiadomości (ilość wiadomości):", len(Message.load_all_messages(cursor)), "\n")
# for single_message in Message.load_all_messages(cursor):
#     print("message ID:", single_message.get_message_id)
#     print("sent from user:", single_message.from_id)
#     print("sent to user:", single_message.to_id)
#     print("message sent:", single_message.text)
#     print("sent on:", single_message.date, "\n")


cursor.close()
cnx.close()

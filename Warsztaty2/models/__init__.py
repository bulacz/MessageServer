from Warsztaty2.clcrypto import password_hash
from Warsztaty2.clcrypto import check_password


class User:

    def __init__(self, cursor):
        self.__id = -1
        self.username = None
        self.__hashed_password = None
        self.email = None
        self._cursor = cursor

    @property
    def id(self):
        return self.__id

    @property
    def hashed_password(self):
        return self.__hashed_password

    def set_hashed_password(self, password, salt=None):
        if len(password) >= 8:
            self.__hashed_password = password_hash(password, salt)
            return True
        else:
            return False

    def save(self):
        if self.id == -1:
            sql = f"insert into user_table (username, hashed_password, email) " \
                  f"values ('{self.username}', '{self.hashed_password}', '{self.email}') returning 'id';"
            self._cursor.execute(sql)
            self.__id = self._cursor.fetchone()[0]
        else:
            sql = f"UPDATE user_table " \
                  f"SET username = '{self.username}', hashed_password = '{self.hashed_password}', " \
                  f"email = '{self.email}' WHERE id= '{self.id}';"
            self._cursor.execute(sql)
        return True

    def update_password(self):
        sql = f"UPDATE user_table " \
              f"SET username = '{self.username}', hashed_password = '{self.hashed_password}', " \
              f"email = '{self.email}' WHERE id= '{self.id}';"
        self._cursor.execute(sql)


    @staticmethod
    def load_by_id(cursor, id):
        sql = f"SELECT id, username, email, hashed_password FROM user_table WHERE id='{id}';"
        cursor.execute(sql)
        data = cursor.fetchone()
        if data:
            loaded_user = User(cursor)
            loaded_user._User__id = data[0]
            loaded_user.username = data[1]
            loaded_user.email = data[2]
            loaded_user._User__hashed_password = data[3]
            return loaded_user
        else:
            print("Nie znaleziono użytkownika")
            return None

    @staticmethod
    def load_by_email(cursor, email):
        sql = f"SELECT id, username, email, hashed_password FROM user_table WHERE email='{email}';"
        cursor.execute(sql)
        data = cursor.fetchone()
        if data:
            loaded_user = User(cursor)
            loaded_user._User__id = data[0]
            loaded_user.username = data[1]
            loaded_user.email = data[2]
            loaded_user._User__hashed_password = data[3]
            return loaded_user
        else:
            return False

    @staticmethod  #metoda validate_password powstała po napisaniu obsługi użytkowników, z myślą o uproszczeniu kodu do obsługi wiadomości.
    def validate_password(cursor, email_to_check, password_to_check):
        try:
            loaded_user = User.load_by_email(cursor, email_to_check)
            if check_password(password_to_check, loaded_user.hashed_password):
                return True
        except AttributeError:
            return False

    @staticmethod
    def load_all_users(cursor):
        return_table = []
        retsgl = f"SELECT * FROM user_table;"
        cursor.execute(retsgl)
        for row in cursor.fetchall():
            loaded_user = User(cursor)
            loaded_user._id = row[0]
            loaded_user.email = row[1]
            loaded_user.username = row[2]
            loaded_user._hashed_password = row[3]
            return_table.append(loaded_user)
        return return_table

    def delete_user(self, cursor, id):
        sql = f"delete from user_table where id = {id};"
        cursor.execute(sql)
        self._id = -1
        return True

    def delete_user_by_mail(self, cursor, email):
        sql = f"delete from user_table where email = '{email}';"
        cursor.execute(sql)
        self._id = -1


class Message:

    @staticmethod
    def create_message_table(cursor):
        set_table_sql = f"CREATE TABLE Message(id serial, from_id int not null, to_id int not null, " \
                        f"from_email varchar(150), to_email varchar(150), text varchar(255) not null, " \
                        f"creation_date timestamp, primary key (id), " \
                        f"foreign key (from_id) references user_table (id), " \
                        f"foreign key (to_id) references user_table (id), " \
                        f"foreign key (from_email) references user_table (email), " \
                        f"foreign key (to_email) references user_table (email));"
        cursor.execute(set_table_sql)

    @staticmethod
    def drop_message_table(cursor):
        drop_table_sql = f"DROP TABLE Message;"
        cursor.execute(drop_table_sql)

    def __init__(self, cursor):
        self.__id = -1
        self.sender_id = 0
        self.receiver_id = 0
        self.sender_email = ""
        self.receiver_email = ""
        self.text = ""
        self.date = ""
        self._cursor = cursor

    @property
    def get_message_id(self):
        return self.__id

    def send_message(self):  #odpowiada metodzie save_to_db z polecenia
        if self.__id == -1:
            if len(self.text) > 0:
                send_message_sql = f"insert into Message (from_id, to_id, from_email, to_email, "\
                                   f"text, creation_date) " \
                                   f"values ('{self.sender_id}', '{self.receiver_id}', " \
                                   f"'{self.sender_email}', '{self.receiver_email}', '{self.text}', " \
                                   f"CAST('{self.date}' as timestamp));"
                self._cursor.execute(send_message_sql)
                return True
            else:
                return False

    @staticmethod
    def load_message_by_id(cursor, message_id):
        load_message_by_id_sql = f"select id, from_id, to_id, from_email, to_email, text, creation_date " \
                                 f"from Message " \
                                 f"where id = {message_id};"
        cursor.execute(load_message_by_id_sql)
        data = cursor.fetchone()
        if data:
            loaded_message = Message(cursor)
            loaded_message._Message__id = data[0]
            loaded_message.from_id = data[1]
            loaded_message.to_id = data[2]
            loaded_message.sender_email = data[3]
            loaded_message.receiver_email = data[4]
            loaded_message.text = data[5]
            loaded_message.date = data[6]
            return loaded_message
        else:
            print("No such message")
            return None

    @staticmethod
    def load_message_for_user(cursor, user_id):
        return_message_for_user_table = []
        load_message_for_user_sql = f"select id, from_id, to_id, from_email, to_email, text, creation_date " \
                                    f"from Message " \
                                    f"where to_id = {user_id};"
        cursor.execute(load_message_for_user_sql)
        for table_row in cursor.fetchall():
            loaded_message = Message(cursor)
            loaded_message._Message__id = table_row[0]
            loaded_message.from_id = table_row[1]
            loaded_message.to_id = table_row[2]
            loaded_message.sender_email = table_row[3]
            loaded_message.receiver_email = table_row[4]
            loaded_message.text = table_row[5]
            loaded_message.date = table_row[6]
            return_message_for_user_table.append(loaded_message)
        return return_message_for_user_table

    @staticmethod
    def load_message_for_user_by_email(cursor, user_email):
        return_load_message_from_user_table = []
        load_message_from_user_sql = f"select id, from_id, to_id, from_email, to_email, text, creation_date " \
                                     f"from Message where to_email = '{user_email}' order by creation_date;"
        cursor.execute(load_message_from_user_sql)
        for table_row in cursor.fetchall():
            loaded_message = Message(cursor)
            loaded_message._Message__id = table_row[0]
            loaded_message.from_id = table_row[1]
            loaded_message.to_id = table_row[2]
            loaded_message.sender_email = table_row[3]
            loaded_message.receiver_email = table_row[4]
            loaded_message.text = table_row[5]
            loaded_message.date = table_row[6]
            return_load_message_from_user_table.append(loaded_message)
        return return_load_message_from_user_table

    @staticmethod
    def load_message_from_user(cursor, user_id):
        return_load_message_from_user_table = []
        load_message_from_user_sql = f"select id, from_id, to_id, from_email, to_email, text, creation_date " \
                                     f"from Message " \
                                     f"where from_id = {user_id};"
        cursor.execute(load_message_from_user_sql)
        for table_row in cursor.fetchall():
            loaded_message = Message(cursor)
            loaded_message._Message__id = table_row[0]
            loaded_message.from_id = table_row[1]
            loaded_message.to_id = table_row[2]
            loaded_message.sender_email = table_row[3]
            loaded_message.receiver_email = table_row[4]
            loaded_message.text = table_row[5]
            loaded_message.date = table_row[6]
            return_load_message_from_user_table.append(loaded_message)
        return return_load_message_from_user_table

    @staticmethod
    def load_all_messages(cursor):
        return_load_all_messages_table = []
        load_all_messages_sql = "SELECT * from message;"
        cursor.execute(load_all_messages_sql)
        for table_row in cursor.fetchall():
            loaded_message = Message(cursor)
            loaded_message._Message__id = table_row[0]
            loaded_message.from_id = table_row[1]
            loaded_message.to_id = table_row[2]
            loaded_message.sender_email = table_row[3]
            loaded_message.receiver_email = table_row[4]
            loaded_message.text = table_row[5]
            loaded_message.date = table_row[6]
            return_load_all_messages_table.append(loaded_message)
        return return_load_all_messages_table

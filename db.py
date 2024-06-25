import psycopg2

import os

from dotenv import load_dotenv

load_dotenv("D:\PDP\projects\p24\.env")


class Database:
    def __init__(self):
        self.db = psycopg2.connect(
            host="localhost",
            dbname="todo_db",
            password=os.getenv("POSTGRESS_PASSWORD"),
            user=os.getenv("POSTGRESS_USER"),
        )
        self.db.autocommit = True

    def create_user_table(self):
        cursor = self.db.cursor()
        create_user_sql = """
            create table users(
                id serial primary key,
                username varchar(128) unique not null, 
                password varchar(128) not null,
                email varchar(56),
                phone varchar(56)
            );             
        """
        cursor.execute(create_user_sql)
        self.db.commit()

    def create_todo_table(self):
        cursor = self.db.cursor()
        create_user_sql = """
                    create table todo(
                        id serial primary key,
                        title varchar(128) unique not null, 
                        status varchar(128) not null,
                        owner_id int references users(id),
                        deadline timestamp default now()+interval '1 day'
                    );             
                """
        cursor.execute(create_user_sql)
        self.db.commit()
        self.db.close()

    def insert_user(self, username, password, email, phone):
        insert_user_sql = """
        insert into users(username, password, email, phone) values (%s,%s,%s,%s);
        """

        cursor = self.db.cursor()
        cursor.execute(insert_user_sql, (username, password, email, phone))
        self.db.commit()

    def insert_todo(self, title, status, owner_id):
        insert_todo_sql = """
        insert into todo(title, status, owner_id) values (%s,%s,%s);
        """
        cursor = self.db.cursor()
        cursor.execute(insert_todo_sql, (title, status, owner_id))
        self.db.commit()
        self.db.close()

    def check_username_unique(self, username):
        search_username_unique_sql = """
                select * from users where username=%s;
                """
        cursor = self.db.cursor()
        cursor.execute(search_username_unique_sql, (username,))
        result = cursor.fetchall()
        self.db.commit()
        if result:
            return False
        else:
            return True

    def get_user_by_username(self, username):
        search_username_sql = """
                        select * from users where username=%s;
                        """
        cursor = self.db.cursor()
        cursor.execute(search_username_sql, (username,))
        result = cursor.fetchone()
        return result

    def update_todo(self, todo_id, value):
        update_todo_sql = """
            update todo set status=%s where id=%s
        
        """
        cursor = self.db.cursor()
        cursor.execute(update_todo_sql, (value, todo_id))
        self.db.commit()

    def delete_todo(self, todo_id):
        delete_todo_sql = """
            delete from todo where id=%s
        
        """
        cursor = self.db.cursor()
        cursor.execute(delete_todo_sql, (todo_id,))
        self.db.commit()

    def my_todos(self, user_id):
        my_todo_sql = "select * from todo where owner_id=%s"
        cursor = self.db.cursor()
        cursor.execute(my_todo_sql, (user_id,))
        data = cursor.fetchall()
        self.db.commit()
        return data


if __name__ == '__main__':
    db = Database()
    # db.create_user_table()
    # db.create_todo_table()
    # db.insert_user("ahmadjon", "testpassword", "ahmadjon@gmail.com", "+998911112233")
    # db.insert_todo("make gpt 4a", "todo", "1")
    print(db.get_user_by_username("ahmadjon"))

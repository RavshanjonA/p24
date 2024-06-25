from exceptions import BadRequestException
from models import User
from services import AuthService, TodoService

session_user = None


def main_menu():
    global session_user
    if session_user:
        print("1.my todos")
        print("2.create todo")
        print("3.update todo")
        print("4.delete todo")
    else:
        print("1.login")
        print("2.register")

    ch = input(">> ")
    if session_user:
        user_menu(ch)
    else:
        auth_menu(ch)


def auth_menu(ch):
    global session_user
    auth_serive = AuthService()
    try:
        match ch:
            case "1":
                username = input("Username: ")
                password = input("Password: ")
                session_user = auth_serive.login_user(username=username, password=password)
            case "2":
                username = input("Username: ")
                password = input("Password: ")
                email = input("Email: ")
                phone = input("Phone: ")
                auth_serive.register_user(User(
                    username=username,
                    password=password,
                    email=email,
                    phone=phone)
                )
                print("User successfully registered")
    except BadRequestException as e:
        print(e.message)
    main_menu()


def user_menu(ch):
    global session_user
    user_todo = TodoService(user=session_user)
    match ch:
        case "1":
            data = user_todo.my_todos()

            for todo in data:
                print(" | ".join(list(map(str, todo))))
        case "2":
            title = input("Enter Todo title: ")
            user_todo.create_todo(title=title)
        case "3":
            todo_id = input("Enter Todo id: ")
            print("choose status: ")
            print("1. todo: ")
            print("2. process: ")
            print("3. done: ")
            s = input("Choose status: ")
            match s:
                case "1":
                    status = "todo"
                case "2":
                    status = "process"
                case "3":
                    status = "done"
            user_todo.update_todo(todo_id, status=status)
        case "4":
            todo_id = input("Enter Todo id: ")
            user_todo.delete_todo(todo_id=todo_id)
    main_menu()


if __name__ == '__main__':
    main_menu()


from app_enum import UserEnum
from view.auth import auth_view

def choose_client_type():
    
    choice = input("Do you want student(1) or teacher(2): ")

    if choice == "1":
        print("Hi Student!")
        auth_view(UserEnum.STUDENT)
        
    elif choice == "2":
        print("Hi Teacher!")
        auth_view(UserEnum.TEACHER)

    else:
        exit()

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os

def initialize_firestore():
    '''Create database connection'''

    #google cloud key
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]  = "bus-data-base-30fc8-firebase-adminsdk-x8ffm-f68a8dfb6e.json"

    #credentials - project id
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred, {'prodjectId': 'bus-data-base-30fc8',})

    # Get reference to database
    db = firestore.client()
    return db

def already_existing(db, user):
    '''Check for an already existing user'''
    result = db.collection("patrons").document(user).get()
    if result.exists:
        given_user = input("Username already exists. Please sign in.")

def get_user():
    return input("Please sign in\nUsername: ")

def get_pass():
    return input("Password: ")

def add_user(db):
    user = input("Enter a username: ")
    password = input("Enter a password: ")
    expired = input("Is this pass current and paid for? (Y/N)" ).upper()
    if expired == "Y":
        expired = False
    else:
        expired = True
    already_existing(db, user)

    #build dictionary for user information
    data = {"password": password, 
            "expired" : expired}
    db.collection("patrons").document(user).set(data)

def update_pass(db):
    user = input("Username: ")
    new_pass = input("Input new password: ")
    #check to see if the user exists
    result = db.collection("patrons").document(user).get()
    if not result.exits:
        print("Invalid Username")
        return False
    data =  result.to_dict()

    data["password"] = new_pass
    db.collection("patrons").document(user).set(data)

def sign_in(db):
    user = get_user()
    password = get_pass()
    info = db.collection("patrons").document(user).get()
    result = info.to_dict()
    if result["password"] == password:
        print(f"Welcome {user}!")
        return True
    else:
        print("Invalid username.")

def menu1():
    print("Welcome to the bus pass system.")
    print("What would you like to do?")
    print("1) Create a new user")
    print("2) Sign in")
    print("3) Quit")
    choice1 = int(input("Please enter the number of your choice: "))
    return choice1

def main():
    db = initialize_firestore()
    logged_in = False
    quit = False

    while quit != True:
        choice1 = menu1()
        if choice1 == 1:
            add_user(db)
        elif choice1 == 2:
            while logged_in == False:
                sign_in(db)
        elif choice1 == 3:
            quit = True
        else: 
            print("Invalid Option")

main()
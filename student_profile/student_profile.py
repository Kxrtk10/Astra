import json
import os

USERS_FOLDER = "users"


def create_account():

    print("\nCreate New Account\n")

    name = input("Name: ")
    username = input("Choose username: ")
    password = input("Choose password: ")

    learner_type = input(
        "Learner Type (school / competitive / college / professional / other): "
    )

    goal = input("Exam or goal (CAT, JEE, NEET, etc): ")

    subjects = input(
        "Subjects you want help with (comma separated): "
    ).split(",")

    study_hours = input("Study hours per day: ")

    user_data = {
        "name": name,
        "username": username,
        "password": password,
        "learner_type": learner_type,
        "goal": goal,
        "subjects": subjects,
        "study_hours": study_hours,
        "progress": {},
        "missed_topics": []
    }

    filepath = f"{USERS_FOLDER}/{username}.json"

    with open(filepath, "w") as f:
        json.dump(user_data, f, indent=4)

    print("\nAccount created successfully!\n")

    return user_data


def login():

    print("\nLogin\n")

    username = input("Username: ")
    password = input("Password: ")

    filepath = f"{USERS_FOLDER}/{username}.json"

    if not os.path.exists(filepath):
        print("User not found.")
        return None

    with open(filepath, "r") as f:
        user_data = json.load(f)

    if user_data["password"] != password:
        print("Incorrect password.")
        return None

    print(f"\nWelcome {user_data['name']}!\n")

    return user_data


def load_or_create_profile():

    print("1 - Login")
    print("2 - Create Account")

    choice = input("Select option: ")

    if choice == "1":
        user = login()

        if user:
            return user

        else:
            return load_or_create_profile()

    elif choice == "2":
        return create_account()

    else:
        print("Invalid choice")
        return load_or_create_profile()
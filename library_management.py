import json
from datetime import datetime
import os
import re

user_data = {'Member': [], 'Librarian': [], 'Admin': []}
user_type = None
user_database = 'account.txt'
loans_file = 'loanedmembers.txt'
books_file = 'books.txt'
current_time = datetime.now()

def sys_admin(role = 'admin'):
    picked_num = options(role)
    if picked_num == 1:
        member_manage(role)
    if picked_num == 2:
        librarian_manage(role)
    if picked_num == 3:
        print(f'\033[93m[*]\033[0m You have successfully logged out!\n')
        main()

def super_admin(role = 'super_admin'):
    picked_num = options(role)
    if picked_num == 1:
        member_manage(role)
    if picked_num == 2:
        librarian_manage(role)
    if picked_num == 3:
        admin_manage()
    if picked_num == 4:
        print(f'\033[93m[*]\033[0m You have successfully logged out!\n')
        main()
def options(role): #Main panel options
    generate_title('Welcome to Admin Panel')
    option_list = ['Member Account Management', 'Librarian Account Management', 'Logout']
    if role == 'super_admin':
        option_list.insert(2, 'Admin Account Management')
    generate_options(option_list)

    #To make sure the input is only 1 and 2
    while True:
        picked_num = input(f'\033[93m[*]\033[0m Enter the number to manage the users: ')
        try:
            input_value = int(picked_num)

            if not 0 < input_value <= len(option_list):
                raise ValueError
            return input_value

        #To handle invalid inputs rather than integers
        except ValueError:
            print(f'\033[91m[ERROR] Invalid input! Please enter again.\033[0m')
            continue

def cmd_option(user_type): #Create the options for the admin's command
    options = f'''
    Available commands:
    - add: Add a new {user_type}
    - view: View {user_type} details
    - search: Search {user_type} information
    - edit: Edit {user_type} information
    - delete: delete a {user_type}
    - options: Show the available commnads
    - exit: Back to Main Menu
    '''
    print(options)

def save_data(file_name, data): #To store the data into the database
    with open(file_name, 'w') as f:
        json.dump(data, f, indent=4)

def load_data(): #To load the data from the database
    global user_data
    try:
        if os.path.exists(user_database):
            with open(user_database, 'r') as f:
                user_data = json.load(f)
                return user_data
        else:
            user_data = {'Member': [], 'Librarian': [], 'Admin': []}
    except json.JSONDecodeError:
        user_data = {'Member': [], 'Librarian': [], 'Admin': []}

def generate_title(title): #Generate the title automatically
    print()
    print(f'{title.title()}')
    print(f'{"-" * 15}')

def generate_options(option_list): #Generate the option automatically
    number = 1
    for i in option_list:
        print(f'{number}. {i.title()}')
        number += 1
    print()

def generate_id():
    load_data()
    global user_type
    member_type = user_type.title()

    #To return default id value if there is no user in the database
    if not user_data[member_type]:
        return 101

    #To return the maximun value + 1 if the database has data.
    max_id = max(int(user['id'])for user in user_data[member_type])
    return max_id + 1

def member_manage(role): #Member Management Panel
    print()
    generate_title('Member Account Management')
    print("\033[93m[*]\033[0m Use [options] to view the available commands.\n")

    while True:
        global user_type
        user_type = 'member'
        command = input(f'\033[91mAdmin\033[0m~# ').strip()
        if command == 'add':
            add_data()
        elif command == 'view':
            view_data()
        elif command == 'search':
            search_data()
        elif command == 'edit':
            edit_data()
        elif command == 'delete':
            delete_data()
        elif command == 'options':
            cmd_option(user_type)
        elif command == 'exit':
            print()
            if role == 'admin':
                sys_admin()
            if role == 'super_admin':
                super_admin()
        else:
            print(f"\033[91m[ERROR] Unknown command. Type 'options' for a list of available commands.\033[0m")

def librarian_manage(role): #Librarian Management Panel
    print()
    generate_title('Librarian Account Management')
    print("\033[93m[*]\033[0m Use [options] to view the available commands.\n")

    while True:
        global user_type
        user_type = 'librarian'
        command = input(f'\033[91mAdmin\033[0m~# ').strip()
        if command == 'add':
            add_data()
        elif command == 'view':
            view_data()
        elif command == 'search':
            search_data()
        elif command == 'edit':
            edit_data()
        elif command == 'delete':
            delete_data()
        elif command == 'options':
            cmd_option(user_type)
        elif command == 'exit':
            print()
            if role == 'admin':
                sys_admin()
            if role == 'super_admin':
                super_admin()
        else:
            print(f"\033[91m[ERROR] Unknown command. Type 'options' for a list of available commands.\033[0m")

def admin_manage(): #Admin Management Panel
    print()
    generate_title('Admin Account Management')
    print("\033[93m[*]\033[0m Use [options] to view the available commands.\n")

    while True:
        global user_type
        user_type = 'admin'
        command = input(f'\033[91mAdmin\033[0m~# ').strip()
        if command == 'add':
            add_data()
        elif command == 'view':
            view_data()
        elif command == 'search':
            search_data()
        elif command == 'edit':
            edit_data()
        elif command == 'delete':
            delete_data()
        elif command == 'options':
            cmd_option(user_type)
        elif command == 'exit':
            print()
            super_admin()
        else:
            print(f"\033[91m[ERROR] Unknown command. Type 'options' for a list of available commands.\033[0m")


def role_validation(): #To validate the user role
    global user_type
    roles = ['member', 'librarian', 'admin']
    while True:
        role = input('Enter the role: ').lower().strip()

        if user_type.lower() == 'member' and role == roles[0]: #Check the role is member
                return role
        elif user_type.lower() == 'librarian' and role == roles[1]:  # Check the role is member
                return role
        elif user_type.lower() == 'admin' and role == roles[2]: #Check the role is member
                return role
        else:
            print(f'\033[91m[ERROR] Invalid role! Only "{user_type.lower()}" role is accepted.\033[0m')
            continue

def validate_data(pattern_key): #To validate the user information
    #Patterns to validate the input from the users
    global user_type
    member_type = user_type.title()
    patterns = {
        'full_name': re.compile(r'^[a-zA-Z0-9][\w\s.-_]{0,18}$'),
        'email': re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$'),
        'username': re.compile(r'^[a-zA-Z0-9][\w.-]{1,13}$'),
        'password': re.compile(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&]{1,5})[A-Za-z\d@$!%*?&]{8,}$')
    }
    pattern = patterns.get(pattern_key)

    if not pattern: #If there is no valid pattern in 'patterns' dictionary
        raise ValueError('Invalid Pattern Key!')

    while True:
        input_value = input(f'Enter the {pattern_key}: ').strip()
        match = pattern.fullmatch(input_value) #Match the input with the specific pattern

        if match:
            if pattern_key == 'email':
                if any(user['email'] == input_value for user in user_data[member_type]):
                    print(f'\033[91m[ERROR] This email is already registered. Please use a different email.\033[0m')
                    continue
            if pattern_key == 'full_name':
                if any(user['full_name'] == input_value for user in user_data[member_type]):
                    print(f'\033[91m[ERROR] This name is already used. Please choose a different first name.\033[0m')
                    continue
            if pattern_key == 'username':
                if any(user['username'] == input_value for user in user_data[member_type]):
                    print(f'\033[91m[ERROR] This username is already used. Please choose a different username.\033[0m')
                    continue
            return input_value

        else: #Raise the errors when the pattern is not matched with the input
            error_messages = {
                'full_name': 'Only alphabets, digits, and hyphens are allowed! Maximum length is 20 characters.',
                'email': 'Invalid email address format! Example: example@domain.com',
                'username': 'Invalid Username! Maximum length is 15 characters. Example: user_name123',
                'password': 'The password must be at least 8 characters long and include:\n- At least one uppercase letter\n- At least one lowercase letter\n- At least one number\n- At least one special character (@, $, !, %, *, ?, &)'
            }
            print(f'\033[91m[ERROR] {error_messages.get(pattern_key, "Invalid input.")}\033[0m')

def show_data(data_list, counter): #Function to dispaly the searched data
    print()
    print(f'\033[42m \033[30m\033[1m {"Id":<10} {"Full_name":<20} {"Email":<25} '
                      f'{"Username":<20} {"Password":<22} {"Role":<14} {"Registration_date":<20} \033[0m')
    for data in data_list:
        print(
            f'  {data.get("id"):<10} {data.get("full_name"):<20} {data.get("email"):<25} '
            f'{data.get("username"):<20} {data.get("password"):<22} {data.get("role"):<14} {data.get("registration_date"):<20}')
    print()
    if counter == 0:
        print(f'\n\033[93m[*] No data found!\033[0m')
    if counter > 0:
        print(f'\033[93m[*]\033[0m {counter} user{"" if counter == 1 or 0 else "s"} found!')
    print()

def add_data(): #To add user data into the database
    try:
        load_data()
        global user_type
        member_type = user_type.title() #Store the user for later usage

        data = {
            'id': generate_id(),
            'full_name': validate_data('full_name'),
            'email': validate_data('email'),
            'username': validate_data('username'),
            'password': validate_data('password'),
            'role': role_validation(),
            'registration_date': datetime.now().strftime('%d-%B-%Y')
        }

        #Add the member into the 'user_data' and store that in database using 'save_data' function.
        user_data[member_type].append(data)
        save_data(user_database, user_data)
        print(f'\033[92m[*] The {member_type} has been created successfully.\033[0m\n')
    except Exception as e:
        # Handle unexpected errors
        print(f'\033[91m[ERROR] An error occurred while adding the data: {e}\033[0m')

def view_data(): #To view details information of the users
    load_data()
    global user_type
    member_type = user_type.title()
    show_data(user_data[member_type], len(user_data[member_type]))

def search_data(): #To search the users using a specific keyword
    load_data()
    global user_type
    member_type = user_type.title()

    while True:
        option_list = ['id', 'full_name', 'email', 'username', 'exit']
        search_key = input(f'\033[93m\n[*]\033[0m Options: (id, full_name, email, username, \'exit\' to quit)\n'
                            f'Which field would you like to search?: ').lower()

        if search_key == 'exit':
            print(f'\033[93m[*] Exiting the searching process.\033[0m\n')
            break

        try:
            if not search_key in option_list: #To check the input is in option_list(line263)
                raise ValueError

            counter = 0
            search_value = input('Enter the keyword to search: ')
            data_list = []

            for data in user_data[member_type]: #To search the user data using the re module
                match_data = re.search(search_value, str(data[search_key]), flags=re.IGNORECASE)

                if match_data:
                    data_list.append(data)
                    counter += 1

            show_data(data_list, counter)
        except ValueError:
            print(f'\033[91m[ERROR] Invalid option! Please enter the valid option.\033[0m')

def edit_data(): #To edit the user data using 'id'
    view_data()
    global user_type
    member_type = user_type.title()

    while True:
        id = input(f'\033[93m[*]\033[0m Enter the {user_type}\'s ID you want to edit (or type \'exit\' to quit): ').lower()

        if id == 'exit':
            print(f'\033[93m[*]\033[0m Exiting the editing process.\n')
            break
        try:
            max_id = max(int(data['id']) for data in user_data[member_type]) + 1
            valid_id = int(id)  # Check whether the id is integer and within the valid range
            if not 100 < valid_id < max_id:
                raise ValueError("ID out of acceptable range.")
            for data in user_data[member_type]:  # loop the data inside database to compare with the id
                if valid_id == data['id']:
                    while True:  # Allow to choose the options to edit the user information
                        choice_to_edit = input(
                            f'\n\033[93m[*]\033[0m Options: (full_name, email, username, password)\n'
                            f'\033[93m[*]\033[0m Which field would you like to update?: ').lower()
                        option_list = ['full_name', 'email', 'username', 'password',]
                        if choice_to_edit in option_list:  # Check the input option is valid or not
                            edited_data = validate_data(choice_to_edit)
                            data[choice_to_edit] = edited_data
                            save_data(user_database, user_data)
                            print(f'\033[92m[*] The {member_type} has been edited successfully.\033[0m')

                            while True:
                                still_edit = input(f'\033[93m[*]\033[0m Do you want to continue editing this {member_type}? '
                                                   f'(Press \'n\' -> No, \'y\' -> Yes): ').lower()
                                if still_edit in ['y', 'n']:
                                    break
                                print(f'\033[91m[ERROR] Invalid option! Please enter again.\033[0m')
                            if still_edit == 'y':
                                continue
                            elif still_edit == 'n':
                                break

                        else:
                            print(f'\033[91m[ERROR] Invalid option! Please enter again.\033[0m')
                    break
            else:
                print(f'\033[91m[ERROR] The ID {valid_id} does not exist in the database. Please enter again.\033[0m')
        except ValueError:
            print(f'\033[91m[ERROR] Invalid ID! Please enter a valid ID, or ensure the ID exists in the database.\033[0m')

def delete_data(): #Delete the user data from the database using 'id'
    load_data()
    global user_type
    member_type = user_type.title()

    while True:
        id = input(f'\033[93m[*]\033[0m Enter the {member_type}\'s ID you want to delete (or type \'exit\' to quit): ')

        if id == 'exit':
            print(f'\033[93m[*] Exiting the deleting process.\033[0m\n')
            break

        try: #Try to validate the id before remove from the database
            max_id = max(int(id['id']) for id in user_data[member_type]) + 1
            valid_id = int(id)
            if not 100 < valid_id < max_id: #To make sure the id is within the valid range
                raise ValueError
            for data in user_data[member_type]: #Find the id and remove from the database
                if valid_id == data['id']:
                    user_data[member_type].remove(data)

                    counter_id = 101 #Rearrange the id number after deleting the user
                    for user in user_data[member_type]:
                        user['id'] = counter_id
                        counter_id += 1
                    save_data(user_database, user_data)
                    print(f'\033[92m[*] The {member_type} has been deleted successfully.\033[0m')

        except ValueError:
            print(f'\033[91m[ERROR] Invalid ID! Please enter a valid ID, or ensure the ID exists in the database.\033[0m')

##################################################### Member #############################################################
def libmeminterface(user):
    generate_title(f"Welcome User {user['username']}")
    option_list = ['Search books', 'View loaned books', 'Update profile', 'Check_out book', 'Logout']
    generate_options(option_list)

    while True:  # custom error message if they input strings
        try:
            action = int(input('Enter options: '))
            if 1 <= action <= 5:
                break
            else:
                print('Please Enter a number between 1 and 4!')
        except:
            print('You must enter a valid number!')

    if action == 1:
        searchbooks(user)
    elif action == 2:
        viewloanedbooks(user)
    elif action == 3:
        update_profile(user)  # need to create defs for the actions
    elif action == 4:
        book_checkout(user)
    else:
        main()

def goback(user):  # going back to the main menu function
    while True:
        try:
            backaction = input("Enter 'q' to 'exit'> ").upper()
            if backaction == 'Q':
                libmeminterface(user)
            else:
                continue
        except ValueError:
            print("Enter a valid answer! ")

def viewloanedbooks(user):
    username = user['username']
    cal_overdue_fee(username)
    print('Here are your loaned books')
    print('----------------------')
    print(
        f"\033[42m\033[30m{'BookID':<15} {'Name':<45} {'Genre':<15} {'Author':<20} {'LoanDate':<15} {'DueDate':<15} {'OverDueFees':<15}\033[0m")
    allbooks = []
    with open(loans_file, 'r') as f:
        allbooks = json.load(f)
    for book in allbooks[user['username']]:  # change after i got user log in
        print(
            f"{book['book_ID']:<15} {book['book_name']:<45} {book['genre']:<15} {book['author']:<20} {book['loaned_date']:<15} {book['due_date']:<15} {book['overdue_fee']:<15}")
    goback(user)

def searchbooks(user):
    sbook = []
    with open(books_file, 'r') as f:
        sbook = json.load(f)

    try:
        search = int(input(
            'WELCOME TO SEARCH MENU \n---------------------- \n1. Book_ID \n2. Status \nEnter the field you would like to search: '))

        if not 1 <= search <=2:
            raise ValueError

        print(f"\033[42m\033[30m{'BookID':<15} {'Name':<50} {'Genre':<20} {'Author':<15}\033[0m")
        for book in sbook['books']:
            print(f"{book['book_ID']:<15} {book['book_name']:<50} {book['genre']:<20} {book['author']}")

        if search == 1:
            bookid = input('Enter bookID: ').upper()
            print(f"\033[42m\033[30m{'BookID':<15} {'Name':<50} {'Genre':<15} {'Author':<15}\033[0m")
            for book in sbook['books']:
                if bookid == book['book_ID']:
                    print(f"{book['book_ID']:<15} {book['book_name']:<50} {book['genre']:<15} {book['author']:<15} ")
            goback(user)

        elif search == 2:
            status = int(input('1. Search available books \n2. Search loaned books \nEnter option:'))
            print(f"\033[42m\033[30m{'BookID':<15} {'Name':<50} {'Status':<15}\033[0m")
            with open(books_file, 'r') as f:
                avbook = json.load(f)
            if status == 2:
                for book in avbook['books']:
                    if book['status'] == 'Loaned':
                        print(f"{book['book_ID']:<15} {book['book_name']:<50} {book['status']:<15}")
                goback(user)
            elif status == 1:
                for book in sbook['books']:
                    if book['status'] == 'Not Loaned':
                        print(f" {book['book_ID']:<15} {book['book_name']:<50} {book['status']:<15}")
                goback(user)
            else:
                print('Enter a valid answer')
    except ValueError:
        print('Please enter a valid option.')
        searchbooks(user)
        goback(user)

def update_profile(user):
    load_data()
    global user_type
    user_type = 'Member'
    generate_title('User Information')
    restricted_field = ['role', 'registration_date']
    for key,value in user.items():
        if key in restricted_field:
            continue
        print(f"{key}: {value}")

    while True:
        try:
            option = input("Which field do you want to update (full_name, email, username, password): ")
            option_list = ['full_name', 'email', 'username', 'password', ]
            if option in option_list:
                for data in user_data['Member']:
                    if user['id'] == data['id']:
                        updated_data = validate_data(option)
                        data[option] = updated_data
                        new_user_info = data

                        if option == option_list[2]:
                            member_book = loans_file
                            with open(member_book, 'r') as f:
                                loaned_book_data = json.load(f)

                                if user['username'] in loaned_book_data:
                                    loaned_book_data[updated_data] = loaned_book_data.pop(user['username'])
                            with open(member_book, 'w') as f:
                                json.dump(loaned_book_data, f, indent=4)

                        save_data(user_database, user_data)

                        exit = input("Do you want to still editing the data (Press 'n' -> No, 'y' -> Yes): ")
                        if exit.lower() == 'y':
                            continue
                        if exit.lower() == 'n':
                            print()
                            libmeminterface(new_user_info)
            else:
                print(f'\033[91m[ERROR] Invalid option! Please enter again.\033[0m')
        except ValueError:
            print("Please enter a valid number.")

def book_checkout(user):
    books = load_book_data(books_file)
    loans = load_book_data(loans_file)
    try:
        id = input(f"\033[93m[*]\033[0m Type the book id you want to check out: ")
    except ValueError:
        print('Invalid input. Please enter book id.')

    found = False
    for item in loans[user['username']]:
        if id in item['book_ID']:
            loans[user['username']].remove(item)
            save_data(loans_file, loans)
            print('\033[92m[*]\033[0m The book is checked out successfully!')
            found = True
            break
    if not found:
        print(f"The book id doesn't exist.")

    for book in books['books']:
        if book['book_ID'] == id:
            book['status'] = 'Not Loaned'
            save_data(books_file, books)


################################################ LIBRARIAN ################################################################
def librarian_interface():
    while True:
        generate_title("Library Management System")
        option_list = ["Add Book", "Loan Process", "Edit Book", "View Books", "Delete Book", "Logout"]
        generate_options(option_list)

        choice = input("Enter your choice: ")

        if choice == '1':
            add_new_book()
        elif choice == '2':
            loan_process()
        elif choice == '3':
            edit_book()
        elif choice == '4':
            view_books()
        elif choice == '5':
            delete_book()
        elif choice == '6':
            print("Exiting the Library Management System.")
            break
        else:
            print("Invalid choice. Please try again.")
def load_book_data(file_name):
    try:
        with open(file_name, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"books": []}

def cal_overdue_fee(user):
    loan_data = load_book_data(loans_file)
    current_time = datetime.now()


    try:
        total = 0
        for item in loan_data[user]:
            due_date = datetime.strptime(item['due_date'], "%d-%m-%Y")
            overdue_days = (current_time - due_date).days
            fee = calculate_overdue_fee(overdue_days)
            item['overdue_fee'] = fee
            total += fee
        save_data(loans_file, loan_data)
        return total
    except KeyError:
        return 0

def calculate_overdue_fee(days_passed):
    if days_passed == 1:
        return 2.00
    elif days_passed == 2:
        return 3.00
    elif days_passed == 3:
        return 4.00
    elif days_passed == 4:
        return 5.00
    elif days_passed == 5:
        return 6.00
    elif days_passed < 0:
        return 0.00
    else:
        return 10.00

def get_due_date():
    date_str = input("Enter the due date (dd-mm-yyyy): ")
    return datetime.strptime(date_str, "%d-%m-%Y")

# Function to add new book to books.txt
def add_new_book():
    # Load existing books data
    books_data = load_book_data(books_file)

    # New book details
    book_id = input("Enter new book ID: ")
    book_name = input("Enter book name: ")
    genre = input("Enter genre: ")
    author = input("Enter author: ")
    status = "Not Loaned"

    new_book = {
        "book_ID": book_id,
        "book_name": book_name,
        "genre": genre,
        "author": author,
        "status": status
    }

    # Add new book to books list
    books_data["books"].append(new_book)

    # Save updated books data
    save_data(books_file, books_data)
    print(f"New book '{book_name}' has been added to the library.")

def edit_book():
    books_data = load_book_data(books_file)
    book_id = input("Enter the book ID to edit: ")
    for book in books_data["books"]:
        if book["book_ID"] == book_id:
            book["book_name"] = input("Enter new book name: ")
            book["genre"] = input("Enter new genre: ")
            book["author"] = input("Enter new author: ")
            book["status"] = input("Enter new status: ")
            save_data(books_file, books_data)
            print(f"Book '{book_id}' has been updated.")
            return
    print(f"Book '{book_id}' not found.")

def view_books():
    books = load_book_data(books_file)

    print(f"\033[42m\033[30m{'BookID':<15} {'Name':<50} {'Genre':<20} {'Author':<20} {'Status':<15}\033[0m")
    for book in books['books']:
        print(f"{book['book_ID']:<15} {book['book_name']:<50} {book['genre']:<20} {book['author']:<20} {book['status']:<15}")
    exit = input("Enter 'q' to 'exit'> ")
    if exit.lower() == 'q':
        pass

# Function to delete a book from books.txt
def delete_book():
    books_data = load_book_data(books_file)
    book_id = input("Enter the book ID to delete: ")
    for book in books_data["books"]:
        if book["book_ID"] == book_id:
            books_data["books"].remove(book)
            save_data(books_file, books_data)
            print(f"Book '{book_id}' has been deleted.")
            return
    print(f"Book '{book_id}' not found.")

# Function to handle loan process
def loan_process():
    # Load existing loan data
    loans = load_book_data(loans_file)
    books = load_book_data(books_file)

    while True:
        try:
            # Get username and book_id as input
            username = str(input("Enter the username: "))
            book_id = str(input("Enter the book ID: "))
            break
        except ValueError:
            print('Invalid Input. Please try again.')

    # Check the user has already loaned 5 books
    user_account = load_data()
    if username in loans and username in (user['username'] for user in user_account['Member']): #check the user exists in the account file and loan file
        if len(loans[username]) >= 5:
            print('The user has already loaned 5 books.')
            return
    else:
        print("The user doesn't exist.")
        return

    # Check whether the user has overdue_fee or not
    overdue_fee = cal_overdue_fee(username)
    if overdue_fee > 0:
        print('The user has overdue fee and cannot proceed to the loan process!')
        return

    # Check whether the book is loaned or not
    if book_id in [item['book_ID'] for item in books['books']]:
        for item in books['books']:
            if item['status'] == 'Loaned' and item['book_ID'] == book_id:
                print('The book is already loaned.\n')
                return
            if item['status'] == 'Not Loaned' and item['book_ID'] == book_id:
                item['status'] = 'Loaned'
                save_data(books_file, books)
                break
    else:
        print("The book id doesn't exists. Please try again.\n")
        return


    # Get the due date from user input
    due_date = get_due_date()

    # Calculate the difference
    time_difference = due_date - current_time

    if time_difference.days >= 0:
        # If due date is in the future
        days = time_difference.days
        hours, remainder = divmod(time_difference.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        print(f"Time left until due date: {days} days, {hours} hours, and {minutes} minutes.")
    else:
        # If due date is in the past
        days_passed = abs(time_difference.days)
        overdue_fee = calculate_overdue_fee(days_passed)
        print(f"{days_passed} day(s) have passed since the due date.")
        print(f"Overdue fee: RM {overdue_fee:.2f}")

    # Display user and book information
    print(f"Username: {username}")
    print(f"Book ID: {book_id}")

    # Add or update loan information

    for book in books['books']:
        if book_id == book['book_ID']:
            book_info = book

    loan_info = {
        "book_ID": book_id,
        "book_name": book_info['book_name'],
        "genre": book_info['genre'],
        "author": book_info['author'],
        "status": 'Loaned',
        "loaned_date": current_time.strftime("%d-%m-%Y"),
        "due_date": due_date.strftime("%d-%m-%Y"),
        "overdue_fee": overdue_fee if time_difference.days < 0 else 0.00
    }

    # Update the loans dictionary
    if username in loans: # To verify the user exists in loanedmembers.txt
        loans[username].append(loan_info)
    else: # if the user doesn't exist, create a new object for user to store loaned books' information
        loans.update({username:[loan_info]})

    # Save updated loan data
    save_data(loans_file, loans)

    print("Loan information has been updated.")

################################################ LIBRARIAN ################################################################
def login_users(data):
    generate_title('Welcome to Brickfields Kuala Lumpur Community Library')
    while True:
        username = input('Enter your email address: ')
        password = input('Enter your password: ')

        for category in data.values():
            for user in category:
                if user["email"] == username and user["password"] == password:
                    print(f"\033[92m[*]\033[0m Login successful! Welcome {user['username']}, Role: {user['role']}\n")
                    return user
        print("\033[93m[*]\033[0m Invalid email or password, try again.\n")

def select_interface(user):
    interface = user["role"]

    if interface == "admin":
        sys_admin(interface)
    if interface == 'super_admin':
        super_admin(interface)
    if interface == 'member':
        libmeminterface(user)
    if interface == 'librarian':
        librarian_interface()

def main():
    account_data = load_data()

    while True:
        user = login_users(account_data)
        if user:
            select_interface(user)


if __name__ == '__main__':
    main()


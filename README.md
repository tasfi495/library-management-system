# Library Management System

A command-line Library Management System developed in Python for Brickfields Kuala Lumpur Community Library.

## Features

- Login system for Super Admin, Admin, Librarian, and Member
- Add, view, search, edit, and delete user accounts
- Add, edit, view, and delete books
- Process book loans and returns
- Track due dates and overdue fees
- Search books by ID or loan status
- Update member profile information
- Store data using JSON-formatted text files

## Technologies Used

- Python
- JSON
- Python standard libraries:
  - `json`
  - `datetime`
  - `os`
  - `re`

## Project Files

```text
library_management.py
account.txt
books.txt
loanedmembers.txt
README.md
```

## How to Run

1. Make sure Python is installed.
2. Keep all project files in the same folder.
3. Open the folder in a terminal.
4. Run:

```bash
python library_management.py
```

## User Roles

- **Super Admin:** Manages Admin, Librarian, and Member accounts
- **Admin:** Manages Librarian and Member accounts
- **Librarian:** Manages books and loan records
- **Member:** Searches books, views loans, updates profile, and returns books

## Important Notes

The program expects these exact file names:

```text
account.txt
books.txt
loanedmembers.txt
```

The account file contains sample login details. Replace any personal information and passwords before uploading the project publicly.

## Contributors

- Hein Htet
- Mohammad Abu Nur Tasfi
- Aung Kaung Khant
- Moe Lwin Paing Htoo

## Purpose

This project was created as a Python Programming group assignment at Asia Pacific University of Technology & Innovation.

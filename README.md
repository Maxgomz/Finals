# Barangay Service Request Desk

A desktop application for organizing requests from residents in a barangay or
small organization. It supports categorized requests, priority queues, staff
assignment, in-progress tracking, completion, cancellation, search, CSV export,
SQLite storage, audit logging, and database backups.

## Why This Is an Original Project Idea

The photo's examples were suggestions only. This project uses the less-common
idea of a barangay service request desk rather than copying a listed example.
Residents can submit service requests with a category and details. Staff can
start the next waiting request, assign it to a staff member, complete or cancel
it, search records, and export reports. Requests persist through application
restarts.

## Included Data Structures and Modules

The project was written for Modules 1-10:

1. Python functions, variables, collections, and object-oriented classes
2. Big-O complexity analysis
3. Lists and abstract data types
4. Stack ADT for undo
5. Queue ADT using `collections.deque`
6. Recursion for BST counting and traversal
7. Singly linked list for registration history
8. Doubly linked list and circular linked list
9. Sequential search, binary search, and merge sort
10. Binary search tree with insertion, search, and deletion

No heap or heap algorithms are used.

## Project Summary

- `Patient` represents one resident or service request.
- `Stack` stores recently started requests for undo operations.
- `deque` manages emergency, urgent, and routine waiting lines.
- `SinglyLinkedList` keeps registration history.
- `DoublyLinkedList` supports forward and backward navigation.
- `CircularLinkedList` demonstrates circular traversal and deletion.
- `PatientBST` organizes waiting requests by patient/request ID.
- `ClinicSystem` connects the structures with application operations.
- `ClinicApplication` provides the Tkinter graphical interface.
- SQLite provides persistent waiting, in-progress, completed, cancelled, settings,
  and audit records. A small schema migration keeps databases made by earlier
  project versions usable.

## Run the Application

### Recommended: Standalone executable

Run:

`dist\BarangayServiceRequestDesk.exe`

No Python installation is required for the built executable.

### Run from Python

Python 3 with Tkinter is required:

```bat
python Finals.py
```

For the text menu:

```bat
python Finals.py --cli
```

For a custom organization name and database:

```bat
python Finals.py --organization "Community Service Office" --database "service.db"
```

The executable does not accept custom database arguments. It stores
`clinic_records.db` in the current Windows user's local application data folder:
`%LOCALAPPDATA%\BarangayServiceRequestDesk`.

## Database and Data Safety

SQLite automatically creates these tables:

- `settings`: stores counters used for request IDs and arrival numbers
- `patients`: stores requests and their lifecycle status, category, details,
  assigned staff, and timestamps
- `audit_log`: records registration, service, cancellation, undo, export, and backup actions

The Reports tab can:

- create a database backup
- export all request statuses to CSV

The backup and export folders are created automatically.

## Real-World Scope

This is usable for a **single-computer local pilot** by a small organization.
It is not a shared multi-user system: two installations do not synchronize their
databases, and there is no staff login or permissions model.
For multi-user or mission-critical deployment, it would additionally need:

- staff login and role permissions
- centralized database hosting
- network/server access
- encrypted backups and privacy controls
- scheduled backup testing
- formal medical or financial compliance when applicable
- automated unit and integration tests

Do not store sensitive medical, financial, or similarly protected information
in this classroom pilot. Use only the minimum resident information needed for
testing and demonstration.

## Main Files

- `Finals.py`: main source code
- `run_barangay_desk.bat`: launcher for Python
- `BarangayServiceRequestDesk.spec`: PyInstaller build configuration
- `dist\BarangayServiceRequestDesk.exe`: standalone Windows executable
- `clinic_records.db`: SQLite database created on first run
- `README.md`: project documentation
- `test_service_requests.py`: automated checks for lifecycle, migration, export,
  backup, and input validation

Run the checks with:

```bat
python -m unittest test_service_requests.py -v
```

## Build the Executable Again

From this folder:

```bat
python -m pip install pyinstaller
python -m PyInstaller --clean --noconfirm --onefile --windowed --name BarangayServiceRequestDesk Finals.py
```

The executable is written to `dist\BarangayServiceRequestDesk.exe`.

## Code Length and Quality

The current source is about 1,400 lines. Making it roughly 2,500 lines would
not automatically improve it or reduce bugs. Extra lines usually mean duplicated
code, more code paths, and more chances for mistakes.

A better project is measured by:

- clear class names
- one function doing one responsibility
- tested edge cases
- persistent and recoverable data
- useful error handling
- small, understandable modules
- no duplicate implementations

This project should stay close to its current level of complexity for a
second-year Python course: classes, basic Tkinter, linked structures, recursion,
sorting, searching, and SQLite.  

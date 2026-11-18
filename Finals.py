import argparse
import csv
import json
import os
import sqlite3
import sys
import tkinter as tk
from collections import deque
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from tkinter import messagebox, ttk


@contextmanager
def database_connection(database_file):
    connection = sqlite3.connect(database_file)
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


class Patient:
    def __init__(
        self,
        patient_id,
        name,
        priority,
        arrival_number,
        registered_at=None,
        category="General",
        description="",
        assigned_to="",
        status="waiting",
        completed_at=None,
        residency_verified=False,
        residency_method="",
        verified_by="",
        verified_at=None,
    ):
        self.patient_id = patient_id
        self.name = name.strip()
        self.priority = priority
        self.arrival_number = arrival_number
        self.registered_at = (
            datetime.now() if registered_at is None else registered_at
        )
        self.category = category
        self.description = description
        self.assigned_to = assigned_to
        self.status = status
        self.completed_at = completed_at
        self.residency_verified = residency_verified
        self.residency_method = residency_method
        self.verified_by = verified_by
        self.verified_at = verified_at

    def __repr__(self):
        return (
            f"Patient(id={self.patient_id}, name={self.name!r}, "
            f"priority={self.priority}, arrival={self.arrival_number})"
        )

# Module 4: Stack ADT
class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if self.is_empty():
            return None
        return self.items.pop()

    def peek(self):
        if self.is_empty():
            return None
        return self.items[-1]

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)


# Module 7: singly linked list
class ListNode:
    def __init__(self, data):
        self.data = data
        self.next = None


class SinglyLinkedList:
    def __init__(self):
        self.head = None

    def insert_at_end(self, data):
        new_node = ListNode(data)
        if self.head is None:
            self.head = new_node
            return

        current = self.head
        while current.next is not None:
            current = current.next
        current.next = new_node

    def to_list(self):
        result = []
        current = self.head
        while current is not None:
            result.append(current.data)
            current = current.next
        return result

    def delete_by_id(self, patient_id):
        if self.head is None:
            return False

        if self.head.data.patient_id == patient_id:
            self.head = self.head.next
            return True

        current = self.head
        while current.next is not None:
            if current.next.data.patient_id == patient_id:
                current.next = current.next.next
                return True
            current = current.next
        return False


# Module 8: doubly linked list
class DoublyNode:
    def __init__(self, data):
        self.data = data
        self.previous = None
        self.next = None


class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, data):
        new_node = DoublyNode(data)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
            return

        new_node.previous = self.tail
        self.tail.next = new_node
        self.tail = new_node

    def delete_by_id(self, patient_id):
        current = self.head
        while current is not None:
            if current.data.patient_id == patient_id:
                if current.previous is not None:
                    current.previous.next = current.next
                else:
                    self.head = current.next

                if current.next is not None:
                    current.next.previous = current.previous
                else:
                    self.tail = current.previous
                return True
            current = current.next
        return False

    def forward(self):
        result = []
        current = self.head
        while current is not None:
            result.append(current.data)
            current = current.next
        return result

    def backward(self):
        result = []
        current = self.tail
        while current is not None:
            result.append(current.data)
            current = current.previous
        return result


# Module 8: circular singly linked list
class CircularLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, data):
        new_node = ListNode(data)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
            new_node.next = self.head
        else:
            self.tail.next = new_node
            self.tail = new_node
            new_node.next = self.head

    def delete_by_id(self, patient_id):
        if self.head is None:
            return False

        current = self.head
        previous = self.tail
        for _ in range(self.length()):
            if current.data.patient_id == patient_id:
                if current is self.head and current is self.tail:
                    self.head = None
                    self.tail = None
                elif current is self.head:
                    self.head = current.next
                    self.tail.next = self.head
                elif current is self.tail:
                    previous.next = self.head
                    self.tail = previous
                else:
                    previous.next = current.next
                return True
            previous = current
            current = current.next
        return False

    def length(self):
        if self.head is None:
            return 0
        count = 1
        current = self.head.next
        while current is not None and current is not self.head:
            count += 1
            current = current.next
        return count

    def to_list(self):
        if self.head is None:
            return []
        result = [self.head.data]
        current = self.head.next
        while current is not None and current is not self.head:
            result.append(current.data)
            current = current.next
        return result


# Module 10: Binary Search Tree
class BSTNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


class PatientBST:
    def __init__(self):
        self.root = None

    def insert(self, patient):
        self.root = self._insert(self.root, patient)

    def _insert(self, node, patient):
        if node is None:
            return BSTNode(patient)
        if patient.patient_id < node.data.patient_id:
            node.left = self._insert(node.left, patient)
        elif patient.patient_id > node.data.patient_id:
            node.right = self._insert(node.right, patient)
        return node

    def search(self, patient_id):
        return self._search(self.root, patient_id)

    def _search(self, node, patient_id):
        if node is None:
            return None
        if patient_id == node.data.patient_id:
            return node.data
        if patient_id < node.data.patient_id:
            return self._search(node.left, patient_id)
        return self._search(node.right, patient_id)

    def delete(self, patient_id):
        self.root = self._delete(self.root, patient_id)

    def _delete(self, node, patient_id):
        if node is None:
            return None
        if patient_id < node.data.patient_id:
            node.left = self._delete(node.left, patient_id)
        elif patient_id > node.data.patient_id:
            node.right = self._delete(node.right, patient_id)
        else:
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left

            successor = node.right
            while successor.left is not None:
                successor = successor.left
            node.data = successor.data
            node.right = self._delete(node.right, successor.data.patient_id)
        return node

    def inorder(self):
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node is not None:
            self._inorder(node.left, result)
            result.append(node.data)
            self._inorder(node.right, result)


class ClinicSystem:
    """Clinic waiting-line system using module-based data structures."""

    PRIORITIES = {"routine": 3, "urgent": 2, "emergency": 1}
    CATEGORIES = (
        "General",
        "Documents",
        "Health",
        "Infrastructure",
        "Social Services",
        "Other",
    )

    def __init__(self, data_file=None):
        self.next_arrival = 1
        self.next_patient_id = 1
        if data_file is None:
            if getattr(sys, "frozen", False):
                application_folder = Path(
                    os.environ.get(
                        "LOCALAPPDATA",
                        Path.home() / "AppData" / "Local",
                    )
                ) / "BarangayServiceRequestDesk"
            else:
                application_folder = Path(__file__).resolve().parent
            self.data_file = application_folder / "clinic_records.db"
        else:
            self.data_file = Path(data_file)
            if self.data_file.suffix.lower() != ".db":
                self.data_file = self.data_file.with_suffix(".db")

        if self.data_file.suffix == ".json":
            self.data_file = self.data_file.with_suffix(".db")

        # Module 5: Queue ADT implemented with collections.deque
        self.routine_queue = deque()
        self.urgent_queue = deque()
        self.emergency_queue = deque()

        # Module 4: Stack ADT
        self.undo_stack = Stack()

        # Modules 7 and 8: linked lists
        self.registration_history = SinglyLinkedList()
        self.waiting_doubly = DoublyLinkedList()
        self.waiting_circular = CircularLinkedList()

        # Module 10: Binary Search Tree
        self.waiting_bst = PatientBST()

        self.active_requests = []
        self.served_patients = []
        self.cancelled_requests = []
        self.records_by_id = []
        self.init_database()
        self.load()

    def init_database(self):
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        with database_connection(self.data_file) as connection:
            connection.execute("PRAGMA foreign_keys = ON")
            connection.execute("PRAGMA journal_mode = WAL")
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value INTEGER NOT NULL
                )
                """
            )
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS patients (
                    patient_id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    priority TEXT NOT NULL,
                    arrival_number INTEGER NOT NULL,
                    registered_at TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'waiting',
                    category TEXT NOT NULL DEFAULT 'General',
                    description TEXT NOT NULL DEFAULT '',
                    assigned_to TEXT NOT NULL DEFAULT '',
                    completed_at TEXT
                )
                """
            )
            existing_columns = {
                row[1]
                for row in connection.execute("PRAGMA table_info(patients)")
            }
            migrations = {
                "category": "TEXT NOT NULL DEFAULT 'General'",
                "description": "TEXT NOT NULL DEFAULT ''",
                "assigned_to": "TEXT NOT NULL DEFAULT ''",
                "completed_at": "TEXT",
            }
            for column, definition in migrations.items():
                if column not in existing_columns:
                    connection.execute(
                        f"ALTER TABLE patients ADD COLUMN {column} {definition}"
                    )
            connection.execute(
                "UPDATE patients SET status = 'completed' WHERE status = 'served'"
            )
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS audit_log (
                    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    action TEXT NOT NULL,
                    patient_id INTEGER,
                    details TEXT,
                    created_at TEXT NOT NULL
                )
                """
            )

    def add_audit(self, action, patient_id=None, details=""):
        with database_connection(self.data_file) as connection:
            connection.execute(
                """
                INSERT INTO audit_log (action, patient_id, details, created_at)
                VALUES (?, ?, ?, ?)
                """,
                (
                    action,
                    patient_id,
                    details,
                    datetime.now().isoformat(),
                ),
            )

    def create_backup(self, backup_folder=None):
        if backup_folder is None:
            backup_folder = self.data_file.parent / "backups"
        else:
            backup_folder = Path(backup_folder)
        backup_folder.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = backup_folder / f"{self.data_file.stem}_{timestamp}.db"

        source = sqlite3.connect(self.data_file)
        destination = None
        try:
            destination = sqlite3.connect(backup_file)
            source.backup(destination)
        finally:
            if destination is not None:
                destination.close()
            source.close()
        return backup_file

    def recent_audit(self, limit=20):
        if not isinstance(limit, int) or limit < 1:
            raise ValueError("Audit limit must be a positive whole number.")
        with database_connection(self.data_file) as connection:
            return connection.execute(
                """
                SELECT action, patient_id, details, created_at
                FROM audit_log
                ORDER BY log_id DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()

    def export_csv(self, export_file=None):
        if export_file is None:
            export_file = self.data_file.parent / (
                f"barangay_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            )
        else:
            export_file = Path(export_file)

        export_file.parent.mkdir(parents=True, exist_ok=True)
        with export_file.open("w", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file)
            writer.writerow([
                "Patient ID",
                "Name",
                "Priority",
                "Arrival Number",
                "Registered At",
                "Status",
                "Category",
                "Request Details",
                "Assigned Staff",
            ])
            for patient in self.all_waiting():
                writer.writerow(self.patient_csv_row(patient, "Waiting"))
            for patient in self.served_patients:
                writer.writerow(self.patient_csv_row(patient, "Completed"))
            for patient in self.active_requests:
                writer.writerow(self.patient_csv_row(patient, "In progress"))
            for patient in self.cancelled_requests:
                writer.writerow(self.patient_csv_row(patient, "Cancelled"))
        self.add_audit("EXPORT_CSV", details=str(export_file))
        return export_file

    @staticmethod
    def patient_csv_row(patient, status):
        return [
            patient.patient_id,
            patient.name,
            patient.priority.title(),
            patient.arrival_number,
            patient.registered_at.isoformat()
            if isinstance(patient.registered_at, datetime)
            else str(patient.registered_at),
            status,
            patient.category,
            patient.description,
            patient.assigned_to,
        ]

    def save(self):
        with database_connection(self.data_file) as connection:
            connection.execute(
                "INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)",
                ("next_arrival", self.next_arrival),
            )
            connection.execute(
                "INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)",
                ("next_patient_id", self.next_patient_id),
            )
            connection.execute("DELETE FROM patients")
            records = (
                [(patient, "waiting") for patient in self.all_waiting()]
                + [(patient, "in_progress") for patient in self.active_requests]
                + [(patient, "completed") for patient in self.served_patients]
                + [(patient, "cancelled") for patient in self.cancelled_requests]
            )
            for patient, status in records:
                connection.execute(
                    """
                    INSERT INTO patients
                    (patient_id, name, priority, arrival_number, registered_at, status,
                     category, description, assigned_to, completed_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        patient.patient_id,
                        patient.name,
                        patient.priority,
                        patient.arrival_number,
                        patient.registered_at.isoformat()
                        if isinstance(patient.registered_at, datetime)
                        else str(patient.registered_at),
                        status,
                        patient.category,
                        patient.description,
                        patient.assigned_to,
                        patient.completed_at.isoformat()
                        if isinstance(patient.completed_at, datetime)
                        else None,
                    ),
                )

    def load(self):
        with database_connection(self.data_file) as connection:
            settings = dict(
                connection.execute("SELECT key, value FROM settings").fetchall()
            )
            self.next_arrival = int(settings.get("next_arrival", 1))
            self.next_patient_id = int(settings.get("next_patient_id", 1))
            rows = connection.execute(
                """
                SELECT patient_id, name, priority, arrival_number, registered_at, status,
                       category, description, assigned_to, completed_at
                FROM patients
                ORDER BY
                    arrival_number
                """
            ).fetchall()

        for (
            patient_id,
            name,
            priority,
            arrival_number,
            registered_at,
            status,
            category,
            description,
            assigned_to,
            completed_at,
        ) in rows:
            patient = Patient(
                patient_id=patient_id,
                name=name,
                priority=priority,
                arrival_number=arrival_number,
                registered_at=datetime.fromisoformat(registered_at)
                if registered_at
                else datetime.now(),
                category=category,
                description=description,
                assigned_to=assigned_to,
                status=status,
                completed_at=datetime.fromisoformat(completed_at)
                if completed_at
                else None,
            )
            self.next_arrival = max(self.next_arrival, arrival_number + 1)
            self.next_patient_id = max(self.next_patient_id, patient_id + 1)
            self.records_by_id.append(patient)
            self.registration_history.insert_at_end(patient)
            if status == "completed":
                self.served_patients.append(patient)
                continue
            if status == "cancelled":
                self.cancelled_requests.append(patient)
                continue
            if status == "in_progress":
                self.active_requests.append(patient)
                self.undo_stack.push(patient)
                continue
            if patient.priority == "emergency":
                self.emergency_queue.append(patient)
            elif patient.priority == "urgent":
                self.urgent_queue.append(patient)
            else:
                patient.priority = "routine"
                self.routine_queue.append(patient)
            self.waiting_doubly.append(patient)
            self.waiting_circular.append(patient)
            self.waiting_bst.insert(patient)
        self.records_by_id.sort(key=lambda patient: patient.patient_id)

    def add_patient(
        self,
        name,
        priority="routine",
        category="General",
        description="",
        assigned_to="",
    ):
        name = name.strip()
        if not name:
            raise ValueError("Patient name cannot be empty.")
        if len(name) > 100:
            raise ValueError("Resident name must be 100 characters or fewer.")
        priority = priority.lower()
        if priority not in self.PRIORITIES:
            raise ValueError("Priority must be routine, urgent, or emergency.")
        if category not in self.CATEGORIES:
            raise ValueError("Choose a valid request category.")
        description = description.strip()
        if len(description) > 1000:
            raise ValueError("Request details must be 1,000 characters or fewer.")
        assigned_to = assigned_to.strip()
        if len(assigned_to) > 100:
            raise ValueError("Staff name must be 100 characters or fewer.")

        patient = Patient(
            patient_id=self.next_patient_id,
            name=name,
            priority=priority,
            arrival_number=self.next_arrival,
            category=category,
            description=description,
            assigned_to=assigned_to,
        )
        self.records_by_id.append(patient)
        self.next_patient_id += 1
        self.next_arrival += 1

        if priority == "emergency":
            self.emergency_queue.append(patient)
        elif priority == "urgent":
            self.urgent_queue.append(patient)
        else:
            self.routine_queue.append(patient)

        self.registration_history.insert_at_end(patient)
        self.waiting_doubly.append(patient)
        self.waiting_circular.append(patient)
        self.waiting_bst.insert(patient)
        self.save()
        self.add_audit(
            "REGISTER",
            patient.patient_id,
            f"{patient.name}; category={category}; priority={priority}",
        )
        return patient

    def all_waiting(self):
        return (
            list(self.emergency_queue)
            + list(self.urgent_queue)
            + list(self.routine_queue)
        )

    def waiting_count(self):
        return len(self.emergency_queue) + len(self.urgent_queue) + len(self.routine_queue)

    def all_open(self):
        return self.all_waiting() + list(self.active_requests)

    def all_records(self):
        return (
            self.all_open()
            + list(self.served_patients)
            + list(self.cancelled_requests)
        )

    def call_next_patient(self):
        if self.emergency_queue:
            patient = self.emergency_queue.popleft()
        elif self.urgent_queue:
            patient = self.urgent_queue.popleft()
        elif self.routine_queue:
            patient = self.routine_queue.popleft()
        else:
            return None

        patient.status = "in_progress"
        self.active_requests.append(patient)
        self.undo_stack.push(patient)
        self._remove_from_waiting_structures(patient.patient_id)
        self.save()
        self.add_audit(
            "START_WORK",
            patient.patient_id,
            f"{patient.name}; priority={patient.priority}",
        )
        return patient

    def undo_last_start(self):
        patient = None
        while not self.undo_stack.is_empty():
            candidate = self.undo_stack.pop()
            patient = next(
                (
                    item
                    for item in self.active_requests
                    if item.patient_id == candidate.patient_id
                ),
                None,
            )
            if patient is not None:
                break
        if patient is None:
            return None
        self.active_requests.remove(patient)
        patient.status = "waiting"
        if patient.priority == "emergency":
            self.emergency_queue.appendleft(patient)
        elif patient.priority == "urgent":
            self.urgent_queue.appendleft(patient)
        else:
            self.routine_queue.appendleft(patient)

        self.waiting_doubly.append(patient)
        self.waiting_circular.append(patient)
        self.waiting_bst.insert(patient)
        self.save()
        self.add_audit("UNDO_START", patient.patient_id, patient.name)
        return patient

    def cancel_by_id(self, patient_id):
        patient = self.waiting_bst.search(patient_id)
        if patient is not None:
            if patient.priority == "emergency":
                self.emergency_queue = deque(
                    item for item in self.emergency_queue
                    if item.patient_id != patient_id
                )
            elif patient.priority == "urgent":
                self.urgent_queue = deque(
                    item for item in self.urgent_queue
                    if item.patient_id != patient_id
                )
            else:
                self.routine_queue = deque(
                    item for item in self.routine_queue
                    if item.patient_id != patient_id
                )
            self._remove_from_waiting_structures(patient_id)
        else:
            patient = next(
                (
                    item for item in self.active_requests
                    if item.patient_id == patient_id
                ),
                None,
            )
            if patient is None:
                return False
            self.active_requests.remove(patient)

        patient.status = "cancelled"
        self.cancelled_requests.append(patient)
        self.save()
        self.add_audit("CANCEL", patient_id, patient.name)
        return True

    def complete_request(self, patient_id):
        patient = next(
            (
                item for item in self.active_requests
                if item.patient_id == patient_id
            ),
            None,
        )
        if patient is None:
            return False
        self.active_requests.remove(patient)
        patient.status = "completed"
        patient.completed_at = datetime.now()
        self.served_patients.append(patient)
        self.save()
        self.add_audit("COMPLETE", patient_id, patient.name)
        return True

    def assign_request(self, patient_id, assigned_to):
        assigned_to = assigned_to.strip()
        if not assigned_to:
            raise ValueError("Staff name cannot be empty.")
        if len(assigned_to) > 100:
            raise ValueError("Staff name must be 100 characters or fewer.")
        patient = next(
            (
                item for item in self.all_open()
                if item.patient_id == patient_id
            ),
            None,
        )
        if patient is None:
            return False
        patient.assigned_to = assigned_to
        self.save()
        self.add_audit("ASSIGN", patient_id, assigned_to)
        return True

    def _remove_from_waiting_structures(self, patient_id):
        self.waiting_doubly.delete_by_id(patient_id)
        self.waiting_circular.delete_by_id(patient_id)
        self.waiting_bst.delete(patient_id)

    # Module 9: sequential search
    def sequential_search_by_name(self, name):
        needle = name.strip().lower()
        if not needle:
            return []
        return [
            patient
            for patient in self.all_records()
            if needle in patient.name.lower()
        ]

    # Module 9: binary search on a patient ID-sorted list
    def binary_search_by_id(self, patient_id):
        ordered = self.records_by_id
        low = 0
        high = len(ordered) - 1
        while low <= high:
            middle = (low + high) // 2
            current_id = ordered[middle].patient_id
            if current_id == patient_id:
                return ordered[middle]
            if patient_id < current_id:
                high = middle - 1
            else:
                low = middle + 1
        return None

    # Module 9: merge sort
    def merge_sort_by_name(self, patients):
        if len(patients) <= 1:
            return patients
        middle = len(patients) // 2
        left = self.merge_sort_by_name(patients[:middle])
        right = self.merge_sort_by_name(patients[middle:])
        return self._merge_by_name(left, right)

    def _merge_by_name(self, left, right):
        result = []
        i = 0
        j = 0
        while i < len(left) and j < len(right):
            if left[i].name.lower() <= right[j].name.lower():
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result

    def sorted_by_priority(self):
        return sorted(
            self.all_waiting(),
            key=lambda patient: (
                self.PRIORITIES[patient.priority],
                patient.arrival_number,
            ),
        )

    # Module 6: recursive tree counting
    def count_waiting_recursively(self):
        return self._count_nodes(self.waiting_bst.root)

    def _count_nodes(self, node):
        if node is None:
            return 0
        return 1 + self._count_nodes(node.left) + self._count_nodes(node.right)


def print_waiting(clinic):
    open_requests = clinic.all_open()
    if not open_requests:
        print("\nThere are no open service requests.")
        return
    print("\n--- Open Service Requests ---")
    for patient in open_requests:
        print(
            f"[{patient.patient_id}] {patient.name} - {patient.category} - "
            f"{patient.priority.title()} - {patient.status.replace('_', ' ').title()}"
        )


def print_complexities():
    print("\n--- Complexity Summary ---")
    print("Queue enqueue/dequeue: O(1)")
    print("Stack push/pop/peek: O(1)")
    print("Singly linked list traversal: O(n)")
    print("Doubly linked list insertion at tail: O(1)")
    print("BST average search/insertion/deletion: O(log n)")
    print("BST worst-case search/insertion/deletion: O(n)")
    print("Sequential search: O(n)")
    print("Binary search: O(log n)")
    print("Merge sort: O(n log n)")


class ClinicApplication:
    def __init__(self, root, clinic, organization="Barangay Service Request Desk"):
        self.root = root
        self.clinic = clinic
        self.organization = organization

        root.title(organization)
        root.geometry("1120x680")
        root.minsize(900, 560)

        style = ttk.Style(root)
        if "clam" in style.theme_names():
            style.theme_use("clam")
        style.configure("Title.TLabel", font=("Segoe UI", 20, "bold"))
        style.configure("Card.TLabelframe", padding=12)
        style.configure("CardTitle.TLabel", font=("Segoe UI", 10, "bold"),
                        foreground="#5b6472")
        style.configure("CardValue.TLabel", font=("Segoe UI", 20, "bold"))
        style.configure("Primary.TButton", padding=(12, 8))

        header = ttk.Frame(root, padding=(18, 14, 18, 8))
        header.pack(fill="x")
        ttk.Label(
            header,
            text=organization,
            style="Title.TLabel",
        ).pack(side="left")
        ttk.Label(
            header,
            text=datetime.now().strftime("%A, %B %d, %Y"),
            foreground="#5b6472",
        ).pack(side="right")

        cards = ttk.Frame(root, padding=(18, 8, 18, 8))
        cards.pack(fill="x")

        self.waiting_card = ttk.LabelFrame(
            cards, text=" Waiting Requests ", style="Card.TLabelframe"
        )
        self.waiting_card.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.waiting_value = ttk.Label(
            self.waiting_card, text="0", style="CardValue.TLabel"
        )
        self.waiting_value.pack()

        self.emergency_card = ttk.LabelFrame(
            cards, text=" Emergency ", style="Card.TLabelframe"
        )
        self.emergency_card.pack(side="left", fill="x", expand=True, padx=8)
        self.emergency_value = ttk.Label(
            self.emergency_card, text="0", style="CardValue.TLabel"
        )
        self.emergency_value.pack()

        self.served_card = ttk.LabelFrame(
            cards, text=" Completed Total ", style="Card.TLabelframe"
        )
        self.served_card.pack(side="left", fill="x", expand=True, padx=(8, 0))
        self.served_value = ttk.Label(
            self.served_card, text="0", style="CardValue.TLabel"
        )
        self.served_value.pack()

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=18, pady=8)

        self.queue_tab = ttk.Frame(self.notebook, padding=12)
        self.register_tab = ttk.Frame(self.notebook, padding=12)
        self.search_tab = ttk.Frame(self.notebook, padding=12)
        self.reports_tab = ttk.Frame(self.notebook, padding=12)

        self.notebook.add(self.queue_tab, text="  Queue  ")
        self.notebook.add(self.register_tab, text="  New Request  ")
        self.notebook.add(self.search_tab, text="  Search  ")
        self.notebook.add(self.reports_tab, text="  Reports  ")

        self.build_queue_tab()
        self.build_register_tab()
        self.build_search_tab()
        self.build_reports_tab()

        self.status = tk.StringVar(value="Ready")
        ttk.Label(
            root,
            textvariable=self.status,
            anchor="w",
            padding=(18, 6),
            background="#eef1f5",
        ).pack(fill="x", side="bottom")

        root.bind("<F5>", lambda _event: self.refresh())
        self.refresh()

    def build_queue_tab(self):
        toolbar = ttk.Frame(self.queue_tab)
        toolbar.pack(fill="x", pady=(0, 8))
        ttk.Button(
            toolbar,
            text="Start Next Request",
            style="Primary.TButton",
            command=self.call_next,
        ).pack(side="left")
        ttk.Button(
            toolbar,
            text="Complete Selected",
            command=self.complete_selected,
        ).pack(side="left", padx=8)
        ttk.Button(
            toolbar,
            text="Assign Staff",
            command=self.assign_selected,
        ).pack(side="left")
        ttk.Button(
            toolbar,
            text="Undo Last Start",
            command=self.undo_last,
        ).pack(side="left", padx=8)
        ttk.Button(
            toolbar,
            text="Cancel Selected",
            command=self.cancel_selected,
        ).pack(side="left")
        ttk.Button(
            toolbar,
            text="Refresh",
            command=self.refresh,
        ).pack(side="right", padx=(8, 0))
        ttk.Label(toolbar, text="Show:").pack(side="right")
        self.queue_filter = ttk.Combobox(
            toolbar,
            values=("All Open", "Waiting", "In Progress"),
            state="readonly",
            width=14,
        )
        self.queue_filter.set("All Open")
        self.queue_filter.pack(side="right")
        self.queue_filter.bind("<<ComboboxSelected>>", lambda _event: self.refresh())

        columns = (
            "id", "name", "category", "priority", "status",
            "assigned", "arrival", "registered",
        )
        self.waiting_tree = ttk.Treeview(
            self.queue_tab,
            columns=columns,
            show="headings",
            height=18,
        )
        headings = {
            "id": ("Request ID", 85),
            "name": ("Resident", 180),
            "category": ("Category", 135),
            "priority": ("Priority", 100),
            "status": ("Status", 105),
            "assigned": ("Assigned Staff", 140),
            "arrival": ("Arrival #", 85),
            "registered": ("Created At", 145),
        }
        for column, (heading, width) in headings.items():
            self.waiting_tree.heading(column, text=heading)
            self.waiting_tree.column(column, width=width, anchor="w")
        self.waiting_tree.pack(fill="both", expand=True)
        self.waiting_tree.bind("<Double-1>", self.show_request_details)

    def build_register_tab(self):
        container = ttk.Frame(self.register_tab)
        container.place(relx=0.5, rely=0.42, anchor="center")

        ttk.Label(
            container,
            text="New Service Request",
            font=("Segoe UI", 16, "bold"),
        ).grid(
            row=0, column=0, columnspan=2, pady=(0, 20), sticky="w"
        )
        ttk.Label(container, text="Resident name").grid(
            row=1, column=0, sticky="w", pady=6
        )
        self.name_entry = ttk.Entry(container, width=38)
        self.name_entry.grid(row=1, column=1, padx=(12, 0), pady=6)

        ttk.Label(container, text="Request category").grid(
            row=2, column=0, sticky="w", pady=6
        )
        self.category_combo = ttk.Combobox(
            container,
            values=self.clinic.CATEGORIES,
            state="readonly",
            width=35,
        )
        self.category_combo.set(self.clinic.CATEGORIES[0])
        self.category_combo.grid(row=2, column=1, padx=(12, 0), pady=6)

        ttk.Label(container, text="Priority").grid(
            row=3, column=0, sticky="w", pady=6
        )
        self.priority_combo = ttk.Combobox(
            container,
            values=("Emergency", "Urgent", "Routine"),
            state="readonly",
            width=35,
        )
        self.priority_combo.set("Routine")
        self.priority_combo.grid(row=3, column=1, padx=(12, 0), pady=6)

        ttk.Label(container, text="Assigned staff (optional)").grid(
            row=4, column=0, sticky="w", pady=6
        )
        self.assigned_entry = ttk.Entry(container, width=38)
        self.assigned_entry.grid(row=4, column=1, padx=(12, 0), pady=6)

        ttk.Label(container, text="Request details (optional)").grid(
            row=5, column=0, sticky="nw", pady=6
        )
        self.description_text = tk.Text(container, width=38, height=5, wrap="word")
        self.description_text.grid(row=5, column=1, padx=(12, 0), pady=6)

        ttk.Button(
            container,
            text="Register Request",
            style="Primary.TButton",
            command=self.register_patient,
        ).grid(row=6, column=1, pady=(18, 0), sticky="e")

        self.registration_result = ttk.Label(container, text="")
        self.registration_result.grid(row=7, column=0, columnspan=2, pady=12)
        self.name_entry.bind("<Return>", lambda _event: self.register_patient())

    def build_search_tab(self):
        toolbar = ttk.Frame(self.search_tab)
        toolbar.pack(fill="x", pady=(0, 10))
        ttk.Label(toolbar, text="Search:").pack(side="left")
        self.search_entry = ttk.Entry(toolbar, width=32)
        self.search_entry.pack(side="left", padx=8)
        ttk.Button(toolbar, text="By Name", command=self.search_name).pack(side="left")
        ttk.Button(toolbar, text="By Patient ID", command=self.search_id).pack(
            side="left", padx=8
        )
        ttk.Button(toolbar, text="Clear", command=self.clear_search).pack(side="right")

        columns = (
            "id", "name", "category", "priority",
            "status", "assigned", "arrival",
        )
        self.search_tree = ttk.Treeview(
            self.search_tab,
            columns=columns,
            show="headings",
        )
        for column, (heading, width) in {
            "id": ("Request ID", 90),
            "name": ("Resident", 180),
            "category": ("Category", 135),
            "priority": ("Priority", 100),
            "status": ("Status", 110),
            "assigned": ("Assigned Staff", 150),
            "arrival": ("Arrival #", 90),
        }.items():
            self.search_tree.heading(column, text=heading)
            self.search_tree.column(column, width=width)
        self.search_tree.pack(fill="both", expand=True)

    def build_reports_tab(self):
        action_bar = ttk.Frame(self.reports_tab)
        action_bar.pack(fill="x", pady=(0, 8))
        ttk.Button(
            action_bar,
            text="Refresh Report",
            command=self.refresh_report,
        ).pack(side="left")
        ttk.Button(
            action_bar,
            text="Export to CSV",
            command=self.export_report,
        ).pack(side="left", padx=8)
        ttk.Button(
            action_bar,
            text="Create Database Backup",
            command=self.create_backup,
        ).pack(side="left")

        self.report_text = tk.Text(
            self.reports_tab,
            height=22,
            wrap="word",
            font=("Consolas", 10),
        )
        self.report_text.pack(fill="both", expand=True)

    def set_status(self, message):
        self.status.set(message)

    def get_selected_patient_id(self, tree):
        selection = tree.selection()
        if not selection:
            return None
        values = tree.item(selection[0], "values")
        return int(values[0]) if values else None

    def register_patient(self):
        name = self.name_entry.get()
        priority = self.priority_combo.get().lower()
        category = self.category_combo.get()
        description = self.description_text.get("1.0", "end").strip()
        assigned_to = self.assigned_entry.get()
        try:
            patient = self.clinic.add_patient(
                name,
                priority,
                category,
                description,
                assigned_to,
            )
        except (ValueError, OSError, sqlite3.Error) as error:
            messagebox.showerror("Registration Error", str(error))
            self.set_status("Registration failed")
            return

        self.name_entry.delete(0, "end")
        self.assigned_entry.delete(0, "end")
        self.description_text.delete("1.0", "end")
        self.registration_result.configure(
            text=f"Registered request #{patient.patient_id} for {patient.name}"
        )
        self.set_status(f"Registered request #{patient.patient_id}")
        self.refresh()
        self.name_entry.focus()

    def call_next(self):
        patient = self.clinic.call_next_patient()
        if patient is None:
            messagebox.showinfo("Queue Status", "There are no patients waiting.")
            self.set_status("Queue is empty")
            return
        self.set_status(
            f"Started request #{patient.patient_id} for {patient.name}"
        )
        self.refresh()

    def undo_last(self):
        patient = self.clinic.undo_last_start()
        if patient is None:
            messagebox.showinfo(
                "Undo",
                "There is no active request that can be returned to the queue.",
            )
            return
        self.set_status(f"Restored {patient.name} to the queue")
        self.refresh()

    def complete_selected(self):
        patient_id = self.get_selected_patient_id(self.waiting_tree)
        if patient_id is None:
            messagebox.showwarning(
                "No Selection", "Select an in-progress request to complete."
            )
            return
        patient = next(
            (
                item for item in self.clinic.active_requests
                if item.patient_id == patient_id
            ),
            None,
        )
        if patient is None:
            messagebox.showwarning(
                "Not In Progress", "Start the request before completing it."
            )
            return
        if not messagebox.askyesno(
            "Complete Request",
            f"Mark request #{patient_id} for {patient.name} as complete?",
        ):
            return
        if self.clinic.complete_request(patient_id):
            self.set_status(f"Completed request #{patient_id}")
            self.refresh()

    def assign_selected(self):
        patient_id = self.get_selected_patient_id(self.waiting_tree)
        if patient_id is None:
            messagebox.showwarning(
                "No Selection", "Select an open request to assign."
            )
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("Assign Staff")
        dialog.transient(self.root)
        dialog.resizable(False, False)
        dialog.grab_set()
        frame = ttk.Frame(dialog, padding=16)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text="Staff member name:").pack(anchor="w")
        staff_entry = ttk.Entry(frame, width=35)
        staff_entry.pack(fill="x", pady=(6, 12))

        def save_assignment():
            try:
                updated = self.clinic.assign_request(
                    patient_id,
                    staff_entry.get(),
                )
            except (ValueError, OSError, sqlite3.Error) as error:
                messagebox.showerror("Assignment Error", str(error), parent=dialog)
                return
            if updated:
                self.set_status(f"Assigned request #{patient_id}")
                self.refresh()
                dialog.destroy()
            else:
                messagebox.showwarning(
                    "Not Found",
                    "The request is no longer open.",
                    parent=dialog,
                )

        ttk.Button(frame, text="Save Assignment", command=save_assignment).pack(
            anchor="e"
        )
        staff_entry.focus_set()
        staff_entry.bind("<Return>", lambda _event: save_assignment())

    def cancel_selected(self):
        patient_id = self.get_selected_patient_id(self.waiting_tree)
        if patient_id is None:
            messagebox.showwarning("No Selection", "Select a patient in the queue.")
            return
        patient = next(
            (
                item for item in self.clinic.all_open()
                if item.patient_id == patient_id
            ),
            None,
        )
        if patient is not None:
            if not messagebox.askyesno(
                "Cancel Patient",
                f"Cancel request #{patient_id} for {patient.name}?",
            ):
                return
        if self.clinic.cancel_by_id(patient_id):
            self.set_status(f"Cancelled Patient #{patient_id}")
            self.refresh()
        else:
            messagebox.showwarning("Not Found", "The patient could not be found.")

    def search_name(self):
        query = self.search_entry.get()
        matches = self.clinic.sequential_search_by_name(query)
        self.populate_search(matches)
        self.set_status(f"{len(matches)} request match(es) found")

    def search_id(self):
        query = self.search_entry.get().strip()
        try:
            patient_id = int(query)
        except ValueError:
            messagebox.showerror("Invalid ID", "Enter a numeric request ID.")
            return
        patient = self.clinic.binary_search_by_id(patient_id)
        self.populate_search([patient] if patient is not None else [])
        self.set_status("Patient found" if patient is not None else "Patient not found")

    def populate_search(self, patients):
        for item in self.search_tree.get_children():
            self.search_tree.delete(item)
        for patient in patients:
            self.search_tree.insert(
                "",
                "end",
                values=(
                    patient.patient_id,
                    patient.name,
                    patient.category,
                    patient.priority.title(),
                    patient.status.replace("_", " ").title(),
                    patient.assigned_to,
                    patient.arrival_number,
                ),
            )

    def show_request_details(self, event):
        selected = self.waiting_tree.identify_row(event.y)
        if not selected:
            return
        self.waiting_tree.selection_set(selected)
        patient_id = self.get_selected_patient_id(self.waiting_tree)
        patient = next(
            (
                item for item in self.clinic.all_open()
                if item.patient_id == patient_id
            ),
            None,
        )
        if patient is None:
            return
        details = (
            f"Request ID: {patient.patient_id}\n"
            f"Resident: {patient.name}\n"
            f"Category: {patient.category}\n"
            f"Priority: {patient.priority.title()}\n"
            f"Status: {patient.status.replace('_', ' ').title()}\n"
            f"Assigned staff: {patient.assigned_to or 'Unassigned'}\n"
            f"Registered: {patient.registered_at}\n\n"
            f"Details:\n{patient.description or 'No details provided.'}"
        )
        messagebox.showinfo("Request Details", details, parent=self.root)

    def clear_search(self):
        self.search_entry.delete(0, "end")
        self.populate_search([])
        self.set_status("Search cleared")

    def export_report(self):
        try:
            export_file = self.clinic.export_csv()
        except (OSError, sqlite3.Error) as error:
            messagebox.showerror("Export Error", str(error))
            return
        self.set_status("CSV report exported")
        self.refresh_report()
        messagebox.showinfo(
            "Export Complete",
            f"Report saved to:\n{export_file}",
        )

    def create_backup(self):
        try:
            backup_file = self.clinic.create_backup()
        except (OSError, sqlite3.Error) as error:
            messagebox.showerror("Backup Error", str(error))
            return
        self.clinic.add_audit("BACKUP", details=str(backup_file))
        self.set_status("Database backup created")
        self.refresh_report()
        messagebox.showinfo(
            "Backup Complete",
            f"Backup saved to:\n{backup_file}",
        )

    def refresh(self):
        for item in self.waiting_tree.get_children():
            self.waiting_tree.delete(item)

        waiting = self.clinic.all_waiting()
        active = self.clinic.active_requests
        view = self.queue_filter.get() if hasattr(self, "queue_filter") else "All Open"
        if view == "Waiting":
            open_requests = waiting
        elif view == "In Progress":
            open_requests = active
        else:
            open_requests = self.clinic.all_open()

        for patient in open_requests:
            registered_at = patient.registered_at
            if isinstance(registered_at, datetime):
                registered_at = registered_at.strftime("%Y-%m-%d %H:%M")
            self.waiting_tree.insert(
                "",
                "end",
                values=(
                    patient.patient_id,
                    patient.name,
                    patient.category,
                    patient.priority.title(),
                    patient.status.replace("_", " ").title(),
                    patient.assigned_to or "Unassigned",
                    patient.arrival_number,
                    registered_at,
                ),
            )

        self.waiting_value.configure(
            text=f"{len(waiting)} waiting / {len(active)} active"
        )
        emergency_count = len(self.clinic.emergency_queue)
        self.emergency_value.configure(text=str(emergency_count))
        self.served_value.configure(text=str(len(self.clinic.served_patients)))
        self.refresh_report()

    def refresh_report(self):
        waiting = self.clinic.all_waiting()
        active = self.clinic.active_requests
        by_name = self.clinic.merge_sort_by_name(self.clinic.all_open())
        bst_ids = [
            str(patient.patient_id)
            for patient in self.clinic.waiting_bst.inorder()
        ]

        lines = [
            "SERVICE REQUEST OPERATIONS REPORT",
            "=" * 70,
            f"Waiting patients: {len(waiting)}",
            f"In-progress requests: {len(active)}",
            f"Emergency: {len(self.clinic.emergency_queue)}",
            f"Urgent: {len(self.clinic.urgent_queue)}",
            f"Routine: {len(self.clinic.routine_queue)}",
            f"Completed requests: {len(self.clinic.served_patients)}",
            f"Cancelled requests: {len(self.clinic.cancelled_requests)}",
            "",
            "OPEN REQUESTS SORTED BY NAME (MERGE SORT)",
            "-" * 70,
        ]
        if by_name:
            lines.extend(
                f"[{patient.patient_id}] {patient.name} - {patient.category} - "
                f"{patient.status.replace('_', ' ').title()}"
                for patient in by_name
            )
        else:
            lines.append("No waiting patients.")

        lines.extend([
            "",
            "BST IN-ORDER PATIENT IDs",
            "-" * 70,
            ", ".join(bst_ids) if bst_ids else "No waiting patients.",
            "",
            "DOUBLY LINKED LIST - FORWARD",
            "-" * 70,
        ])
        lines.extend(
            f"[{patient.patient_id}] {patient.name}"
            for patient in self.clinic.waiting_doubly.forward()
        )
        lines.extend([
            "",
            "CIRCULAR LINKED LIST",
            "-" * 70,
        ])
        lines.extend(
            f"[{patient.patient_id}] {patient.name}"
            for patient in self.clinic.waiting_circular.to_list()
        )
        lines.extend([
            "",
            "MODULE COMPLEXITY SUMMARY",
            "-" * 70,
            "Queue enqueue/dequeue: O(1)",
            "Stack push/pop/peek: O(1)",
            "Singly linked traversal: O(n)",
            "Doubly linked tail insertion: O(1)",
            "BST average operations: O(log n)",
            "BST worst-case operations: O(n)",
            "Sequential search: O(n)",
            "Binary search: O(log n)",
            "Merge sort: O(n log n)",
            "",
            "Persistence file: " + str(self.clinic.data_file),
            "",
            "RECENT AUDIT ACTIVITY",
            "-" * 70,
        ])
        for action, patient_id, details, created_at in self.clinic.recent_audit(10):
            request_reference = (
                f"Request #{patient_id}" if patient_id is not None else "System"
            )
            lines.append(
                f"{created_at} | {action} | {request_reference} | {details or ''}"
            )

        self.report_text.configure(state="normal")
        self.report_text.delete("1.0", "end")
        self.report_text.insert("1.0", "\n".join(lines))
        self.report_text.configure(state="disabled")


def menu(clinic=None):
    if clinic is None:
        clinic = ClinicSystem()
    while True:
        print("\n===== BARANGAY SERVICE REQUEST DESK =====")
        print("1. Register service request")
        print("2. Start next request")
        print("3. Cancel request")
        print("4. Undo last request start")
        print("5. Display open requests")
        print("6. Search by name (sequential search)")
        print("7. Search by ID (BST and binary search)")
        print("8. Sort names (merge sort)")
        print("9. Sort patients by priority")
        print("10. Display doubly linked list forward")
        print("11. Display doubly linked list backward")
        print("12. Display circular linked list")
        print("13. Show served patients")
        print("14. Show BST in-order traversal")
        print("15. Show complexity summary")
        print("16. Exit")
        print("17. Complete in-progress request")

        choice = input("Enter choice: ").strip()
        try:
            if choice == "1":
                name = input("Patient name: ").strip()
                priority = input(
                    "Priority (routine/urgent/emergency): "
                ).strip().lower()
                print("Categories:", ", ".join(clinic.CATEGORIES))
                category = input("Category (default General): ").strip() or "General"
                description = input("Request details (optional): ")
                assigned_to = input("Assigned staff (optional): ")
                patient = clinic.add_patient(
                    name,
                    priority,
                    category,
                    description,
                    assigned_to,
                )
                print(
                    f"Registered request #{patient.patient_id} for {patient.name} "
                    f"as {patient.priority}."
                )
            elif choice == "2":
                patient = clinic.call_next_patient()
                if patient:
                    print(
                        f"Started [{patient.patient_id}] "
                        f"{patient.name} ({patient.priority})."
                    )
                else:
                    print("There are no patients waiting.")
            elif choice == "3":
                patient_id = int(input("Patient ID to cancel: ").strip())
                print(
                    "Patient cancelled."
                    if clinic.cancel_by_id(patient_id)
                    else "Patient not found."
                )
            elif choice == "4":
                patient = clinic.undo_last_start()
                print(
                    f"Restored [{patient.patient_id}] {patient.name}."
                    if patient
                    else "There is no active request that can be restored."
                )
            elif choice == "5":
                print_waiting(clinic)
            elif choice == "6":
                matches = clinic.sequential_search_by_name(input("Search name: "))
                if matches:
                    for patient in matches:
                        print(
                            f"[{patient.patient_id}] {patient.name} "
                            f"- {patient.priority.title()}"
                        )
                else:
                    print("No matching patient found.")
            elif choice == "7":
                patient_id = int(input("Patient ID: ").strip())
                patient = clinic.binary_search_by_id(patient_id)
                if patient:
                    print(
                        f"Found [{patient.patient_id}] {patient.name} "
                        f"- {patient.priority.title()}."
                    )
                else:
                    print("Patient not found.")
            elif choice == "8":
                print("\n--- Sorted by Name (Merge Sort) ---")
                for patient in clinic.merge_sort_by_name(clinic.all_waiting()):
                    print(
                        f"{patient.name} [{patient.patient_id}] "
                        f"- {patient.priority.title()}"
                    )
            elif choice == "9":
                print("\n--- Sorted by Priority ---")
                for patient in clinic.sorted_by_priority():
                    print(
                        f"{patient.priority.title()} - "
                        f"{patient.name} [{patient.patient_id}]"
                    )
            elif choice == "10":
                print("\n--- Doubly Linked List: Forward ---")
                for patient in clinic.waiting_doubly.forward():
                    print(f"[{patient.patient_id}] {patient.name}")
            elif choice == "11":
                print("\n--- Doubly Linked List: Backward ---")
                for patient in clinic.waiting_doubly.backward():
                    print(f"[{patient.patient_id}] {patient.name}")
            elif choice == "12":
                print("\n--- Circular Linked List ---")
                for patient in clinic.waiting_circular.to_list():
                    print(f"[{patient.patient_id}] {patient.name}")
            elif choice == "13":
                if not clinic.served_patients:
                    print("No patients have been served.")
                else:
                    print("\n--- Served Patients ---")
                    for patient in clinic.served_patients:
                        print(f"[{patient.patient_id}] {patient.name}")
            elif choice == "14":
                print("\n--- BST In-Order Traversal ---")
                for patient in clinic.waiting_bst.inorder():
                    print(f"[{patient.patient_id}] {patient.name}")
                print(
                    f"Recursive waiting count: "
                    f"{clinic.count_waiting_recursively()}"
                )
            elif choice == "15":
                print_complexities()
            elif choice == "16":
                print("Thank you for using Barangay Service Request Desk.")
                break
            elif choice == "17":
                patient_id = int(input("In-progress request ID: ").strip())
                print(
                    "Request completed."
                    if clinic.complete_request(patient_id)
                    else "No matching in-progress request."
                )
            else:
                print("Invalid choice.")
        except (ValueError, TypeError) as error:
            print(f"Invalid input: {error}")


def main():
    parser = argparse.ArgumentParser(
        description="Barangay Service Request Desk"
    )
    parser.add_argument(
        "--cli",
        action="store_true",
        help="Run the text-based menu instead of the desktop interface.",
    )
    parser.add_argument(
        "--database",
        default=None,
        help="Use a specific SQLite database file.",
    )
    parser.add_argument(
        "--organization",
        default="Barangay Service Desk",
        help="Name shown in the application window.",
    )
    args = parser.parse_args()
    if args.cli:
        menu(ClinicSystem(args.database))
        return

    root = tk.Tk()
    clinic = ClinicSystem(args.database)
    ClinicApplication(root, clinic, args.organization)
    root.mainloop()


if __name__ == "__main__":
    main()

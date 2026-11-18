import csv
import sqlite3
import tempfile
import unittest
from pathlib import Path

from Finals import ClinicSystem


class ServiceRequestTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.database_file = Path(self.temporary_directory.name) / "requests.db"
        self.system = ClinicSystem(self.database_file)

    def test_request_lifecycle_survives_restart(self):
        request = self.system.add_patient(
            "Alex Santos",
            "urgent",
            "Documents",
            "Needs a residency certificate.",
        )
        self.assertTrue(self.system.assign_request(request.patient_id, "Mina"))
        self.assertEqual(self.system.call_next_patient().patient_id, request.patient_id)
        self.assertEqual(self.system.active_requests[0].assigned_to, "Mina")
        self.assertTrue(self.system.complete_request(request.patient_id))

        reopened = ClinicSystem(self.database_file)
        self.assertEqual(reopened.waiting_count(), 0)
        self.assertEqual(len(reopened.active_requests), 0)
        self.assertEqual(len(reopened.served_patients), 1)
        completed = reopened.served_patients[0]
        self.assertEqual(completed.category, "Documents")
        self.assertEqual(completed.description, "Needs a residency certificate.")
        self.assertEqual(completed.assigned_to, "Mina")
        self.assertEqual(completed.status, "completed")
        self.assertEqual(
            reopened.binary_search_by_id(request.patient_id).status,
            "completed",
        )
        self.assertTrue(any(row[0] == "COMPLETE" for row in reopened.recent_audit()))

    def test_undo_start_and_cancel_keep_request_history(self):
        first = self.system.add_patient("Ari", "emergency")
        second = self.system.add_patient("Bea", "routine")
        self.system.call_next_patient()
        self.assertEqual(self.system.undo_last_start().patient_id, first.patient_id)
        self.assertTrue(self.system.cancel_by_id(second.patient_id))

        reopened = ClinicSystem(self.database_file)
        self.assertEqual(reopened.waiting_count(), 1)
        self.assertEqual(reopened.all_waiting()[0].patient_id, first.patient_id)
        self.assertEqual(len(reopened.cancelled_requests), 1)
        self.assertEqual(reopened.cancelled_requests[0].patient_id, second.patient_id)

    def test_in_progress_request_can_be_undone_after_restart(self):
        request = self.system.add_patient("Morgan", "urgent")
        self.system.call_next_patient()

        reopened = ClinicSystem(self.database_file)
        restored = reopened.undo_last_start()
        self.assertEqual(restored.patient_id, request.patient_id)
        self.assertEqual(reopened.waiting_count(), 1)
        self.assertEqual(reopened.active_requests, [])

    def test_old_database_schema_is_migrated(self):
        legacy_database = Path(self.temporary_directory.name) / "legacy.db"
        connection = sqlite3.connect(legacy_database)
        try:
            connection.execute(
                """
                CREATE TABLE patients (
                    patient_id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    priority TEXT NOT NULL,
                    arrival_number INTEGER NOT NULL,
                    registered_at TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'waiting'
                )
                """
            )
            connection.execute(
                """
                INSERT INTO patients
                VALUES (1, 'Casey', 'routine', 1, '2026-01-01T10:00:00', 'served')
                """
            )
            connection.commit()
        finally:
            connection.close()

        migrated = ClinicSystem(legacy_database)
        self.assertEqual(migrated.waiting_count(), 0)
        self.assertEqual(len(migrated.served_patients), 1)
        self.assertEqual(migrated.served_patients[0].status, "completed")
        self.assertEqual(migrated.served_patients[0].category, "General")

    def test_csv_export_and_backup_include_saved_records(self):
        self.system.add_patient("Dana", "routine", "Other", "Tree pickup")
        exported = self.system.export_csv(
            Path(self.temporary_directory.name) / "report.csv"
        )
        with exported.open(newline="", encoding="utf-8-sig") as file:
            rows = list(csv.reader(file))
        self.assertEqual(rows[1][1], "Dana")
        self.assertEqual(rows[1][6], "Other")
        self.assertEqual(rows[1][7], "Tree pickup")

        backup = self.system.create_backup(
            Path(self.temporary_directory.name) / "backups"
        )
        self.assertTrue(backup.is_file())
        connection = sqlite3.connect(backup)
        try:
            count = connection.execute(
                "SELECT COUNT(*) FROM patients"
            ).fetchone()[0]
        finally:
            connection.close()
        self.assertEqual(count, 1)

    def test_validation_rejects_invalid_category_and_long_text(self):
        with self.assertRaises(ValueError):
            self.system.add_patient("Eli", category="Unknown")
        with self.assertRaises(ValueError):
            self.system.add_patient("Eli", description="x" * 1001)


if __name__ == "__main__":
    unittest.main()

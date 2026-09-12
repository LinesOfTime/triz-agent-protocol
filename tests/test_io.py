import tempfile
import unittest
from pathlib import Path

from triz_protocol.io import atomic_write_text


class AtomicWriteTests(unittest.TestCase):
    def test_creates_parent_and_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "nested/result.txt"
            atomic_write_text(path, "ready\n")
            self.assertEqual(path.read_text(encoding="utf-8"), "ready\n")

    def test_refuses_overwrite_by_default(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "result.txt"
            path.write_text("original", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                atomic_write_text(path, "replacement")
            self.assertEqual(path.read_text(encoding="utf-8"), "original")

    def test_explicit_overwrite_replaces_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "result.txt"
            path.write_text("original", encoding="utf-8")
            atomic_write_text(path, "replacement", overwrite=True)
            self.assertEqual(path.read_text(encoding="utf-8"), "replacement")


if __name__ == "__main__":
    unittest.main()

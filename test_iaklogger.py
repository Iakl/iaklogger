import unittest
from iaklogger import log_to_file, OPTIONS, DEFAULT


class TestLogger(unittest.TestCase):
    def test_log_to_file(self):
        # Test when file size is less than max size
        OPTIONS.log_file = "test.log"
        OPTIONS.log_file_max_size_mb = 10
        log_to_file("This is a test log")
        with open(OPTIONS.log_file, "r") as f:
            content = f.read()
        self.assertEqual(content, "This is a test log\n")

        # Test when file size exceeds max size
        OPTIONS.log_file_max_size_mb = 0.001
        log_to_file("This is another test log")
        with open(OPTIONS.log_file, "r") as f:
            content = f.read()
        self.assertEqual(
            content, "This is a test log\nThis is another test log\n")

        # Test when file size exceeds max size and previous logs are removed
        OPTIONS.log_file_max_size_mb = 0.001
        log_to_file("This is a long log that exceeds the max size")
        with open(OPTIONS.log_file, "r") as f:
            content = f.read()
        self.assertTrue(content.endswith(
            "This is a long log that exceeds the max size\n"))


if __name__ == '__main__':
    unittest.main()

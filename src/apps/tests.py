from django.test import TestCase
from apps.log_processor.management.commands.process_log import process_log_entry


class CommandTests(TestCase):
    def test_process_log_entry_function(self):
        """Test the individual processing of a log entry."""
        raw_log = '{"time": "17/May/2015:08:05:32", "remote_ip": "93.180.71.3"}'
        entry = process_log_entry(raw_log)
        assert entry is not None
        assert entry.ip_address == "93.180.71.3"

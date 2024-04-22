import json
import logging

import requests
from datetime import datetime
from django.core.management.base import BaseCommand
from django.db import transaction
from multiprocessing import Pool, cpu_count

from apps.log_processor.models import NginxLogEntry

logger = logging.getLogger(__name__)


def process_log_entry(log_line):
    """Function to process a single log line into a NginxLogEntry instance."""

    import orjson

    try:
        line = orjson.loads(log_line)
        request = line.get("request", "")
        method, uri = request.split()[:2] if request else None, None
        date = line.get("time", datetime.strftime(datetime.now(), "%d/%b/%Y:%H:%M:%S"))
        entry = NginxLogEntry(
            request_uri=uri,
            http_method=method,
            ip_address=line.get("remote_ip", None),
            response_size=int(line.get("bytes", 0)),
            response_code=int(line.get("response", 0)),
            date=datetime.strptime(date, "%d/%b/%Y:%H:%M:%S"),
        )
        return entry
    except Exception as e:
        logger.error(f"Error: {e}")
        # handle exceptions or errors in processing a single line
        return None


class Command(BaseCommand):
    """Custom Django management command class."""

    help = "Processes an Nginx log file and stores entries in the database"

    def add_arguments(self, parser):
        parser.add_argument(
            "log_url", type=str, help="URL of the Nginx log file to process"
        )

    def handle(self, *args, **options):
        """
        The main handler for the management command.
        Get data from a URL in a multiprocessor pool by number of processors.
        """

        log_url = options["log_url"]
        self.stdout.write(
            self.style.SUCCESS(f"Starting to process log from: {log_url}")
        )

        try:
            with requests.get(log_url, stream=True) as r:
                r.raise_for_status()
                log_lines = list(r.iter_lines(decode_unicode=True))
                if log_lines:
                    with Pool(processes=cpu_count()) as pool:
                        entries = pool.map(process_log_entry, log_lines)
                        entries = [
                            entry for entry in entries if entry is not None
                        ]  # remove None entries from failed processing
                        self.bulk_insert_entries(entries)
                self.stdout.write(
                    self.style.SUCCESS("Successfully processed all log entries.")
                )
        except requests.RequestException as e:
            self.stderr.write(self.style.ERROR(f"Failed to download the log file: {e}"))
        except json.JSONDecodeError as e:
            self.stderr.write(
                self.style.ERROR(f"Error decoding JSON from the log file: {e}")
            )
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"An unexpected error occurred: {e}"))

    @transaction.atomic
    def bulk_insert_entries(self, entries, batch_size=1000):
        """
        Method to perform bulk insert operations in batches.
        This method is wrapped in a Django transaction to ensure that all database
        operations are atomic.
        """
        try:
            for i in range(0, len(entries), batch_size):
                NginxLogEntry.objects.bulk_create(entries[i : i + batch_size])
        except Exception as e:
            self.stderr.write(
                self.style.ERROR(f"Failed to bulk insert log entries: {e}")
            )

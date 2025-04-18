import time
import logging
from typing import List, Dict, Optional


class BrowserLogs:
    def __init__(self, driver, tags: Optional[List[str]] = None, entries: int = 1,
                 ts: Optional[int] = None, log_type: str = 'performance', s: int = 10):
        self.driver = driver
        self.log_type = log_type
        self.seconds = s
        self.entry_num = entries
        self.tags = tags if tags is not None else []
        self.global_storage: List[Dict] = []
        self.target_event: List[Dict] = []
        self.timestamp = self.get_timestamp(ts)
        self.get_log()

    def get_timestamp(self, ts: Optional[int]) -> int:
        """Returns the current timestamp in milliseconds if `ts` is None or True."""
        if isinstance(ts, bool) and ts:
            return round(time.time() * 1000)
        return ts if ts is not None else 0

    def take_all_logs(self) -> bool:
        """Stores all logs if tags are not provided."""
        if not self.tags:
            self.global_storage.extend(self.logs)
            return True
        return False

    def skip_outdated_logs(self, entry: Dict) -> Optional[Dict]:
        """Returns the entry if it's not outdated based on the timestamp."""
        if self.timestamp and entry['timestamp'] < self.timestamp:
            return None
        return entry

    def save_result(self, entry: Dict) -> bool:
        """Saves the entry if all tags match."""
        if all(tag in str(entry) for tag in self.tags):
            self.target_event.append(entry)
            return len(self.target_event) == self.entry_num
        return False

    def get_log(self) -> None:
        """Retrieves logs from the browser."""
        timing = time.time()
        while time.time() - timing < self.seconds:
            self.logs = self.driver.get_log(self.log_type)
            if self.logs:
                if self.take_all_logs():
                    continue

                for entry in self.logs:
                    valid_entry = self.skip_outdated_logs(entry)
                    if valid_entry is None:
                        continue

                    self.global_storage.append(valid_entry)
                    if self.save_result(valid_entry):
                        return  # Exit on finding enough results

        logging.warning(f'{self.__class__.__name__}: search time is over')

#!/usr/bin/env python3
from tqdm import tqdm
from datetime import datetime, timedelta


class ProgressTracker:
    def __init__(self, total: int, desc: str = "Processing"):
        self.pbar = tqdm(
            total=total,
            desc=desc,
            unit="items",
            bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]'
        )
        self.start_time = datetime.now()

    def update(self, n: int = 1):
        self.pbar.update(n)

    def set_description(self, desc: str):
        self.pbar.set_description(desc)

    def close(self):
        self.pbar.close()

    def get_eta(self) -> str:
        if self.pbar.n == 0:
            return "Calculating..."

        elapsed = (datetime.now() - self.start_time).total_seconds()
        rate = self.pbar.n / elapsed if elapsed > 0 else 0
        remaining = self.pbar.total - self.pbar.n

        if rate > 0:
            eta_seconds = remaining / rate
            eta = timedelta(seconds=int(eta_seconds))
            return str(eta)
        return "Unknown"

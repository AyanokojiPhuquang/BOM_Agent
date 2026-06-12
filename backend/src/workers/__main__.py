"""Entry point for running the workers package as a module.

Usage:
    python -m src.workers.drive_worker  (runs the drive worker directly)
    python -m src.workers               (also runs the drive worker)
"""

import asyncio
import logging
import signal

from src.workers.drive_worker import DriveTaskWorker


def main() -> None:
    """Run the Drive Task Worker."""
    worker = DriveTaskWorker()

    def shutdown(sig, frame):
        worker._running = False

    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    asyncio.run(worker.run())


if __name__ == "__main__":
    main()

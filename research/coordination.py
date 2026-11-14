"""Opt-in local coordination for cooperating native supervisors.

No existing runner imports this module. All cooperating supervisors must use the
same private directory. This is an exclusive advisory lease, not an OS process
limiter, seed registry, shared time budget, or distributed lock. A crashed owner's
file deliberately remains and requires manual reconciliation; there is no takeover.
"""
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import secrets


class LeaseBusy(RuntimeError):
    """Another operation (or an unreconciled crash) holds the lease."""


class NativeLease:
    """Serialize opt-in native operations with exclusive, durable file creation.

    Declared workers are restricted to 1..4. The owner must itself enforce that
    count on child processes and keep its persistent experiment budget. Do not
    delete/replace a held file from another process, even when its PID looks old.
    Local exclusive-file semantics are assumed; network filesystems are untested.
    """
    def __init__(self, directory, experiment, workers=1):
        if type(workers) is not int or not 1 <= workers <= 4:
            raise ValueError("Declared native workers must be an integer from 1 to 4")
        if not isinstance(experiment, str) or not experiment.strip() or len(experiment) > 120:
            raise ValueError("Experiment identity is required")
        self.directory = Path(directory).resolve()
        self.path = self.directory / "native-execution.lease.json"
        self.experiment, self.workers = experiment, workers
        self._token = None

    def acquire(self):
        if self._token is not None:
            raise RuntimeError("Lease instance is already held")
        self.directory.mkdir(parents=True, exist_ok=True)
        token = secrets.token_hex(32)
        payload = dict(schema=1, experiment=self.experiment, workers=self.workers,
                       owner_pid=os.getpid(), acquired_utc=datetime.now(timezone.utc).isoformat(),
                       owner_token=token)
        try:
            stream = self.path.open("x", encoding="utf8", newline="\n")
        except FileExistsError as error:
            raise LeaseBusy("Native lease exists; do not bypass or automatically remove it") from error
        # Any interruption after exclusive creation leaves the file blocking new
        # work. Never silently delete a partial acquisition or stale owner.
        with stream:
            stream.write(json.dumps(payload, allow_nan=False, indent=2) + "\n")
            stream.flush()
            os.fsync(stream.fileno())
        self._token = token
        return self

    def assert_owned(self):
        if self._token is None:
            raise RuntimeError("Lease instance is not held")
        try:
            payload = json.loads(self.path.read_text(encoding="utf8"))
        except (OSError, ValueError) as error:
            raise RuntimeError("Lease evidence missing or malformed; reconcile manually") from error
        if not isinstance(payload, dict) or payload.get("owner_token") != self._token or \
                payload.get("owner_pid") != os.getpid() or payload.get("experiment") != self.experiment or \
                payload.get("workers") != self.workers:
            raise RuntimeError("Lease ownership changed; reconcile manually")
        return payload

    def release(self):
        self.assert_owned()
        self.path.unlink()
        self._token = None

    def __enter__(self):
        return self.acquire()

    def __exit__(self, error_type, error, traceback):
        self.release()
        return False

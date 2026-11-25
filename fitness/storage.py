import csv, io, json, shutil
from dataclasses import asdict
from .config import DATA_FILE, FIELDS
from .models import Session
from .validation import validate


class Store:
    """JSON-backed session storage with corruption recovery."""

    def __init__(self, path=DATA_FILE):
        self.path = path
        self.sessions: list[Session] = []
        self.load()

    def load(self):
        self.path.parent.mkdir(exist_ok=True)
        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
            self.sessions = [Session(**{k: r[k] for k in FIELDS if k in r}) for r in raw]
        except FileNotFoundError:
            self.sessions = []
            self.save()
        except (json.JSONDecodeError, TypeError, KeyError):
            shutil.copy(self.path, self.path.with_suffix(".corrupt.bak"))
            self.sessions = []
            self.save()

    def save(self):
        self.path.write_text(json.dumps([asdict(s) for s in self.sessions], indent=2),
                             encoding="utf-8")

    def next_id(self):
        return max((s.id for s in self.sessions), default=0) + 1

    def add(self, **values):
        s = Session(id=self.next_id(), **values)
        self.sessions.append(s)
        self.save()
        return s

    def delete(self, ids):
        self.sessions = [s for s in self.sessions if s.id not in ids]
        self.save()

    def import_csv(self, text):
        """Bulk import. Returns (imported_count, list_of_error_strings)."""
        ok, errs = 0, []
        reader = csv.DictReader(io.StringIO(text))
        need = {"date", "activity", "duration_min"}
        if not reader.fieldnames or not need <= set(reader.fieldnames):
            return 0, [f"Header must contain at least: {', '.join(sorted(need))}"]
        for n, row in enumerate(reader, start=2):
            v, err = validate(row.get("date"), (row.get("activity") or "").strip().title(),
                              row.get("duration_min"), row.get("distance_km"),
                              row.get("calories"), row.get("notes"))
            if err:
                errs.append(f"Row {n}: {err}")
            else:
                self.sessions.append(Session(id=self.next_id(), **v))
                ok += 1
        self.save()
        return ok, errs

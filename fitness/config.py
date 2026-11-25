from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DATA_FILE = BASE / "data" / "sessions.json"
EXPORT_DIR = BASE / "exports"

ACTIVITIES = {"Walking": 3.5, "Running": 9.0, "Cycling": 7.5, "Swimming": 8.0,
              "Hiking": 6.0, "Yoga": 2.5, "Gym": 5.0}   # MET values
WEIGHT_KG = 70            # used only to estimate calories when left blank
WEEKLY_GOAL_MIN = 150
LIMITS = {"duration": (1, 600), "distance": (0, 200), "calories": (0, 5000)}
FIELDS = ["id", "date", "activity", "duration_min", "distance_km", "calories", "notes"]

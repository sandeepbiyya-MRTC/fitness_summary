# Fitness Activity Summary (Python + NiceGUI)

    pip install -r requirements.txt
    python main.py        # opens http://localhost:8080

Structure
- main.py            entry point
- gui.py             NiceGUI interface (only file that uses nicegui)
- fitness/           pure-Python logic: config, models, validation, storage, analytics, charts (matplotlib), reports
- data/sessions.json persisted data (pre-loaded with 40 samples; auto-created if missing, corrupt files backed up)
- sample_data/       CSV/JSON samples + bad_rows.csv for the import-error demo
- make_sample_data.py regenerates sample data

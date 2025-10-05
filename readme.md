# 📦 Project Setup

---

# Calculator — README

This repository contains an educational, extensible calculator application implemented in Python. It demonstrates several object-oriented design patterns (Strategy, Observer, Memento, Factory) and uses pandas for simple history persistence.

This README explains how to set up the project, run the interactive REPL, run tests, and where to look for logs and history files.

## Requirements

- Python 3.10+
- Install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate   # mac/linux
.venv\Scripts\activate.bat # windows
pip install -r requirements.txt
```

If `requirements.txt` is empty or missing, the project relies on the standard library plus pandas. Install pandas manually if needed: `pip install pandas`.

## Run the application (REPL)

Start the interactive calculator REPL:

```bash
python main.py
```

Once started, you can use these commands:

- `help` — show commands
- `add`, `subtract`, `multiply`, `divide`, `power`, `root` — perform operations
- `history` — show recent calculations
- `clear` — clear history
- `undo` / `redo` — undo or redo last operation
- `save` / `load` — persist or reload history to/from disk
- `exit` — exit the REPL (saves history on exit)

When performing an operation, the REPL will prompt for two numbers (enter `cancel` to abort).

Examples:

```
> add
First number: 2
Second number: 3
Result: 5

> history
1. Addition(2, 3) = 5
```

## Configuration

Configuration is handled by `app/calculator_config.py` via the `CalculatorConfig` class. By default files are stored under the project `base_dir`. You can pass a custom config when constructing `Calculator(config=CalculatorConfig(...))` in code or tests.

- Logs: default `logs/calculator.log` (configurable)
- History: default `history/calculator_history.csv` (configurable)

Note: The Calculator implementation configures logging during initialization. Tests may patch or avoid that configuration to capture logs reliably.

## Tests

Run the unit test suite with pytest:

```bash
pytest -q
```

Testing notes:
- Many tests use temporary directories and patch `CalculatorConfig` properties to avoid touching your real filesystem.
- Some tests patch module-level logging functions (or `_setup_logging`) because the application configures logging with `basicConfig(force=True)` which can detach pytest's `caplog` handler.

## Developer notes

- Code lives in the `app/` package. Key modules:
   - `calculation.py` — Calculation value object and arithmetic handling
   - `calculator.py` — Calculator orchestration (history, observers, persistence)
   - `calculator_repl.py` — REPL UI
   - `history.py` — Observer implementations (auto-save, logging)

- Persistence currently uses CSV via pandas for history. Consider Parquet or a small embedded DB for larger datasets.
- The code demonstrates Strategy, Observer, Factory, and Memento patterns — useful as a template for extensible apps.

## Continuous Integration

A workflow is included at `.github/workflows/ci.yml` which runs pytest on pushes and pull requests.

## Contributing

If you want to extend the project:

- Add new operations by implementing the Operation interface and registering via OperationFactory.
- Add new observers by extending `HistoryObserver` and registering with `Calculator.add_observer()`.
- Keep I/O isolated so unit tests can patch it easily (avoid global side-effects at import-time).

## Contacts / Attribution

Author: Aaron Samuel and Thomas Licciardello

---

If you want the README to include a quick developer setup section for VS Code, or to switch history persistence to Parquet with atomic saves, tell me which you'd prefer and I can add it.
   - Click **New SSH Key**, paste the key, save.

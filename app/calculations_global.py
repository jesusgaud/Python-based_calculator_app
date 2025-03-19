import os
import pandas as pd
from collections import deque
from decimal import Decimal
from typing import List, Optional
from app.core.history_interface import HistoryInterface
from app.core.calculation import Calculation  # Using the canonical Calculation class
from app.math_operations import operations  # ✅ Import operations safely

# Define history file path
HISTORY_FILE = "history.csv"

class Calculations(HistoryInterface):
    """Singleton class to manage calculation history."""
    _instance = None  # Singleton instance

    def __new__(cls):
        """Ensures only one instance of the class exists (Singleton Pattern)."""
        if cls._instance is None:
            cls._instance = super(Calculations, cls).__new__(cls)
            cls._instance._initialized = False  # Mark as uninitialized initially
        return cls._instance

    def __init__(self):
        """Initialize only once to avoid re-initialization issues."""
        if not getattr(self, "_initialized", False):
            self.history: deque = deque()
            self.load_history()
            self._initialized = True  # Mark as initialized

    def add_calculation(self, calculation) -> None:
        """Adds a Calculation object to the history & saves it to CSV."""
        if not isinstance(calculation, Calculation):
            raise TypeError("Expected a Calculation instance.")

        # Prevent duplicate consecutive entries
        if self.history:
            last = self.history[-1]
            if (isinstance(last, Calculation) and
                    last.a == calculation.a and last.b == calculation.b and
                    last.operation_name == calculation.operation_name and
                    last.result == calculation.result):
                # Duplicate found; skip adding
                return

        # ✅ Limit history size to prevent excessive storage
        if len(self.history) >= 5:
            self.history.popleft()

        self.history.append(calculation)
        self.save_history()

    def get_latest(self) -> Optional[Calculation]:
        """Returns the latest calculation if available."""
        return self.history[-1] if self.history else None

    def get_history(self) -> List[Calculation]:
        """Returns the entire calculation history as a list."""
        return list(self.history)

    def clear_history(self) -> None:
        """Clears history from memory and removes the CSV file."""
        self.history.clear()
        if os.path.exists(HISTORY_FILE):
            os.remove(HISTORY_FILE)
        print("Calculation history cleared.")

    def find_by_operation(self, operation: str) -> List[Calculation]:
        """Finds calculations in history by the operation name."""
        return [calc for calc in self.history if isinstance(calc, Calculation) and calc.operation_name == operation]

    def save_history(self) -> None:
        """Saves the history to a CSV file using pandas."""
        if not self.history:
            return  # No history to save

        data = [{
            "num1": str(calc.a),
            "num2": str(calc.b),
            "operation": str(calc.operation_name),  # ✅ Ensure operation name is stored
            "result": str(calc.result)
        } for calc in self.history]
        df = pd.DataFrame(data)
        df.to_csv(HISTORY_FILE, index=False)
        print(f"History saved to {HISTORY_FILE}")

    def load_history(self) -> None:
        """Loads calculation history from a CSV file (if it exists) on startup."""
        if os.path.exists(HISTORY_FILE):
            df = pd.read_csv(HISTORY_FILE)
            for _, row in df.iterrows():
                calc = Calculation.from_history(row["num1"], row["num2"], row["operation"], row["result"])
                self.history.append(calc)
            print(f"Loaded {len(self.history)} calculations from history.")

    # ** Implementations of HistoryInterface abstract methods: **

    def add(self, expression, result):
        """Add a calculation result (expression and result) to the history (as a raw record)."""
        self.history.append((expression, result))
        return True

    def get_last(self):
        """Retrieve the last recorded history entry (calculation or raw record)."""
        return self.history[-1] if self.history else None

    def get_all(self):
        """Retrieve all history entries."""
        return list(self.history)

    def search(self, keyword):
        """Search the history for entries containing the given keyword."""
        results = []
        for entry in self.history:
            try:
                if isinstance(entry, Calculation):
                    # Search within Calculation fields
                    if (keyword in entry.operation_name or
                        keyword in str(entry.result) or
                        keyword in str(entry.a) or
                        keyword in str(entry.b)):
                        results.append(entry)
                elif isinstance(entry, tuple) and len(entry) == 2:
                    expr, res = entry
                    if keyword in str(expr) or keyword in str(res):
                        results.append(entry)
                else:
                    if keyword in str(entry):
                        results.append(entry)
            except Exception:
                continue
        return results

    def remove_last(self):
        """Remove the last history entry and return it."""
        return self.history.pop() if self.history else None

    def clear(self):
        """Clear all entries from the history (memory and file)."""
        self.history.clear()
        if os.path.exists(HISTORY_FILE):
            os.remove(HISTORY_FILE)
        return True

    def count(self):
        """Return the number of entries currently in the history."""
        return len(self.history)

    def add_history(self, item):
        """Add a generic item to the history (for testing or generic use)."""
        self.history.append(item)

    @classmethod
    def _reset_instance(cls):
        """Resets the Singleton instance (for testing purposes only)."""
        cls._instance = None

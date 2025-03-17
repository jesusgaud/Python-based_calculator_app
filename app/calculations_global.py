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
    history: deque = deque()

    def __new__(cls):
        """Ensures only one instance of the class exists (Singleton Pattern)."""
        if cls._instance is None:
            cls._instance = super(Calculations, cls).__new__(cls)
            cls._instance.load_history()
        return cls._instance

    def add_calculation(self, calculation) -> None:
        """Adds a calculation to the history & saves it to CSV."""
        if not isinstance(calculation, Calculation):
            raise TypeError("Expected a Calculation instance.")

        # Prevent duplicate entries:
        if self.history:
            last = self.history[-1]
            if (last.a == calculation.a and
                last.b == calculation.b and
                last.operation_name == calculation.operation_name and
                last.result == calculation.result):
                # Duplicate found; skip adding.
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
        """Returns the entire calculation history."""
        return list(self.history)

    def clear_history(self) -> None:
        """Clears history from memory and removes the CSV file."""
        self.history.clear()
        if os.path.exists(HISTORY_FILE):
            os.remove(HISTORY_FILE)
        print("Calculation history cleared.")

    def find_by_operation(self, operation: str) -> List[Calculation]:
        """Finds calculations based on the operation name."""
        return [calc for calc in self.history if calc.operation_name == operation]

    def save_history(self) -> None:
        """Saves the history to a CSV file using Pandas."""
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
        """Loads calculation history from a CSV file on startup."""
        if os.path.exists(HISTORY_FILE):
            df = pd.read_csv(HISTORY_FILE)
            for _, row in df.iterrows():
                calculation = Calculation.from_history(
                    row["num1"], row["num2"], row["operation"], row["result"]
                )
                self.history.append(calculation)
            print(f"Loaded {len(self.history)} calculations from history.")

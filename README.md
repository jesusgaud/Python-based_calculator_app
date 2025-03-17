# 🧮 Python-Based Calculator Application

## 📌 Overview
This project is a fully modular and extensible calculator application built with **Object-Oriented Programming (OOP)** and design patterns to ensure **maintainability, scalability, and testability**.

The application follows core software engineering principles, including:
- **SOLID Principles** (Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion)
- **DRY** (Don't Repeat Yourself)
- **GRASP** (General Responsibility Assignment Software Patterns)
- **Separation of Concerns** (Modular architecture)

It provides an **interactive REPL (Read-Eval-Print Loop)** where users can execute mathematical operations, manage calculation history, and extend functionality through a **plugin system**.

## 🛠 Features
✔️ Supports fundamental arithmetic operations (**Add, Subtract, Multiply, Divide**)  
✔️ Implements a **REPL-based command execution system**  
✔️ Saves and loads calculation history using **Pandas & CSV**  
✔️ Implements **plugin support** for extending functionality dynamically  
✔️ Includes **comprehensive unit tests** with pytest and **code coverage analysis**  
✔️ Uses **design patterns** to enforce maintainability and extensibility  

---

## 📐 Architecture & Design Patterns Used
This project follows **industry-standard design patterns** to ensure modularity and reusability:

### 1️⃣ Facade Pattern
- **Where?** `calculations.py` (Manages Pandas operations)  
- **Why?** Encapsulates the complexity of loading, saving, and managing history using Pandas, providing a simple interface for other components.

### 2️⃣ Command Pattern
- **Where?** `commands/` (Handles REPL commands dynamically)  
- **Why?** Enables commands like `add`, `subtract`, `history` to be executed independently while maintaining loose coupling.

### 3️⃣ Factory Method Pattern
- **Where?** `calculations.py`  
- **Why?** Instantiates the history manager dynamically while allowing subclassing if needed.

### 4️⃣ Singleton Pattern
- **Where?** `calculations_global.py`  
- **Why?** Ensures only one instance of the history manager exists throughout the application.

### 5️⃣ Strategy Pattern
- **Where?** `operations.py`  
- **Why?** Dynamically selects the appropriate calculation strategy (e.g., addition, subtraction, multiplication, division).

---

## 🛠 Installation & Setup

### Prerequisites
Ensure you have **Python 3.12 or higher** installed.

### Clone the Repository
```sh
git clone https://github.com/jesusgaud/Python-based_calculator_app.git
cd Python-based_calculator_app
```

### Create a Virtual Environment
```sh
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate      # Windows
```

### Install Dependencies
```sh
pip install -r requirements.txt
```

---

### 🚀 Usage

### To start the REPL interface, run:
```sh
python main.py
```

---

### Available Commands

| Command      | Description                 |
|-------------|-----------------------------|
| `add x y`   | Adds two numbers            |
| `subtract x y` | Subtracts y from x       |
| `multiply x y` | Multiplies two numbers   |
| `divide x y`   | Divides x by y           |
| `history`   | Displays past calculations  |
| `exit`      | Exits the program           |

---

### 🧪 Running Tests & Code Quality Checks
### Run Unit Tests
```sh
pytest
```
### Run Tests with Coverage
```sh
pytest --cov
```
### Run Linting Checks (Pylint)
```sh
pytest --pylint
```

---

### 🛠 Plugin System
The calculator application supports plugin-based extensibility, allowing new operations to be added dynamically.
### Adding a New Plugin

1. Navigate to `app/plugins/`
2. Create a new Python file (e.g., `modulus.py`)
3. Implement a new operation as a function
4. The system will automatically detect and register the plugin

### Example Plugin (`modulus.py`)

Create a new plugin file inside `app/plugins/` and define an operation:

```python
def operation(a, b):
    return a % b
```
To enable plugin discovery, ensure the following is included:
```python
from app.operations import load_plugins
load_plugins()
```

---

## 🛠 Development & Contribution Guidelines

### Branching Strategy
- **main** → Stable production branch
- **feature-branches** → Feature development
- **bugfix-branches** → Fixes for existing issues

### How to Contribute
1. **Fork the repository** on GitHub.
2. **Create a new branch** for your feature or fix:
   ```sh
   git checkout -b feature-new-command
   ```
3. **Make your changes** and commit: 
   ```sh
   git commit -m "Added new command feature"
   ```
4. **Push** to GitHub: 
   ```sh
   git push origin feature-new-command
   ```
5. **Open a Pull Request (PR)** to GitHub for review. 

---

## 📜 License

This project is licensed under the **MIT License**.

---

## 📞 Contact

For questions, please reach out via **[GitHub Issues](https://github.com/jesusgaud/Python-based_calculator_app/issues)**.

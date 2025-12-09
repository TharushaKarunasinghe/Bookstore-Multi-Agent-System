# Bookstore Management System (BMS) - Ontology & Multi-Agent Simulation

## 📌 Project Overview

This project is a **Bookstore Management System** that simulates the interactions between customers, employees, and inventory in a bookstore environment. It combines **Multi-Agent Systems (MAS)** using the _Mesa_ framework with **Knowledge Representation** using an OWL Ontology (_Owlready2_).

The simulation visually demonstrates:

- **Customers** randomly browsing and purchasing books.
- **Employees** monitoring shelves and restocking items when inventory is low.
- **Real-time Logic** governed by Python agents and Semantic Web Rule Language (SWRL) concepts.

## 🚀 Features

- **Multi-Agent Simulation:** Autonomous agents (Customers, Employees) moving on a grid.
- **Ontology Integration:** Uses `Owlready2` to define classes (`Book`, `Customer`, `Order`) and properties (`has_price`, `purchases`).
- **Dynamic Inventory:** Stock levels decrease upon purchase and increase upon employee restocking.
- **Interactive Interface:**
  - **Visual Grid:** Shows agents moving in real-time.
  - **Toggleable Chart:** A "Show/Hide Stock Chart" button to view inventory trends without cluttering the screen.
- **Message Bus:** A communication system logs events (Sales/Restocks) to the console.

## 🛠️ Project Structure

- `run.py`: The main entry point to launch the application.
- `server.py`: Handles the Visualization (HTML/CSS/JS), the Grid, and the Toggle Button interface.
- `model.py`: Defines the `BookstoreModel`, initialization of agents, and the Message Bus.
- `agents.py`: Contains the logic for `CustomerAgent`, `EmployeeAgent`, and `BookAgent`.
- `bms_ontology.py`: Defines the OWL Ontology, Classes, Properties, and SWRL rules.
- `bookstore_ontology.owl`: (Generated automatically) The saved ontology file.
- `requirements.txt`: List of dependencies.

## ⚙️ Installation & Setup

### 1. Prerequisites

- Python 3.8 or higher

### 2. Set up the Environment

Open your terminal in the project directory:

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## ▶️ How to Run

Ensure your virtual environment is active.

Run the application:

```bash
python run.py
```

Open your web browser and go to the local server address shown in the terminal (usually http://127.0.0.1:9001).

## 🎮 User Guide

**Start Simulation:** Click the Start button in the top-right corner of the browser interface.

**Observe Agents:**

- 🔵 Blue Circles: Customers.
- 🔴 Red Circles: Employees.
- 🟩 Green Squares: Bookshelves (Numbers inside indicate current stock).

**View Data:** Click the "📊 Show/Hide Stock Chart" button below the grid to reveal the real-time stock history graph.

**Check Logs:** Check your terminal/console to see the "Message Bus" outputs (e.g., [BUS]: PURCHASE...).

## 🧠 Logic & Rules

**Purchase Rule:** When a Customer lands on a book with stock > 0, they buy it. This triggers a stock reduction and updates the Ontology Order class.

**Restock Rule:** If an Employee detects a book with stock < 3, they restock it (+10 units).

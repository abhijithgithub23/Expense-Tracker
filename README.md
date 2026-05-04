#  Expense Tracker (Python GUI)

A lightweight, standalone desktop application built with Python and Tkinter to manage daily finances. This project demonstrates a clear separation of concerns by isolating the graphical user interface (GUI) from the underlying CRUD data logic.

##  Features

*   **Full CRUD Functionality:** Create, Read, Update, and Delete income and expense records.
*   **Dynamic Dashboard:** Real-time calculation of Total Income, Total Expenses, and Net Balance.
*   **Category Breakdown:** Auto-generated summaries showing exactly how much is spent per category (Food, Travel, Bills, etc.).
*   **Data Validation:** Built-in safeguards to prevent users from submitting empty fields, non-numeric values, or zero/negative amounts.
*   **Persistent Storage:** Uses a local `.json` file as a lightweight database so data remains across sessions.
*   **Smooth UX:** Features click-to-populate update fields, table-click un-selection, and instant UI refreshing.

##  Tech Stack

*   **Language:** Python 3
*   **GUI Framework:** Tkinter / ttk (Python Standard Library)
*   **Database:** JSON (Local File I/O)

##  Project Structure

The codebase is intentionally split into two distinct layers to separate the UI from the data logic:
```text
expense_tracker/
│
├── main.py          # The Frontend (Tkinter Layout, Event Bindings, UI updates)
├── data.py          # The Backend (File I/O, CRUD operations, Calculations)
└── data.json        # The Database (Auto-generates upon first transaction)

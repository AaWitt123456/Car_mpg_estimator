
import sqlite3
import tkinter as tk
from pathlib import Path
from tkinter import messagebox

import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def show_scatterplot():
    database_path = (
            Path(__file__).resolve().parent / ".." / ".." / "SQLDatabase" / "CarInfoDatabase.db"
    ).resolve()

    try:
        # Connect to the database
        connection = sqlite3.connect(database_path)

        # Get vehicle weight and MPG
        df = pd.read_sql_query(
            """
            SELECT
                [Kerb Weight],
                [Miles Per Gallon]
            FROM CarStats
            """,
            connection
        )

        connection.close()

        # Convert values to numeric
        df["Kerb Weight"] = pd.to_numeric(
            df["Kerb Weight"],
            errors="coerce"
        )

        df["Miles Per Gallon"] = pd.to_numeric(
            df["Miles Per Gallon"],
            errors="coerce"
        )


        # Create popup window
        chart_window = tk.Toplevel()
        chart_window.title("Vehicle Weight vs MPG")
        chart_window.geometry("800x600")
        chart_window.configure(bg="white")

        # Create scatterplot
        figure = Figure(figsize=(8, 5), dpi=100)
        plot = figure.add_subplot(111)

        plot.scatter(
            df["Kerb Weight"],
            df["Miles Per Gallon"],
            alpha=0.7
        )

        #Add labels
        plot.set_title(
            "Vehicle Weight vs Miles Per Gallon"
        )

        plot.set_xlabel("Kerb Weight")
        plot.set_ylabel("Miles Per Gallon")

        plot.grid(True)

        figure.tight_layout()

        # Display plot inside popup window
        canvas = FigureCanvasTkAgg(
            figure,
            master=chart_window
        )

        canvas.draw()

        canvas.get_tk_widget().pack(
            fill=tk.BOTH,
            expand=True
        )

    except Exception as error:
        messagebox.showerror(
            "Scatterplot Error",
            f"Unable to create scatterplot:\n{error}"
        )


import sqlite3
import tkinter as tk
from pathlib import Path
from tkinter import messagebox

import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def show_line_chart():
    database_path = (
            Path(__file__).resolve().parent / ".." / ".." / "SQLDatabase" / "CarInfoDatabase.db"
    ).resolve()

    try:
        connection = sqlite3.connect(database_path)

        df = pd.read_sql_query(
            """
            SELECT
                [Horse Power],
                [Miles Per Gallon]
            FROM CarStats
            """,
            connection
        )
        connection.close()

        # Convert values to numeric data
        df["Horse Power"] = pd.to_numeric(
            df["Horse Power"], errors="coerce"
        )
        df["Miles Per Gallon"] = pd.to_numeric(
            df["Miles Per Gallon"], errors="coerce"
        )


        # Calculate average MPG for each horsepower value
        average_mpg = (
            df.groupby("Horse Power")["Miles Per Gallon"]
            .mean()
            .sort_index()
        )

        # Create popup window
        chart_window = tk.Toplevel()
        chart_window.title("MPG vs Horsepower")
        chart_window.geometry("800x600")
        chart_window.configure(bg="white")

        # Create chart
        figure = Figure(figsize=(8, 5), dpi=100)
        plot = figure.add_subplot(111)

        plot.plot(
            average_mpg.index,
            average_mpg.values,
            marker="o",
            linestyle="-"
        )

        plot.set_title("MPG vs Horsepower")
        plot.set_xlabel("Horsepower")
        plot.set_ylabel("Miles Per Gallon")
        plot.grid(True)

        figure.tight_layout()

        # Display chart
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
            "Line Chart Error",
            f"Unable to create line chart:\n{error}"
        )



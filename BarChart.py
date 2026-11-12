
import sqlite3
import tkinter as tk
from pathlib import Path
from tkinter import messagebox

import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def show_bar_chart():
    database_path = (
            Path(__file__).resolve().parent / ".." / ".." / "SQLDatabase" / "CarInfoDatabase.db"
    ).resolve()

    try:
        connection = sqlite3.connect(database_path)

        df = pd.read_sql_query(
            """
            SELECT
                [Cylinder Number],
                [Miles Per Gallon]
            FROM CarStats
            """,
            connection
        )
        connection.close()

        df["Cylinder Number"] = pd.to_numeric(
            df["Cylinder Number"], errors="coerce"
        )
        df["Miles Per Gallon"] = pd.to_numeric(
            df["Miles Per Gallon"], errors="coerce"
        )

        df = df.dropna(
            subset=["Cylinder Number", "Miles Per Gallon"]
        )

        average_mpg = (
            df.groupby("Cylinder Number")["Miles Per Gallon"]
            .mean()
            .sort_index()
        )

        chart_window = tk.Toplevel()
        chart_window.title("Average MPG by Cylinder Count")
        chart_window.geometry("800x600")
        chart_window.configure(bg="white")

        figure = Figure(figsize=(8, 5), dpi=100)
        plot = figure.add_subplot(111)

        plot.bar(
            average_mpg.index.astype(int).astype(str),
            average_mpg.values,
            edgecolor="black",
            alpha=0.7
        )

        plot.set_title("Average MPG by Cylinder Count")
        plot.set_xlabel("Number of Cylinders")
        plot.set_ylabel("Average Miles Per Gallon")
        plot.grid(True, axis="y")

        figure.tight_layout()

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
            "Bar Chart Error",
            f"Unable to create bar chart:\n{error}"
        )

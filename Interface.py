import tkinter as tk
from tkinter import messagebox
from Scatterplot import show_scatterplot
from BarChart import show_bar_chart
from LineChart import show_line_chart

from PredictMpg import predict_mpg


def launch_interface(model):
    # Creates the GUI
    root = tk.Tk()
    root.title("Car MPG Predictor")
    root.geometry("650x650")
    root.configure(bg="white")
    root.resizable(False, False)

    tk.Label(
        root,
        text="Car MPG Predictor",
        font=("Arial", 24),
        bg="white",
        fg="red"
    ).pack(pady=(20, 15))

    # Input form
    form = tk.Frame(root, bg="white")
    form.pack(fill="x", padx=30)

    def add_field(label_text, row):
        tk.Label(
            form,
            text=label_text,
            font=("Arial", 15),
            bg="white",
            fg="black"
        ).grid(
            row=row, column=0,
            sticky="w", pady=8
        )

        entry = tk.Entry(
            form,
            font=("Arial", 15),
            width=22
        )

        entry.grid(
            row=row, column=1,
            padx=(25, 0), pady=8
        )

        return entry

    # Create the four input fields
    hp_entry = add_field("Horse Power", 0)
    cylinder_entry = add_field("Cylinder Number", 1)
    displacement_entry = add_field("Engine Displacement (cm³)", 2)
    weight_entry = add_field("Kerb Weight (kg)", 3)

    # Result display
    tk.Label(
        root,
        text="Estimated MPG",
        font=("Arial", 11),
        bg="white",
        fg="black"
    ).pack(pady=(15, 0))

    result_label = tk.Label(
        root,
        text="-- MPG",
        font=("Arial", 16),
        bg="white",
        fg="black"
    )
    result_label.pack(pady=8)

    # Handle the Predict MPG button
    def on_predict():
        try:
            horsepower = float(hp_entry.get())
            cylinders = int(cylinder_entry.get())
            displacement = float(
                displacement_entry.get()
            )
            weight = float(weight_entry.get())

            if min(
                    horsepower, cylinders,
                    displacement, weight
            ) <= 0:
                raise ValueError

            mpg = predict_mpg(
                model,
                horsepower,
                cylinders,
                displacement,
                weight
            )

            result_label.config(
                text=f"{mpg:.2f} MPG"
            )

        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Enter positive numeric values in all fields."
            )

    Rainbow_button = tk.Button(
        root,
        text="Predict MPG",
        command=on_predict,
        font=("Arial", 10),
        padx=15,
        pady=5
    )
    Rainbow_button.pack(pady=12)

    rainbow_colors = [
        "#FF0000",
        "#FF8C00",
        "#FFFF00",
        "#00FF00",
        "#0080FF",
        "#8B00FF",
    ]

    def change_button_color(index=0):
        Rainbow_button.config(
            bg=rainbow_colors[index]
        )

        next_index = (index + 1) % len(rainbow_colors)

        root.after(
            700,
            lambda: change_button_color(next_index)
        )

    change_button_color()

    scatterplot_button = tk.Button(
        root,
        text="Weight vs MPG",
        command=show_scatterplot,
        font=("Arial", 10),
        padx=15,
        pady=5
    )

    scatterplot_button.pack(pady=12)

    bar_chart_button = tk.Button(
        root,
        text="Average MPG by Cylinders",
        command=show_bar_chart,
        font=("Arial", 10),
        padx=15,
        pady=5
    )
    bar_chart_button.pack(pady=12)

    line_chart_button = tk.Button(
        root,
        text="MPG vs Horsepower",
        command=show_line_chart,
        font=("Arial", 10),
        padx=15,
        pady=5
    )
    line_chart_button.pack(pady=12)

    hp_entry.focus_set()

    root.mainloop()



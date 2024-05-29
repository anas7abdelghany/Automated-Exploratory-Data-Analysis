import customtkinter as ctk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


app = ctk.CTk()

data = None  
def sw_com():
    if switch.get():
        ctk.set_appearance_mode("Light")
    else:
        ctk.set_appearance_mode("Dark")

def upload_file():
    global data
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx")])
    if file_path:
        if file_path.endswith('.csv'):
            data = pd.read_csv(file_path)
        elif file_path.endswith('.xlsx'):
            data = pd.read_excel(file_path)
        messagebox.showinfo("Info", "File uploaded successfully!")
        print("Data before processing:")
        print(data.head())

def remove_duplicates():
    global data
    if data is not None:
        print("Data before removing duplicates:")
        print(data.head())
        data = data.drop_duplicates()
        print("Data after removing duplicates:")
        print(data.head())
        messagebox.showinfo("Info", "Duplicates removed successfully!")


def fill_missing_values():
    global data
    if data is not None:
        print("Data before filling missing values:")
        print(data.head())
        numeric_cols = data.select_dtypes(include=['float64', 'int64']).columns
        categorical_cols = data.select_dtypes(include=['object']).columns
        
        data[numeric_cols] = data[numeric_cols].apply(lambda col: col.fillna(col.mean()))
        data[categorical_cols] = data[categorical_cols].apply(lambda col: col.fillna(col.mode()[0]))

        print("Data after filling missing values:")
        print(data.head())
        messagebox.showinfo("Info", "Missing values filled successfully!")

def perform_eda():
    global data
    if data is not None:
        eda_window = ctk.CTkToplevel(app)
        eda_window.geometry("720x520")
        eda_window.title("Exploratory Data Analysis (EDA)")

        eda_frame = ctk.CTkFrame(eda_window)
        eda_frame.pack(padx=10, pady=10, fill="both", expand=True)

        dtypes_label = ctk.CTkLabel(eda_frame, text="visualization ", font=('arial', 16, 'bold'))
        dtypes_label.pack(pady=10)
        
        visualiz_columns = list(data.columns)
        numeric_columns = data[visualiz_columns].select_dtypes(include=['number']).columns

        for column in numeric_columns:
            fig, ax = plt.subplots(figsize=(8, 4))
            sns.histplot(data=data, x=column, kde=True, ax=ax)
            ax.set_title(f"Histogram for {column}")
            ax.set_xlabel(column)
            ax.set_ylabel("Frequency")
            canvas = FigureCanvasTkAgg(fig, master=eda_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(pady=10)

        for column in numeric_columns:
            fig, ax = plt.subplots(figsize=(8, 4))
            sns.boxplot(data=data, y=column, ax=ax)
            ax.set_title(f"Box Plot for {column}")
            ax.set_ylabel(column)
            canvas = FigureCanvasTkAgg(fig, master=eda_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(pady=10)

        if len(numeric_columns) >= 2:
            for i in range(len(numeric_columns)):
                for j in range(i + 1, len(numeric_columns)):
                    fig, ax = plt.subplots(figsize=(8, 6))
                    sns.scatterplot(data=data, x=numeric_columns[i], y=numeric_columns[j], ax=ax)
                    ax.set_title(f"Scatter Plot: {numeric_columns[i]} vs {numeric_columns[j]}")
                    ax.set_xlabel(numeric_columns[i])
                    ax.set_ylabel(numeric_columns[j])
                    canvas = FigureCanvasTkAgg(fig, master=eda_frame)
                    canvas.draw()
                    canvas.get_tk_widget().pack(pady=10)

        if len(numeric_columns) >= 2:
            correlation_matrix = data[numeric_columns].corr()
            fig, ax = plt.subplots(figsize=(10, 8))
            sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=1, ax=ax)
            ax.set_title("Correlation Matrix")
            canvas = FigureCanvasTkAgg(fig, master=eda_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(pady=10)
                                 

app.geometry("720x520")
app.title("Automated Exploratory Data Analysis")
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme('blue')

frame = ctk.CTkFrame(app, height=100, width=200, fg_color='lightgray')
frame.pack(padx=30, pady=40, fill="both", expand=True)

label = ctk.CTkLabel(frame, text_color='black', font=('arial', 20, 'bold'), text="Automated Exploratory Data Analysis")
label.pack(pady=20)

switch = ctk.CTkSwitch(app, text="Mode", command=sw_com)
switch.pack(padx=0, pady=10)

upload_button = ctk.CTkButton(frame, text="Upload CSV or Excel file", command=upload_file)
upload_button.pack(pady=10)


remove_duplicates_button = ctk.CTkButton(frame, text="Remove Duplicates", command=remove_duplicates)
remove_duplicates_button.pack(pady=10)

fill_missing_values_button = ctk.CTkButton(frame, text="Fill Missing Values", command=fill_missing_values)
fill_missing_values_button.pack(pady=10)

eda_button = ctk.CTkButton(frame, text="Perform EDA", command=perform_eda)
eda_button.pack(pady=10)


app.mainloop()

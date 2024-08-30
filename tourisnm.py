import tkinter as tk
from tkinter import ttk, scrolledtext
import sqlite3
import requests
from googlesearch import search
from bs4 import BeautifulSoup

root = tk.Tk()
root.title("---NOne---")

# Database connection below
db_conn = sqlite3.connect('Tourism_Data.db')
print("File Created")
db_cursor = db_conn.cursor()

# Creating table
db_cursor.execute('''CREATE TABLE IF NOT EXISTS Tourist_data_1 (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT,
                            Age TEXT,
                            Gender TEXT,
                            current_location TEXT,
                            country_to_visit TEXT,
                            Mode_of_transport TEXT,
                            PLace_decrption TEXT,
                            Travelling_Total_cost FLOAT
                        )''')
print("Tourist_data_1 Table created")
db_conn.commit()

def insert_data(name, Age, Gender, current_location, country_to_visit, Mode_of_transport, PLace_decrption, Travelling_Total_cost):
    db_conn = sqlite3.connect('Tourism_Data.db')  # Corrected database name
    db_cursor = db_conn.cursor()

    insert_query = '''
        INSERT INTO Tourist_data_1 (name, Age, Gender, current_location, country_to_visit, Mode_of_transport, PLace_decrption, Travelling_Total_cost)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    '''

    db_cursor.execute(insert_query, (name, Age, Gender, current_location, country_to_visit, Mode_of_transport, PLace_decrption, Travelling_Total_cost))
    db_conn.commit()

def extract_summary_from_link(link):
    try:
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html.parser')
        summary = soup.get_text()
        return summary
    except Exception as e:
        print(f"Error extracting summary: {str(e)}")
        return "Error extracting summary."

def search_google(current_location, country_to_visit, Mode_of_transport, num_results=5):
    search_query1 = f"Google search for Everything about {country_to_visit}"
    search_query2 = f"Google search for What is the cost for Journey From {current_location} To {country_to_visit} through {Mode_of_transport} available and its ticket prices"
    results1 = search(search_query1, num_results=num_results)
    results2 = search(search_query2, num_results=num_results)

    summary_1 = ''
    for i, Place_description in enumerate(results1, 1):
        if i == 2:
            link_summary = extract_summary_from_link(Place_description)
            summary_1 += f"\nResult {i} Summary:\n{link_summary}\n"

    summary_2 = ''
    for j, Travelling_Total_cost in enumerate(results2, 1):
        if j == 1:
            link_summary = extract_summary_from_link(Travelling_Total_cost)
            summary_2 += f"\nResult {j} Summary:\n{link_summary}\n"

    return summary_1, summary_2

def save_to_database():
    name = name_entry.get()
    Age = Age_entry.get()
    Gender = Gender_entry.get()
    current_location = current_location_entry.get()
    country_to_visit = country_to_visit_entry.get()
    Mode_of_transport = Mode_of_transport_entry.get()

    db_cursor.execute('''CREATE TABLE IF NOT EXISTS Tourist_data_1 (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT,
                            Age TEXT,
                            Gender TEXT,
                            current_location TEXT,
                            country_to_visit TEXT,
                            Mode_of_transport TEXT,
                            PLace_description TEXT,
                            Travelling_Total_cost FLOAT
                        )''')
    db_conn.commit()

    result_summary_1, result_summary_2 = search_google(current_location, country_to_visit, Mode_of_transport, num_results=2)

    insert_data(name, Age, Gender, current_location, country_to_visit, Mode_of_transport, result_summary_1, result_summary_2)

    result_text_1.config(state=tk.NORMAL)
    result_text_1.delete(1.0, tk.END)
    result_text_1.insert(tk.END, result_summary_1)
    result_text_1.config(state=tk.DISABLED)

    result_label_1.config(text="Data stored, and Google search performed successfully.")

    result_text_2.config(state=tk.NORMAL)
    result_text_2.delete(1.0, tk.END)
    result_text_2.insert(tk.END, result_summary_2)
    result_text_2.config(state=tk.DISABLED)

    result_label_2.config(text="Data stored, and Google search performed successfully.")

# Create Text widgets globally
result_text_1 = scrolledtext.ScrolledText(root, width=40, height=10)
result_text_2 = scrolledtext.ScrolledText(root, width=40, height=10)

# Widgets
name_label = ttk.Label(root, text="Enter Your Name:")
name_label.pack(pady=10)
name_entry = ttk.Entry(root)
name_entry.pack(pady=5)

Age_label = ttk.Label(root, text="Enter Your Age:")
Age_label.pack(pady=5)
Age_entry = ttk.Entry(root)
Age_entry.pack(pady=5)

Gender_label = ttk.Label(root, text="Enter Your Gender:")
Gender_label.pack(pady=5)
Gender_entry = ttk.Entry(root)
Gender_entry.pack(pady=5)

current_location_label = ttk.Label(root, text="Enter Your current_location:")
current_location_label.pack(pady=5)
current_location_entry = ttk.Entry(root)
current_location_entry.pack(pady=5)

country_to_visit_label = ttk.Label(root, text="Enter Your country_to_visit:")
country_to_visit_label.pack(pady=5)
country_to_visit_entry = ttk.Entry(root)
country_to_visit_entry.pack(pady=5)

Mode_of_transport_label = ttk.Label(root, text="Enter Your Mode_of_transport:")
Mode_of_transport_label.pack(pady=5)
Mode_of_transport_entry = ttk.Entry(root)
Mode_of_transport_entry.pack(pady=5)

submit_button = ttk.Button(root, text="Submit", command=save_to_database)
submit_button.pack(pady=10)

def open_second_window():
    second_window = tk.Toplevel(root)
    second_window.title("Second Window")

    label = tk.Label(second_window, text="This is the second window.")
    label.pack()

    result_label_1 = ttk.Label(second_window, text="Search Results:")
    result_label_1.pack()

    result_text_1.pack()

    result_label_2 = ttk.Label(second_window, text="Search Results:")
    result_label_2.pack()

    result_text_2.pack()

button = tk.Button(root, text="Open Second Window", command=open_second_window)
button.pack()

root.mainloop()

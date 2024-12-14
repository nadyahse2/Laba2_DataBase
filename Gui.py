import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
import os

from main import TravelManager

class TravelGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Travel Manager")
        self.database = TravelManager()
        self.create_widgets()

    def create_widgets(self):
        self.labels = ['trip_id', 'destination', 'start_date', 'end_date', 'transport']
        self.entries = {}
        for i, label_text in enumerate(self.labels):
            ttk.Label(self.root, text=f"{label_text.capitalize()}:").grid(row=i, column=0, padx=5, pady=5, sticky=tk.W)
            entry = ttk.Entry(self.root)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky=tk.EW)
            self.entries[label_text] = entry
            if label_text in ['start_date','end_date']:
                entry.insert(0, "YYYY-MM-DD")

        # --- Buttons ---
        add_button = ttk.Button(self.root, text="Add Record", command=self.add_record)
        add_button.grid(row=0, column=2, padx=10, pady=10)

        delete_button = ttk.Button(self.root, text="Delete Record", command=self.delete_record)
        delete_button.grid(row=1, column=2, padx=10, pady=10)

        search_button = ttk.Button(self.root, text="Search Record", command=self.search_record)
        search_button.grid(row=2, column=2, padx=10, pady=10)

        export_excel_button = ttk.Button(self.root, text="Import to Excel", command=self.export_to_excel)
        export_excel_button.grid(row=3, column=2, padx=10, pady=10)

        backup_button = ttk.Button(self.root, text="Create Backup", command=self.create_backup)
        backup_button.grid(row=4, column=2, padx=10, pady=10)

        restore_button = ttk.Button(self.root, text="Restore Backup", command=self.restore_backup)
        restore_button.grid(row=5, column=2, padx=10, pady=10)

        open_db_button = ttk.Button(self.root, text="Open Database", command=self.open_database_file)
        open_db_button.grid(row=6, column=2, padx=10, pady=10)

        create_db_button = ttk.Button(self.root, text="Create Database", command=self.create_database)
        create_db_button.grid(row=7, column=2, padx=10, pady=10)

        delete_db_button = ttk.Button(self.root, text="Delete Database", command=self.delete_database)
        delete_db_button.grid(row=8, column=2, padx=10, pady=10)


        self.root.columnconfigure(1, weight=1)  # Make the entry column expand


    def validate_data(self, data):
          try:
            trip_id = int(data[0]) if data[0] else None
            if trip_id is None:
                return False, "Trip ID must be an integer."
            destination = str(data[1]) if data[1] else None
            if destination is None:
                return False, "Destination must be a non-empty string"
            start_date = datetime.strptime(data[2], "%Y-%m-%d").date() if data[2] != None and data[2] != "YYYY-MM-DD" else None
            if start_date is None:
                return False, "Start date must be a valid date in the format YYYY-MM-DD"
            end_date = datetime.strptime(data[3], "%Y-%m-%d").date() if data[3] != None and data[3] != "YYYY-MM-DD" else None
            if end_date is None:
                return False, "End date must be a valid date in the format YYYY-MM-DD"
            transport = str(data[4]) if data[4] else None
            if transport is None:
                return False, "Transport must be a non-empty string"

            return True, [trip_id,destination,start_date,end_date,transport]

          except ValueError as e:
              return False, str(e)
    def clear_entries(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
            if entry in [self.entries['start_date'],self.entries['end_date']]:
                 entry.insert(0, "YYYY-MM-DD")

    def add_record(self):
        data = [entry.get() for entry in self.entries.values()]
        is_valid, validated_data = self.validate_data(data)
        if is_valid:
           success = self.database.add_row(validated_data)
           if success:
              self.database.save_db()
              messagebox.showinfo("Success", "Record added successfully.")
              self.clear_entries()
           else:
               messagebox.showerror("Error", validated_data[1])
        else:
           messagebox.showerror("Error", validated_data)

    def delete_record(self):
       data = [entry.get() for entry in self.entries.values()]
       search_values = [item for item in data if item != '']
       if not search_values or len(search_values) != 1:
           messagebox.showerror("Error", "Please provide at least one field for deletion.")
           return
       success = self.database.delete_row(*search_values)
       if success:
           self.database.save_db()
           messagebox.showinfo("Success", "Record(s) deleted successfully.")
           self.clear_entries()
       else:
           messagebox.showerror("Error", "No matching records found for deletion.")


    def search_record(self):
        data = [entry.get() for entry in self.entries.values()]
        search_values = [item for item in data if item != '']
        if not search_values or search_values != 1:
            messagebox.showerror("Error", "Please provide at least one field for searching.")
            return
        result = self.database.search_row(*search_values)

        if result:
            self.display_results(result)
        else:
            messagebox.showinfo("Not found", "Record not found")
        self.clear_entries()

    def display_results(self, results):
        if not results:
            messagebox.showinfo("Search Results", "No results found")
            return
        output_str = ""
        for row in results:
            output_str += f"Trip ID: {row[0]}, Destination: {row[1]}, Start Date: {row[2]}, End Date: {row[3]}, Transport: {row[4]}\n"
        messagebox.showinfo("Search Results", output_str)


    def export_to_excel(self):
        try:
            excel_path = self.database.import_from_excel()
            messagebox.showinfo("Export Successful", f"Data exported to Excel at: {excel_path}")
        except Exception as e:
             messagebox.showerror("Export Error", str(e))

    def create_backup(self):
         success = self.database.create_backup()
         if success:
            messagebox.showinfo("Backup Successful", "Backup created successfully.")
         else:
            messagebox.showerror("Backup Error", "Failed to create backup.")

    def restore_backup(self):
        success, message = self.database.restore_from_backup()
        if success:
            messagebox.showinfo("Restore Successful", "Database restored from backup.")
        else:
           messagebox.showerror("Restore Error", message)

    def open_database_file(self):
        file_path = self.database.file
        if os.path.exists(file_path):
            try:
                os.startfile(file_path)
            except AttributeError:  # For macOS and Linux
                os.system(f"open '{file_path}'")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open database file: {e}")
        else:
            messagebox.showerror("Error", f"Database file not found: {file_path}")

    def create_database(self):
        self.database.delete_db()
        self.database = TravelManager()
        messagebox.showinfo("Success", "Database created successfully.")
        self.clear_entries()

    def delete_database(self):
        self.database.delete_db()
        messagebox.showinfo("Success", "Database deleted successfully.")
        self.clear_entries()
if __name__ == "__main__":
    root = tk.Tk()
    gui = TravelGUI(root)
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("Application is closing...")
    finally:
        print("Closing.")
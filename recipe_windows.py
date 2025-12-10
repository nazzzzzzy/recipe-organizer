import tkinter as tk
from tkinter import messagebox
import database

def open_add_window(parent, refresh_cb):
    win = tk.Toplevel(parent)
    win.title("add recipe")
    win.geometry("420x520")

    labels = ["name","ingredients (comma separated)","steps","category","prep time","notes"]
    entries = {}

    for i,l in enumerate(labels):
        tk.Label(win, text=l).pack(anchor="w", padx=10, pady=(8 if i==0 else 4))

        if l == "steps" or l == "notes":
            t = tk.Text(win, height=6)
            t.pack(fill="x", padx=10)
            entries[l] = t
        else:
            e = tk.Entry(win)
            e.pack(fill="x", padx=10)
            entries[l] = e

    def save():
        name = entries["name"].get().strip()
        ing = entries["ingredients (comma separated)"].get().strip()
        steps = entries["steps"].get("1.0", "end").strip()
        category = entries["category"].get().strip()
        prep = entries["prep time"].get().strip()
        notes = entries["notes"].get("1.0", "end").strip()

        if not name:
            messagebox.showerror("error","name required")
            return

        ing_list = [i.strip() for i in ing.split(",") if i.strip()]
        database.add_recipe(name, ing_list, steps, category, prep, notes)
        refresh_cb()
        win.destroy()

    tk.Button(win, text="save", command=save).pack(pady=10)

def open_edit_window(parent, rid, refresh_cb):
    data = database.get_recipe_by_id(rid)
    if not data:
        return

    win = tk.Toplevel(parent)
    win.title("edit recipe")
    win.geometry("420x520")

    labels = ["name","ingredients (comma separated)","steps","category","prep time","notes"]
    entries = {}

    for i,l in enumerate(labels):
        tk.Label(win, text=l).pack(anchor="w", padx=10, pady=(8 if i==0 else 4))

        if l == "steps" or l == "notes":
            t = tk.Text(win, height=6)
            t.pack(fill="x", padx=10)
            entries[l] = t
        else:
            e = tk.Entry(win)
            e.pack(fill="x", padx=10)
            entries[l] = e

    entries["name"].insert(0, data["name"])
    entries["ingredients (comma separated)"].insert(0, ", ".join(data["ingredients"]))
    entries["steps"].insert("1.0", data["steps"])
    entries["category"].insert(0, data["category"] or "")
    entries["prep time"].insert(0, data["prep_time"] or "")
    entries["notes"].insert("1.0", data["notes"] or "")

    def save():
        name = entries["name"].get().strip()
        ing = entries["ingredients (comma separated)"].get().strip()
        steps = entries["steps"].get("1.0", "end").strip()
        category = entries["category"].get().strip()
        prep = entries["prep time"].get().strip()
        notes = entries["notes"].get("1.0", "end").strip()

        if not name:
            messagebox.showerror("error","name required")
            return

        ing_list = [i.strip() for i in ing.split(",") if i.strip()]
        database.update_recipe(rid, name, ing_list, steps, category, prep, notes)
        refresh_cb()
        win.destroy()

    tk.Button(win, text="save changes", command=save).pack(pady=10)

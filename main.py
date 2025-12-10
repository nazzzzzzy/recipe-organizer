import tkinter as tk
from tkinter import messagebox, simpledialog
import database, recipe_windows, suggestions

# -------------------- gui theme --------------------

BG_MAIN = "#fff9f4"        
BG_SIDEBAR = "#f7dce5"     
BG_BUTTON = "#fcefe8"      
BG_BUTTON_HOVER = "#f8e1ff"  
TEXT_DARK = "#4a3c2c"      

FONT_TITLE = ("Helvetica", 16, "bold")
FONT_BUTTON = ("Helvetica", 11)
FONT_LABEL = ("Helvetica", 10)

def style_button(btn):
    btn.config(
        bg=BG_BUTTON,
        activebackground=BG_BUTTON_HOVER,
        relief="flat",
        bd=0,
        padx=10,
        pady=6,
        font=FONT_BUTTON,
        fg=TEXT_DARK
    )
    btn.bind("<Enter>", lambda e: btn.config(bg=BG_BUTTON_HOVER))
    btn.bind("<Leave>", lambda e: btn.config(bg=BG_BUTTON))

# ----------------------------------------------------------

def refresh_list(lb, status):
    lb.delete(0, "end")
    rows = database.get_all_recipes()
    for r in rows:
        lb.insert("end", f"{r[0]} - {r[1]} ({r[3] or 'no category'})")
    status.set(f"{len(rows)} recipes")

def view_recipe(rid):
    data = database.get_recipe_by_id(rid)
    if not data:
        messagebox.showinfo("not found","recipe not found")
        return

    win = tk.Toplevel(root)
    win.title(data["name"])
    win.geometry("520x580")
    win.config(bg=BG_MAIN)

    tk.Label(win, text=data["name"], font=FONT_TITLE, bg=BG_MAIN, fg=TEXT_DARK).pack(pady=6)
    tk.Label(win, text=f"category: {data.get('category','')} | prep: {data.get('prep_time','')}",
             bg=BG_MAIN, fg=TEXT_DARK).pack()

    tk.Label(win, text="ingredients:", font=("Helvetica", 12, "bold"),
             bg=BG_MAIN, fg=TEXT_DARK).pack(anchor="w", padx=10, pady=(12,0))

    for i in data["ingredients"]:
        tk.Label(win, text=f"• {i}", bg=BG_MAIN, fg=TEXT_DARK).pack(anchor="w", padx=25)

    tk.Label(win, text="steps:", font=("Helvetica",12,"bold"),
             bg=BG_MAIN, fg=TEXT_DARK).pack(anchor="w", padx=10, pady=(12,0))

    st = tk.Text(win, height=12, bg="#ffffff", fg=TEXT_DARK, wrap="word")
    st.pack(fill="both", padx=10, pady=6)
    st.insert("1.0", data["steps"])
    st.config(state="disabled")

    if data.get("notes"):
        tk.Label(win, text="notes:", font=("Helvetica",12,"bold"),
                 bg=BG_MAIN, fg=TEXT_DARK).pack(anchor="w", padx=10, pady=(12,0))
        tk.Label(win, text=data["notes"], bg=BG_MAIN, fg=TEXT_DARK, wraplength=450).pack(anchor="w", padx=25)

def on_add():
    recipe_windows.open_add_window(root, lambda: refresh_list(listbox, status_var))

def on_edit():
    sel = listbox.curselection()
    if not sel:
        messagebox.showerror("error","select a recipe to edit")
        return
    rid = int(listbox.get(sel[0]).split(" - ")[0])
    recipe_windows.open_edit_window(root, rid, lambda: refresh_list(listbox, status_var))

def on_delete():
    sel = listbox.curselection()
    if not sel:
        messagebox.showerror("error","select a recipe to delete")
        return

    rid = int(listbox.get(sel[0]).split(" - ")[0])
    if messagebox.askyesno("confirm","delete this recipe?"):
        database.delete_recipe(rid)
        refresh_list(listbox, status_var)

def on_search():
    term = search_var.get().strip()
    if not term:
        refresh_list(listbox, status_var)
        return

    if search_mode.get() == "category":
        rows = database.search_by_category(term)
    else:
        rows = database.search_by_ingredient(term)

    listbox.delete(0, "end")
    for r in rows:
        listbox.insert("end", f"{r[0]} - {r[1]} ({r[3] or 'no category'})")

    status_var.set(f"{len(rows)} results")

def on_view():
    sel = listbox.curselection()
    if not sel:
        messagebox.showerror("error","select a recipe to view")
        return
    rid = int(listbox.get(sel[0]).split(" - ")[0])
    view_recipe(rid)

def on_suggest():
    inp = simpledialog.askstring("ingredients","enter available ingredients (comma separated)")
    if not inp:
        return

    parts = [p.strip() for p in inp.split(",") if p.strip()]
    results = suggestions.suggest_recipes(parts)

    if not results:
        messagebox.showinfo("none","no suggestions")
        return

    win = tk.Toplevel(root)
    win.title("suggestions")
    win.geometry("520x560")
    win.config(bg=BG_MAIN)

    for r in results:
        tk.Label(win, text=r["name"], font=("Helvetica", 13, "bold"),
                 bg=BG_MAIN, fg=TEXT_DARK).pack(anchor="w", padx=10, pady=(10,0))
        tk.Label(win, text=f"category: {r['category']} | prep: {r['prep_time']}",
                 bg=BG_MAIN, fg=TEXT_DARK).pack(anchor="w", padx=15)
        tk.Label(win, text="ingredients: " + ", ".join(r["ingredients"]),
                 bg=BG_MAIN, fg=TEXT_DARK).pack(anchor="w", padx=15)

# ----------------------------------------------------------

if __name__ == "__main__":
    database.init_db()

    root = tk.Tk()
    root.title("🍓 recipe organizer")
    root.geometry("980x550")
    root.config(bg=BG_MAIN)

    # left sidebar
    sidebar = tk.Frame(root, bg=BG_SIDEBAR, width=180)
    sidebar.pack(side="left", fill="y")

    # header text
    tk.Label(sidebar, text="my recipes", bg=BG_SIDEBAR, fg=TEXT_DARK,
             font=FONT_TITLE).pack(pady=15)

    # search area
    tk.Label(sidebar, text="search", bg=BG_SIDEBAR, fg=TEXT_DARK).pack(anchor="w", padx=10)
    search_var = tk.StringVar()
    search_entry = tk.Entry(sidebar, textvariable=search_var)
    search_entry.pack(fill="x", padx=10, pady=(0,5))

    search_mode = tk.StringVar(value="ingredient")

    tk.Radiobutton(sidebar, text="ingredient", variable=search_mode, value="ingredient",
                   bg=BG_SIDEBAR, fg=TEXT_DARK, selectcolor=BG_SIDEBAR).pack(anchor="w", padx=10)
    tk.Radiobutton(sidebar, text="category", variable=search_mode, value="category",
                   bg=BG_SIDEBAR, fg=TEXT_DARK, selectcolor=BG_SIDEBAR).pack(anchor="w", padx=10)

    # buttons
    button_list = [
        ("search", on_search),
        ("view", on_view),
        ("add", on_add),
        ("edit", on_edit),
        ("delete", on_delete),
        ("suggest recipes", on_suggest)
    ]

    for txt, cmd in button_list:
        b = tk.Button(sidebar, text=txt, command=cmd)
        style_button(b)
        b.pack(fill="x", padx=15, pady=4)

    status_var = tk.StringVar()
    tk.Label(sidebar, textvariable=status_var, bg=BG_SIDEBAR, fg=TEXT_DARK).pack(pady=10)

    # recipe list
    listbox = tk.Listbox(root, width=40, height=25, bg="#ffffff", fg=TEXT_DARK, font=("Helvetica",10))
    listbox.pack(side="left", fill="y", padx=(10,0), pady=10)

    scrollbar = tk.Scrollbar(root, orient="vertical", command=listbox.yview)
    scrollbar.pack(side="left", fill="y", pady=10)
    listbox.config(yscrollcommand=scrollbar.set)

    refresh_list(listbox, status_var)

    # --------------- right banner -----------------

    try:
        banner = tk.PhotoImage(file="vertical_banner.png")
        banner_label = tk.Label(root, image=banner, bg=BG_MAIN)
        banner_label.image = banner  # keep reference
        banner_label.pack(side="right", fill="both", padx=10, pady=10)
    except:
        tk.Label(root, text="(vertical banner missing)", bg=BG_MAIN, fg="red").pack(side="right", padx=10)

    # --------------------------------------------------------

    root.mainloop()

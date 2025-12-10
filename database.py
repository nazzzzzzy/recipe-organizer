import sqlite3, json, os

db_path = os.path.join(os.path.dirname(__file__), "recipes.db")

def init_db():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS recipes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        ingredients TEXT NOT NULL,
        steps TEXT NOT NULL,
        category TEXT,
        prep_time TEXT,
        notes TEXT
    )
    """)

    # check for if empty
    c.execute("SELECT COUNT(*) FROM recipes")
    count = c.fetchone()[0]

    # sample recipes to have loaded - ONLY if DB is already empty
    if count == 0:
        samples = [
            {
                "name": "Lasagna",
                "ingredients": ["lasagna noodles", "ground beef", "ricotta cheese", "mozzarella cheese", "parmesan cheese", "tomato sauce", "onion", "garlic", "olive oil", "salt", "pepper", "Italian seasoning"],
                "steps": "Cook noodles. Brown beef with onion and garlic. Add tomato sauce and seasoning. Layer noodles with meat sauce and cheeses in a baking dish. Bake at 375°F for 35–45 minutes until bubbly.",
                "category": "Dinner",
                "prep_time": "1 hr",
                "notes": "Let it rest 10–15 minutes before slicing for clean layers."
            },
            {
                "name": "Pancakes",
                "ingredients": ["flour", "milk", "egg", "sugar", "baking powder", "butter"],
                "steps": "Mix dry ingredients. Whisk wet ingredients. Combine and cook on griddle.",
                "category": "Breakfast",
                "prep_time": "15 min",
                "notes": ""
            },
            {
                "name": "Vegetable Pizza",
                "ingredients": ["pizza dough", "tomato sauce", "mozzarella cheese", "bell peppers", "onions", "mushrooms", "spinach", "olive oil", "Italian seasoning"],
                "steps": "Spread tomato sauce on pizza dough. Add vegetables and mozzarella. Drizzle with olive oil and season. Bake at 450°F for 12–15 minutes until crust is golden.",
                "category": "Dinner",
                "prep_time": "30 min",
                "notes": "Quick and easy, customizable with any toppings you like."

            },
            {
                "name": "Chocolate Chip Cookies",
                "ingredients": ["flour", "sugar", "brown sugar", "butter", "eggs", "chocolate chips", "vanilla"],
                "steps": "Mix wet ingredients. Add dry ingredients. Fold in chocolate chips. Bake at 350°F for 12 minutes.",
                "category": "Dessert",
                "prep_time": "30 min",
                "notes": "Soft and chewy."
            },
            {
                "name": "Caesar Salad",
                "ingredients": ["lettuce", "croutons", "parmesan", "caesar dressing"],
                "steps": "Chop lettuce. Toss with dressing, croutons, and parmesan.",
                "category": "Lunch",
                "prep_time": "10 min",
                "notes": ""
            },
            {
                "name": "Omelette",
                "ingredients": ["eggs", "cheese", "salt", "pepper", "butter"],
                "steps": "Beat eggs. Melt butter in pan. Cook eggs and fold in cheese.",
                "category": "Breakfast",
                "prep_time": "8 min",
                "notes": ""
            }
        ]

        for r in samples:
            c.execute(
                "INSERT INTO recipes (name, ingredients, steps, category, prep_time, notes) VALUES (?, ?, ?, ?, ?, ?)",
                (r["name"], json.dumps(r["ingredients"]), r["steps"], r["category"], r["prep_time"], r["notes"])
            )

    conn.commit()
    conn.close()

def add_recipe(name, ingredients, steps, category="", prep_time="", notes=""):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("INSERT INTO recipes (name, ingredients, steps, category, prep_time, notes) VALUES (?, ?, ?, ?, ?, ?)",
              (name, json.dumps(ingredients), steps, category, prep_time, notes))
    conn.commit()
    conn.close()

def get_all_recipes():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT id, name, ingredients, category FROM recipes ORDER BY name")
    rows = c.fetchall()
    conn.close()
    return rows

def get_recipe_by_id(rid):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT id, name, ingredients, steps, category, prep_time, notes FROM recipes WHERE id = ?", (rid,))
    row = c.fetchone()
    conn.close()
    if not row:
        return None

    return {
        "id": row[0],
        "name": row[1],
        "ingredients": json.loads(row[2]),
        "steps": row[3],
        "category": row[4],
        "prep_time": row[5],
        "notes": row[6]
    }

def update_recipe(rid, name, ingredients, steps, category="", prep_time="", notes=""):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("UPDATE recipes SET name = ?, ingredients = ?, steps = ?, category = ?, prep_time = ?, notes = ? WHERE id = ?",
              (name, json.dumps(ingredients), steps, category, prep_time, notes, rid))
    conn.commit()
    conn.close()

def delete_recipe(rid):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("DELETE FROM recipes WHERE id = ?", (rid,))
    conn.commit()
    conn.close()

def search_by_category(category):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT id, name, ingredients, category FROM recipes WHERE category LIKE ? ORDER BY name",
              (f"%{category}%",))
    rows = c.fetchall()
    conn.close()
    return rows

def search_by_ingredient(term):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT id, name, ingredients, category FROM recipes")
    rows = c.fetchall()
    results = []
    term_lower = term.lower()

    for r in rows:
        ing_list = json.loads(r[2])
        joined = " ".join(ing_list).lower()
        if term_lower in joined:
            results.append(r)

    conn.close()
    return results
from database import get_all_recipes, get_recipe_by_id

def suggest_recipes(available_ingredients):
    available = [i.strip().lower() for i in available_ingredients if i.strip()]
    rows = get_all_recipes()
    scored = []

    for r in rows:
        rid = r[0]
        data = get_recipe_by_id(rid)
        if not data:
            continue

        recipe_ings = [ing.strip().lower() for ing in data["ingredients"]]

        # match only exact ingredient names 
        match_count = sum(1 for a in available if a in recipe_ings)

        # skip recipes with 0 matching ingredients
        if match_count == 0:
            continue

        score = match_count / len(recipe_ings)
        scored.append((score, data))

    scored.sort(reverse=True, key=lambda x: x[0])

    # return only matched recipes
    return [d for s, d in scored]

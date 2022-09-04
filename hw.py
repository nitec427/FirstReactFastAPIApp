from typing import Optional, List, Any
from fastapi import FastAPI, APIRouter, Query, HTTPException
from pydantic import BaseModel
from app.schemas import RecipeSearchResults, Recipe, RecipeCreate
# FastAPI provides a convenience tool to structure the application while preserving the flexibility
app = FastAPI(title="Recipe API", openapi_url="/openapi.json")


# With pydantic, we're able to make our own data types.
# Recipe can inherit BaseModel and properties is added with Python Type hinting
class Recipe(BaseModel):
    id: int
    label: str
    source: str

class Meal(BaseModel):
    meals: List[Recipe] # recursively define predefined type

RECIPES = [
    {
        "id": 1,
        "label": "Chicken Vesuvio",
        "source": "Serious Eats",
        "url": "http://www.seriouseats.com/recipes/2011/12/chicken-vesuvio-recipe.html",
    },
    {
        "id": 2,
        "label": "Chicken Paprikash",
        "source": "No Recipes",
        "url": "http://norecipes.com/recipe/chicken-paprikash/",
    },
    {
        "id": 3,
        "label": "Cauliflower and Tofu Curry Recipe",
        "source": "Serious Eats",
        "url": "http://www.seriouseats.com/recipes/2011/02/cauliflower-and-tofu-curry-recipe.html",
    },
]

api_router = APIRouter()

# group your API endpoints with api_router
@api_router.get("/", status_code=200)
def root() -> dict:
    """get root"""
    return {"msg": "Hello World!"}

@api_router.get("/search/", status_code=200,response_model=RecipeSearchResults)
def search_recipes(
    keyword: Optional[str] = Query(None, min_length=3, example="Chicken"), 
    max_results: Optional[int] = 10,
    
) -> dict:
    """ Search for recipes based on their label """
    
    if not keyword:
        return {"results": RECIPES[:max_results]}

    results = filter(lambda recipe: keyword.lower() in recipe["label"].lower(), RECIPES)
    return {"results": list(results)[:max_results]}

# Before updating with Pydantic data structures
# @api_router.get("/recipe/{recipe_id}", status_code=200)
# def fetch_recipe(*, recipe_id:int) -> dict:
#     """ Fetch a single recipe with its id """
#     print(recipe_id)
#     result = [recipe for recipe in RECIPES if recipe["id"] == recipe_id]
#     if result:
#         return result[0]
    
# Updated (Recipe response_model below is imported from schema.py file). Defined structure of JSON file
# @api_router.get("/recipe/{recipe_id}", status_code=200, response_model=Recipe)
# def fetch_recipe(*, recipe_id:int) -> Any:
#     """ Fetch a single recipe with its id """
#     print(recipe_id)
#     result = [recipe for recipe in RECIPES if recipe["id"] == recipe_id]
#     if result:
#         return result[0]

# For error handling part
@api_router.get("/recipe/{recipe_id}", status_code=200, response_model=Recipe)
def fetch_recipe(*, recipe_id:int) -> Any:
    """ Fetch a single recipe with its id """
    result = [recipe for recipe in RECIPES if recipe["id"] == recipe_id]
    if not result:
        # Notice we RAISE, NOT RETURN Exception, otherwise validation error occurs.
        raise HTTPException(
            status_code=404, detail=f"Recipe with id {recipe_id} not found "
        )
    return result[0]

@api_router.post("/recipe/", status_code=201, response_model=Recipe)
def create_recipe(*, recipe_in: RecipeCreate) -> dict:
    """ Create a new recipe (in memory only) """
    
    new_entry_id = len(RECIPES) + 1
    print(new_entry_id)
    recipe_entry = Recipe(
        id = new_entry_id,
        label = recipe_in.label,
        source = recipe_in.source,
        url = recipe_in.url,
    )
    RECIPES.append(recipe_entry.dict())
    return recipe_entry

app.include_router(api_router)

raw_recipe = {"id": 1, "label": "lasagna", "source": "Grandma"}

processed_recipe = Recipe(**raw_recipe)
print(processed_recipe.id)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host = "0.0.0.0", port = 8080, log_level="debug")
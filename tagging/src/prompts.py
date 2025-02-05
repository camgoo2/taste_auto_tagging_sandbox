RECIPE_TAGGING_PROMPT = """
Categories:
{categories}

JSON Data:
{data}
"""


RECIPE_TAGGING_PROMPT_INSTRUCTIONS = """

You will be given a recipe description along with its ingredients and method steps.
Your task is to classify the recipe into the 5 categories provided.

1.main-ingredient
2.ingredient-category
3.recipe
4.recipe-type
5.cuisine

The result should be a JSON object following the specified structure,
with a clear classification explanation, along with confidence and salience scores.

Guidelines:
Use only the tag categories and tags from the provided list.
Do not create additional categories or modify the provided ones,
if you are unsure, do not return the corresponding tag.
Double-check that each category exists in the provided list before assigning it to a recipe.
Return all the tags that are relevant from the list provided.

Explanation Guidelines:
The explanation should clearly state why the chosen categories apply to the recipe,
based on the ingredients, cuisine, and cooking/preparation methods.
Ensure the explanation does not contain any double quotes or commas inside the text.
Do not add a period at the end of the explanation.

Input:

{
"id": "61cf9d5a-9abe-406b-9d9c-40b6e5f7dbfd",
  "recipe_title": "Classic Beef Lasagne",
  "description": "A classic Italian lasagna with layers of beef, pasta, and cheese, baked to perfection.",
  "ingredients": "beef, pasta, cheese, tomato sauce, onions",
  "methodSteps": "Preheat the oven to 190°C or 170°C fan. Lightly spray a baking dish with oil.,
  Heat oil in a large pan over medium heat. Add onions, garlic, and carrots, cooking until softened.
  Stir in minced beef, cooking until browned., Add tomato paste, chopped tomatoes, and herbs.
  Simmer for 20 minutes, stirring occasionally. Season with salt and pepper to taste.,
  Prepare a béchamel sauce by melting butter in a saucepan. Stir in flour and cook for 1 minute.
  Gradually add milk, whisking until smooth. Cook until the sauce thickens. Stir in grated cheese.,
  Spoon a layer of meat sauce into the baking dish, followed by lasagne sheets.
  Add a layer of béchamel sauce. Repeat layers until all ingredients are used,
  finishing with a béchamel layer., Sprinkle grated mozzarella and Parmesan over the top.
  Bake for 30-40 minutes or until golden and bubbling. Let stand for 10 minutes before serving."
}

Output:

{
  "response": {
    "classification": [
      {
        "category": "main-ingredient",
        "tags": [
          {
            "tag": "beef",
            "confidence": 0.95,
            "salience": 0.8,
            "explanation": "Beef is the main protein listed in the ingredients."
          },
          {
            "tag": "pasta",
            "confidence": 0.9,
            "salience": 0.7,
            "explanation": "Pasta is a core component of the lasagna layers."
          }
        ]
      },
      {
        "category": "ingredient-category",
        "tags": [
          {
            "tag": "cheese",
            "confidence": 0.9,
            "salience": 0.6,
            "explanation": "Cheese is used in the béchamel sauce and as a topping."
          },
          {
            "tag": "tomato sauce",
            "confidence": 0.85,
            "salience": 0.5,
            "explanation": "Tomato sauce forms the base of the meat sauce."
          },
          {
            "tag": "onions",
            "confidence": 0.8,
            "salience": 0.4,
            "explanation": "Onions are used to flavor the meat sauce."
          }
        ]
      },
      {
        "category": "recipe",
        "tags": [
          {
            "tag": "baked dish",
            "confidence": 0.85,
            "salience": 0.6,
            "explanation": "The recipe involves baking in an oven."
          },
          {
            "tag": "layered dish",
            "confidence": 0.8,
            "salience": 0.5,
            "explanation": "The recipe involves layering pasta, meat sauce, and béchamel."
          }
        ]
      },
      {
        "category": "recipe type",
        "tags": [
          {
            "tag": "dinner",
            "confidence": 0.95,
            "salience": 0.9,
            "explanation": "Lasagna is typically served as a dinner option."
          }
        ]
      },
      {
        "category": "cuisine",
        "tags": [
          {
            "tag": "italian",
            "confidence": 0.95,
            "salience": 0.9,
            "explanation": "Lasagna is a classic Italian dish."
          }
        ]
      }
    ]
  }
}


"""

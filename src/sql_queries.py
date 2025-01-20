QUERY_RECIPE = """
WITH ranked_recipes AS (
  SELECT
    dw_partition_date,
    t.id,
    t.title AS recipe_title,
    t.description,
    (
      SELECT STRING_AGG(DISTINCT ing.ingredientId, ', ')
      FROM UNNEST(t.recipeSections) AS rs
      CROSS JOIN UNNEST(rs.ingredients) AS ing
    ) AS ingredients,
    (
      SELECT STRING_AGG(ms, ', ')
      FROM UNNEST(t.methodSteps) AS ms
    ) AS method_steps,
    ROW_NUMBER() OVER (PARTITION BY t.id ORDER BY dw_partition_date DESC) AS row_num
  FROM `{project_id}.cdm_fapi.recipes` AS t
  WHERE origin = 'taste'
)

SELECT
  dw_partition_date,
  id,
  recipe_title,
  description,
  ingredients,
  method_steps
FROM ranked_recipes
WHERE row_num = 1
LIMIT 2;
"""

QUERY_TAXONOMY_OLD = """
SELECT
  tag_category,
  tag
FROM `{project_id}.taste_auto_tagging.taxonomy_full`
"""

QUERY_TAXONOMY = """
SELECT
  tag_category,
  tag
FROM `{project_id}.taste_auto_tagging.recipe_tag_taxonomy`
"""

EVAL_QUERY = """
WITH ranked_recipes AS (
  SELECT
    id,
    title,
    description,
    category,
    created,
    (
      SELECT ARRAY_AGG(DISTINCT ing.ingredientId IGNORE NULLS)
      FROM UNNEST(recipeSections) AS rs
      CROSS JOIN UNNEST(rs.ingredients) AS ing
    ) AS ingredients,
    (
      SELECT ARRAY_AGG(ms IGNORE NULLS)
      FROM UNNEST(methodSteps) AS ms
    ) AS method_steps,
    ROW_NUMBER() OVER (PARTITION BY category ORDER BY created DESC) AS row_num
  FROM
    `{project_id}.cdm_fapi.recipes`,
    UNNEST(categories) AS category
  WHERE
    category IN (
      SELECT raw_tag
      FROM `{project_id}.taste_auto_tagging.recipe_tag_taxonomy`
    )
    AND origin = 'taste'
    AND created < '{max_create_date}'
),
unique_recipes AS (
  SELECT
    id,
    MAX(title) AS title,
    MAX(description) AS description,
    ANY_VALUE(method_steps) AS method_steps,
    ANY_VALUE(ingredients) AS ingredients
  FROM
    ranked_recipes
  WHERE
    row_num = 1
  GROUP BY
    id
),
categories_array AS (
  SELECT DISTINCT
    id,
    ARRAY_AGG(DISTINCT category IGNORE NULLS) AS categories
  FROM
    ranked_recipes
  GROUP BY
    id
)
SELECT
  ur.id,
  ur.title,
  ur.description,
  ur.method_steps,
  ur.ingredients,
  ca.categories AS filteredCategories
FROM
  unique_recipes ur
JOIN
  categories_array ca
ON
  ur.id = ca.id
  LIMIT 500
"""

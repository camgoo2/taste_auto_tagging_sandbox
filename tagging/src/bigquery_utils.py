from typing import Dict
from typing import List
from typing import Optional

from google.cloud import bigquery


def read_sql_to_dicts(
    sql_query: str, project_id: str, news_query_prd_project_id: Optional[str] = ""
) -> List[Dict]:
    """
    Executes a BigQuery SQL query and returns the results as a list of dictionaries.

    Args:
      sql_query: The SQL query to execute.
      project_id: The ID of your Google Cloud project.

    Returns:
      A list of dictionaries, where each dictionary represents a row from the query results.
    """

    # Create a BigQuery client object
    client = bigquery.Client(project=project_id)
    sql_query = sql_query.format(
        project_id=project_id, news_query_prd_project_id=news_query_prd_project_id
    )

    # Execute the query
    query_job = client.query(sql_query)
    results = query_job.result()

    # Convert the results to a list of dictionaries
    rows = []
    for row in results:
        # Convert each row to a dictionary
        row_dict = dict(row.items())
        rows.append(row_dict)
        print("I am printint the row dict")
        print(row_dict)
    return rows


def write_data_bq(
    project_id: str, dataset_id: str, table_id: str, rows: List[Dict]
) -> List:
    """Writes nested data to a BigQuery table using a temporary file.

    Args:
        project_id (str): The Google Cloud Project ID.
        dataset_id (str): The BigQuery dataset ID.
        table_id (str): The BigQuery table ID.
        rows (list): A list of dictionaries, where each dictionary represents a row of data.
    """
    client = bigquery.Client(project_id)
    table_name = f"{dataset_id}.{table_id}"

    table = client.get_table(table_name)
    start = 0
    errors = []

    # Batch insert in chunks
    while start < len(rows):
        # Inserting in batches of 1000 to avoid hanging of insert operation
        end = min(start + 1000, len(rows))
        # Insert rows in the current batch
        batch_errors = client.insert_rows(table=table, rows=rows[start:end])

        # If there are any errors, append them
        if batch_errors:
            errors.extend(batch_errors)

        start = end

    # Return errors if there are any
    return errors if errors else []


def write_overall_metrics_bq(
    project_id: str, dataset_id: str, table_id: str, row: Dict
) -> Dict:
    """Writes overall metrics to a BigQuery table.

    Args:
        project_id (str): The Google Cloud Project ID.
        dataset_id (str): The BigQuery dataset ID.
        table_id (str): The BigQuery table ID.
        eval_result (dict): The dictionary containing evaluation metrics.

    Returns:
        List: A list of errors, if any, encountered during the insertion.
    """
    # Initialize BigQuery client
    client = bigquery.Client(project=project_id)

    # Define the BigQuery table
    table_name = f"{dataset_id}.{table_id}"
    table = client.get_table(table_name)

    # Create a list of rows to insert (in this case, it's a single row)
    row_to_insert = [row]

    # Insert the data into the table
    errors = client.insert_rows_json(table, row_to_insert)

    # Return errors if there are any
    return errors if errors else []


def fetch_candidate_tags(sql_query: str, project_id: str) -> Dict:
    client = bigquery.Client(project=project_id)
    sql_query = sql_query.format(project_id=project_id)

    query_job = client.query(sql_query)
    results = query_job.result()

    # Convert results to dictionary format
    dynamic_recipes: Dict = {}
    for row in results:
        tag_category = row.tag_category
        tag = row.tag

        if tag_category not in dynamic_recipes:
            dynamic_recipes[tag_category] = []

        dynamic_recipes[tag_category].append(tag)

    return {"categories": dynamic_recipes}

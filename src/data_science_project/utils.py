import importlib
import os
import pandas as pd


def read_sql_data() -> pd.DataFrame:
	"""Read source dataset from MySQL (if configured) or CSV fallback.

	Priority:
	1) MySQL table read when DB env vars are present.
	2) CSV path from DATA_SOURCE_PATH.
	3) notebook/data/raw.csv
	4) data/raw.csv
	"""
	mysql_host = os.environ.get("MYSQL_HOST")
	mysql_user = os.environ.get("MYSQL_USER")
	mysql_password = os.environ.get("MYSQL_PASSWORD")
	mysql_db = os.environ.get("MYSQL_DB")
	mysql_table = os.environ.get("MYSQL_TABLE", "students")

	if all([mysql_host, mysql_user, mysql_password, mysql_db]):
		try:
			pymysql = importlib.import_module("pymysql")

			connection = pymysql.connect(
				host=mysql_host,
				user=mysql_user,
				password=mysql_password,
				database=mysql_db,
				port=int(os.environ.get("MYSQL_PORT", "3306")),
			)
			try:
				return pd.read_sql_query(f"SELECT * FROM {mysql_table}", connection)
			finally:
				connection.close()
		except ModuleNotFoundError as exc:
			raise ModuleNotFoundError(
				"pymysql is required for MySQL ingestion. Install it or use CSV source."
			) from exc

	candidate_paths = [
		os.environ.get("DATA_SOURCE_PATH"),
		os.path.join("notebook", "data", "raw.csv"),
		os.path.join("data", "raw.csv"),
	]
	source_path = next((p for p in candidate_paths if p and os.path.exists(p)), None)

	if source_path is None:
		raise FileNotFoundError(
			"Raw data file not found. Add CSV at notebook/data/raw.csv or data/raw.csv, "
			"or set DATA_SOURCE_PATH, or configure MySQL env vars."
		)

	return pd.read_csv(source_path)

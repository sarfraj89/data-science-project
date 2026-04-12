from src.data_science_project.components.data_ingestion import DataIngestion


class TrainPipeline:
	def __init__(self):
		self.data_ingestion = DataIngestion()

	def run_pipeline(self):
		return self.data_ingestion.initiate_data_ingestion()

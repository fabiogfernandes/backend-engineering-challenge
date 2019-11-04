import json

class ResultsWriter:

	def __init__(self, results_file):
		self.results_file = results_file
		self.file_ref = open(self.results_file, "w")

	def write_result(self, result):
		self.file_ref.write(json.dumps(result) + "\n")

	def close(self):
		self.file_ref.close()
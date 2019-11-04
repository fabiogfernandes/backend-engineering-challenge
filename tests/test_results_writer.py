import sys, os
import json

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

from results_writer import ResultsWriter as rw

# Test object and file creation
def test_init():
	filename = "./tests/data/test.json"
	results_writer = rw(filename)
	results_writer.close()
	assert results_writer.results_file == filename and os.path.isfile(filename)

# Write two events and read them from file and test if they exist
def test_write_result():
	filename = "./tests/data/test.json"
	test_event1 = {"date": "2018-12-26 18:11:00", "average_delivery_time": 0}
	test_event2 = {"date": "2018-12-26 18:12:00", "average_delivery_time": 20}
	results_writer = rw(filename)
	results_writer.write_result(test_event1)
	results_writer.write_result(test_event2)
	results_writer.close()
	assert True
	with open(filename) as file_reader:
		event1 = json.loads(file_reader.readline())
		event2 = json.loads(file_reader.readline())

	assert test_event1 == event1 and test_event2 == event2


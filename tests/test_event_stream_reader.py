import sys, os
import json

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

from event_stream_reader import EventStreamReader as evs

def test_event_missing_duration():
	event = {"timestamp": "2018-12-26 18:11:00.000000", "translation_id": "5aa5b2f39f7254a75aa5"}
	res = evs.is_translation_event(event)
	assert res == False

def test_event_malformed_duration():
	event = {"timestamp": "2018-12-26 18:11:00.000000", "duration":"text", "translation_id": "5aa5b2f39f7254a75aa5"}
	res = evs.is_translation_event(event)
	assert res == False

def test_event_missing_timestamp():
	event = {"duration": 10, "translation_id": "5aa5b2f39f7254a75aa5"}
	res = evs.is_translation_event(event)
	assert res == False

def test_event_malformed_timestamp():
	event = {"timestamp": "text", "duration": 10, "translation_id": "5aa5b2f39f7254a75aa5"}
	res = evs.is_translation_event(event)
	assert res == False

def test_event_ok():
	event = {"timestamp": "2018-12-26 18:11:00.000000", "duration": 10, "translation_id": "5aa5b2f39f7254a75aa5"}
	res = evs.is_translation_event(event)
	assert res

def get_all_events(filename):
	reader = evs(filename)
	events = []
	for event in reader:
		events.append(event)

	return events

# First event in file has invalid JSON format and is discarded
def test_iterate_malformed_json():
	res_set = get_all_events("./tests/data/events_test_malformed.json")
	size_test = len(res_set) == 2
	first_valid = res_set[0]["translation_id"] == "5aa5b2f39f7254a75aa4"
	second_valid = res_set[1]["translation_id"] == "5aa5b2f39f7254a75bb33"
	assert size_test and first_valid and second_valid

# Two first events missing necessary fields for timeslot average calculation
def test_iterate_invalid_translation_event():
	res_set = get_all_events("./tests/data/events_test_missing_fields.json")
	size_test = len(res_set) == 1
	first_valid = res_set[0]["translation_id"] == "5aa5b2f39f7254a75bb33"
	assert size_test and first_valid

# Event set from example
def test_iterate_all_events_ok():
	res_set = get_all_events("./tests/data/events_test.json")
	size_test = len(res_set) == 3
	first_valid = res_set[0]["translation_id"] == "5aa5b2f39f7254a75aa5"
	second_valid = res_set[1]["translation_id"] == "5aa5b2f39f7254a75aa4"
	third_valid = res_set[2]["translation_id"] == "5aa5b2f39f7254a75bb33"
	assert size_test and first_valid and second_valid and third_valid

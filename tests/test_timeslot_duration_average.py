import sys, os
import pytest
from datetime import datetime, timedelta

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

from timeslot_duration_average import TimeslotDurationAverage as tsa

def test_init():
	dt = datetime.strptime("2018-12-26 18:11:00.000000", "%Y-%m-%d %H:%M:%S.%f")
	window_size = 2
	calculator = tsa(dt, window_size)
	assert calculator.window_size == 2 and calculator.current_timeslot == dt

def test_beginning_period():
	dt = datetime.strptime("2018-12-26 18:11:25.000000", "%Y-%m-%d %H:%M:%S.%f")
	dt_beginning_minute = datetime(2018, 12, 26, 18, 11)
	dt_res = tsa.beginning_period(dt)
	assert dt_beginning_minute == dt_res

def test_next_timeslot():
	dt = datetime.strptime("2018-12-26 18:11:00.000000", "%Y-%m-%d %H:%M:%S.%f")
	window_size = 2
	calculator = tsa(dt, window_size)
	calculator.next_timeslot()
	next_minute = datetime(2018, 12, 26, 18, 12)
	assert calculator.current_timeslot == next_minute

def test_to_datetime_valid():
	date_str = "2018-12-26 18:11:00.000000"
	dt_test = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S.%f")
	res = tsa.to_datetime(date_str)
	assert dt_test == res

def test_to_datetime_invalid():
	date_str = "ola"
	res = tsa.to_datetime(date_str)
	assert res == None

def test_datetime_to_str_valid():
	date_str = "2018-12-26 18:11:00.000000"
	dt_test = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S.%f")
	res = tsa.datetime_to_str(dt_test)
	assert res == date_str

def test_datetime_to_str_invalid():
	with pytest.raises(TypeError, match=r".* object but received a .*") :
		res = tsa.datetime_to_str(1)

def test_add_event():
	dt = datetime.strptime("2018-12-26 18:11:00.000000", "%Y-%m-%d %H:%M:%S.%f")
	window_size = 2
	calculator = tsa(dt, window_size)
	event = {"timestamp": "2018-12-26 18:23:19.903159", "translation_id": "5aa5b2f39f7254a75bb33", "duration": 54}
	calculator.add_event(event)
	assert len(calculator.events_window) == 1 and calculator.events_window[0]["translation_id"] == "5aa5b2f39f7254a75bb33"

def test__refresh_events_window():
	event1 = {"timestamp": "2018-12-26 18:15:19.903159", "translation_id": "5aa5b2f39f7254a75aa4", "duration": 31}
	event2 = {"timestamp": "2018-12-26 18:18:00.000000", "translation_id": "5aa5b2f39f7254a75aa3", "duration": 31}
	event3 = {"timestamp": "2018-12-26 18:23:00.000000", "translation_id": "5aa5b2f39f7254a75aa5", "duration": 20}
	dt = datetime.strptime("2018-12-26 18:20:00.000000", "%Y-%m-%d %H:%M:%S.%f")
	window_size = 2
	calculator = tsa(dt, window_size)
	calculator.add_event(event1)
	calculator.add_event(event2)
	calculator.add_event(event3)
	# Erases first 2 events because they are out of window for average calculation
	calculator._refresh_events_window()
	assert len(calculator.events_window) == 1 and calculator.events_window[0]["translation_id"] == "5aa5b2f39f7254a75aa5"

def test_calculate_average():
	event1 = {"timestamp": "2018-12-26 18:15:19.903159", "translation_id": "5aa5b2f39f7254a75aa4", "duration": 31}
	event2 = {"timestamp": "2018-12-26 18:18:01.000000", "translation_id": "5aa5b2f39f7254a75aa6", "duration": 30}
	event3 = {"timestamp": "2018-12-26 18:19:00.000000", "translation_id": "5aa5b2f39f7254a75aa3", "duration": 20}
	event4 = {"timestamp": "2018-12-26 18:23:00.000000", "translation_id": "5aa5b2f39f7254a75aa5", "duration": 20}
	dt = datetime.strptime("2018-12-26 18:20:00.000000", "%Y-%m-%d %H:%M:%S.%f")
	window_size = 2
	calculator = tsa(dt, window_size)
	calculator.add_event(event1)
	calculator.add_event(event2)
	calculator.add_event(event3)
	calculator.add_event(event4)
	# First event is removed because it is out of the window and last event is not considered because it surpasses current_timeslot
	# Average between events 2 and 3 = 50 / 2
	res = calculator.calculate_average()
	assert res == 25

def test_calculate_average_empty():
	dt = datetime.strptime("2018-12-26 18:20:00.000000", "%Y-%m-%d %H:%M:%S.%f")
	window_size = 2
	calculator = tsa(dt, window_size)
	res = calculator.calculate_average()
	assert res == 0











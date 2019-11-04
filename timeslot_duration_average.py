from datetime import datetime, timedelta

class TimeslotDurationAverage:

	def __init__(self, current_timeslot, window_size):
		self.current_timeslot = current_timeslot
		self.window_size = window_size
		self.events_window = []

	# Set date to beginning of minute
	def beginning_period(date):
		return datetime(date.year, date.month, date.day, date.hour, date.minute)

	# Advance current timesplot in one minute
	def next_timeslot(self):
		self.current_timeslot += timedelta(minutes=1)

	# Convert string to datetime object in the format used in the examples
	def to_datetime(str):
		try:
			dt = datetime.strptime(str, "%Y-%m-%d %H:%M:%S.%f")
		except ValueError:
			dt = None

		return dt

	# Convert datetime object to string format used in the examples
	def datetime_to_str(date):
		return datetime.strftime(date, "%Y-%m-%d %H:%M:%S.%f")

	# Add translation event to the events window
	def add_event(self, event):
		self.events_window.append(event)

	# Clean old events from events window assuming list is ordered 
	def _refresh_events_window(self):
		i = 0
		# find index of events older than current timeslot minus window_size
		while i < len(self.events_window) and \
			TimeslotDurationAverage.to_datetime(self.events_window[i]['timestamp']) <= (self.current_timeslot - timedelta(minutes=self.window_size)):
			i += 1

		self.events_window = self.events_window[i:]
		return self.events_window

	# Calculate translation duration average with events inside the window
	def calculate_average(self):
		self._refresh_events_window()
		sum = 0
		count = 0
		for event in self.events_window:
			if TimeslotDurationAverage.to_datetime(event['timestamp']) <= self.current_timeslot:
				sum += event['duration']
				count += 1

		# Return average 0 if there are no events
		if count == 0:
			return 0
		else:
			return sum / count

import json

from timeslot_duration_average import TimeslotDurationAverage as tsa

# Iterator class to read JSON events from file (JSON lines format)
class EventStreamReader:
	def __init__(self, filepath):
		self.filepath = filepath
		self.file_ref = open(self.filepath)

	def __iter__(self):
		return self

	# Test if event has fields necessary to calculate timeslot average
	def is_translation_event(event):

		duration = event.get('duration')
		timestamp = event.get('timestamp')
		if duration and timestamp:
			if isinstance(duration, int) and tsa.to_datetime(timestamp):
				return True

		return False

	def __next__(self):

		event = None
		# Read next valid event until end of file
		while event == None:
			try:
				line = self.file_ref.readline()
				if line == "": #End of file
					self.file_ref.close()
					raise StopIteration

				event = json.loads(line)
				if not EventStreamReader.is_translation_event(event):
					raise ValueError
			except ValueError:
				event = None
		return event
import click

from event_stream_reader import EventStreamReader
from timeslot_duration_average import TimeslotDurationAverage as tsa
from results_writer import ResultsWriter

@click.command()
@click.option("--input_file", type=click.Path(exists=True), help="File in JSON format to read translation events (must exists).")
@click.option("--window_size", type=click.IntRange(1, 60), help="Average window size in minutes.")
@click.option("--output_file", type=click.Path(), help="File to store the translation average info.")

def process_events(input_file, window_size, output_file):
	reader = EventStreamReader(input_file)

	calculator = None

	writer = ResultsWriter(output_file)

	for event in reader:
		event_ts = tsa.to_datetime(event["timestamp"])
		# initial case for first average
		if calculator == None:
			start_timeslot = tsa.beginning_period(event_ts)
			calculator = tsa(start_timeslot, window_size)

		# calculate all average timeslots until next event timeslot
		while event_ts > calculator.current_timeslot:
			current_ts = tsa.datetime_to_str(calculator.current_timeslot)
			average = calculator.calculate_average()
			result = {"date": current_ts, "average_delivery_time": average}
			writer.write_result(result)
			calculator.next_timeslot()

		calculator.add_event(event)

	# Last timeslot if needed
	if calculator and calculator.current_timeslot >= event_ts:
		average = calculator.calculate_average()
		current_ts = tsa.datetime_to_str(calculator.current_timeslot)
		result = {"date": current_ts, "average_delivery_time": average}
		writer.write_result(result)

	writer.close()

if __name__ == "__main__":
	process_events()
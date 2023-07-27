import time

def _print_progress(total_runs: int, run_number: int, start_time: int, end: str = '\r'):
	print(f"Completed {run_number} out of {total_runs} simulations. Elapsed time: {_format_elapsed_time(start_time)}", end=end)

def _format_elapsed_time(start_time: int):
	elapsed_seconds = int(time.time()) - start_time

	if elapsed_seconds > 60 * 60:
		hours, minutes = divmod(elapsed_seconds, 60 * 60)
		minutes, seconds = divmod(minutes, 60)
		return f"{hours}h {minutes}m {seconds}s"

	elif elapsed_seconds > 60:
		minutes, seconds = divmod(elapsed_seconds, 60)
		return f"{minutes}m {seconds}s"

	else:
		return f"{elapsed_seconds}s"
"""Utility functions for the simulation common module.

Functions for displaying the simulation progress and formatting the output are exported.

Exported functions:
- `_print_progress()`
- `_format_elapsed_time()`

See individual functions for further documentation.
"""

import time

def _print_progress(total_runs: int, completed_sims: int, failed_sims: int, start_time: int, end: str = '\r'):
	"""Displays the simulation progress.

	Displays the number of simulations completed, total simulations and the time elapsed.
	"""
	print(f"Completed: {completed_sims}. Failed: {failed_sims}. Total: {total_runs}. Elapsed time: {_format_elapsed_time(start_time)}{f'. Average: {_format_elapsed_time(start_time, completed_sims)} per simulation.' if completed_sims > 0 else ''}", end=end)

def _format_elapsed_time(start_time: int, divisor: int = 1):
	"""Formats the elapsed time (in seconds) into hours, minutes, and seconds format.
	"""
	elapsed_seconds = int((int(time.time()) - start_time) / divisor)

	if elapsed_seconds > 60 * 60:
		hours, minutes = divmod(elapsed_seconds, 60 * 60)
		minutes, seconds = divmod(minutes, 60)
		return f"{hours}h {minutes}m {seconds}s"

	elif elapsed_seconds > 60:
		minutes, seconds = divmod(elapsed_seconds, 60)
		return f"{minutes}m {seconds}s"

	else:
		return f"{elapsed_seconds}s"
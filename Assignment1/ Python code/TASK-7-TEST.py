import importlib.util

spec = importlib.util.spec_from_file_location("task7", "TASK-7.py")
task7 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(task7)

print("Using TASK-7.py")
print("Rate:", task7.rate_per_litre(4.2, 8.7))
print("Payout:", task7.payout(8.5, 4.2, 8.7))
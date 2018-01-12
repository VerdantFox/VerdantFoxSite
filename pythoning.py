import datetime

new_time = datetime.datetime.now(tz=datetime.timezone.utc)
print(new_time)

old_time = datetime.datetime(
    2018, 1, 11, 6, 10, 5, 123456, tzinfo=datetime.timezone.utc)
print(old_time)

time_delta = new_time - old_time
print(time_delta)

if time_delta < datetime.timedelta(hours=17):
    print(True)
else:
    print(False)
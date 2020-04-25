import datetime
from datetime import timezone
UTC_datetime = datetime.datetime.utcnow()
UTC_datetime_timestamp = float(UTC_datetime.strftime("%s"))
local_datetime_converted = datetime.datetime.fromtimestamp(UTC_datetime_timestamp)


print(local_datetime_converted)

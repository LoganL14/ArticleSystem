from datetime import datetime, timedelta
from zoneinfo import ZoneInfo



# Get current time in Los Angeles
tz = ZoneInfo("UTC")
now_time = datetime.now(tz)
twodaysago_time= now_local - timedelta(days = 2)
#print(now_local)


#convert to UTC time
start_utc = now_time.astimezone(ZoneInfo("GMT"))
end_utc   = twodaysago_time.astimezone(ZoneInfo("GMT"))
#print(start_utc, end_utc)


#format for query
fmt = "%Y%m%d%H%M"

start_utc_formatted =  start_utc.strftime(start_utc)
end_utc_formatted =  end_utc.strftime(end_utc)
print(start_utc_formatted)
print(end_utc_formatted)




# start_local = datetime(now_local.year, now_local.month, now_local.day, 0, 0, tzinfo=tz)
# end_local = start_local + timedelta(days=1)


# # Convert to UTC for arXiv query
# start_utc = start_local.astimezone(ZoneInfo("UTC"))
# end_utc = end_local.astimezone(ZoneInfo("UTC"))


# # Format for query
# fmt = "%Y%m%d%H%M"
# time = f"submittedDate:[{start_utc.strftime(fmt)} TO {end_utc.strftime(fmt)}]"


# query = f"all:technology AND {time}"

# print(query)
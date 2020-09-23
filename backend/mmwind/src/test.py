from env.sol import env

import datetime
import pytz



local_time = datetime.datetime.now()
print(f'Local Time {local_time}')
local_time = local_time.replace(tzinfo=pytz.timezone(env['timezone']))

print(f'Local Time TZ {local_time}')
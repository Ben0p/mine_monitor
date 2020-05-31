

import pymssql
import json
import datetime
import time


cnxn = pymssql.connect(
    server = "SOLOPSRS02",
    port = 1433,
    user = "svc.sol.wind@SOLOPSRS02",
    password = "5U!Y7$gaxS!NVnO78l$c"
)

cursor = cnxn.cursor()

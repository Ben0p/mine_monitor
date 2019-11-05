import time



eight_hours = time.time() + 28800

formatted = time.strftime('%d/%m/%Y %X', time.localtime(eight_hours))

print(formatted)
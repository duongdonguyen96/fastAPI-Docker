import os
print('______________________')
DB_CONFIG = {
    "host": os.getenv("HOST"),
    "port": os.getenv("PORT"),
    "user_name": os.getenv("USER_NAME"),
    "password": os.getenv("PASSWORD"),
    "service_name": os.getenv("SERVICE_NAME")
}

print('______________')
print(DB_CONFIG)
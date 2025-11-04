#!/usr/bin/python3
import seed
from itertools import islice

stream_users = __import__("0-stream_users")  

# insert data first
connection = seed.connect_to_prodev()
seed.insert_data(connection, "data.csv")
connection.close()

# iterate over the generator and print only the first 6 rows
for user in islice(stream_users.stream_users(), 6):
    print(user)


from itertools import islice
import pagination_users

# Fetch pages of 5 users
for page in pagination_users.lazy_pagination(5):
    for user in page:
        print(user)

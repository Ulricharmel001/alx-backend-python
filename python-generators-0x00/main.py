#!/usr/bin/python3
from itertools import islice
stream_users = __import__('0-stream_users')

# iterate over the generator and print only the first 6 rows
for user in islice(stream_users.stream_users(), 6):
    print(user)


from lazy_paginate import lazy_pagination
for page in lazy_pagination(100):
    for user in page:
        print(user)

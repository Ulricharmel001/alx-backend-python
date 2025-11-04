#!/usr/bin/python3
seed = __import__('seed')

def paginate_users(page_size, offset):
    """
    Fetch a page of users from the database starting at offset.
    Returns a list of dictionaries.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM user_data ORDER BY user_id LIMIT %s OFFSET %s",
        (page_size, offset)
    )
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows


def lazy_pagination(page_size):
    """
    Generator to lazily fetch users page by page.
    Yields one page (list of dictionaries) at a time.
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:  # stop when no more rows
            break
        yield page
        offset += page_size

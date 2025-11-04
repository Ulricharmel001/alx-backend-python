# File: 1-batch_processing.py
#!/usr/bin/python3
seed = __import__('seed')


def stream_users_in_batches(batch_size):
    """
    Generator function to fetch users in batches from the database.
    """
    offset = 0

    while True:
        connection = seed.connect_to_Alx_prodev()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM user_data LIMIT {batch_size} OFFSET {offset}")
        batch = cursor.fetchall()
        connection.close()

        if not batch:  # Stop iteration if no more data
            break

        # Yield the batch without using return
        yield batch
        offset += batch_size


def batch_processing(batch_size):
    """
    Processes each batch and prints users over the age of 25.
    """
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user["age"] > 25:
                print(user)
    
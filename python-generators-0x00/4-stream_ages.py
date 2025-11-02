#!/usr/bin/env python3
def stream_user_ages():
    """
    Generator function that yields user ages one by one.
    Replace the sample data with your actual dataset if needed.
    """
    users = [
        {"name": "Alice", "age": 25},
        {"name": "Bob", "age": 30},
        {"name": "Charlie", "age": 22},
        {"name": "David", "age": 35},
        {"name": "Eve", "age": 28},
    ]
    
    for user in users:
        yield user["age"]


def calculate_average_age():
    total_age = 0
    count = 0

    # Use only one loop over the generator
    for age in stream_user_ages():
        total_age += age
        count += 1

    average = total_age / count if count > 0 else 0
    print(f"Average age of users: {average:.2f}")


if __name__ == "__main__":
    calculate_average_age()

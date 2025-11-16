# Unit Testing `access_nested_map`

This project contains a simple Python utility function, `access_nested_map`, and its corresponding unit tests using `unittest` and `parameterized`.

## Overview

- `utils.py`: Implements `access_nested_map` to access nested dictionaries via a path of keys.
- `test_utils.py`: Contains unit tests for `access_nested_map` including:
  - Normal cases where the function returns the expected value.
  - Exception cases where a `KeyError` is raised for invalid paths.

## How to Run Tests

1. Install dependencies:
```bash
pip install parameterized

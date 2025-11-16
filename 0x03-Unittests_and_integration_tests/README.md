# Unit Testing `access_nested_map`

This project contains a Python utility function, `access_nested_map`, and its corresponding unit and integration tests using `unittest` and `parameterized`.

## Overview

- `utils.py`: Implements `access_nested_map`, `get_json`, and `memoize`.
- `test_utils.py`: Contains tests for:
  - `access_nested_map`: normal and exception cases.
  - `get_json`: mocked HTTP calls.
  - `memoize`: ensures caching works as expected.

## How to Run Tests

1. Install dependencies:
```bash
pip install parameterized

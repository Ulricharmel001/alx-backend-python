#!/usr/bin/env python3
import unittest
from unittest.mock import patch
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize

class TestAccessNestedMap(unittest.TestCase):
    """Tests for access_nested_map."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Check correct value returned."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Check KeyError raised for invalid path."""
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)

class TestGetJson(unittest.TestCase):
    """Tests for get_json."""
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"value": 1}),
    ])
    def test_get_json(self, url, expected_payload):
        """Mock requests.get and check JSON returned."""
        with patch("utils.requests.get") as mock_get:
            mock_get.return_value.json.return_value = expected_payload
            self.assertEqual(get_json(url), expected_payload)
            mock_get.assert_called_once_with(url)

class TestMemoize(unittest.TestCase):
    """Tests for memoize decorator."""
    def test_memoize(self):
        """Check method result cached and called once."""
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        instance = TestClass()
        with patch.object(TestClass, "a_method", return_value=42) as mock_method:
            value1 = instance.a_property
            value2 = instance.a_property
            self.assertEqual(value1, 42)
            self.assertEqual(value2, 42)
            mock_method.assert_called_once()


class TestGetJsonIntegration(unittest.TestCase):
    """Integration test for get_json."""

    @patch("utils.requests.get")
    def test_get_json_integration(self, mock_get):
        """Check full JSON flow with mock."""
        expected_data = {"name": "Holberton", "status": "active"}
        mock_get.return_value.json.return_value = expected_data
        result = get_json("http://fakeurl.com/api")
        self.assertEqual(result, expected_data)
        mock_get.assert_called_once_with("http://fakeurl.com/api")

if __name__ == "__main__":
    unittest.main()

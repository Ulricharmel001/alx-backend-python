#!/usr/bin/env python3
"""Unit and integration tests for client.py."""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD

# Extract data from TEST_PAYLOAD
first_payload = TEST_PAYLOAD[0]
org_payload = first_payload[0]
repos_payload = first_payload[1]

# Prepare expected outputs
expected_repos = [repo["name"] for repo in repos_payload]
apache2_repos = [
    repo["name"] for repo in repos_payload
    if repo.get("license") and repo["license"].get("key") == "bsd-3-clause"
]


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that org property returns correct JSON payload."""
        mock_get_json.return_value = {"key": "value"}
        client = GithubOrgClient(org_name)
        result = client.org
        self.assertEqual(result, {"key": "value"})
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    def test_public_repos_url(self):
        """Test _public_repos_url property returns the org repos URL."""
        client = GithubOrgClient("google")
        with patch.object(
            GithubOrgClient, "org", new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = {"repos_url": "https://api.github.com/orgs/google/repos"}
            self.assertEqual(
                client._public_repos_url, "https://api.github.com/orgs/google/repos"
            )

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test public_repos returns repo names, optionally filtered by license."""
        mock_get_json.return_value = repos_payload
        client = GithubOrgClient("google")
        with patch.object(
            GithubOrgClient, "_public_repos_url", new_callable=PropertyMock
        ) as mock_url:
            mock_url.return_value = "https://api.github.com/orgs/google/repos"
            self.assertEqual(client.public_repos(), [repo["name"] for repo in repos_payload])
            self.assertEqual(client.public_repos(license="bsd-3-clause"), apache2_repos)
            mock_get_json.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license static method."""
        self.assertEqual(GithubOrgClient.has_license(repo, license_key), expected)


@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos."""

    @classmethod
    def setUpClass(cls):
        """Patch get_json for integration tests."""
        patcher = patch("client.get_json")  # store patch object locally
        cls.mock_get = patcher.start()      # start patching, get mock object
        cls.patcher = patcher                # store patcher to stop later

        # Return org_payload for org URL, repos_payload for repos URL
        def side_effect(url):
            if url == cls.org_payload["repos_url"]:
                return cls.repos_payload
            return cls.org_payload

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patching."""
        cls.patcher.stop()

    def test_public_repos(self):
        """Test that public_repos returns all repo names."""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test that public_repos filters repos by license key."""
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos(license="bsd-3-clause"), self.apache2_repos
        )


if __name__ == "__main__":
    unittest.main()

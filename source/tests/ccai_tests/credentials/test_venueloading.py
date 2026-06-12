"""
    Unit tests for venue-credential loading through the public
    :meth:`CredentialManager.load_credentials` path, and for the secret-safe
    serialization helpers (``as_redacted_dict`` / ``__repr__``).

    These cover the surfaces that previously hid two release blockers: venue
    credentials silently dropped by the manager, and plaintext secrets leaking
    through serialization.
"""

import unittest

from ccai.errors.exceptions import ConfigurationError

from ccai.credentials.basecredential import REDACTED_PLACEHOLDER
from ccai.credentials.basiccredential import BasicCredential
from ccai.credentials.awsaccesskeycredential import AwsAccessKeyCredential
from ccai.credentials.credentialmanager import CredentialManager
from ccai.credentials.digitaloceanapitokencredential import DigitalOceanApiTokenCredential


class TestVenueCredentialLoading(unittest.TestCase):
    """
        Verify venue credentials load via the public manager path using the
        ``provider`` discriminator (previously silently dropped).
    """

    def test_cloud_venue_credential_with_provider_loads(self) -> None:
        cm = CredentialManager()
        cm.load_credentials({"credentials": [
            {"identifier": "do1", "category": "cloud-venue", "provider": "digitalocean", "token": "dop_v1_xyz"}
        ]})
        self.assertIn("do1", cm.credentials)
        cred = cm.credentials["do1"]
        self.assertIsInstance(cred, DigitalOceanApiTokenCredential)
        self.assertEqual(cred.token, "dop_v1_xyz")
        return

    def test_venue_credential_missing_provider_raises(self) -> None:
        cm = CredentialManager()
        with self.assertRaises(ConfigurationError):
            cm.load_credentials({"credentials": [
                {"identifier": "do2", "category": "cloud-venue", "token": "dop_v1_abc"}
            ]})
        return

    def test_venue_credential_unknown_provider_raises(self) -> None:
        cm = CredentialManager()
        with self.assertRaises(ConfigurationError):
            cm.load_credentials({"credentials": [
                {"identifier": "x1", "category": "cloud-venue", "provider": "not-a-provider", "token": "t"}
            ]})
        return

    def test_truly_unknown_category_raises_not_silently_dropped(self) -> None:
        cm = CredentialManager()
        with self.assertRaises(ConfigurationError):
            cm.load_credentials({"credentials": [
                {"identifier": "weird", "category": "no-such-category", "token": "t"}
            ]})
        return

    def test_loaded_venue_credential_is_findable_by_category(self) -> None:
        cm = CredentialManager()
        cm.load_credentials({"credentials": [
            {"identifier": "do3", "category": "cloud-venue", "provider": "digitalocean", "token": "dop_v1_q"}
        ]})
        matches = cm.get_credentials_by_categories(categories=["cloud-venue"])
        identifiers = [c.identifier for c in matches]
        self.assertIn("do3", identifiers)
        return


class TestRedactedSerialization(unittest.TestCase):
    """
        Verify the secret-safe serialization surfaces redact secret material while
        ``as_dict`` retains full data for round-tripping.
    """

    def test_as_redacted_dict_masks_password(self) -> None:
        cred = BasicCredential(identifier="b1", categories=["basic"], username="user", password="SUPERSECRET")
        redacted = cred.as_redacted_dict()
        self.assertEqual(redacted["password"], REDACTED_PLACEHOLDER)
        self.assertEqual(redacted["username"], "user")  # non-secret preserved
        self.assertNotIn("SUPERSECRET", str(redacted))
        return

    def test_as_redacted_dict_masks_secret_field(self) -> None:
        cred = AwsAccessKeyCredential(identifier="a1", categories=["aws-access-key"], keyid="AKIA", secret="TOPSECRETKEY")
        redacted = cred.as_redacted_dict()
        self.assertEqual(redacted["secret"], REDACTED_PLACEHOLDER)
        self.assertEqual(redacted["keyid"], "AKIA")
        return

    def test_as_dict_still_carries_secret_for_round_trip(self) -> None:
        cred = BasicCredential(identifier="b2", categories=["basic"], username="user", password="pw")
        data = cred.as_dict()
        self.assertEqual(data["password"], "pw")
        rebuilt = BasicCredential(**data)
        self.assertEqual(rebuilt.as_dict(), data)
        return

    def test_repr_does_not_leak_secret_for_legacy_class(self) -> None:
        cred = BasicCredential(identifier="b3", categories=["basic"], username="user", password="SUPERSECRET")
        text = repr(cred)
        self.assertNotIn("SUPERSECRET", text)
        self.assertIn(REDACTED_PLACEHOLDER, text)
        return


if __name__ == "__main__":
    unittest.main()

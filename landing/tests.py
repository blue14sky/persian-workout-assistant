from django.test import TestCase
from django.urls import reverse

from .models import EarlyAccessSignup


class LandingTests(TestCase):
    def test_landing_renders(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "فیتو")

    def test_health_stays_healthy(self):
        self.assertEqual(self.client.get("/health/").json(), {"status": "ok"})

    def test_manifest(self):
        response = self.client.get("/manifest.webmanifest")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["display"], "standalone")

    def test_signup_requires_consent(self):
        response = self.client.post("/join/", {"email": "sample@example.com"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(EarlyAccessSignup.objects.count(), 0)

    def test_signup_creates_one_entry(self):
        payload = {"email": "SAMPLE@example.com", "consent": "yes"}
        self.client.post("/join/", payload)
        self.client.post("/join/", payload)
        self.assertEqual(EarlyAccessSignup.objects.count(), 1)
        self.assertEqual(EarlyAccessSignup.objects.first().email, "sample@example.com")

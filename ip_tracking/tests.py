from django.test import TestCase, Client
from .models import RequestLog

class MiddlewareTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_ip_logging_middleware_creates_log(self):
        self.client.get("/test-url/")
        self.assertEqual(RequestLog.objects.count(), 1)
        log = RequestLog.objects.first()
        self.assertEqual(log.path, "/test-url/")
        self.assertTrue(log.ip_address)

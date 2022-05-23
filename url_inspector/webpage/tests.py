from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from webpage.extractor import LinkExtractor
from django.test import Client


class WebPageTestCase(TestCase):

    def test_extractor(self):
        extractor = LinkExtractor()
        result = extractor.extract("http://www.google.com")
        self.assertEqual(result["total"], 5)

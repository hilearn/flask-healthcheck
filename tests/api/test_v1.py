import unittest
from api.app import app
from store.models import GreetingType


class V2Tester(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.app_context().push()
        cls.client = app.test_client()

    def test_get_greet(self):
        resp = self.client.get(
            '/v1/greet',
            query_string={'greeting_type': GreetingType.FORMAL.value})
        self.assertEqual(resp.status_code, 200)
        self.assertDictEqual(resp.json,
                             {'category': 'formal', 'reply_msg': 'Hello'})

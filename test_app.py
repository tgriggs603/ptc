
from flask import Flask, request, jsonify
from werkzeug import exceptions
from unittest import mock
from dns.resolver import NoAnswer, NXDOMAIN, NoNameservers, Timeout, Answer
import app
import unittest

class TestApp(unittest.TestCase):

    def setup(self):
        app.flask_app.config['TESTING'] = True
        self.app = app.flask_app.Flask(__name__)

    def test_answer_split(self):
        with mock.patch('dns.resolver.query') as query:
            query.answer = "10 mail2.example.com"
            self.assertEqual(query.answer.split(' '),["10", "mail2.example.com"])

    def test_get_no_answer(self):
        with mock.patch('dns.resolver.query') as query:
            query.side_effect = NoAnswer()
            with app.flask_app.test_client() as client:
                response = client.get('/mxrecords/example.com')
                json_data = response.get_json()
                self.assertEqual(json_data['exception'], 'NoAnswer -- mx record not found')
                self.assertEqual(response.status_code, 500)
                self.assertRaises(exceptions.InternalServerError)
                
    def test_get_nxdomain_exception(self):
        with mock.patch('dns.resolver.query') as query:
            query.side_effect = NXDOMAIN()
            with app.flask_app.test_client() as client:
                response = client.get('/mxrecords/example.com')
                json_data = response.get_json()
                self.assertEqual(json_data['exception'], 'NXDOMAIN Exception -- mx record not found')
                self.assertEqual(response.status_code, 500)
                self.assertRaises(exceptions.InternalServerError)

    def test_get_timeout_exception(self):
        with mock.patch('dns.resolver.query') as query:
            query.side_effect = Timeout()
            with app.flask_app.test_client() as client:
                response = client.get('/mxrecords/example.com')
                json_data = response.get_json()
                self.assertEqual(json_data['exception'], 'Timeout -- mx record not found')
                self.assertEqual(response.status_code, 500)
                self.assertRaises(exceptions.InternalServerError)

    def test_get_no_records(self):
        with mock.patch('dns.resolver.query') as query:
            query.return_value = []
            with app.flask_app.test_client() as client:
                response = client.get('/mxrecords/example.com')
                json_data = response.get_json()
                self.assertEqual(json_data['exception'], 'mx record not found')
                self.assertEqual(response.status_code, 404)
                self.assertRaises(exceptions.NotFound)

    def test_get_records(self):
        with mock.patch('dns.resolver.query') as query:
            query.return_value = ["10 mail2.example.com","20 mail3.example.com"]
            with app.flask_app.test_client() as client:
                response = client.get('/mxrecords/example.com')
                json_data = response.get_json()
                self.assertEqual(json_data['records'], [{'preference':'10','exchange':'mail2.example.com'},
                {'preference':'20','exchange':'mail3.example.com'}])
                self.assertEqual(response.status_code, 200)

    def test_post(self):
        with app.flask_app.test_client() as client:
            response = client.post('/mxrecords/')
            self.assertEqual(response.status_code, 400)
            self.assertRaises(exceptions.BadRequest)

    def test_put(self):
        with app.flask_app.test_client() as client:
            response = client.put('/mxrecords/')
            self.assertEqual(response.status_code, 400)
            self.assertRaises(exceptions.BadRequest)

    def test_delete(self):
        with app.flask_app.test_client() as client:
            response = client.delete('/mxrecords/')
            self.assertEqual(response.status_code, 400)
            self.assertRaises(exceptions.BadRequest)


if __name__ == '__main__':
    unittest.main()


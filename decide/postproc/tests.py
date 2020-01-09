from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from base import mods

import os 

class PostProcTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        mods.mock_query(self.client)

    def tearDown(self):
        self.client = None

    def test_identity(self):
        data = {
            'type': 'IDENTITY',
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 5 },
                { 'option': 'Option 2', 'number': 2, 'votes': 0 },
                { 'option': 'Option 3', 'number': 3, 'votes': 3 },
                { 'option': 'Option 4', 'number': 4, 'votes': 2 },
                { 'option': 'Option 5', 'number': 5, 'votes': 5 },
                { 'option': 'Option 6', 'number': 6, 'votes': 1 },
            ]
        }

        expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 5, 'postproc': 5 },
            { 'option': 'Option 5', 'number': 5, 'votes': 5, 'postproc': 5 },
            { 'option': 'Option 3', 'number': 3, 'votes': 3, 'postproc': 3 },
            { 'option': 'Option 4', 'number': 4, 'votes': 2, 'postproc': 2 },
            { 'option': 'Option 6', 'number': 6, 'votes': 1, 'postproc': 1 },
            { 'option': 'Option 2', 'number': 2, 'votes': 0, 'postproc': 0 },
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_weigth_gender(self):
        data = {
            'type': 'GENDER',
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 5, 'votesFemale': 2, 'votesMale': 3 },
                { 'option': 'Option 2', 'number': 2, 'votes': 53, 'votesFemale': 3, 'votesMale': 50 },
                { 'option': 'Option 3', 'number': 3, 'votes': 28, 'votesFemale': 10, 'votesMale': 14 },
                { 'option': 'Option 4', 'number': 4, 'votes': 68, 'votesFemale': 45, 'votesMale': 23 },
                { 'option': 'Option 5', 'number': 5, 'votes': 110, 'votesFemale': 63, 'votesMale': 47 },
                { 'option': 'Option 6', 'number': 6, 'votes': 70, 'votesFemale': 14, 'votesMale': 56 },
            ]
        }

        expected_result = [
            {'option': 'Option 1', 'number': 1, 'votes': 5, 'votesFemale': 2, 'votesMale': 3, 'postproc': 7},
            { 'option': 'Option 2', 'number': 2, 'votes': 53, 'votesFemale': 3, 'votesMale': 50, 'postproc': 56 },
            { 'option': 'Option 3', 'number': 3, 'votes': 28, 'votesFemale': 10, 'votesMale': 14, 'postproc': 34 },
            { 'option': 'Option 4', 'number': 4, 'votes': 68, 'votesFemale': 45, 'votesMale': 23, 'postproc': 113 },
            { 'option': 'Option 5', 'number': 5, 'votes': 110, 'votesFemale': 63, 'votesMale': 47, 'postproc': 173 },
            { 'option': 'Option 6', 'number': 6, 'votes': 70, 'votesFemale': 14, 'votesMale': 56, 'postproc': 84 },
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)


    def test_parity(self):
        data = {
            'type': 'PARITY',
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 5, 'gender' : 'F' },
                { 'option': 'Option 2', 'number': 2, 'votes': 0, 'gender' : 'F'  },
                { 'option': 'Option 3', 'number': 3, 'votes': 3, 'gender' : 'F'  },
                { 'option': 'Option 4', 'number': 4, 'votes': 2, 'gender' : 'M'  },
                { 'option': 'Option 5', 'number': 5, 'votes': 4, 'gender' : 'M'  },
                { 'option': 'Option 6', 'number': 6, 'votes': 1, 'gender' : 'M'  },
            ]
        }

        expected_result = [
            {'option': 'Option 1', 'number': 1, 'votes': 5, 'gender': 'F'},
            {'option': 'Option 5', 'number': 5, 'votes': 4, 'gender': 'M'},
            {'option': 'Option 3', 'number': 3, 'votes': 3, 'gender': 'F'},
            {'option': 'Option 4', 'number': 4, 'votes': 2, 'gender': 'M'},
            {'option': 'Option 6', 'number': 6, 'votes': 1, 'gender': 'M'},
            {'option': 'Option 2', 'number': 2, 'votes': 0, 'gender': 'F'},
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()


        self.assertEqual(values, expected_result)

    def test_county(self):
        data = {
            'type': 'COUNTY_EQUALITY',
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': {'41927': 1, '21002': 5} },
                { 'option': 'Option 2', 'number': 2, 'votes': {'41927': 20, '21002': 1} },
                { 'option': 'Option 3', 'number': 3, 'votes': {'41927': 15, '21002': 1} },
                { 'option': 'Option 4', 'number': 4, 'votes': {'41927': 25, '21002': 1} },
                { 'option': 'Option 5', 'number': 5, 'votes': {'41927': 30, '21002': 1} },
                { 'option': 'Option 6', 'number': 6, 'votes': {'41927': 9, '21002': 1} },
            ]
        }

        expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': {'41927': 1, '21002': 5}, 'postproc': 51 },
            { 'option': 'Option 5', 'number': 5, 'votes': {'41927': 30, '21002': 1}, 'postproc': 40 },
            { 'option': 'Option 4', 'number': 4, 'votes': {'41927': 25, '21002': 1}, 'postproc': 35 },
            { 'option': 'Option 2', 'number': 2, 'votes': {'41927': 20, '21002': 1}, 'postproc': 30 },
            { 'option': 'Option 3', 'number': 3, 'votes': {'41927': 15, '21002': 1}, 'postproc': 25 },
            { 'option': 'Option 6', 'number': 6, 'votes': {'41927': 9, '21002': 1}, 'postproc': 19 },
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()

        self.assertEqual(values, expected_result)

    def test_equalityProvince(self):
        data = {
            'type': 'EQUALITY_PROVINCE',
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': '50', 'postal_code': '41927' },
                { 'option': 'Option 2', 'number': 2, 'votes': '60', 'postal_code': '06005' },
                { 'option': 'Option 3', 'number': 3, 'votes': '50', 'postal_code': '41012' },
                { 'option': 'Option 4', 'number': 4, 'votes': '50', 'postal_code': '16812' },
                { 'option': 'Option 5', 'number': 5, 'votes': '40', 'postal_code': '10004' },
                { 'option': 'Option 6', 'number': 6, 'votes': '30', 'postal_code': '44001' },
            ]
        }

        expected_result = [
            { 'option': 'Option 2', 'number': 2, 'votes': '60', 'postal_code': '06005', 'postproc': 74},
            { 'option': 'Option 4', 'number': 4, 'votes': '50', 'postal_code': '16812', 'postproc': 72},
            { 'option': 'Option 5', 'number': 5, 'votes': '40', 'postal_code': '10004', 'postproc': 53},
            { 'option': 'Option 1', 'number': 1, 'votes': '50', 'postal_code': '41927', 'postproc': 52},
            { 'option': 'Option 3', 'number': 3, 'votes': '50', 'postal_code': '41012', 'postproc': 52},
            { 'option': 'Option 6', 'number': 6, 'votes': '30', 'postal_code': '44001', 'postproc': 44}
        ]


        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_equalityProvince_bad_data1(self):
        data = {
            'type': 'EQUALITY_PROVINCE',
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': '50' },
                { 'option': 'Option 2', 'number': 2, 'votes': '60' },
                { 'option': 'Option 3', 'number': 3, 'votes': '50' },
                { 'option': 'Option 4', 'number': 4, 'votes': '50' },
                { 'option': 'Option 5', 'number': 5, 'votes': '40' },
                { 'option': 'Option 6', 'number': 6, 'votes': '30' },
            ]
        }

        expected_result = [{'error': 'An exception occurred with equality province method'}]


        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_no_type_defined(self):
        data = {
            'type': '',
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': '50' },
                { 'option': 'Option 2', 'number': 2, 'votes': '60' },
                { 'option': 'Option 3', 'number': 3, 'votes': '50' },
                { 'option': 'Option 4', 'number': 4, 'votes': '50' },
                { 'option': 'Option 5', 'number': 5, 'votes': '40' },
                { 'option': 'Option 6', 'number': 6, 'votes': '30' },
            ]
        }

        expected_result = {}


        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_equalityProvince_bad_data2(self):
        data = {
            'type': 'EQUALITY_PROVINCE',
            'options': [
                { 'option': 'Option 1', 'number': 1 },
                { 'option': 'Option 2', 'number': 2},
                { 'option': 'Option 3', 'number': 3},
                { 'option': 'Option 4', 'number': 4},
                { 'option': 'Option 5', 'number': 5},
                { 'option': 'Option 6', 'number': 6},
            ]
        }

        expected_result = [{'error': 'An exception occurred with equality province method'}]


        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_equalityProvince_bad_data3(self):
        data = {
            'type': 'EQUALITY_PROVINCE',
            'options': [
                { 'option': 'Option 1'},
                { 'option': 'Option 2'},
                { 'option': 'Option 3'},
                { 'option': 'Option 4'},
                { 'option': 'Option 5'},
                { 'option': 'Option 6'},
            ]
        }

        expected_result = [{'error': 'An exception occurred with equality province method'}]


        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_equalityProvince_bad_data4(self):
     data = {
            'type': 'EQUALITY_PROVINCE',
            'options': [
                { 'option': 'Option 1', 'votes': '50' },
                { 'option': 'Option 2', 'number': 2, 'votes': '60' },
                { 'option': 'Option 3', 'number': 3,},
                { 'option': 'Option 4', 'number': 4, 'votes': '50' },
                { 'number': 5, 'votes': '40' },
                { 'option': '', 'number': 6, 'votes': '30' },
            ]
        }

        expected_result = [{'error': 'An exception occurred with equality province method'}]


        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)    

    def test_equalityProvince_bad_data5(self):
     data = {
            'type': 'EQUALITY_PROVINCE',
            'options': [
                { 'optiosdsn': 'Option 1', 'votes': '50' },
                { 'optifgfon': 'Option 2', 'number': 2, 'votsdfes': '60' },
                { 'optsdfion': 'Option 3', 'number': 3,},
                { 'optsdfion': 'Option 4', 'number': 4, 'vosdftes': '50' },
                { 'nusdfmber': 5, 'votes': '40' },
                { 'optsdfion': '', 'numgber': 6, 'votes': '30' },
            ]
        }

        expected_result = [{'error': 'An exception occurred with equality province method'}]


        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)       

   def test_equalityProvince_not_data(self):
        data = {}

        expected_result = [{'error': 'The Data is empty'}]


        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)






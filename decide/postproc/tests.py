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
                { 'option': 'Option 1', 'number': 1, 'votes': 5, 'votesFemale': 2, 'pondFemale': 2, 'votesMale': 3, 'pondMale': 3 },
                { 'option': 'Option 2', 'number': 2, 'votes': 53, 'votesFemale': 3, 'pondFemale': 1, 'votesMale': 50, 'pondMale': 5 },
                { 'option': 'Option 3', 'number': 3, 'votes': 28, 'votesFemale': 10, 'pondFemale': 5, 'votesMale': 14, 'pondMale': 2 },
                { 'option': 'Option 4', 'number': 4, 'votes': 68, 'votesFemale': 45, 'pondFemale': 4, 'votesMale': 23, 'pondMale': 1 },
                { 'option': 'Option 5', 'number': 5, 'votes': 110, 'votesFemale': 63, 'pondFemale': 3, 'votesMale': 47, 'pondMale': 1 },
                { 'option': 'Option 6', 'number': 6, 'votes': 70, 'votesFemale': 14, 'pondFemale': 4, 'votesMale': 56, 'pondMale': 3 },
            ]
        }

        expected_result = [
            {'option': 'Option 1', 'number': 1, 'votes': 5, 'votesFemale': 2, 'pondFemale': 2, 'votesMale': 3, 'pondMale': 3, 'postproc': 13},
            { 'option': 'Option 2', 'number': 2, 'votes': 53, 'votesFemale': 3, 'pondFemale': 1, 'votesMale': 50, 'pondMale': 5, 'postproc': 253 },
            { 'option': 'Option 3', 'number': 3, 'votes': 28, 'votesFemale': 10, 'pondFemale': 5, 'votesMale': 14, 'pondMale': 2, 'postproc': 78 },
            { 'option': 'Option 4', 'number': 4, 'votes': 68, 'votesFemale': 45, 'pondFemale': 4, 'votesMale': 23, 'pondMale': 1, 'postproc': 203 },
            { 'option': 'Option 5', 'number': 5, 'votes': 110, 'votesFemale': 63, 'pondFemale': 3, 'votesMale': 47, 'pondMale': 1, 'postproc': 236 },
            { 'option': 'Option 6', 'number': 6, 'votes': 70, 'votesFemale': 14, 'pondFemale': 4, 'votesMale': 56, 'pondMale': 3, 'postproc': 224 },
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_voter_age(self):
        data = {
            'type': 'AGERANGE',
            'options': [
                {'option': 'Option 1', 'number': 1, 'ageRange': {'18to27': 4, '28to37':0, '38to47': 1, '48to57':0, '58to67':0, '68to77':0, '78to87':0, '88to97':0}},

            ]
        }

        expected_result = [
            {'option': 'Option 1', 'number': 1, 'ageRange': {'18to27': 4, '28to37':0, '38to47': 1, '48to57':0, '58to67':0, '68to77':0, '78to87':0, '88to97':0}, 'postproc': 7},

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

    def test_county_simple(self):
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

    def test_county_oneCP(self):
        data = {
            'type': 'COUNTY_EQUALITY',
            'options': [
                {'option': 'Option 1', 'number': 1, 'votes': {'41927': 1}},
                {'option': 'Option 2', 'number': 2, 'votes': {'41927': 20}},
                {'option': 'Option 3', 'number': 3, 'votes': {'41927': 15}},
                {'option': 'Option 4', 'number': 4, 'votes': {'41927': 25}},
                {'option': 'Option 5', 'number': 5, 'votes': {'41927': 30}},
                {'option': 'Option 6', 'number': 6, 'votes': {'41927': 9}},
            ]
        }

        expected_result = [
            {'option': 'Option 5', 'number': 5, 'votes': {'41927': 30}, 'postproc': 30},
            {'option': 'Option 4', 'number': 4, 'votes': {'41927': 25}, 'postproc': 25},
            {'option': 'Option 2', 'number': 2, 'votes': {'41927': 20}, 'postproc': 20},
            {'option': 'Option 3', 'number': 3, 'votes': {'41927': 15}, 'postproc': 15},
            {'option': 'Option 6', 'number': 6, 'votes': {'41927': 9}, 'postproc': 9},
            {'option': 'Option 1', 'number': 1, 'votes': {'41927': 1}, 'postproc': 1},
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()

        self.assertEqual(values, expected_result)

    def test_county_random(self):
        data = {
            'type': 'COUNTY_EQUALITY',
            'options': [
                {'option': 'Option 1', 'number': 1, 'votes': {'41927': 25, '21002': 747, '11001': 823}},
                {'option': 'Option 2', 'number': 2, 'votes': {'41927': 3, '21002': 246, '11001': 103}},
                {'option': 'Option 3', 'number': 3, 'votes': {'41927': 442, '21002': 842, '11001': 679}},
                {'option': 'Option 4', 'number': 4, 'votes': {'41927': 870, '21002': 986, '11001': 999}},
            ]
        }

        expected_result = [
            {'option': 'Option 4', 'number': 4, 'votes': {'41927': 870, '21002': 986, '11001': 999} , 'postproc': 138 },
            {'option': 'Option 3', 'number': 3, 'votes': {'41927': 442, '21002': 842, '11001': 679}, 'postproc': 89 },
            {'option': 'Option 1', 'number': 1, 'votes': {'41927': 25, '21002': 747, '11001': 823}, 'postproc': 60},
            {'option': 'Option 2', 'number': 2, 'votes': {'41927': 3, '21002': 246, '11001': 103}, 'postproc': 13 },
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()

        self.assertEqual(values, expected_result)

    def test_hondt(self):
        data = {
            'type': 'HONDT',
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 5 },
                { 'option': 'Option 2', 'number': 2, 'votes': 0 },
                { 'option': 'Option 3', 'number': 3, 'votes': 3 },
               
            ],
             'nSeats': 5
        }

        expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 5, 'seats': 3 },
            { 'option': 'Option 3', 'number': 3, 'votes': 3, 'seats': 2 },
            { 'option': 'Option 2', 'number': 2, 'votes': 0, 'seats': 0 },

           
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_hondt_zero(self):
        data = {
            'type': 'HONDT',
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 0 },
                { 'option': 'Option 2', 'number': 2, 'votes': 0 },
                { 'option': 'Option 3', 'number': 3, 'votes': 0 },
               
            ],
             'nSeats': 5
        }

        expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 0, 'seats': 0 },
            { 'option': 'Option 2', 'number': 2, 'votes': 0, 'seats': 0 },
            { 'option': 'Option 3', 'number': 3, 'votes': 0, 'seats': 0 },

           
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_hondt_noSeats(self):
        data = {
            'type': 'HONDT',
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 5 },
                { 'option': 'Option 2', 'number': 2, 'votes': 3 },
                { 'option': 'Option 3', 'number': 3, 'votes': 2 },
               
            ],
             'nSeats': 0
        }

        expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 5, 'seats': 0 },
            { 'option': 'Option 2', 'number': 2, 'votes': 3, 'seats': 0 },
            { 'option': 'Option 3', 'number': 3, 'votes': 2, 'seats': 0 },

           
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



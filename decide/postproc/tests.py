from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from base import mods


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
                { 'option': 'Option 1', 'number': 1, 'votes': 5, 'votesFemale': 2, 'pondFemale': 2, 'votesMale': 3, 'pondMale': 1 },
                { 'option': 'Option 2', 'number': 2, 'votes': 53, 'votesFemale': 3, 'pondFemale': 2, 'votesMale': 50, 'pondMale': 1 },
                { 'option': 'Option 3', 'number': 3, 'votes': 28, 'votesFemale': 10, 'pondFemale': 2, 'votesMale': 14, 'pondMale': 1 },
                { 'option': 'Option 4', 'number': 4, 'votes': 68, 'votesFemale': 45, 'pondFemale': 2, 'votesMale': 23, 'pondMale': 1 },
                { 'option': 'Option 5', 'number': 5, 'votes': 110, 'votesFemale': 63, 'pondFemale': 2, 'votesMale': 47, 'pondMale': 1 },
                { 'option': 'Option 6', 'number': 6, 'votes': 70, 'votesFemale': 14, 'pondFemale': 2, 'votesMale': 56, 'pondMale': 1 },
            ]
        }

        expected_result = [
            {'option': 'Option 1', 'number': 1, 'votes': 5, 'votesFemale': 2, 'pondFemale': 2, 'votesMale': 3, 'pondMale': 1, 'postproc': 7},
            { 'option': 'Option 2', 'number': 2, 'votes': 53, 'votesFemale': 3, 'pondFemale': 2, 'votesMale': 50, 'pondMale': 1, 'postproc': 56 },
            { 'option': 'Option 3', 'number': 3, 'votes': 28, 'votesFemale': 10, 'pondFemale': 2, 'votesMale': 14, 'pondMale': 1, 'postproc': 34 },
            { 'option': 'Option 4', 'number': 4, 'votes': 68, 'votesFemale': 45, 'pondFemale': 2, 'votesMale': 23, 'pondMale': 1, 'postproc': 113 },
            { 'option': 'Option 5', 'number': 5, 'votes': 110, 'votesFemale': 63, 'pondFemale': 2, 'votesMale': 47, 'pondMale': 1, 'postproc': 173 },
            { 'option': 'Option 6', 'number': 6, 'votes': 70, 'votesFemale': 14, 'pondFemale': 2, 'votesMale': 56, 'pondMale': 1, 'postproc': 84 },
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

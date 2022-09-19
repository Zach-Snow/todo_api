import unittest
import requests
from typing import Dict
from database import db


class testEndPoints(unittest.TestCase):

    def setUp(self):
        self.correct_put_details = {
            "title": "test title",
            "description": "test description"
        }

        self.false_put_update_details = {
            "titl": "mock title 2",
            "descriptio": "Mock description"
        }

        self.correct_update_det_single = {
            "title": "updated test title",
        }

        self.correct_update_det_full = {
            "title": "updated test title second run",
            "description": "updated test description"
        }

        self.base_url = "http://localhost:5001/v1/todo/"

    # the test cases have been tagged with alphabest so that they run in a sequential manner
    def test_a_put(self):
        # correct response for correct put request dict
        correct_response = requests.put(self.base_url, self.correct_put_details)
        # response for false put request dict
        false_response = requests.put(self.base_url, self.false_put_update_details)
        # correct response for empty put request dict
        empty_response = requests.put(self.base_url, {})
        self.assertEqual(correct_response.status_code, 200)
        self.assertEqual(false_response.status_code, 400)
        self.assertEqual(empty_response.status_code, 400)

    def test_b_get(self):
        whole_response = requests.get(self.base_url)
        # an id that is already available in the database, the dataset that we just put in
        single_id = db.TODO_Collection.find_one({"title": "test title", }, {"_id": False})["id"]
        # gets a single existing data set
        single_response = requests.get(self.base_url + single_id)
        # Tries to get a dataset with an id that does not exist
        wrong_response = requests.get(self.base_url + str("ad1223sad223"))
        self.assertTrue(type(whole_response.json), Dict)
        self.assertEqual(whole_response.status_code, 200)
        self.assertEqual(single_response.status_code, 200)
        self.assertEqual(wrong_response.status_code, 404)

    def test_c_update(self):
        # finds the latets input that we just did
        single_id = db.TODO_Collection.find_one({"title": "test title", }, {"_id": False})["id"]
        # updates the latets input with only one key
        correct_resp_single = requests.patch(self.base_url + single_id, self.correct_update_det_single)
        self.assertEqual(correct_resp_single.status_code, 200)
        # updates the latets input with only all key
        correct_resp_whole = requests.patch(self.base_url + single_id, self.correct_update_det_full)
        self.assertEqual(correct_resp_whole.status_code, 200)
        # tries to update the latets input with wrong data dict
        wrong_resp_input_details = requests.patch(self.base_url + single_id, self.false_put_update_details)
        self.assertEqual(wrong_resp_input_details.status_code, 400)
        # tries to update the latets input with wrong dataset id
        wrong_resp_id = requests.patch(self.base_url + "asdad23435asd", self.correct_update_det_single)
        self.assertEqual(wrong_resp_id.status_code, 400)
        # tries to update the latets input with empty dataset id
        empty_resp = requests.patch(self.base_url + single_id, {})
        self.assertEqual(empty_resp.status_code, 400)

    def test_d_delete(self):
        # finds the latets input that we just updated
        single_id = db.TODO_Collection.find_one({"title": "updated test title second run"}, {"_id": False})["id"]
        # deletes the latest test input in database
        del_response = requests.delete(self.base_url + single_id)
        # tries to delete a non existing dataset
        del_response_error = requests.delete(self.base_url + "asd727edasd")

        self.assertEqual(del_response.status_code, 200)
        self.assertEqual(del_response_error.status_code, 400)

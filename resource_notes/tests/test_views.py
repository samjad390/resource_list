import json
import uuid

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.exceptions import ValidationError

from resource_notes.models import ResourceNotes


class ResourceNotesViewSetTest(APITestCase):

    def setUp(self) -> None:
        super(ResourceNotesViewSetTest, self).setUp()
        self.url_resource_notes_list = reverse('resource_notes:resource_notes-list')
        for i in range(1000):
            ResourceNotes.objects.create(name=f"test_name_{i}", email=f"test_{i}@xyz.com", notes="some test notes")
        self.instance = ResourceNotes.objects.first()
        # self.url_resource_notes_detail = reverse(
        #     'resource_notes:resource_notes-detail', kwargs={'pk': self.instance.pk}
        # )
        # self.url_resource_notes_detail_with_random_argument = reverse(
        #     'resource_notes:resource_notes-detail', kwargs={'pk': str(uuid.uuid4())}
        # )
    def get_resource_detail_url(self, pk):
        return reverse('resource_notes:resource_notes-detail', kwargs={'pk': pk})

    def test_resource_list_get_method(self):
        response = self.client.get(self.url_resource_notes_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_resource_list_get_method_with_some_results(self):
        response = self.client.get(self.url_resource_notes_list)
        response = response.json()
        results = response.get('results')
        self.assertNotEqual(results, [])

    def test_resource_list_get_method_with_offset_and_default_limit(self):
        url = f"{self.url_resource_notes_list}?offset=50"
        response = self.client.get(url)
        response = response.json()
        results = response.get('results')
        self.assertEqual(len(results), 25)

    def test_resource_list_get_method_with_limit(self):
        url = f"{self.url_resource_notes_list}?limit=50"
        response = self.client.get(url)
        response = response.json()
        results = response.get('results')
        self.assertEqual(len(results), 50)

    def test_resource_list_get_method_with_offset_and_limit(self):
        url = f"{self.url_resource_notes_list}?offset=50&limit=100"
        response = self.client.get(url)
        response = response.json()
        results = response.get('results')
        self.assertEqual(len(results), 100)

    def test_resource_list_post_method_with_correct_payload(self):
        data = {'name': 'test_test', 'email': 'test@xyz.com', 'notes': 'some random notes'}
        response = self.client.post(self.url_resource_notes_list, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_resource_list_post_method_with_missing_notes_field_in_payload(self):
        data = {'name': 'test_test', 'email': 'test@xyz.com'}
        response = self.client.post(self.url_resource_notes_list, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_resource_list_post_method_with_missing_email_field_in_payload(self):
        data = {'name': 'test_test', 'notes': 'some random notes'}
        response = self.client.post(self.url_resource_notes_list, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_resource_list_post_method_with_missing_name_field_in_payload(self):
        data = {'email': 'test@xyz.com', 'notes': 'some random notes'}
        response = self.client.post(self.url_resource_notes_list, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_resource_list_post_method_with_exceeded_name_length(self):
        data = {'name': 'text' * 256, 'email': 'test@xyz.com', 'notes': 'some random notes'}
        response = self.client.post(self.url_resource_notes_list, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_resource_list_post_method_with_incorrect_email(self):
        data = {'name': 'text', 'email': 'testxyz.com', 'notes': 'some random notes'}
        response = self.client.post(self.url_resource_notes_list, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_resource_list_post_method_with_empty_payload(self):
        response = self.client.post(self.url_resource_notes_list, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_resource_detail_get_method_with_correct_id(self):
        url = self.get_resource_detail_url(self.instance.pk)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_resource_detail_get_method_with_random_id(self):
        url = self.get_resource_detail_url(str(uuid.uuid4()))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_resource_detail_put_method_with_correct_id(self):
        data = {'name': 'test_test', 'email': 'test@xyz.com', 'notes': 'some random notes'}
        url = self.get_resource_detail_url(self.instance.pk)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = response.json()
        self.assertEqual(response['name'], 'test_test')

    def test_resource_detail_put_method_with_correct_id_and_exceeded_name_length(self):
        data = {'name': 'test_test' * 256, 'email': 'test@xyz.com', 'notes': 'some random notes'}
        url = self.get_resource_detail_url(self.instance.pk)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_resource_detail_put_method_with_correct_id_and_invalid_email(self):
        data = {'name': 'test_test', 'email': 'testxyz.com', 'notes': 'some random notes'}
        url = self.get_resource_detail_url(self.instance.pk)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_resource_detail_put_method_with_correct_id_and_missing_notes_field(self):
        data = {'name': 'test_test', 'email': 'test@xyz.com'}
        url = self.get_resource_detail_url(self.instance.pk)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_resource_detail_put_method_with_correct_id_and_missing_email_field(self):
        data = {'name': 'test_test', 'notes': 'some random notes'}
        url = self.get_resource_detail_url(self.instance.pk)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_resource_detail_put_method_with_correct_id_and_missing_name_field(self):
        data = { 'email': 'test@xyz.com', 'notes': 'some random notes'}
        url = self.get_resource_detail_url(self.instance.pk)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_resource_detail_put_method_with_correct_id_and_empty_payload(self):
        data = {}
        url = self.get_resource_detail_url(self.instance.pk)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_resource_detail_patch_method_with_incorrect_id(self):
        data = {}
        url = self.get_resource_detail_url(str(uuid.uuid4()))
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_resource_detail_patch_method_with_correct_id_and_empty_payload(self):
        data = {}
        url = self.get_resource_detail_url(self.instance.pk)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_resource_detail_patch_method_with_correct_id_and_name_update(self):
        data = {'name': 'test_test_test'}
        url = self.get_resource_detail_url(self.instance.pk)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = response.json()
        self.assertEqual(response['name'], 'test_test_test')

    def test_resource_detail_patch_method_with_correct_id_and_exceeded_name_length(self):
        data = {'name': 'test_test_test' * 256}
        url = self.get_resource_detail_url(self.instance.pk)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_resource_detail_patch_method_with_correct_id_and_invalid_email(self):
        data = {'email': 'textwxyz.com'}
        url = self.get_resource_detail_url(self.instance.pk)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_resource_detail_patch_method_with_correct_id_name_and_email_update(self):
        data = {'name': 'test_te', 'email': 'text@wxyz.com'}
        url = self.get_resource_detail_url(self.instance.pk)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = response.json()
        self.assertEqual(response['name'], 'test_te')
        self.assertEqual(response['email'], 'text@wxyz.com')

    def test_resource_detail_delete_method_with_correct_id(self):
        url = self.get_resource_detail_url(self.instance.pk)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_resource_detail_delete_method_with_incorrect_id(self):
        url = self.get_resource_detail_url(str(uuid.uuid4()))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

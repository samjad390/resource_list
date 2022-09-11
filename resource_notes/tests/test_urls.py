import json
import uuid

from django.urls import resolve, reverse, NoReverseMatch

from rest_framework.test import APITestCase
from rest_framework import status

from resource_notes.models import ResourceNotes


class ResourceNotesURLs(APITestCase):

    def setUp(self) -> None:
        super(ResourceNotesURLs, self).setUp()
        self.url_resource_notes_list = reverse('resource_notes:resource_notes-list')
        self.instance = ResourceNotes.objects.create(name="test_name", email="test@xyz.com", notes="some test notes")
        self.url_resource_notes_detail = reverse(
            'resource_notes:resource_notes-detail', kwargs={'pk': self.instance.pk}
        )
        self.url_resource_notes_detail_with_random_argument = reverse(
            'resource_notes:resource_notes-detail', kwargs={'pk': str(uuid.uuid4())}
        )

    def test_resource_notes_list_url(self):
        url = '/api/v1/resource_notes/'
        self.assertEqual(url, self.url_resource_notes_list)

    def test_resource_notes_list_url_with_wrong_name(self):
        url = '/api/v1/test_url/'
        self.assertNotEqual(url, self.url_resource_notes_list)

    def test_resource_notes_list_get(self):
        response = self.client.get(self.url_resource_notes_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_resource_notes_list_post_with_wrong_payload(self):
        response = self.client.post(self.url_resource_notes_list, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_resource_notes_list_put_not_allowed(self):
        response = self.client.put(self.url_resource_notes_list, {})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_resource_notes_list_patch_not_allowed(self):
        response = self.client.patch(self.url_resource_notes_list, {})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_resource_notes_list_delete_not_allowed(self):
        response = self.client.delete(self.url_resource_notes_list)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_resource_notes_detail_url(self):
        url = f'/api/v1/resource_notes/{self.instance.pk}/'
        self.assertEqual(url, self.url_resource_notes_detail)

    def test_resource_notes_detail_url_with_missing_argument(self):
        url = '/api/v1/resource_notes/'
        self.assertNotEqual(url, self.url_resource_notes_detail)

    def test_resource_notes_detail_url_with_wrong_argument(self):
        url = '/api/v1/resource_notes/5/'
        self.assertNotEqual(url, self.url_resource_notes_detail)

    def test_resource_notes_detail_url_with_wrong_name(self):
        url = '/api/v1/test_url/'
        self.assertNotEqual(url, self.url_resource_notes_detail)

    def test_resource_notes_detail_get_with_correct_argument(self):
        response = self.client.get(self.url_resource_notes_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_resource_notes_detail_get_with_random_argument(self):
        response = self.client.get(self.url_resource_notes_detail_with_random_argument)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_resource_notes_detail_post_method_not_allowed(self):
        response = self.client.post(self.url_resource_notes_detail, {})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_resource_notes_detail_post_method_not_allowed_with_random_argument(self):
        response = self.client.post(self.url_resource_notes_detail_with_random_argument, {})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_resource_notes_detail_put_wrong_payload(self):
        response = self.client.put(self.url_resource_notes_detail, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_resource_notes_detail_put_wrong_payload_and_random_argument(self):
        response = self.client.put(self.url_resource_notes_detail_with_random_argument, {})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_resource_notes_detail_patch(self):
        response = self.client.patch(self.url_resource_notes_detail, {})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_resource_notes_detail_patch_wrong_payload_and_random_argument(self):
        response = self.client.patch(self.url_resource_notes_detail_with_random_argument, {})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_resource_notes_detail_delete_with_correct_argument(self):
        response = self.client.delete(self.url_resource_notes_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_resource_notes_detail_delete_with_random_argument(self):
        response = self.client.delete(self.url_resource_notes_detail_with_random_argument)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

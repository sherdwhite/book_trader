# encoding: utf-8

import logging
import random

from books.models import Publisher
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

logger = logging.getLogger(__name__)


class TestPublisherEndpoints(APITestCase):
    def setUp(self):
        self.publisher = Publisher.objects.create(name="The Education Bros")

        self.full_data = {"name": self.publisher.name}

        self.detail_url = reverse("publisher-detail", kwargs={"pk": self.publisher.pk})
        self.list_url = reverse("publisher-list")

    def test_get_publisher(self):
        """GET /api/publisher/{publisher.pk}/ should return the publisher"""
        response = self.client.get(self.detail_url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["pk"] == self.publisher.pk
        assert response.data["name"] == self.publisher.name

    def test_patch_publisher(self):
        """PATCH /api/publisher/{publisher.pk}/ should update the publisher"""
        expected_name = "We Make Books"
        response = self.client.patch(self.detail_url, data={"name": expected_name})
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == expected_name

    def test_put_publisher(self):
        """PUT /api/publisher/{publisher.pk}/ should update the publisher"""
        expected_name = "We Make Books"
        self.full_data["name"] = expected_name
        response = self.client.put(self.detail_url, data=self.full_data)
        assert response.data["name"] == expected_name
        assert Publisher.objects.first().name == expected_name

    def test_delete_publisher(self):
        """DELETE /api/publisher/{publisher.pk}/ should delete the publisher"""
        expected_publishers = Publisher.objects.count() - 1
        response = self.client.delete(self.detail_url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Publisher.objects.count() == expected_publishers

    def test_post_publisher(self):
        """POST /api/publisher/ should create a publisher"""
        expected_publishers = Publisher.objects.count() + 1
        response = self.client.post(self.list_url, data=self.full_data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Publisher.objects.count() == expected_publishers

    def test_list_publisher(self):
        """GET /api/publisher/ should list all publishers"""
        num_created = random.randint(5, 10)
        expected_publishers = Publisher.objects.count() + num_created
        for i in range(num_created):
            Publisher.objects.create(name=f"Book Factory {i}")

        response = self.client.get(self.list_url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == expected_publishers
        for publisher, response_item in zip(Publisher.objects.all(), response.data):
            assert response_item["pk"] == publisher.pk

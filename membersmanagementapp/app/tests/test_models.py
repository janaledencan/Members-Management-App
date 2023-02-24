from django.test import TestCase
from app.models import Owner
from django.contrib.auth.models import User


class OwnerModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        created_user = User.objects.create_user(
            username="testuser", password="testpass"
        )
        owner = Owner.objects.create(
            user=created_user,
            business="My job",
            address="Trpimirova",
            country="Croatia",
        )

    def test_username_label(self):
        owner = Owner.objects.get(id=1)
        field_label = owner._meta.get_field("username").verbose_name
        self.assertEqual(field_label, "username")

    def test_business_label(self):
        owner = Owner.objects.get(id=1)
        field_label = owner._meta.get_field("business").verbose_name
        self.assertEqual(field_label, "business")

    def test_business_max_length(self):
        owner = Owner.objects.get(id=1)
        max_length = owner._meta.get_field("business").max_length
        self.assertEqual(max_length, 20)

    def test_object_name_is_username(self):
        owner = Owner.objects.get(id=1)
        expected_object_name = f"{owner.username}"
        self.assertEqual(str(owner), expected_object_name)

from datetime import date
from accounts.models import Partner, User
from django.test import TestCase


class PartnerTestModel(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.normal_user = User.objects.create(
            email="testmail@mail.com",
            password="1234",
            full_name="John Wick Loves his dog",
            cpf="12345678912",
            phone="31912345678",
        )

        cls.partner = Partner.objects.create(
            partners_id=cls.normal_user.id,
            describe="Some description.",
            gender="F",
            birthday="1999/08/15",
            service_id=1,
            address_id=1
        )

    def test_it_has_partner_infos(self):

        user_infos = User.objects.get(id=self.partner.partners_id)

        self.assertIsInstance(user_infos.full_name, str)
        self.assertIsInstance(user_infos.is_partner, bool)
        self.assertIsInstance(self.partner.partners_id, int)
        self.assertIsInstance(self.partner.describe, str)
        self.assertIsInstance(self.partner.gender, str)
        self.assertIsInstance(self.partner.birthday, date)
        self.assertIsInstance(self.partner.service_id, int)
        self.assertIsInstance(self.partner.address_id, int)
        self.assertEqual(user_infos.full_name, self.normal_user.full_name)

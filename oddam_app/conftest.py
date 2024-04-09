import pytest

from oddam_app.models import Category, Institution, Donation, TYPES


@pytest.fixture
def categories():
    categories = []
    category1 = Category.objects.create(name="category1")
    category2 = Category.objects.create(name="category2")
    categories.append(category1)
    categories.append(category2)
    return categories

@pytest.fixture
def institutions():
    institutions = []
    institution1 = Institution.objects.create(name="institution1")
    institution2 = Institution.objects.create(name="institution2")
    institutions.append(institution1)
    institutions.append(institution2)
    return institutions

@pytest.fixture
def donations(categories, institutions):
    donations = []
    donation1 = Donation.objects.create(quantity=1, institution=institutions[0],
                                        address="Street 1", phone_number=111222111, city="City", zip_code=11222,
                                        pick_up_date="2020-02-22", pick_up_time="10:00:00",
                                        pick_up_comment="comment")
    donation1.categories.set(categories)
    donation2 = Donation.objects.create(quantity=2, institution=institutions[1],
                                        address="Street 2", phone_number=111333111, city="City 2", zip_code=22333,
                                        pick_up_date="2020-02-23", pick_up_time="12:00:00",
                                        pick_up_comment="comment1")
    donation2.categories.set(categories)
    donations.append(donation1)
    donations.append(donation2)
    return donations




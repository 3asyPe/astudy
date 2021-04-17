import pytest


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def category(course_factory, mixer):
    category = mixer.blend("categories.Category", title="Test category")
    category.courses.add(course_factory())
    return category




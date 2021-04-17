import random
import string

import pytest


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def category(course_factory, mixer):
    category = mixer.blend("categories.Category", title="Test category")
    category.courses.add(course_factory())
    return category


@pytest.fixture
def course_factory(mixer):
    def course_mixer():
        return mixer.blend(
            "courses.Course", 
            title=''.join([random.choice(string.hexdigits) for _ in range(0, 8)]),
            subtitle=''.join([random.choice(string.hexdigits) for _ in range(0, 8)]),
            price=3.33,
            description=''.join([random.choice(string.hexdigits) for _ in range(0, 8)]),
        )
    return course_mixer

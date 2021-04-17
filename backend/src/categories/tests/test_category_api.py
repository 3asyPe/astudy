import logging
import pytest
import random
import string

from mixer.backend.django import mixer

from categories.utils import CategoryErrorMessages


logger = logging.getLogger(__name__)

pytestmark = [pytest.mark.django_db]


def test_get_category_api(api, category):
    response = api.get("/api/category/get/", {"slug": category.slug})
    assert response["title"] == category.title


@pytest.mark.parametrize("url", ['/api/category/get/', '/api/category/courses/'])
def test_get_wrong_category(api, url):
    response = api.get(url, {
        "slug": "unknown-slug"
    }, expected_status_code=404)

    response["error"] == CategoryErrorMessages.CATEGORY_DOES_NOT_EXIST_ERROR.value


@pytest.mark.parametrize("url", ['/api/category/get/', '/api/category/courses/'])
def test_get_category_without_required_slug(api, url):
    response = api.get(url, {
        "someotherfield": "some value"
    }, expected_status_code=400)

    response["error"] == CategoryErrorMessages.REQUEST_FIELDS_ERROR.value


def test_fetching_category_courses_api(api, category):
    response = api.get('/api/category/courses/', {
        "slug": category.slug,
    })

    course = category.courses.first()
    res_course = response[0]

    assert course.slug == res_course['slug']
    assert str(course.image) in res_course['image']
    assert course.title == res_course['title']
    assert course.subtitle == res_course['subtitle']
    assert str(course.price) == res_course['price']
    assert "lectures_count" in res_course
    assert "duration_time" in res_course

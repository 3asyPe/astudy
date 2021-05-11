import pytest

from courses.utils import CourseErrorMessages


pytestmark = [pytest.mark.django_db]


def test_get_course_info_api_with_slug(api, course):
    response = api.get("/api/course/get/", {
        "slug": course.slug,
    })

    assert response["slug"] == course.slug

def test_get_course_info_api_without_slug(api):
    response = api.get("/api/course/get/", {}, expected_status_code=400)

    assert response["error"] == CourseErrorMessages.REQUEST_FIELDS_ERROR.value


def test_get_course_info_api_with_wrong_slug(api):
    response = api.get("/api/course/get/", {
        "slug": "somerandomslug",
    }, expected_status_code=404)

    assert response["error"] == CourseErrorMessages.COURSE_DOES_NOT_EXIST_ERROR.value
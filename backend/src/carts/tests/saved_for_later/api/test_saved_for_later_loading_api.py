import pytest

from carts.models import SavedForLater


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def s_list_with_course(saved_for_later, course_factory):
    saved_for_later.courses.add(course_factory())
    return saved_for_later


@pytest.fixture
def s_list_without_user_with_course(saved_for_later_without_user, course_factory):
    saved_for_later_without_user.courses.add(course_factory())
    return saved_for_later_without_user


def test_loading_s_list_api(api, cart, saved_for_later):
    response = api.get("/api/savedforlater/get/", {
        "cart_id": cart.id,
        "saved_for_later_id": saved_for_later.id, 
    })

    assert response["id"] == saved_for_later.id
    assert "courses" in response


def test_loading_s_list_without_user_api(anon, cart, saved_for_later):
    response = anon.get("/api/savedforlater/get/", {
        "cart_id": cart.id,
        "saved_for_later_id": saved_for_later.id,
    })

    assert response['id'] != saved_for_later.id
    assert response["courses"] == []

     
def test_loading_s_list_without_id_api(api, cart, saved_for_later):
    response = api.get("/api/savedforlater/get/", {
        "cart_id": cart.id
    })

    assert response["id"] == saved_for_later.id


def test_loading_s_list_with_user_and_different_id_api(api, cart, saved_for_later, another_saved_for_later):
    response = api.get("/api/savedforlater/get/", {
        "cart_id": cart.id,
        "saved_for_later_id": another_saved_for_later.id,
    })

    assert response["id"] == saved_for_later.id


def test_loading_s_list_with_user_and_different_id_with_courses_api(api, cart, s_list_with_course, s_list_without_user_with_course):
    course = s_list_without_user_with_course.courses.first()
    response = api.get("/api/savedforlater/get/", {
        "cart_id": cart.id,
        "saved_for_later_id": s_list_without_user_with_course.id,
    })

    s_list_with_course.refresh_from_db()

    assert response["id"] == s_list_with_course.id
    assert len(response["courses"]) == 2
    
    assert not SavedForLater.objects.filter(id=s_list_without_user_with_course.id).exists()
    assert s_list_with_course.courses.count() == 2
    assert course in s_list_with_course.courses.all()


def test_loading_s_list_without_anything_api(anon, cart):
    response = anon.get("/api/savedforlater/get/", {
        "cart_id": cart.id
    })

    assert "id" in response
    assert "courses" in response


def test_loading_s_list_courses_api(api, cart, s_list_with_course):
    response = api.get("/api/savedforlater/get/", {
        "cart_id": cart.id,
        "saved_for_later_id": s_list_with_course.id
    })

    course = s_list_with_course.courses.first()
    res_course = response["courses"][0]

    assert res_course["slug"] == course.slug
    assert str(course.image) in res_course["image"]
    assert res_course["title"] == course.title
    assert res_course["subtitle"] == course.subtitle
    assert res_course["price"] == str(course.price)
    assert "discount" in res_course


def test_loading_s_list_for_user_without_s_list(api, cart):
    response = api.get("/api/savedforlater/get/", {
        "cart_id": cart.id,
    })

    assert "id" in response
    assert response["courses"] == []

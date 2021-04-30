import pytest

from carts.models import SavedForLater
from carts.services import SavedForLaterToolkit


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def s_list_with_course(saved_for_later, course_factory):
    course = course_factory()
    saved_for_later.courses.add(course)
    return saved_for_later


@pytest.fixture
def s_list_without_user_with_course(saved_for_later_without_user, course_factory):
    course = course_factory()
    saved_for_later_without_user.courses.add(course)
    return saved_for_later_without_user


def test_loading_s_list_with_user_and_is_for_same_s_list(saved_for_later):
    test_s_list = SavedForLaterToolkit.load_saved_for_later(
        user=saved_for_later.user,
        saved_for_later_id=saved_for_later.id,
    )

    assert test_s_list == saved_for_later


def test_loading_s_list_with_user(saved_for_later):
    test_s_list = SavedForLaterToolkit.load_saved_for_later(user=saved_for_later.user)

    assert test_s_list == saved_for_later


def test_loading_s_list_without_user(mocker, saved_for_later):
    create_new_s_list = mocker.patch("carts.services.SavedForLaterToolkit._create_new_saved_for_later")
    test_s_list = SavedForLaterToolkit.load_saved_for_later(saved_for_later_id=saved_for_later.id)

    create_new_s_list.assert_called_once()


def test_loading_s_list_with_user_and_different_id(saved_for_later, another_saved_for_later):
    test_s_list = SavedForLaterToolkit.load_saved_for_later(
        user=saved_for_later.user,
        saved_for_later_id=another_saved_for_later.id,
    )

    assert test_s_list == saved_for_later


def test_loading_s_list_with_user_and_different_id_with_courses(s_list_with_course, s_list_without_user_with_course):
    course = s_list_without_user_with_course.courses.first()
    test_s_list = SavedForLaterToolkit.load_saved_for_later(
        user=s_list_with_course.user,
        saved_for_later_id=s_list_without_user_with_course.id,
    )

    assert test_s_list == s_list_with_course
    assert not SavedForLater.objects.filter(id=s_list_without_user_with_course.id).exists()
    assert s_list_with_course.courses.count() == 2
    assert course in s_list_with_course.courses.all()


def test_loading_s_list_for_user_without_s_list(mocker, user):
    create_new_s_list = mocker.patch("carts.services.SavedForLaterToolkit._create_new_saved_for_later")
    test_s_list = SavedForLaterToolkit.load_saved_for_later(user=user)

    create_new_s_list.assert_called_once()


def test_loading_s_list_without_arguments(mocker):
    create_new_s_list = mocker.patch("carts.services.SavedForLaterToolkit._create_new_saved_for_later")
    test_s_list = SavedForLaterToolkit.load_saved_for_later()

    create_new_s_list.assert_called_once()

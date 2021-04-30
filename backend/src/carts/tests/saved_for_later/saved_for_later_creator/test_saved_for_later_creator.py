import pytest

from app.errors import ValidationError
from carts.services import SavedForLaterCreator
from carts.utils import SavedForLaterErrorMessages


pytestmark = [pytest.mark.django_db]


def test_s_list_creation_with_user(user):
    s_list = SavedForLaterCreator(user=user)()

    assert s_list.user == user
    assert s_list.courses.count() == 0


def test_s_list_creation_without_user():
    s_list = SavedForLaterCreator()()

    assert s_list.user == None
    assert s_list.courses.count() == 0


def test_s_list_creation_with_anonymous_user(anonymous_user):
    s_list = SavedForLaterCreator(user=anonymous_user)()

    assert s_list.user == None
    assert s_list.courses.count() == 0


def test_s_list_creation_for_user_with_existed_s_list(saved_for_later, user):
    with pytest.raises(ValidationError) as exc:
        s_list = SavedForLaterCreator(user=user)()
    
    assert str(exc.value) == SavedForLaterErrorMessages.SAVED_FOR_LATER_LIST_ALREADY_EXISTS_ERROR.value

    
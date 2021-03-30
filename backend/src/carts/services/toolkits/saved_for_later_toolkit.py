import logging

from django.conf import settings

from carts.models import SavedForLater
from carts.services import SavedForLaterCreator
from courses.services import CourseSelector


logger = logging.getLogger(__name__)

User = settings.AUTH_USER_MODEL


class SavedForLaterToolkit:
    @classmethod
    def load_saved_for_later(cls, user: User, saved_for_later_id: int) -> SavedForLater:
        s_list = None
        if not user.is_authenticated:
            s_list_by_user_qs = SavedForLater.objects.none()
        else:
            s_list_by_user_qs = SavedForLater.objects.filter(user=user)
        
        s_list_by_id_qs = SavedForLater.objects.filter(id=saved_for_later_id)
        if s_list_by_id_qs.exists() and s_list_by_user_qs.exists():
            s_list_by_id = s_list_by_id_qs.last()
            s_list_by_user = s_list_by_user_qs.last()
            s_list = cls._choose_saved_for_later_by_user_or_by_id(s_list_by_id, s_list_by_user)
        elif s_list_by_user_qs.exists():
            s_list = s_list_by_user_qs.last()
        elif s_list_by_id_qs.exists():
            s_list_by_id = s_list_by_id_qs.last()
            if user.is_authenticated:
                if s_list_by_id.user is None:
                    s_list_by_id.user = user
                    s_list_by_id.save()
                    s_list = s_list_by_id
                elif s_list_by_id.user != user:
                    s_list = cls._create_new_saved_for_later(user=user)
                else:
                    s_list = s_list_by_id
            else:
                if s_list_by_id.user is not None:
                    s_list = cls._create_new_saved_for_later(user=user)
                else:
                    s_list = s_list_by_id
        else:
            s_list = cls._create_new_saved_for_later(user=user)
        return s_list

    @classmethod
    def add_course_to_saved_for_later(cls, s_list: SavedForLater, course_slug: str) -> SavedForLater:
        course = CourseSelector.get_course_by_slug(slug=course_slug)
        if course not in s_list.courses.all():
            s_list.courses.add(course)
        return s_list

    @classmethod
    def remove_course_from_saved_for_later(cls, s_list: SavedForLater, course_slug: str) -> SavedForLater:
        course = CourseSelector.get_course_by_slug(slug=course_slug)
        if course in s_list.courses.all():
            s_list.courses.remove(course)
        return s_list

    @classmethod
    def check_on_course_in_saved_for_later(cls, s_list: SavedForLater, course_slug: str) -> bool:
        course = CourseSelector.get_course_by_slug(slug=course_slug)
        return course in s_list.courses.all()

    @classmethod
    def _create_new_saved_for_later(cls, user=None) -> SavedForLater:
        return SavedForLaterCreator(user=user)()

    @classmethod
    def _choose_saved_for_later_by_user_or_by_id(cls, s_list_by_id: SavedForLater, s_list_by_user: SavedForLater) -> SavedForLater:
        if s_list_by_id != s_list_by_user:
            if s_list_by_id.user is not None and s_list_by_id.user != s_list_by_user.user:
                return s_list_by_user
            else:
                s_list_by_user.add_courses(courses=s_list_by_id.courses.all())
                s_list_by_id.delete()
                return s_list_by_user
        return s_list_by_id

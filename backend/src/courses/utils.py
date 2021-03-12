import enum

from app.utils import get_upload_image_path


class CourseErrorMessages(enum.Enum):
    COURSE_DOES_NOT_EXIST_ERROR = "COURSE_DOES_NOT_EXIST_ERROR"
    REQUEST_FIELDS_ERROR = "REQUEST_FIELDS_ERROR"


def get_course_upload_image_path(*args, **kwargs):
    return get_upload_image_path(*args, **kwargs, prefix="course")


def update_duration_time_hours_minutes(cur_hours, cur_minutes, new_hours, new_minutes) -> (int, int):
    minutes = cur_minutes + new_minutes
    additional_hour = 0
    if minutes > 59:
        additional_hour = 1
        minutes -= 60
    hours = cur_hours + new_hours + additional_hour
    return hours, minutes


def update_duration_time_hours_minutes_seconds(cur_hours, cur_minutes, cur_seconds, 
                                               new_hours, new_minutes, new_seconds) -> (int, int, int):
    seconds = cur_seconds + new_seconds
    additional_minut = 0
    if seconds > 59:
        additional_minut = 1
        seconds -= 60
    hours, minutes = update_duration_time_hours_minutes(cur_hours, cur_minutes, new_hours, new_minutes + additional_minut)
    return hours, minutes, seconds

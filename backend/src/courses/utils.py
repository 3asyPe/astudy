import enum

from app.utils import get_upload_image_path


class CourseErrorMessages(enum.Enum):
    COURSE_DOES_NOT_EXIST_ERROR = "COURSE_DOES_NOT_EXIST_ERROR"
    REQUEST_FIELDS_ERROR = "REQUEST_FIELDS_ERROR"



def get_course_upload_image_path(*args, **kwargs):
    return get_upload_image_path(*args, **kwargs, prefix="course")

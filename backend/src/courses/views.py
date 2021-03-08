import logging

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Course
from .selectors import get_course_by_slug
from .serializers import CourseSerializer
from .utils import CourseErrorMessages


logger = logging.getLogger(__name__)


@api_view(["GET"])
def get_course_api(request, *args, **kwargs):
    try:
        data = request.GET
        slug = data["slug"]
    except KeyError:
        logger.error("Request object doesn't have a slug field")
        return Response({"error": CourseErrorMessages.REQUEST_FIELDS_ERROR.value}, status=400)
    
    try:
        course = get_course_by_slug(slug=slug)
    except Course.DoesNotExist:
        logger.warning(f"Course with slug - {slug} doesn't exist")
        return Response({"error": CourseErrorMessages.COURSE_DOES_NOT_EXIST_ERROR.value}, status=404)
    
    serializer = CourseSerializer(instance=course)
    return Response(serializer.data, status=200)
    
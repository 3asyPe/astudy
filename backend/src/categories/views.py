import logging

from courses.selectors import get_courses_by_category
from courses.serializers import CategoryCourseSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Category
from .selectors import (
    get_category_by_slug,
)
from .serializers import (
    CategorySerializer,
)
from .utils import CategoryErrorMessages


logger = logging.getLogger(__name__)


@api_view(["GET"])
def get_category_api(request, *args, **kwargs):
    try:
        data = request.GET
        slug = data["slug"]
    except KeyError:
        logger.error("Request object doesn't have a slug field")
        return Response({"error": CategoryErrorMessages.REQUEST_FIELDS_ERROR.value}, status=400)
    
    try:
        category = get_category_by_slug(slug=slug)
    except Category.DoesNotExist:
        logger.warning(f"Category with slug - {slug} doesn't exist")
        return Response({"error": CategoryErrorMessages.CATEGORY_DOES_NOT_EXIST_ERROR}, status=404)
    
    serializer = CategorySerializer(instance=category)
    return Response(serializer.data, status=200)


@api_view(["GET"])
def fetch_category_courses_api(request, *args, **kwargs):
    try:
        data = request.GET
        slug = data["slug"]
    except KeyError:
        logger.error("Request object doesn't have a slug field")
        return Response({"error": CategoryErrorMessages.REQUEST_FIELDS_ERROR.value}, status=400)
    
    try:
        category = get_category_by_slug(slug=slug)
    except Category.DoesNotExist:
        logger.warning(f"Category with slug - {slug} doesn't exist")
        return Response({"error": CategoryErrorMessages.CATEGORY_DOES_NOT_EXIST_ERROR}, status=404)

    courses = get_courses_by_category(category=category)
    serializer = CategoryCourseSerializer(courses, many=True)
    return Response(serializer.data, status=200)

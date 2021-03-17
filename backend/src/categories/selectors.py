import logging

from .models import Category


logger = logging.getLogger(__name__)


def get_category_by_slug(slug: str):
    qs = Category.objects.filter(slug=slug)
    if qs.exists():
        if not qs.filter(active=True).exists():
            logger.warning(f"There was an attempt to get an inactive category with slug - {slug}")
            raise Category.DoesNotExist()
        return qs.first()
    raise Category.DoesNotExist()

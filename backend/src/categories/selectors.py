from .models import Category


def get_category_by_slug(slug: str):
    qs = Category.objects.filter(slug=slug)
    if qs.exists():
        return qs.first()
    raise Category.DoesNotExist()

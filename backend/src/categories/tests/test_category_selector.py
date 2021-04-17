import pytest

from categories.models import Category
from categories.selectors import get_category_by_slug


pytestmark = [pytest.mark.django_db]


def test_get_category_by_slug(category):
    test_category = get_category_by_slug(category.slug)
    assert test_category == category


def test_get_category_by_slug_with_wrong_slug():
    with pytest.raises(Category.DoesNotExist) as exc:
        get_category_by_slug("test-category-slug")

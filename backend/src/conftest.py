import pytest

from mixer.backend.django import mixer as _mixer


@pytest.fixture
def mixer():
    return _mixer
import pytest


pytestmark = [pytest.mark.django_db]


def test_get_course_info_api(api, course):
    response = api.get("/api/course/get/", {
        "slug": course.slug,
    })

    assert response["slug"] == course.slug
    assert response["category"] == course.category
    assert str(course.image) in response["image"]
    assert response["title"] == course.title
    assert response["subtitle"] == course.subtitle
    assert float(response["price"]) == float(course.price)
    assert response["description"] == course.description
    assert response["students_count"] == course.students_count


def test_get_course_info_api_goals_and_requirements(api, course):
    response = api.get("/api/course/get/", {
        "slug": course.slug,
    })

    goals = response["goals"]
    for goal, r_goal in zip(course.goals.all(), goals):
        assert goal.goal == r_goal["goal"]

    requirements = response["requirements"]
    for requirement, r_requirement in zip(course.requirements.all(), requirements):
        assert requirement.requirement == r_requirement["requirement"]


def test_get_course_info_api_content(api, course):
    response = api.get("/api/course/get/", {
        "slug": course.slug,
    })

    content = course.content
    r_content = response["content"]

    assert r_content["sections_count"] == content.sections_count
    assert r_content["lectures_count"] == content.lectures_count
    assert r_content["articles_count"] == content.articles_count
    assert r_content["resources_count"] == content.resources_count
    assert r_content["assignments_count"] == content.assignments_count
    
    duration_time = content.duration_time
    r_duration_time = r_content["duration_time"]
    
    assert r_duration_time["hours"] == duration_time.hours
    assert r_duration_time["minutes"] == duration_time.minutes


def test_get_course_info_api_sections(api, course):
    response = api.get("/api/course/get/", {
        "slug": course.slug,
    })

    sections = response["content"]["sections"]
    assert len(sections) == course.content.sections.count()

    section = course.content.sections.first()
    r_section = sections[0]

    assert r_section["title"] == section.title
    assert r_section["lectures_count"] == section.lectures_count
    
    duration_time = section.duration_time
    r_duration_time = r_section["duration_time"]

    assert r_duration_time["hours"] == duration_time.hours
    assert r_duration_time["minutes"] == duration_time.minutes


def test_get_course_info_api_lectures(api, course):
    response = api.get("/api/course/get/", {
        "slug": course.slug
    })

    lectures = response["content"]["sections"][0]["lectures"]
    assert len(lectures) == course.content.sections.first().lectures.count()

    lecture = course.content.sections.first().lectures.first()
    r_lecture = lectures[0]

    assert r_lecture["free_opened"] == lecture.free_opened
    assert r_lecture["title"] == lecture.title
    assert r_lecture["description"] == lecture.description
    
    duration_time = lecture.duration_time
    r_duration_time = r_lecture["duration_time"]

    assert r_duration_time["hours"] == duration_time.hours
    assert r_duration_time["minutes"] == duration_time.minutes
    assert r_duration_time["seconds"] == duration_time.seconds


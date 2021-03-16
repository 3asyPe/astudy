from courses.models.course import Course, CourseGoal, CourseRequirement
from courses.models.content import CourseContent, CourseDurationTime
from courses.models.lecture import CourseLecture, CourseLectureDurationTime
from courses.models.section import CourseSection, CourseSectionDurationTime


__all__ = [
    Course,
    CourseContent,
    CourseDurationTime,
    CourseGoal,
    CourseLecture,
    CourseLectureDurationTime,
    CourseRequirement,
    CourseSection,
    CourseSectionDurationTime,
]

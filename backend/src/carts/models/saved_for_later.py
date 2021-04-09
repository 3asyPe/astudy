from django.conf import settings
from django.db import models


User = settings.AUTH_USER_MODEL


class SavedForLater(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    courses = models.ManyToManyField("courses.Course", blank=True, related_name="saved_for_later")
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = ("Saved for later list")
        verbose_name_plural = ("Saved for later lists")
    
    def get_courses_count(self):
        return self.courses.all().count()

    def add_courses(self, courses):
        # self.courses.union(courses)
        for course in courses:
            if course not in self.courses.all():
                self.courses.add(course)
        self.save()
    
    def __str__(self):
        return f"{self.user.__str__()} | Saved for later list"

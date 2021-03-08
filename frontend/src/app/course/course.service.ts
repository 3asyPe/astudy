import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { map } from "rxjs/operators";
import { Course } from "./course.model";

@Injectable({
    providedIn: "root",
})
export class CourseService {
    private courseInfoUrl = "http://localhost:8000/api/course/get/"

    constructor(private http: HttpClient) { }

    fetchCourseInfo(slug: string) {
        return this.http.get<Course>(
            this.courseInfoUrl,
            {
                params: {
                    slug: slug
                }
            }
        ).pipe(
            map(course => {
                return new Course(
                    course.slug,
                    course.category,
                    course.image,
                    course.title,
                    course.subtitle,
                    course.price,
                    course.description,
                    course.students_count,
                    course.lectures_count,
                    course.duration_time,
                    course.goals,
                    course.requirements,
                )
            })
        )
    }
}
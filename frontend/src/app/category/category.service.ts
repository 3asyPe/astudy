import { HttpClient, HttpParams } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { CategoryCourse } from "./category-course.model";

@Injectable({
    providedIn: "root",
})
export class CategoryService {
    private categoryInfoUrl = "http://localhost:8000/api/category/get/";
    private categoryCoursesUrl = "http://localhost:8000/api/category/courses/"

    constructor(private http: HttpClient) { }

    fetchCategoryInfo(slug: string) {
        return this.http.get<{title: string}>(
            this.categoryInfoUrl,
            {
                params: {
                    slug: slug
                }
            }
        )
    }

    fetchCategoryCourses(slug: string) {
        return this.http.get<CategoryCourse[]>(
            this.categoryCoursesUrl,
            {
                params: {
                    slug: slug
                }
            }
        )
    }
}
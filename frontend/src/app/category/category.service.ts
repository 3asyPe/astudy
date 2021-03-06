import { HttpClient, HttpParams } from "@angular/common/http";
import { Injectable } from "@angular/core";

@Injectable({
    providedIn: "root",
})
export class CategoryService {
    private categoryInfoUrl = "http://localhost:8000/api/category/get/";

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
}
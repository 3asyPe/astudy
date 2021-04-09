import { HttpClient, HttpParams } from "@angular/common/http"
import { Injectable } from "@angular/core"
import { BehaviorSubject } from "rxjs"
import { tap } from "rxjs/operators"
import { CartService } from "../cart.service"

@Injectable({
    providedIn: "root",
})
export class SavedForLaterService{
    private savedForLaterGetUrl = "http://localhost:8000/api/savedforlater/get/"
    private savedForLaterAddCourseUrl = "http://localhost:8000/api/savedforlater/add/"
    private savedForLaterRemoveCourseUrl = "http://localhost:8000/api/savedforlater/remove/"

    newCourse = new BehaviorSubject<any>(false)
    discounts = new BehaviorSubject<{
        course_slug: string,
        new_price: number,
        applied_coupon: string,
    }[]>([])

    constructor(private http: HttpClient,
                private cartService: CartService){ }

    fetchSavedForLaterData(){
        let params = this.cartService.createParams()
        return this.http.get<{
            id: string,
            courses: {
                slug: string,
                image: string,
                title: string,
                subtitle: string,
                price: number,
                discount: {
                    applied_coupon: string,
                    course_slug: string,
                    new_price: number,
                }|null,
            }[]
        }>(
            this.savedForLaterGetUrl,
            {
                params: params
            }
        ).pipe(
            tap(response => {
                localStorage.setItem('savedForLaterId', response.id.toString());
            })
        )
    }

    addCourseToSavedForLater(courseSlug: string){
        let params = this.cartService.createParams()
        params = params.set("course_slug", courseSlug)
        return this.http.post<{
            id: number,
            subtotal: number,
            total: number,
        }>(
            this.savedForLaterAddCourseUrl,
            params
        ).pipe(
            tap(
                response => {
                    this.cartService.getCartCoursesCount()
                    this.cartService.handleCartInfoResponse(response)
                }
            )
        )
    }

    removeCourseFromSavedForLater(courseSlug: string){
        let params = this.cartService.createParams()
        params = params.set("course_slug", courseSlug)
        return this.http.post<{}>(
            this.savedForLaterRemoveCourseUrl,
            params,
        )
    }

    handleSavedForLaterDiscountsResponse(response: {
        savedForLaterDiscounts: {
            course_slug: string,
            new_price: number,
            applied_coupon: string,
        }[]
    }){
        this.discounts.next(response.savedForLaterDiscounts)
    }
}
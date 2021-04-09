import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { BehaviorSubject } from "rxjs";
import { tap } from "rxjs/operators";
import { CartService } from "../cart.service";

@Injectable({
    providedIn: "root"
})
export class CartWishlistService{
    private wishlistGetUrl = "http://localhost:8000/api/wishlist/get/"
    private wishlistAddCourseUrl = "http://localhost:8000/api/wishlist/add/"
    private wishlistRemoveCourseUrl = "http://localhost:8000/api/wishlist/remove/"
    private wishlistCheckOnCourseAlreadyInWishlist = "http://localhost:8000/api/wishlist/checkalreadyin/"

    newCourse = new BehaviorSubject<any>(false)
    discounts = new BehaviorSubject<{
        course_slug: string,
        new_price: number,
        applied_coupon: string,
    }[]>([])

    constructor(private http: HttpClient,
                private cartService: CartService){ }

    fetchWishlistData(){
        return this.http.get<{
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
            this.wishlistGetUrl,
        )
    }

    addCourseToWishlist(courseSlug: string){
        let params = this.cartService.createParams()
        params = params.set("course_slug", courseSlug)
        return this.http.post<{
            id: number,
            subtotal: number,
            total: number,
        }>(
            this.wishlistAddCourseUrl,
            params,
        ).pipe(
            tap(
                response => {
                    this.cartService.getCartCoursesCount()
                    this.cartService.handleCartInfoResponse(response)
                }
            )
        )
    }

    removeCourseFromWishlist(courseSlug: string){
        let params = this.cartService.createParams()
        params = params.set("course_slug", courseSlug)
        return this.http.post<{}>(
            this.wishlistRemoveCourseUrl,
            params
        )
    }

    checkOnCourseAlreadyInWishlist(courseSlug: string){
        let params = this.cartService.createParams()
        params = params.set("course_slug", courseSlug)
        return this.http.get<{course_already_in_wishlist: boolean}>(
            this.wishlistCheckOnCourseAlreadyInWishlist,
            {
                params: params
            }
        )
    }

    handleWishlistDiscountsResponse(response: {
        wishlistDiscounts: {
            course_slug: string,
            new_price: number,
            applied_coupon: string,
        }[]
    }){
        this.discounts.next(response.wishlistDiscounts)
    }

}
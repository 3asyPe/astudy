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
            }[]
        }>(
            this.wishlistGetUrl,
        )
    }

    addCourseToWishlist(courseSlug: string){
        let params = this.cartService.createParamsWithIncludedCartId()
        params = params.set("course_slug", courseSlug)
        return this.http.post<{}>(
            this.wishlistAddCourseUrl,
            params,
        ).pipe(
            tap(
                response => {
                    this.cartService.getCartCoursesCount()
                }
            )
        )
    }

    removeCourseFromWishlist(courseSlug: string){
        let params = this.cartService.createParamsWithIncludedCartId()
        params = params.set("course_slug", courseSlug)
        return this.http.post<{}>(
            this.wishlistRemoveCourseUrl,
            params
        ).pipe(
            tap(
                response => {
                    this.cartService.getCartCoursesCount()
                }
            )
        )
    }

    checkOnCourseAlreadyInWishlist(courseSlug: string){
        let params = this.cartService.createParamsWithIncludedCartId()
        params = params.set("course_slug", courseSlug)
        return this.http.get<{course_already_in_wishlist: boolean}>(
            this.wishlistCheckOnCourseAlreadyInWishlist,
            {
                params: params
            }
        )
    }

}
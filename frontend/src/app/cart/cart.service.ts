import { HttpClient, HttpParams } from "@angular/common/http";
import { Injectable} from "@angular/core";
import { BehaviorSubject, Subscription } from "rxjs";
import { tap } from "rxjs/operators";
import { AuthService } from "../auth/auth.service";

@Injectable({
    providedIn: "root",
})
export class CartService{
    private cartGetUrl = "http://localhost:8000/api/cart/get/"
    private cartAddCourseUrl = "http://localhost:8000/api/cart/add/"
    private cartRemoveCourseUrl = "http://localhost:8000/api/cart/remove/"
    private cartGetCartCoursesCountUrl = "http://localhost:8000/api/cart/count/"
    private cartCheckOnCourseAlreadyInCart = "http://localhost:8000/api/cart/checkalreadyin/"

    private userSub!:Subscription;

    cartCoursesCount = new BehaviorSubject<number>(0)
    newCourse = new BehaviorSubject<{
        slug: string,
        image: string,
        title: string,
        subtitle: string,
        price: number
    }|null>(null)
    subTotal = new BehaviorSubject<number>(0.00)
    total = new BehaviorSubject<number>(0.00)

    constructor(private http: HttpClient,
                private authService: AuthService,){ }

    manuallyInitializeService(){
        this.userSub = this.authService.user.subscribe(
            user => {
                this.getCartCoursesCount()
            }
        )
    }

    fetchCartData(){
        let params = this.createParams()
        return this.http.get<{
            id: number, 
            courses: {
                slug: string,
                image: string,
                title: string,
                subtitle: string,
                price: number
            }[],
            subtotal: number,
            total: number,
        }>(
            this.cartGetUrl,
            {
                params: params
            }
        ).pipe(
            tap(response => {
                localStorage.setItem('cartId', response.id.toString());
            })
        )
    }

    addCourseToCart(courseSlug: string){
        let params = this.createParams()
        params = params.set("course_slug", courseSlug)
        return this.http.post<{
            id: number,
            subtotal: number,
            total: number,
        }>(
            this.cartAddCourseUrl,
            params,
        ).pipe(
            tap(response => {
                this.getCartCoursesCount()
                this.handleCartInfoResponse(response)
            })
        )
    }

    removeCourseFromCart(courseSlug: string){
        let params = this.createParams()
        params = params.set("course_slug", courseSlug)
        return this.http.post<{
            id: number,
            subtotal: number,
            total: number,
        }>(
            this.cartRemoveCourseUrl,
            params,
        ).pipe(
            tap(response => {
                this.getCartCoursesCount()
                this.handleCartInfoResponse(response)
            })
        )
    }

    getCartCoursesCount(){
        let params = this.createParams()
        this.http.get<{
            cart_courses_count: number,
            cart_id: number,
        }>(
            this.cartGetCartCoursesCountUrl,
            {
                params: params
            }
        ).subscribe(
            response => {
                this.cartCoursesCount.next(response.cart_courses_count)
                localStorage.setItem('cartId', response.cart_id.toString());
            }
        )
    }

    checkOnCourseAleadyInCart(courseSlug: string){
        let params = this.createParams()
        params = params.set("course_slug", courseSlug)
        return this.http.get<{course_already_in_cart: boolean}>(
            this.cartCheckOnCourseAlreadyInCart,
            {
                params: params
            }
        )
    }

    handleCartInfoResponse(response: {
        id: number,
        subtotal: number,
        total: number,
    }){
        this.subTotal.next(response.subtotal)
        this.total.next(response.total)
    }

    createParams(){
        const cartId =  localStorage.getItem('cartId')
        const savedForLaterId = localStorage.getItem('savedForLaterId')
        let params = new HttpParams()
        if (cartId || cartId === "0"){
            params = params.set("cart_id", cartId)
        }
        if (savedForLaterId || savedForLaterId === "0"){
            params = params.set("saved_for_later_id", savedForLaterId)
        }
        return params
    }
}
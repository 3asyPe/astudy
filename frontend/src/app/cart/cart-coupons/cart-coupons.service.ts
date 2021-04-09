import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { BehaviorSubject } from "rxjs";
import { tap } from "rxjs/operators";
import { CartWishlistService } from "../cart-wishlist/cart-wishlist.service";
import { CartService } from "../cart.service";
import { SavedForLaterService } from "../saved-for-later/saved-for-later.service";


interface DiscountsResponse{
    id: number,
    cart_discounts: {
        course_slug: string,
        new_price: number,
        applied_coupon: string,
    }[],
    wishlist_discounts: {
        course_slug: string,
        new_price: number,
        applied_coupon: string,
    }[],
    saved_for_later_discounts: {
        course_slug: string,
        new_price: number,
        applied_coupon: string,
    }[],
    subtotal: number,
    total: number,
}


@Injectable({
    providedIn: "root",
})
export class CartCouponsService{
    private applyCouponUrl = "http://localhost:8000/api/coupon/apply/"
    private removeCouponUrl = "http://localhost:8000/api/coupon/cancel/"

    coupons = new BehaviorSubject<{code: string}[]>([])

    constructor(private http: HttpClient,
                private cartService: CartService,
                private wishlistServices: CartWishlistService,
                private savedForLaterServices: SavedForLaterService){ }

    applyCoupon(code: string){
        return this.sendRequest(code, this.applyCouponUrl)
    }

    removeCoupon(code: string){
        return this.sendRequest(code, this.removeCouponUrl)
    }

    private sendRequest(code: string, url: string){
        let params = this.cartService.createParams()
        params = params.set("coupon_code", code)
        return this.http.post<DiscountsResponse>(
            url,
            params
        ).pipe(
            tap(
                response => {
                    this.handleDiscountsResponse(response)
                }
            )
        )
    }

    handleDiscountsResponse(response: DiscountsResponse){
        this.cartService.handleCartDiscountsResponse({
            cartDiscounts: response.cart_discounts,
            subtotal: response.subtotal,
            total: response.total,
        })
        this.wishlistServices.handleWishlistDiscountsResponse({
            wishlistDiscounts: response.wishlist_discounts
        })
        this.savedForLaterServices.handleSavedForLaterDiscountsResponse({
            savedForLaterDiscounts: response.saved_for_later_discounts
        })
    }
}
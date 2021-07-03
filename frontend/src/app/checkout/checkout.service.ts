import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";

@Injectable({
    providedIn: "root"
})
export class CheckoutService{
    billingProfileGetUrl = "http://localhost:8000/api/billing/get/"

    constructor(private http: HttpClient){}

    fetchBillingProfileData(){
        return this.http.get<{
            country: string,
            postal_code: string,
            cards: {
                brand: string,
                last4: string,
                default: string,
            }[]
        }>(this.billingProfileGetUrl)
    }
}
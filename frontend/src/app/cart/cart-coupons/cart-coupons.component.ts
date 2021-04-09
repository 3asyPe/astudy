import { Component, Input, OnDestroy, OnInit } from '@angular/core';
import { Subscription } from 'rxjs';
import { CartCouponsService } from './cart-coupons.service';

@Component({
  selector: 'app-cart-coupons',
  templateUrl: './cart-coupons.component.html',
  styleUrls: ['./cart-coupons.component.css']
})
export class CartCouponsComponent implements OnInit, OnDestroy {

  private couponsSub!: Subscription

  coupons: {code: string}[] = []
  error = false

  constructor(private cartCouponsService: CartCouponsService) { }

  ngOnInit(): void {
    this.couponsSub = this.cartCouponsService.coupons.subscribe(
      coupons => {
        this.coupons = coupons
      }
    )
  }

  applyCoupon(code: string){
    for(let coupon of this.coupons){
      if (coupon.code === code){
        return
      }
    }
    this.cartCouponsService.applyCoupon(code).subscribe(
      (response) => {
        this.coupons.push({code: code})
      },
      (error) => {
        console.log(error)
        if (error.error === "INVALID_APPLIED_COUPON_ERROR"){
          this.error = true
        }
      }
    )
  }

  removeCoupon(code: string, index: number){
    this.cartCouponsService.removeCoupon(code).subscribe(
      response => {
        this.coupons.splice(index, 1)
      }
    )
  }

  onInput(){
    this.error = false
  }

  ngOnDestroy(){
    this.couponsSub.unsubscribe()
  }

}

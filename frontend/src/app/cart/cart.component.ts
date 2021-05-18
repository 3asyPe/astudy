import { Component, OnDestroy, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { Subscription } from 'rxjs';

import { AuthService } from '../auth/auth.service';
import { User } from '../auth/user.model';
import { CartCouponsService } from './cart-coupons/cart-coupons.service';
import { CartWishlistService } from './cart-wishlist/cart-wishlist.service';
import { CartService } from './cart.service';
import { SavedForLaterService } from './saved-for-later/saved-for-later.service';

@Component({
  selector: 'app-cart',
  templateUrl: './cart.component.html',
  styleUrls: ['./cart.component.css']
})
export class CartComponent implements OnInit, OnDestroy {

  private userSub!: Subscription;
  private updateSub!: Subscription;
  private totalSub!: Subscription;
  private subTotalSub!: Subscription;
  private discountsSub!: Subscription;
  user: User|null = null;

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
      }|null
  }[] = []
  appliedCoupons: {
    code: string
  }[] = []
  subTotal = 0.00
  total = 0.00

  constructor(private authService: AuthService, 
              private cartService: CartService,
              private cartCouponsServices: CartCouponsService,
              private wishlistService: CartWishlistService,
              private savedForLaterService: SavedForLaterService,
              private router: Router) { }

  ngOnInit(): void {
    this.userSub = this.authService.user.subscribe(
      user => {
        this.user = user
        this.fetchCartData()
      }
    )
    this.updateSub = this.cartService.newCourse.subscribe(
      newCourse => {
        if(newCourse){
          this.courses.push(newCourse)
        }
      }
    )
    this.totalSub = this.cartService.total.subscribe(
      total => {
        this.total = total
      }
    )
    this.subTotalSub = this.cartService.subTotal.subscribe(
      subTotal => {
        this.subTotal = subTotal
      }
    )
    this.discountsSub = this.cartService.discounts.subscribe(
      discounts => {
        this.setUpDiscounts(discounts)
      }
    )
  }

  fetchCartData(){
    this.cartService.fetchCartData().subscribe(
      response => {
        this.courses = response.courses
        this.subTotal = response.subtotal
        this.total = response.total
        this.cartCouponsServices.coupons.next(response.applied_coupons)
      }
    )
  }

  moveCourseToWishlist(courseSlug: string, courseIndex: number){
    this.wishlistService.addCourseToWishlist(courseSlug).subscribe(
      response => {
        this.wishlistService.newCourse.next(this.courses[courseIndex])
        this.courses.splice(courseIndex, 1)
      }
    )
  }

  moveCourseToSavedForLater(courseSlug: string, courseIndex: number){
    this.savedForLaterService.addCourseToSavedForLater(courseSlug).subscribe(
      response => {
        this.savedForLaterService.newCourse.next(this.courses[courseIndex])
        this.courses.splice(courseIndex, 1)
      }
    )
  }

  removeCourseFromCart(courseSlug: string, courseIndex: number){
    this.cartService.removeCourseFromCart(courseSlug).subscribe(
      response => {
        this.courses.splice(courseIndex, 1)
      }
    )
  }

  setUpDiscounts(discounts: {
    course_slug: string,
    new_price: number,
    applied_coupon: string,
  }[]){
    this.courses.forEach(course => {
      let reached = false
      for (let discount of discounts){
        if (course.slug === discount.course_slug){
          course.discount = discount
          reached = true
          break
        }
      }
      if (!reached){
        course.discount = null
      }
    })
  }

  checkout(){
    this.router.navigateByUrl('/cart/checkout');
  }


  ngOnDestroy(){
    this.userSub.unsubscribe()
    this.updateSub.unsubscribe()
    this.totalSub.unsubscribe()
    this.subTotalSub.unsubscribe()
    this.discountsSub.unsubscribe()
  }

}

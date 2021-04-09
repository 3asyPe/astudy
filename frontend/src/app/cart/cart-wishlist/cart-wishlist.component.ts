import { Component, OnDestroy, OnInit } from '@angular/core';
import { Subscription } from 'rxjs';
import { AuthService } from 'src/app/auth/auth.service';
import { CartService } from '../cart.service';
import { CartWishlistService } from './cart-wishlist.service';

@Component({
  selector: 'app-cart-wishlist',
  templateUrl: './cart-wishlist.component.html',
  styleUrls: ['./cart-wishlist.component.css']
})
export class CartWishlistComponent implements OnInit, OnDestroy {

  private userSub!: Subscription
  private updateSub!: Subscription
  private discountsSub!: Subscription;

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

  constructor(private authService: AuthService,
              private wishlistService: CartWishlistService,
              private cartService: CartService) { }

  ngOnInit(): void {
    this.userSub = this.authService.user.subscribe(
      user => {
        if (user){
          this.fetchWishlistData()
        }
      }
    )
    this.updateSub = this.wishlistService.newCourse.subscribe(
      newCourse => {
        if(newCourse){
          this.courses.push(newCourse)
        }
      }
    )
    this.discountsSub = this.wishlistService.discounts.subscribe(
      discounts => {
        this.setUpDiscounts(discounts)
      }
    )
  }

  fetchWishlistData(){
    this.wishlistService.fetchWishlistData().subscribe(
      response => {
        this.courses = response.courses
      }
    )
  }

  moveCourseToCart(courseSlug: string, courseIndex: number){
    this.cartService.addCourseToCart(courseSlug).subscribe(
      response => {
        this.cartService.newCourse.next(this.courses[courseIndex])
        this.courses.splice(courseIndex, 1)
      }
    )
  }

  removeCourseFromWishlist(courseSlug: string, courseIndex: number){
    this.wishlistService.removeCourseFromWishlist(courseSlug).subscribe(
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

  ngOnDestroy(){
    this.userSub.unsubscribe()
    this.updateSub.unsubscribe()
    this.discountsSub.unsubscribe()
  }

}

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

  courses: {
    slug: string,
    image: string,
    title: string,
    subtitle: string,
    price: number
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

  ngOnDestroy(){
    this.userSub.unsubscribe()
    this.updateSub.unsubscribe()
  }

}

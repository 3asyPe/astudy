import { Component, OnDestroy, OnInit } from '@angular/core';
import { Subscription } from 'rxjs';
import { AuthService } from 'src/app/auth/auth.service';
import { User } from 'src/app/auth/user.model';
import { CartService } from '../cart.service';
import { SavedForLaterService } from './saved-for-later.service';

@Component({
  selector: 'app-saved-for-later',
  templateUrl: './saved-for-later.component.html',
  styleUrls: ['./saved-for-later.component.css']
})
export class SavedForLaterComponent implements OnInit, OnDestroy {

  private userSub!: Subscription;
  private updateSub!: Subscription
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
  }|null,
  }[] = []

  constructor(private authService: AuthService,
              private savedForLaterService: SavedForLaterService,
              private cartService: CartService) { }

  ngOnInit(): void {
    this.userSub = this.authService.user.subscribe(
      user => {
        this.user = user
        this.fetchSavedForLaterData()
      }
    )
    this.updateSub = this.savedForLaterService.newCourse.subscribe(
      newCourse => {
        if(newCourse){
          this.courses.push(newCourse)
        }
      }
    )
    this.discountsSub = this.savedForLaterService.discounts.subscribe(
      discounts => {
        this.setUpDiscounts(discounts)
      }
    )
  }

  fetchSavedForLaterData(){
    this.savedForLaterService.fetchSavedForLaterData().subscribe(
      response => {
        console.log(response)
        this.courses = response.courses
      }
    )
  }

  removeCourseFromSavedForLater(courseSlug: string, courseIndex: number){
    this.savedForLaterService.removeCourseFromSavedForLater(courseSlug).subscribe(
      response => {
        this.courses.splice(courseIndex, 1)
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

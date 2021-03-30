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
  user: User|null = null;

  courses: {
    slug: string,
    image: string,
    title: string,
    subtitle: string,
    price: number
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

  ngOnDestroy(){
    this.userSub.unsubscribe()
    this.updateSub.unsubscribe()
  }

}

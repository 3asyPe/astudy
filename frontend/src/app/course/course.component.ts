import { animate, state, style, transition, trigger } from '@angular/animations';
import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { ActivatedRoute, Params } from '@angular/router';
import { CartWishlistService } from '../cart/cart-wishlist/cart-wishlist.service';
import { CartService } from '../cart/cart.service';
import { Course } from './course.model';
import { CourseService } from './course.service';

@Component({
  selector: 'app-course',
  templateUrl: './course.component.html',
  styleUrls: ['./course.component.css'],
  animations: [
    trigger('openCloseSection', [
      state('true', style({
        "max-height": "200px",
        width: "100%",
        overflow: "hidden",
        padding: "20px 40px",
        opacity: 1,
      })),
      state('false', style({
        "max-height": "0px",
        width: "0",
        overflow: "hidden",
        padding: "0",
        opacity: 0,
      })),
      transition('true => false', [
        animate('0.4s ease')
      ]),
      transition('false => true', [
        animate('0.4s ease')
      ]),
    ]),
    trigger('openCloseLectureDescription', [
      state('true', style({
        "max-height": "100px",
        overflow: "hidden",
        "padding": "8px 0",
        opacity: 1,
      })),
      state('false', style({
        "max-height": "0px",
        overflow: "hidden",
        padding: "0",
        opacity: 0,
      })),
      transition('true => false', [
        animate('0.3s ease')
      ]),
      transition('false => true', [
        animate('0.3s ease')
      ]),
    ]),
  ],
})
export class CourseComponent implements OnInit {

  slug = ""
  title = "Course"
  subtitle = "Some course"
  imageUrl = ""
  price = 39.99
  description = "Some description"
  studentsCount = 123
  sectionsCount = 3
  lecturesCount = 35
  articlesCount = 0
  resourcesCount = 0
  assignmentsCount = 0
  durationTime = {
    hours: 8,
    minutes: 35
  }
  goals = [
    {goal: "Some goal number 1"},
    {goal: "Some goal number 2"},
    {goal: "Some goal number 3"},
    {goal: "Some goal number 4"},
  ]
  requirements = [
    {requirement: "Some requirement number 1"},
    {requirement: "Some requirement number 2"},
    {requirement: "Some requirement number 3"},
    {requirement: "Some requirement number 4"},
  ]
  sections = [
    {
      title: "introduction",
      lectures_count: 3,
      duration_time: {
        hours: 1,
        minutes: 25
      },
      lectures: [
        {
          "free_opened": true,
          "title": "Course Introduction",
          "description": "Welcome to this course! Let me introduce myself and explain what the course is about!",
          "duration_time": {
              "hours": 0,
              "minutes": 5,
              "seconds": 12
          }
        },
        {
            "free_opened": false,
            "title": "Software",
            "description": null,
            "duration_time": {
                "hours": 0,
                "minutes": 13,
                "seconds": 52
            }
        },
        {
            "free_opened": false,
            "title": "System setup",
            "description": null,
            "duration_time": {
                "hours": 0,
                "minutes": 21,
                "seconds": 15
            }
        }
      ]
    }
  ]
  alreadyInCart = false;
  alraedyInWihlist = false;

  addToWishlistIsLoading = false

  openedGoalsList = false;
  openedDescription = false;
  openedAllSections = false;
  
  constructor(private cartService: CartService,
              private wishlistService: CartWishlistService,
              private courseService: CourseService,
              private _changeDetectionRef : ChangeDetectorRef,
              private route: ActivatedRoute) { }

  ngOnInit(): void {
    this.route.params.subscribe(
      (params: Params) => {
        this.slug = params["slug"]
        this.fetchCourseInfo()
      }
    )
  }

  fetchCourseInfo(){
    this.courseService.fetchCourseInfo(this.slug).subscribe(
      course => {
        this.parseCourseResponse(course)
        this.checkOnCourseAleadyInCart()
        this.checkOnCourseAlreadyInWishlist()
      }
    )
  }

  parseCourseResponse(courseRes: Course) {
    this.slug = courseRes.slug
    this.title = courseRes.title
    this.subtitle = courseRes.subtitle
    this.imageUrl = courseRes.image
    this.price = courseRes.price
    this.description = courseRes.description
    this.studentsCount = courseRes.students_count
    this.goals = courseRes.goals
    this.requirements = courseRes.requirements

    const content = courseRes.content

    this.sectionsCount = content.sections_count
    this.lecturesCount = content.lectures_count
    this.articlesCount = content.articles_count
    this.resourcesCount = content.resources_count
    this.assignmentsCount = content.assignments_count
    this.durationTime = content.duration_time
    
    const sections = content.sections

    this.sections = sections
    this._changeDetectionRef.detectChanges();
  }

  addCourseToCart(){
    if (!this.slug){
      return
    } 

    this.cartService.addCourseToCart(this.slug).subscribe(
      response => {
        this.alreadyInCart = true
        this.alraedyInWihlist = false
      }
    )
  }

  checkOnCourseAleadyInCart(){
    this.cartService.checkOnCourseAleadyInCart(this.slug).subscribe(
      response => {
        this.alreadyInCart = response.course_already_in_cart
      }
    )
  }

  addOrRemoveCourseToWishlist(){
    if (!this.slug){
      return
    }

    this.addToWishlistIsLoading = true

    if (!this.alraedyInWihlist){ 
      this.wishlistService.addCourseToWishlist(this.slug).subscribe(
        response => {
          this.alreadyInCart = false
          this.alraedyInWihlist = true
          this.addToWishlistIsLoading = false
        }
      )
    } else {
      this.wishlistService.removeCourseFromWishlist(this.slug).subscribe(
        response => {
          this.alraedyInWihlist = false
          this.addToWishlistIsLoading = false
        }
      )
    }
  }

  checkOnCourseAlreadyInWishlist(){
    this.wishlistService.checkOnCourseAlreadyInWishlist(this.slug).subscribe(
      response => {
        this.alraedyInWihlist = response.course_already_in_wishlist
      }
    )
  }

  openSection(section: HTMLElement){
    if(section.classList.contains("faq-active")){
      section.classList.remove("faq-active")
    } else {
      section.classList.add("faq-active")
    }
  }

  openLectureDescription(lecturename: HTMLElement){
    if(lecturename.classList.contains("active")){
      lecturename.classList.remove("active")
    } else {
      lecturename.classList.add("active")
    }
  }

  switchGoalsListOpenMode() {
    this.openedGoalsList = !this.openedGoalsList
  }

  switchDescriptionOpenMode() {
    this.openedDescription = !this.openedDescription
  }

  openAllSections() {
    this.openedAllSections = true
  }

}

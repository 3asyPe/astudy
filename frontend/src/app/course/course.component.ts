import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Params } from '@angular/router';
import { Observable } from 'rxjs';
import { Course } from './course.model';
import { CourseService } from './course.service';

@Component({
  selector: 'app-course',
  templateUrl: './course.component.html',
  styleUrls: ['./course.component.css']
})
export class CourseComponent implements OnInit {

  slug = ""
  title = "Course"
  subtitle = "Some course"
  imageUrl = ""
  price = 39.99
  description = "Some description"
  studentsCount = 123
  lecturesCount = 35
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

  openedGoalsList = false;
  openedDescription = false;
  openedAllSections = false;
  
  constructor(private courseService: CourseService,
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
        this.slug = course.slug
        this.title = course.title
        this.subtitle = course.subtitle
        this.imageUrl = course.image
        this.price = course.price
        this.description = course.description
        this.studentsCount = course.students_count
        this.lecturesCount = course.lectures_count
        this.durationTime = course.duration_time
        this.goals = course.goals
        this.requirements = course.requirements
      }
    )
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

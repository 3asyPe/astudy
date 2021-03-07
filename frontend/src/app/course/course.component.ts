import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-course',
  templateUrl: './course.component.html',
  styleUrls: ['./course.component.css']
})
export class CourseComponent implements OnInit {

  openedGoalsList = false;
  openedDescription = false;
  openedAllSections = false;
  
  constructor() { }

  ngOnInit(): void {
  }

  switchGoalsListOpenMode() {
    this.openedGoalsList = !this.openedGoalsList
  }

  switchDescriptionOpenMode() {
    this.openedDescription = !this.openedDescription
  }

  openAllSections() {
    console.log("OPEN")
    this.openedAllSections = true
  }

}

import { Time } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Params } from '@angular/router';
import { CategoryCourse } from './category-course.model';
import { CategoryService } from './category.service';

@Component({
  selector: 'app-category',
  templateUrl: './category.component.html',
  styleUrls: ['./category.component.css']
})
export class CategoryComponent implements OnInit {

  title = "";
  slug = "";
  courses: CategoryCourse[] = [];

  constructor(private categoryService: CategoryService,
              private route: ActivatedRoute) { }

  ngOnInit(): void {
    this.route.params.subscribe(
      (params: Params) => {
        this.slug = params["slug"]
        this.fetchCategoryInfo()
        this.fetchCategoryCourses()
      }
    )
  }

  fetchCategoryInfo() {
    this.categoryService.fetchCategoryInfo(this.slug).subscribe(
      category => {
        this.title = category.title
      }
    )
  }

  fetchCategoryCourses() {
    this.categoryService.fetchCategoryCourses(this.slug).subscribe(
      courses => {
        this.courses = []
        for (let course of courses) {
          this.courses.push(new CategoryCourse(
            course.slug,
            course.image,
            course.title,
            course.subtitle,
            course.price,
            course.lectures_count,
            course.duration_time,
          ))
        }
      }
    )
  }

}

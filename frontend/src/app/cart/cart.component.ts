import { Component, OnDestroy, OnInit } from '@angular/core';
import { Subscription } from 'rxjs';
import { CartService } from './cart.service';

@Component({
  selector: 'app-cart',
  templateUrl: './cart.component.html',
  styleUrls: ['./cart.component.css']
})
export class CartComponent implements OnInit, OnDestroy {

  courses: {
      slug: string,
      image: string,
      title: string,
      subtitle: string,
      price: number
  }[] = []
  subtotal = 0.00
  total = 0.00

  constructor(private cartService: CartService) { }

  ngOnInit(): void {
    this.fetchCartData()
  }

  fetchCartData(){
    this.cartService.fetchCartData().subscribe(
      response => {
        this.courses = response.courses
        this.subtotal = response.subtotal
        this.total = response.total
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

  ngOnDestroy(){
    
  }

}
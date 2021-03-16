import { Component, OnInit, ViewEncapsulation  } from '@angular/core';
import { AuthService } from './auth/auth.service';
import { CartService } from './cart/cart.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  encapsulation: ViewEncapsulation.None,
})
export class AppComponent implements OnInit{
  title = 'AStudy';

  constructor(private authService: AuthService,
              private cartService: CartService) { }

  ngOnInit(){
    this.authService.autoLogin()
    this.cartService.getCartCoursesCount()
  }
}

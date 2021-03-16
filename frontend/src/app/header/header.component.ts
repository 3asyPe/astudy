import { Component, OnDestroy, OnInit } from '@angular/core';
import { Subscription } from 'rxjs';
import { AuthService } from '../auth/auth.service';
import { User } from '../auth/user.model';
import { CartService } from '../cart/cart.service';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit, OnDestroy {

  menuOpened = false;
  mobileNextMenuOpened = false;
  user: User|null = null;
  cartCoursesCount = 0;
  cartCoursesSub!: Subscription;
  private userSub!: Subscription;

  constructor(private authService: AuthService,
              private cartService: CartService) { }

  ngOnInit(): void {
    this.userSub = this.authService.user.subscribe(
      user => {
        this.user = user
      }
    )
    this.cartCoursesSub = this.cartService.cartCoursesCount.subscribe(
      count => {
        this.cartCoursesCount = count
        console.log(this.cartCoursesCount)
      }
    )
  }

  onLogout() {
    this.authService.logout()
  }

  onOpenMenu(){
    this.menuOpened = true;
  }

  onCloseMenu(){
    this.menuOpened = false;
  }

  onOpenMobileNextMenu() {
    console.log("open")
    this.mobileNextMenuOpened = true;
  }

  onCloseMobileNextMenu() {
    this.mobileNextMenuOpened = false;
  }

  onOpenAuthModal() {
    this.onCloseMenu()
    this.authService.openModal()
  }

  onOpenAuthSignInModal() {
    this.onCloseMenu()
    this.authService.openSignInModal()
  }

  onOpenAuthSignUpModal() {
    this.onCloseMenu()
    this.authService.openSignUpModal()
  }

  ngOnDestroy() {
    this.userSub.unsubscribe()
    this.cartCoursesSub.unsubscribe()
  }

}

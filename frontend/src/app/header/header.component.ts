import { ThrowStmt } from '@angular/compiler';
import { Component, OnInit } from '@angular/core';
import { EventManager } from '@angular/platform-browser';
import { AuthService } from '../auth/auth.service';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit {

  menuOpened = false;

  constructor(private authService: AuthService) { }

  ngOnInit(): void {

  }

  onOpenMenu(){
    this.menuOpened = true;
  }

  onCloseMenu(){
    this.menuOpened = false;
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

}

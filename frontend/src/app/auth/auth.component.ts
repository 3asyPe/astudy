import { Component, OnDestroy, OnInit } from '@angular/core';
import { Form, NgForm } from '@angular/forms';
import { Subscription } from 'rxjs';
import { AuthService } from './auth.service';


@Component({
  selector: 'app-auth',
  templateUrl: './auth.component.html',
  styleUrls: ['./auth.component.css']
})
export class AuthComponent implements OnInit, OnDestroy {

  modalOpened = false;
  signInMode = true;

  private userSub!: Subscription;
  
  private modalSub!: Subscription;
  private modalModeSub!: Subscription;

  constructor(private authService: AuthService) { }

  ngOnInit(): void {
    this.modalSub = this.authService.openedAuthModal.subscribe(opened => {
      this.modalOpened = opened
    })
    this.modalModeSub = this.authService.openedSignInModal.subscribe(signInMode => {
      this.signInMode = signInMode;
    })
  }

  onSignInModeChange(): void {
    this.signInMode = true;
  }

  onSignUpModeChange(): void {
    this.signInMode = false;
  }

  onCloseModal(): void {
    this.authService.closeModal()
  }

  onSignInSubmit(form: NgForm) {
    console.log(form)
    this.userSub = this.authService.signin(
      form.value.email,
      form.value.password,
    ).subscribe()
  }

  onSignUpSubmit(form: NgForm) {
    console.log(form)
    this.userSub = this.authService.signup(
      form.value.name,
      form.value.email, 
      form.value.password
    ).subscribe()
  }

  ngOnDestroy(): void {
    this.modalSub.unsubscribe()
    this.modalModeSub.unsubscribe()
    this.userSub.unsubscribe()
  }
 
}

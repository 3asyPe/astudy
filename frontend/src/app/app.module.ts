import { AngularSvgIconModule } from 'angular-svg-icon';
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { TooltipModule } from 'ng2-tooltip-directive';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HeaderComponent } from './header/header.component';
import { HomeComponent } from './home/home.component';
import { AuthComponent } from './auth/auth.component';
import { FormsModule } from '@angular/forms';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { AuthInterceptorService } from './auth/auth-interceptor.service';
import { CategoryComponent } from './category/category.component';
import { CourseComponent } from './course/course.component';
import { CartComponent } from './cart/cart.component';
import { CartWishlistComponent } from './cart/cart-wishlist/cart-wishlist.component';
import { SavedForLaterComponent } from './cart/saved-for-later/saved-for-later.component';
import { CartCouponsComponent } from './cart/cart-coupons/cart-coupons.component';
import { TooltipDirective } from './shared/tooltip.directive';
import { CheckoutComponent } from './checkout/checkout.component';

@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    HomeComponent,
    AuthComponent,
    CategoryComponent,
    CourseComponent,
    CartComponent,
    CartWishlistComponent,
    SavedForLaterComponent,
    CartCouponsComponent,
    CheckoutComponent,
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    FormsModule,
    AppRoutingModule,
    HttpClientModule,
    AngularSvgIconModule.forRoot(),
    TooltipModule,
  ],
  providers: [
    {
      provide: HTTP_INTERCEPTORS,
      useClass: AuthInterceptorService,
      multi: true,
    }
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }

import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CartComponent } from './cart/cart.component';
import { CategoryComponent } from './category/category.component';
import { CheckoutComponent } from './checkout/checkout.component';
import { CourseComponent } from './course/course.component';
import { HomeComponent } from './home/home.component';

const routes: Routes = [
  { path: "", component: HomeComponent, pathMatch: "full" },
  { path: "home", redirectTo: "/" },
  { path: "cart", component: CartComponent, pathMatch:"full" },
  { path: "cart/checkout", component: CheckoutComponent, pathMatch:"full" },
  { path: "course/:slug", component: CourseComponent, pathMatch:"full" },
  { path: "courses/:slug", component: CategoryComponent, pathMatch:"full" },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }

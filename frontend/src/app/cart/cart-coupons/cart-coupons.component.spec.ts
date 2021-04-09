import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CartCouponsComponent } from './cart-coupons.component';

describe('CartCouponsComponent', () => {
  let component: CartCouponsComponent;
  let fixture: ComponentFixture<CartCouponsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CartCouponsComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(CartCouponsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

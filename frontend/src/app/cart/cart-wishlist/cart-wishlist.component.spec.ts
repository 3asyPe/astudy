import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CartWishlistComponent } from './cart-wishlist.component';

describe('CartWishlistComponent', () => {
  let component: CartWishlistComponent;
  let fixture: ComponentFixture<CartWishlistComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CartWishlistComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(CartWishlistComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

import { AfterViewInit, Component, ElementRef, Input, OnDestroy, OnInit, QueryList, ViewChild, ViewChildren } from '@angular/core';
import { Router } from '@angular/router';
import { Subscription } from 'rxjs';
import { connectableObservableDescriptor } from 'rxjs/internal/observable/ConnectableObservable';
import { AuthService } from '../auth/auth.service';
import { User } from '../auth/user.model';
import { CartService } from '../cart/cart.service';
import { CheckoutService } from './checkout.service';

declare var Stripe: stripe.StripeStatic;

@Component({
  selector: 'app-checkout',
  templateUrl: './checkout.component.html',
  styleUrls: ['./checkout.component.css']
})
export class CheckoutComponent implements OnInit, OnDestroy, AfterViewInit {

    courses: {
        slug: string,
        image: string,
        title: string,
        subtitle: string,
        price: number,
        discount: {
          applied_coupon: string,
          course_slug: string,
          new_price: number,
        }|null
    }[] = [];
    subtotal = 0.00;
    total = 0.00;

    country = "Belarus";
    cards!: {
        brand: string,
        last4: string,
        default: string,
    }[];

    stripe: any;
    cardNumber: any;
    @ViewChildren('cardNumber') cardNumberElement!: QueryList<ElementRef>;
    
    cardExpiry: any;
    @ViewChildren('cardExpiry') cardExpiryElement!: QueryList<ElementRef>;

    cardCvc: any;
    @ViewChildren('cardCvc') cardCvcElement!: QueryList<ElementRef>;

    cardHolderName!: string;
    cardHolderZip!: string;

    cardErrors: any;
    rememberCard = true;

    @Input() paymentMethod = 'newPaymentCard';
    loading = false
    confirmation: any;

    userSub!: Subscription;
    user: User|null = null;

    constructor(private authService: AuthService,
                private cartService: CartService,
                private checkoutService: CheckoutService,
                private router: Router) { }

    ngOnInit(): void {
        this.userSub = this.authService.user.subscribe(
            user => {
                this.user = user
                if (!this.user){

                } else { 
                    this.fetchBillingProfile()
                    this.fetchOrderDetails()
                }
            }
          )

        this.stripe = Stripe('pk_test_51IrhuLAGKJR9v1iN5uumvTHrdJLWXh88hh0V8tjNdt77gmt3c0WVcYlVF36eVcljKL1yKTQbbSGTLtMZS1e7XTfj005p457g4n')
    }

    ngAfterViewInit(){
        var elements = this.stripe.elements();
        this.cardNumber = elements.create('cardNumber', {
            classes: {base: 'input card-input'},
            style: {
                base: {
                    fontFamily: 'Arial',
                    fontWeight: '500',
                    fontSize: '15px',
                },

            },
            placeholder: 'Card Number',
        });
        this.cardNumber.mount(this.cardNumberElement.first.nativeElement)

        this.cardExpiry = elements.create('cardExpiry', {
            classes: {base: 'input card-input'},
            style: {
                base: {
                    fontFamily: 'Arial',
                    fontWeight: '500',
                    fontSize: '15px',
                },

            },
            placeholder: 'MM/YY',
        });
        this.cardExpiry.mount(this.cardExpiryElement.first.nativeElement)

        this.cardCvc = elements.create('cardCvc', {
            classes: {base: 'input card-input'},
            style: {
                base: {
                    fontFamily: 'Arial',
                    fontWeight: '500',
                    fontSize: '15px',
                },

            },
            placeholder: 'Security Code',
        });
        this.cardCvc.mount(this.cardCvcElement.first.nativeElement)
    }

    fetchBillingProfile(){
        this.loading = true
        this.checkoutService.fetchBillingProfileData().subscribe(
            billing_profile => {
                this.country = billing_profile.country
                this.cardHolderZip = billing_profile.postal_code
                this.cards = billing_profile.cards
                this.loading = false
            }
        )
    }

    fetchOrderDetails(){
        this.loading = true
        this.cartService.fetchCartData().subscribe(
            data => {
                console.log(data)
                if (data.courses.length === 0){
                    this.router.navigateByUrl('/cart');
                }
                this.courses = data.courses
                this.subtotal = data.subtotal
                this.total = data.total
                this.loading = false
            }
        )
    }

    async handleCardConfirmation(){
        this.loading = true
        const {token, error} = await this.stripe.createToken(this.cardNumber, {
            name: this.cardHolderName,
            address_zip: this.cardHolderZip,
        })
        console.log(token)
        if (error){
            console.log(error)
            this.cardErrors = error.message
            this.loading = false
        } else {
            this.cardErrors = []
        }
    }

    seperateCardDate(value: string){
        var regExp = /(1[0-2]|0[1-9]|\d)\/(20\d{2}|19\d{2}|0(?!0)\d|[1-9]\d)/;
        var matches = regExp.exec(value);
        if (matches){
            
        }
    }

    ngOnDestroy(){
        this.userSub.unsubscribe()
    }

}

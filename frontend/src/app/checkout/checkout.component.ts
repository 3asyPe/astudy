import { AfterViewInit, Component, ElementRef, Input, OnDestroy, OnInit, QueryList, ViewChild, ViewChildren } from '@angular/core';
import { Subscription } from 'rxjs';
import { connectableObservableDescriptor } from 'rxjs/internal/observable/ConnectableObservable';
import { AuthService } from '../auth/auth.service';
import { User } from '../auth/user.model';

declare var Stripe: stripe.StripeStatic;

@Component({
  selector: 'app-checkout',
  templateUrl: './checkout.component.html',
  styleUrls: ['./checkout.component.css']
})
export class CheckoutComponent implements OnInit, OnDestroy, AfterViewInit {

    total = '';

    country!: string;

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

    @Input() paymentMethod = 'newPaymentCard';
    loading = false
    confirmation: any;

    userSub!: Subscription;
    user: User|null = null;

    constructor(private authService: AuthService) { }

    ngOnInit(): void {
        this.userSub = this.authService.user.subscribe(
            user => {
              this.user = user
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
        this.cardNumberElement.changes.subscribe(item => {
            this.cardNumber.mount(this.cardNumberElement.first.nativeElement)
        })

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
        this.cardExpiryElement.changes.subscribe(item => {
            this.cardExpiry.mount(this.cardExpiryElement.first.nativeElement)
        })

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
        this.cardCvcElement.changes.subscribe(item => {
            this.cardCvc.mount(this.cardCvcElement.first.nativeElement)
        })
    }

    async handleCardConfirmation(){
        const {token, error} = await this.stripe.createToken(this.cardNumber, {
            name: this.cardHolderName,
            address_zip: this.cardHolderZip,
        })
        console.log(token)
        if (error){
            console.log(error)
            const cardErrors = error.message
        } else {
            this.loading = true
            this.loading = false
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

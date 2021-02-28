import { HttpClient, HttpErrorResponse } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { BehaviorSubject, Subject, throwError } from "rxjs";
import { catchError, tap } from 'rxjs/operators';
import { User } from "./user.model";

interface AuthResponse {
    user_id: number;
    email: string;
    admin: boolean;
    token: string;
}

@Injectable({
    providedIn: "root",
})
export class AuthService {

    user = new BehaviorSubject<User|null>(null);

    openedAuthModal = new Subject<boolean>();
    openedSignInModal = new Subject<boolean>();

    signinUrl = "http://localhost:8000/api/auth/";
    signupUrl = "http://localhost:8000/api/registration/";

    constructor(private http: HttpClient) {

    }

    openSignInModal() {
        this.openModal()
        this.openedSignInModal.next(true)
    }

    openSignUpModal() {
        this.openModal()
        this.openedSignInModal.next(false)
    }

    openModal() {
        this.openedAuthModal.next(true);
    }

    closeModal() {
        this.openedAuthModal.next(false);
    }

    signin(email: string, password: string) {
        return this.http.post<AuthResponse>(
            this.signinUrl,
            {
                email: email,
                password: password,
            }
        ).pipe(
            catchError(this.handleError),
            tap((resData: AuthResponse) => {
                this.handleAuthentication(resData)
                this.closeModal()
            })
        )
    }

    signup(name: string, email: string, password: string) {
        return this.http.post<AuthResponse>(
            this.signupUrl,
            {
                name: name,
                email: email,
                password: password,
            }
        ).pipe(
            tap((resData: AuthResponse) => {
                this.handleAuthentication(resData)
                this.closeModal()
            })
        )
    }

    logout() {
        this.user.next(null);
        localStorage.removeItem('userData');
    }

    autoLogin() {
        const userData = localStorage.getItem('userData');
        if (!userData){
            return
        }

        const parsedData = JSON.parse(userData)
        console.log(parsedData)
        this.user.next(
            new User(
                parsedData.email,
                parsedData.id,
                parsedData.isAdmin,
                parsedData._token,
            )
        )
    }

    private handleAuthentication(authResponse: AuthResponse) {
        const user = new User(
            authResponse.email, 
            authResponse.user_id, 
            authResponse.admin,
            authResponse.token
        );
        this.user.next(user)
        console.log(user)
        console.log(JSON.stringify(user))
        localStorage.setItem('userData', JSON.stringify(user));
    }

    private handleError(errorRes: HttpErrorResponse) {
        let errorMessage = 'An unknown error occured!';
        return throwError(errorMessage);
    }

}
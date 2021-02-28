import { HttpHandler, HttpHeaders, HttpInterceptor, HttpParams, HttpRequest } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { exhaustMap, take } from "rxjs/operators";
import { AuthService } from "./auth.service";
import { User } from "./user.model";

@Injectable()
export class AuthInterceptorService implements HttpInterceptor {

    constructor(private authService: AuthService) { }

    intercept(req: HttpRequest<any>, next: HttpHandler){
        return this.authService.user.pipe(
            take(1),
            exhaustMap((user: User|null) => {
                if(!user){
                    return next.handle(req)
                }
                
                const headers = new HttpHeaders({'Authorization': "Token " + user.token})
                const modifiedReq = req.clone({headers})
                return next.handle(modifiedReq)
            })
        )
    }
}
import { Injectable } from "@angular/core";
import { Subject } from "rxjs";

@Injectable({
    providedIn: "root",
})
export class AuthService {

    openedAuthModal = new Subject<boolean>();
    openedSignInModal = new Subject<boolean>();

    openSignInModal () {
        this.openModal()
        this.openedSignInModal.next(true)
    }

    openSignUpModal() {
        this.openModal()
        this.openedSignInModal.next(false)
    }

    openModal () {
        this.openedAuthModal.next(true);
    }

    closeModal () {
        this.openedAuthModal.next(false);
    }
}
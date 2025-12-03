// Angular bypassSecurityTrust XSS
import { DomSanitizer } from '@angular/platform-browser';

export class ProfileComponent {
    constructor(private sanitizer: DomSanitizer) {}
    
    displayBio(userBio: string) {
        // VULNERABLE: Bypassing sanitization
        this.trustedBio = this.sanitizer.bypassSecurityTrustHtml(userBio);
    }
}

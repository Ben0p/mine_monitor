import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { 
  NbTokenService
} from '@nebular/auth';

@Component({
  selector: 'ngx-logout',
  templateUrl: './logout.component.html',
})


export class NgxLogoutComponent implements OnInit {

  value = 0;

  constructor(
    private tokenService: NbTokenService,
    private router: Router
    ) {}

    ngOnInit() {
      const delay = ms => new Promise(res => setTimeout(res, ms));
      const logout = async () => {
        await delay(0);
        this.tokenService.clear()
        let intervalId = setInterval(() => {
          this.value = this.value + 1;
          if(this.value === 100) clearInterval(intervalId)
        }, 20)
      
        await delay(3000);
        this.router.navigate(['auth/login'])
      };

      logout();
      
    }

    get status() {
      if (this.value <= 25) {
        return 'danger';
      } else if (this.value <= 50) {
        return 'warning';
      } else if (this.value <= 75) {
        return 'info';
      } else {
        return 'success';
      }
    }
    

}
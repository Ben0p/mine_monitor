import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute, NavigationStart } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})

export class AppComponent implements OnInit {

  path: any;
  firstPath: string;
  secondPath: string;
  navbarHidden: boolean;

  constructor(
    private route: ActivatedRoute,
    private router: Router
    ) {
      this.router.events
      .subscribe((event) => {
        if (event instanceof NavigationStart) {
          // Could add more chars url:path?=;other possible
          const urlDelimitators = new RegExp(/[?//,;&:#$+=]/);
          this.firstPath = unescape(event.url.slice(1).split(urlDelimitators)[0]);
          this.secondPath = unescape(event.url.slice(1).split(urlDelimitators)[1]);

          if (this.firstPath == 'home' || this.firstPath == 'undefined') {
            this.firstPath = null
          }

          if (this.secondPath == 'returnUrl' || this.secondPath == 'undefined') {
            this.secondPath = null
          }
        }
      });
    }

    hideNav (value) {
      this.navbarHidden = value;
    }


  ngOnInit() {

  }


}
import { Component, OnInit } from "@angular/core";
import { Router, ActivatedRoute, NavigationStart } from "@angular/router";
import { MatSnackBar } from "@angular/material";
import { DataService } from './data.service';

@Component({
  selector: "app-root",
  templateUrl: "./app.component.html",
  styleUrls: ["./app.component.scss"]
})
export class AppComponent implements OnInit {
  path: any;
  firstPath: string;
  secondPath: string;
  navbarHidden: boolean;
  interval: any;
  connection: object;
  snackOpen: boolean = false;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    public snackBar: MatSnackBar,
    private data: DataService
  ) {
    this.router.events.subscribe(event => {
      if (event instanceof NavigationStart) {
        // Could add more chars url:path?=;other possible
        const urlDelimitators = new RegExp(/[?//,;&:#$+=]/);
        this.firstPath = unescape(event.url.slice(1).split(urlDelimitators)[0]);
        this.secondPath = unescape(
          event.url.slice(1).split(urlDelimitators)[1]
        );

        if (this.firstPath == "home" || this.firstPath == "undefined") {
          this.firstPath = null;
        }

        if (this.secondPath == "returnUrl" || this.secondPath == "undefined") {
          this.secondPath = null;
        }
      }
    });
  }

  openSnackBar() {
    this.snackBar.openFromComponent(PizzaPartyComponent, {
      verticalPosition: 'top'
    });
  }

  closeSnackBar() {
    this.snackBar.dismiss()
  }

  hideNav(value) {
    this.navbarHidden = value;
  }

  ngOnInit() {
    this.refreshData();
    this.interval = setInterval(() => { 
      this.refreshData(); 
    }, 1000);
  }

  refreshData() {
    this.data.checkConnection()
      .subscribe((data: {}) => {
        this.connection = data;
        if (this.connection['online'] == true ) {
          this.closeSnackBar()
          this.snackOpen = false
        } else if ( this.connection['online'] == false ) {
          if (this.snackOpen == false) {
            this.openSnackBar()
            this.snackOpen = true
          }
        }
      })
  }

}

@Component({
  selector: 'app-alert',
  templateUrl: 'app.alert.html',
  styles: [`
    .pizza-party {
      color: rgb(255, 150, 150);
      text-align: center;
      width: 100%;
    }
  `],
})
export class PizzaPartyComponent {}

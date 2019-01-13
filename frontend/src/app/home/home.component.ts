import { Component, OnInit, OnDestroy } from '@angular/core';
import { Router } from '@angular/router';
import { DataService } from '../data.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})

export class HomeComponent implements OnInit, OnDestroy {

  overview: any = {};
  interval: any;
  loaded: boolean = false;

  constructor(
    private router: Router,
    private data: DataService
    ) { }

  
  toggle (content, online) {
    if (online) {
      this.router.navigate([content]);
    }
  }

  ngOnInit() {
    this.refreshData();
    this.interval = setInterval(() => { 
      this.refreshData(); 
    }, 1000);
  }


  ngOnDestroy() {
    clearInterval(this.interval);
  }

  refreshData() {
    this.data.getOverview()
      .subscribe((data: {}) => {
        this.overview = data[0];
        this.loaded = true;
      })
  }

}

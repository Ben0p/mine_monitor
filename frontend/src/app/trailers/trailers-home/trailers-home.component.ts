import { Component, OnInit, OnDestroy } from '@angular/core';
import { DataService } from '../../data.service';

@Component({
  selector: 'app-trailers-home',
  templateUrl: './trailers-home.component.html',
  styleUrls: ['./trailers-home.component.scss']
})

export class TrailersHomeComponent implements OnInit, OnDestroy {

  trailers: any = [];
  interval: any;

  constructor(private data: DataService) { }

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
    this.data.getTrailers()
      .subscribe((data: {}) => {
        this.trailers = data;
      })
  }

  onNavigate(ip) {
    window.open("http://"+ip, "_blank");
  }

}

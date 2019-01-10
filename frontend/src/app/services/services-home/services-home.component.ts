import { Component, OnInit, OnDestroy } from '@angular/core';
import { DataService } from '../../data.service';

@Component({
  selector: 'app-services-home',
  templateUrl: './services-home.component.html',
  styleUrls: ['./services-home.component.scss']
})
export class ServicesHomeComponent implements OnInit, OnDestroy {

  services: any = [];
  interval: any;

  constructor(private data: DataService) { }

  ngOnInit() {
    this.refreshData();
    this.interval = setInterval(() => { 
      this.refreshData(); 
    }, 10000);
  }

  ngOnDestroy() {
    clearInterval(this.interval);
  }

  refreshData() {
    this.data.getServices()
      .subscribe((data: {}) => {
        this.services = data;
      })
  }

}

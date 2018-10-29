import { Component, OnInit } from '@angular/core';
import { DataService } from '../data.service';

@Component({
  selector: 'app-trucks',
  templateUrl: './trucks.component.html',
  styleUrls: ['./trucks.component.scss']
})
export class TrucksComponent implements OnInit {

  trucks$: any = [];
  interval: any;
  count: any;

  constructor(private data: DataService) { }

  ngOnInit() {
    this.refreshData();
    this.interval = setInterval(() => { 
      this.refreshData(); 
    }, 1000);
  }

  refreshData() {

    this.data.getTrucks()
      .subscribe((data: {}) => {
        this.trucks$ = data;
      })
  }

  somethingOffline(xim, two, screen) {
    this.count = [xim, two, screen].filter(Boolean).length
    if (this.count > 0 && this.count < 3){
      return(true);
    } else {
      return(false)
    }
  }

}

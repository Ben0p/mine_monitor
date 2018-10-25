import { Component, OnInit } from '@angular/core';
import { DataService } from '../data.service';

@Component({
  selector: 'app-trucks',
  templateUrl: './trucks.component.html',
  styleUrls: ['./trucks.component.scss']
})
export class TrucksComponent implements OnInit {

  trucks$: Object;
  interval: any;

  constructor(private data: DataService) { }

  ngOnInit() {
    this.refreshData();
    this.interval = setInterval(() => { 
      this.refreshData(); 
    }, 5000);
  }

  refreshData() {
    this.data.getTrucks().subscribe(
      data => this.trucks$ = data
    );
  }

}

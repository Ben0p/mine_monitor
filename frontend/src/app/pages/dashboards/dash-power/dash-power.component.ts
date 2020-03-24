import { Component, OnInit, OnDestroy } from '@angular/core';
import { DashService } from './../../../@core/data/dash.service'

@Component({
  selector: 'dash-power',
  templateUrl: './dash-power.component.html',
  styleUrls: ['./dash-power.component.scss']
})
export class DashPowerComponent implements OnInit, OnDestroy {

  sites: any;
  interval: any;

  constructor(
    private dash: DashService,
  ) { }

  ngOnInit() {
    this.refreshData()
    this.interval = setInterval(() => {
      this.refreshData();
    }, 10000);
  }

  ngOnDestroy() { 
    clearInterval(this.interval);
  }

  refreshData() {
    this.dash.getPowerDash().subscribe(
      (
        data: {}) => {
        this.sites = data;
      }
    )
  }
}

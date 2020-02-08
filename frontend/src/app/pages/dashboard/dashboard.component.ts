import { Component, OnInit, OnDestroy } from '@angular/core';
import { AlertService } from './../../@core/data/alerts.service'
import { TetraService } from './../../@core/data/tetra.service'

@Component({
  selector: 'ngx-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss'],
})


export class DashboardComponent implements OnInit, OnDestroy {

  alerts$: Object;
  radios: Object;
  interval: any;

  constructor(
    private alerts: AlertService,
    private tetra: TetraService
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
    this.alerts.getAlertWZ().subscribe(
      (
        data: {}) => {
        this.alerts$ = data;
      }
    )
    this.tetra.getTetraRadioCount('all').subscribe(
      (
        data: {}) => {
        this.radios = data;
        console.log(this.radios)
      }
    )
  }

}
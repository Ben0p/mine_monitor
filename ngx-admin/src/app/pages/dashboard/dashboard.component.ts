import { Component, OnInit, OnDestroy } from '@angular/core';
import { AlertService } from './../../@core/data/alerts.service'

@Component({
  selector: 'ngx-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss'],
})


export class DashboardComponent implements OnInit, OnDestroy {

  alerts$: Object
  interval: any;

  constructor(
    private alerts: AlertService,
  ) { }

  ngOnInit() {
    this.refreshData()
    this.interval = setInterval(() => {
      this.refreshData();
    }, 1000);
  }

  ngOnDestroy() { }

  refreshData() {
    this.alerts.getAlertStatus().subscribe(
      (
        data: {}) => {
        this.alerts$ = data;
      }
    )
  }

}
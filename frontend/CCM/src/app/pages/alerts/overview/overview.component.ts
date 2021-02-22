import { Component, OnInit, OnDestroy } from '@angular/core';
import { AlertService } from '../../../@core/data/alerts.service'

@Component({
  selector: 'ngx-alerts-overview',
  templateUrl: './overview.component.html',
  styleUrls: ['./overview.component.scss']
})

export class OverviewComponent implements OnInit, OnDestroy {

  alerts$: Object
  statuses: Object
  interval: any;
  
  constructor(
    private alerts: AlertService,
  ) { }

  ngOnInit() {
    this.refreshData()
    this.interval = setInterval(() => {
      this.refreshData();
    }, 3000);
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
    this.alerts.getAlertStatus().subscribe(
      (
        data: {}) => {
        this.statuses = data;
      }
    )
  }

}

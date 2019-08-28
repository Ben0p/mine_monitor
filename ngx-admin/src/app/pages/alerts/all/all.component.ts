import { Component, OnInit, OnDestroy } from '@angular/core';
import { AlertService } from '../../../@core/data/alerts.service'

@Component({
  selector: 'all',
  templateUrl: './all.component.html',
  styleUrls: ['./all.component.scss']
})

export class AllComponent implements OnInit, OnDestroy {
  alerts$: Object;
  zones$: Object;
  interval: any;

  constructor(
    private alerts: AlertService,
  ) {}

  ngOnInit() {
    this.refreshData();
    this.interval = setInterval(() => {
      this.refreshData();
    }, 60000);
  }

  ngOnDestroy() {
    clearInterval(this.interval);
  }

  refreshData() {
    this.alerts.getAlerts().subscribe(
      (data: {}) => {
        this.alerts$ = data;
      }
    );
    this.alerts.getAlertZones().subscribe(
      (data: {}) => {
        this.zones$ = data;
      }
    );
  }

}

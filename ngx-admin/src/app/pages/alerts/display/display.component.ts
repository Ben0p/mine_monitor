import { Component, OnInit, OnDestroy } from '@angular/core';
import { AlertService } from '../../../@core/data/alerts.service'

@Component({
  selector: 'display',
  templateUrl: './display.component.html',
  styleUrls: ['./display.component.scss']
})
export class DisplayComponent implements OnInit, OnDestroy {
  alerts$: Object;
  interval: any;

  constructor(
    private alerts: AlertService,
  ) { }

  ngOnInit() {
    this.refreshData();
    this.interval = setInterval(() => {
      this.refreshData();
    }, 5000);
  }

  ngOnDestroy() {
    clearInterval(this.interval);
  }

  refreshData() {
    this.alerts.getAlertAll().subscribe(
      (data: {}) => {
        this.alerts$ = data;
      }
    );
  }

}

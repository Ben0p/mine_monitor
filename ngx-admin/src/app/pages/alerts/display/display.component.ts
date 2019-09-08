import { Component, OnInit, OnDestroy } from '@angular/core';
import { AlertService } from '../../../@core/data/alerts.service'

@Component({
  selector: 'display',
  templateUrl: './display.component.html',
  styleUrls: ['./display.component.scss']
})
export class DisplayComponent implements OnInit, OnDestroy {
  alerts$: [];
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
    this.alerts.getAlertDisplay().subscribe(
      (data: []) => {
        this.alerts$ = data;
      }
    );
  }

}

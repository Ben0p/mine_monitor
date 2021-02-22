import { Component, OnInit, OnDestroy } from '@angular/core';
import { AlertService } from '../../../@core/data/alerts.service'

@Component({
  selector: 'weatherzone',
  templateUrl: './weatherzone.component.html',
  styleUrls: ['./weatherzone.component.scss'],
})

export class WeatherzoneComponent implements OnInit, OnDestroy {

  alerts$: Object
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
  }

}
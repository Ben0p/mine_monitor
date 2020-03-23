import { Component, OnInit, OnDestroy } from '@angular/core';
import { AlertService } from './../../../@core/data/alerts.service'
import { TetraService } from './../../../@core/data/tetra.service'

@Component({
  selector: 'dash-alerts-tetra',
  templateUrl: './dash-alerts-tetra.component.html',
  styleUrls: ['./dash-alerts-tetra.component.scss']
})


export class DashAlertsTetraComponent implements OnInit, OnDestroy {

  alerts$: any;
  radios: any;
  groupCalls: any;
  individualCalls: any;
  sdsCalls: any;
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
      }
    )
    this.tetra.getTetraCallStats('group', 60).subscribe(
      (
        data: {}) => {
        this.groupCalls = data;
      }
    )
    this.tetra.getTetraCallStats('individual', 60).subscribe(
      (
        data: {}) => {
        this.individualCalls = data;
      }
    )
    this.tetra.getTetraCallStats('sds', 60).subscribe(
      (
        data: {}) => {
        this.sdsCalls = data;
      }
    )
  }

}
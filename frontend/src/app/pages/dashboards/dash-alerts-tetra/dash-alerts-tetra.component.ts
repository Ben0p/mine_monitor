import { Component, OnInit, OnDestroy } from '@angular/core';
import { AlertService } from './../../../@core/data/alerts.service'
import { TetraService } from './../../../@core/data/tetra.service'
import { FmService } from './../../../@core/data/fm.service'

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
  fmLive: any;
  alertsLoaded: boolean = false;
  radiosLoaded: boolean = false;
  groupCallsLoaded: boolean = false;
  indCallsLoaded: boolean = false;
  sdsCallsLoaded: boolean = false;
  fmLoaded: boolean = true;
  



  constructor(
    private alerts: AlertService,
    private tetra: TetraService,
    private fm: FmService
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
        this.alertsLoaded = true
      }
    )
    this.tetra.getTetraRadioCount('all').subscribe(
      (
        data: {}) => {
        this.radios = data;
        this.radiosLoaded = true
      }
    )
    this.tetra.getTetraCallStats('group', 60).subscribe(
      (
        data: {}) => {
        this.groupCalls = data;
        this.groupCallsLoaded = true
      }
    )
    this.tetra.getTetraCallStats('individual', 60).subscribe(
      (
        data: {}) => {
        this.individualCalls = data;
        this.indCallsLoaded = true
      }
    )
    this.tetra.getTetraCallStats('sds', 60).subscribe(
      (
        data: {}) => {
        this.sdsCalls = data;
        this.sdsCallsLoaded = true;
      }
    )
    this.fm.getFmLive().subscribe(
      (
        data: {}) => {
        this.fmLive = data;
        this.fmLoaded = true;
      }
    )
  }

}
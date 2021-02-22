import { Component, OnInit, OnDestroy } from '@angular/core';
import { AlertService } from './../../../@core/data/alerts.service'
import { TetraService } from './../../../@core/data/tetra.service'
import { FmService } from './../../../@core/data/fm.service'
import { WindService } from '../../../@core/data/wind.service'
import { WeatherService } from '../../../@core/data/weather.service'

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
  interval2: any;
  fmLive: any;
  alertsLoaded: boolean = false;
  radiosLoaded: boolean = false;
  groupCallsLoaded: boolean = false;
  indCallsLoaded: boolean = false;
  sdsCallsLoaded: boolean = false;
  fmLoaded: boolean = true;
  winds: Object;
  wind_datas: Object;


  constructor(
    private alerts: AlertService,
    private tetra: TetraService,
    private fm: FmService,
    private wind: WindService,
    private weather: WeatherService,
  ) { }

  ngOnInit() {
    this.refreshData()
    this.interval = setInterval(() => {
      this.refreshData();
    }, 10000);

    this.refreshWeather()
    this.interval2 = setInterval(() => {
      this.refreshWeather();
    }, 60000);
    
  }

  ngOnDestroy() {
    clearInterval(this.interval);
    clearInterval(this.interval2);
  }

  ordinal_suffix_of(i) {
    var j = i % 10,
      k = i % 100;
    if (j == 1 && k != 11) {
      return i + "st";
    }
    if (j == 2 && k != 12) {
      return i + "nd";
    }
    if (j == 3 && k != 13) {
      return i + "rd";
    }
    return i + "th";
  }

  getDate(unix) {

    var time = new Date(unix)
    var daystring = new Intl.DateTimeFormat('en-AU', { weekday: 'long' }).format(time)
    var date = time.getDate()
    var datestring = this.ordinal_suffix_of(date)
    var monthstring = new Intl.DateTimeFormat('en-AU', { month: 'long' }).format(time)
    var yearstring = new Intl.DateTimeFormat('en-AU', { year: 'numeric' }).format(time)

    var finaltimestring = `${daystring}, ${monthstring} ${datestring} ${yearstring}`
    return (finaltimestring)
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
    this.wind.getWindAll().subscribe(
      (data: {}) => {
        this.winds = data;
      }
    )
  }

  refreshWeather(){
    this.weather.getWeatherWind().subscribe(
      (data: {}) => {
        this.wind_datas = data;
      }
    );
  }

}
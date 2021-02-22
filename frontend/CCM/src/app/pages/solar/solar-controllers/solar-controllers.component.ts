import { Component, OnInit, OnDestroy } from '@angular/core';
import { SolarService } from '../../../@core/data/solar.service'

@Component({
  selector: 'solar-controllers',
  templateUrl: './solar-controllers.component.html',
  styleUrls: ['./solar-controllers.component.scss']
})

export class SolarControllersComponent implements OnInit, OnDestroy  {
  solar_datas: Object;
  interval: any;
  loaded = false;

  constructor(
    private solar: SolarService,
  ) {}

  ngOnInit() {
    this.refreshData();
    this.loaded = true
    this.interval = setInterval(() => {
      this.refreshData();
    }, 10000);
  }

  ngOnDestroy() {
    clearInterval(this.interval);
  }

  refreshData() {
    this.solar.getSolarData().subscribe(
      (data: {}) => {
        this.solar_datas = data;
      }
    );
  }

}
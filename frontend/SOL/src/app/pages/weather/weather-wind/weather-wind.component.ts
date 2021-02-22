import { Component, OnInit, OnDestroy } from '@angular/core';
import { WeatherService } from '../../../@core/data/weather.service'

@Component({
  selector: 'weather-wind',
  templateUrl: './weather-wind.component.html',
  styleUrls: ['./weather-wind.component.scss'],
})

export class WeatherWindComponent implements OnInit, OnDestroy {
  wind_datas: Object;
  interval: any;
  loaded = false;

  constructor(
    private weather: WeatherService,
  ) { }

  ngOnInit() {
    this.refreshData();
    this.loaded = true
    this.interval = setInterval(() => {
      this.refreshData();
    }, 600000);
  }

  ngOnDestroy() {
    clearInterval(this.interval);
  }

  refreshData() {
    this.weather.getWeatherWind().subscribe(
      (data: {}) => {
        this.wind_datas = data;
      }
    );
  }


}

import { Component, OnDestroy, Input, OnInit } from '@angular/core';
import { NbThemeService, NbColorHelper } from '@nebular/theme';
import { WindService } from '../../../@core/data/wind.service'

@Component({
  selector: 'ngx-wind-line-chart',
  templateUrl: './wind-line-chart.component.html',
  styleUrls: ['./wind-line-chart.component.scss'],
})
export class WindLineChartComponent implements OnInit, OnDestroy {
  @Input() uid: string;
  @Input() range: string;

  data: any;
  options: any;
  themeSubscription: any;
  windspeed: Object;
  interval: any;
  colors: any;
  unit = 'kmh';
  name: string;

  constructor(
    private theme: NbThemeService,
    private wind: WindService,
  ) {


    this.themeSubscription = this.theme.getJsTheme().subscribe(config => {

      this.colors = config.variables;
      const chartjs: any = config.variables.chartjs;

      this.data = {
        labels: [],
        datasets: [{
          data: [],
          label: this.range,
          backgroundColor: NbColorHelper.hexToRgbA(this.colors.primary, 0.3),
          borderColor: this.colors.primary,
        }
        ],
      };

      this.options = {
        responsive: true,
        maintainAspectRatio: false,
        animation: {
          duration: 0
        },
        scales: {
          xAxes: [
            {
              gridLines: {
                display: true,
                color: chartjs.axisLineColor,
              },
              ticks: {
                fontColor: chartjs.textColor,
              },
            },
          ],
          yAxes: [
            {
              gridLines: {
                display: true,
                color: chartjs.axisLineColor,
              },
              ticks: {
                fontColor: chartjs.textColor,
              },
            },
          ],
        },
        legend: {
          labels: {
            fontColor: chartjs.textColor,
          },
        },
      };
    });
  }

  refreshData() {
    if (this.range == 'hour') {
      this.wind.getWindHour(this.uid).subscribe(
        (speeds: {}) => {
          this.name = speeds['name']
          this.windspeed = speeds;
          this.loadData(this.windspeed)
        }
      );
    } else if (this.range == 'day') {
      this.wind.getWindDay(this.uid).subscribe(
        (speeds: {}) => {
          this.name = speeds['name']
          this.windspeed = speeds;
          console.log(speeds)
          this.loadData(this.windspeed)
        }
      );
    }
  }

  ngOnInit() {
    console.log(this.uid)
    this.refreshData();
    this.interval = setInterval(() => {
      this.refreshData();
    }, 30000);
  }

  ngOnDestroy(): void {
    this.themeSubscription.unsubscribe();
    clearInterval(this.interval);
  }

  loadData(windspeed) {

    this.data = {
      labels: windspeed['time'],
      datasets: [{
        data: windspeed[this.unit]['max'],
        label: 'max',
        backgroundColor: NbColorHelper.hexToRgbA(this.colors.danger, 0.3),
        borderColor: this.colors.danger,
      },
      {
        data: windspeed[this.unit]['min'],
        label: 'min',
        backgroundColor: NbColorHelper.hexToRgbA(this.colors.success, 0.3),
        borderColor: this.colors.success,
      },
      {
        data: windspeed[this.unit]['avg'],
        label: 'avg',
        backgroundColor: NbColorHelper.hexToRgbA(this.colors.primary, 0.3),
        borderColor: this.colors.primary,
      }
      ],
    };

  }


}
import { Component, OnDestroy, Input, OnInit } from '@angular/core';
import { NbThemeService, NbColorHelper } from '@nebular/theme';
import { WindService } from '../../../@core/data/wind.service'

@Component({
  selector: 'ngx-wind-line-chart',
  template: `
    <chart type="line" [data]="data" [options]="options"></chart>
  `,
})
export class WindLineChart implements OnInit, OnDestroy {
  @Input() title: string;


  data: any;
  options: any;
  themeSubscription: any;
  windspeed: Object;
  interval: any;
  colors: any;

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
          label: this.title,
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
    this.wind.getWindHourly(this.title, 'kmh').subscribe(
      (speeds: {}) => {
        this.windspeed = speeds;
        this.loadData(this.windspeed)
      }
    );
  }

  ngOnInit() {
    this.refreshData();
    this.interval = setInterval(() => {
      this.refreshData();
    }, 10000);
  }

  ngOnDestroy(): void {
    this.themeSubscription.unsubscribe();
    clearInterval(this.interval);
  }

  loadData(windspeed) {
    this.data = {
      labels: windspeed['time'],
      datasets: [{
        data: windspeed['speed'],
        label: this.title,
        backgroundColor: NbColorHelper.hexToRgbA(this.colors.primary, 0.3),
        borderColor: this.colors.primary,
      }
      ],
    };


  }


}
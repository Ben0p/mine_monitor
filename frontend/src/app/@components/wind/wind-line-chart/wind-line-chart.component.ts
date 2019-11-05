import { Component, OnDestroy, Input, OnInit } from '@angular/core';
import { NbThemeService, NbColorHelper } from '@nebular/theme';
import { WindService } from '../../../@core/data/wind.service'

@Component({
  selector: 'ngx-wind-line-chart',
  templateUrl: './wind-line-chart.component.html',
  styleUrls: ['./wind-line-chart.component.scss'],
})
export class WindLineChartComponent implements OnInit, OnDestroy {
  @Input() name: string;
  @Input() range: string;

  data: any;
  options: any;
  themeSubscription: any;
  windspeed: Object;
  interval: any;
  colors: any;
  unit = 'kmh';

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
    if (this.range == 'minute') {
      this.wind.getWindMinute(this.name, this.unit).subscribe(
        (speeds: {}) => {
          this.windspeed = speeds;
          this.loadData(this.windspeed)
        }
      );
    } else if (this.range == 'hour') {
      this.wind.getWindHour(this.name, this.unit).subscribe(
        (speeds: {}) => {
          this.windspeed = speeds;
          this.loadData(this.windspeed)
        }
      );
    }
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
    if (this.range == 'minute') {
      this.data = {
        labels: windspeed['time'],
        datasets: [{
          data: windspeed['speed'],
          label: 'avg',
          backgroundColor: NbColorHelper.hexToRgbA(this.colors.primary, 0.3),
          borderColor: this.colors.primary,
        }
        ],
      };
    } else if (this.range == 'hour') {
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


}
import { Component, OnDestroy, Input, OnInit } from '@angular/core';
import { NbThemeService, NbColorHelper } from '@nebular/theme';
import { TetraService } from '../../../@core/data/tetra.service'

@Component({
  selector: 'ngx-tetra-calls-line-chart',
  templateUrl: './tetra-calls-line-chart.component.html',
  styleUrls: ['./tetra-calls-line-chart.component.scss']
})
export class TetraCallsLineChartComponent implements OnInit, OnDestroy {
  @Input() name: string;
  @Input() range: string;
  @Input() title: string;

  data: any;
  options: any;
  themeSubscription: any;
  calls: Object;
  interval: any;
  colors: any;
  unit = 'kmh';

  constructor(
    private theme: NbThemeService,
    private tetra: TetraService,
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
    this.tetra.getTetraCallHistory('day').subscribe(
      (history: {}) => {
        this.calls = history;
        this.loadData(this.calls)
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

  loadData(calls) {

    this.data = {
      labels: calls['minutes'],
      datasets: [
        {
          data: calls['group_calls'],
          label: 'Group',
          backgroundColor: NbColorHelper.hexToRgbA(this.colors.success, 0.3),
          borderColor: this.colors.success,
        },
        {
          data: calls['individual_calls'],
          label: 'Individual',
          backgroundColor: NbColorHelper.hexToRgbA(this.colors.danger, 0.3),
          borderColor: this.colors.danger,
        },        
      ],
    };


  }

}

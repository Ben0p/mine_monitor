import { Component, OnDestroy, Input, OnInit } from '@angular/core';
import { NbThemeService, NbColorHelper } from '@nebular/theme';
import { TetraService } from '../../../@core/data/tetra.service'

@Component({
  selector: 'ngx-tetra-bar-chart',
  templateUrl: './tetra-bar-chart.component.html',
  styleUrls: ['./tetra-bar-chart.component.scss'],
})
export class TetraBarChartComponent implements OnInit, OnDestroy {
  @Input() title: string;

  data: any;
  loads: any;
  node_labels: any;
  node_data: any;
  options: any;
  themeSubscription: any;
  interval: any;
  colors: any;
  bar_colors = [{}]
  border_colors = [{}]


  constructor(
    private theme: NbThemeService,
    private tetra: TetraService,
  ) {



    this.themeSubscription = this.theme.getJsTheme().subscribe(config => {

      this.colors = config.variables;
      const chartjs: any = config.variables.chartjs;


      this.data = {
        labels: [],
        datasets: [
          {
            data: [],
            label: "Loading...",
            backgroundColor: NbColorHelper.hexToRgbA(this.colors.primaryLight, 0.8),
            borderColor: NbColorHelper.hexToRgbA(this.colors.primaryLight, 1),
          }
        ]
      };

      this.options = {
        animation: {
          duration: 0
        },
        maintainAspectRatio: false,
        responsive: true,
        legend: {
          labels: {
            fontColor: chartjs.textColor,
          },
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
                autoSkip: false,
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
                beginAtZero: true
              },
            },
          ],
        },
      };


    });
  }

  refreshData() {
    this.tetra.getTetraNodeLoad().subscribe(
      (loads: {}) => {
        this.loads = loads;
        this.loadData()
      }
    );
  }


  ngOnInit() {
    this.refreshData();
    this.interval = setInterval(() => {
      this.refreshData();
    }, 5000);
  }

  ngOnDestroy(): void {
    this.themeSubscription.unsubscribe();
    clearInterval(this.interval);
  }

  loadData() {

    this.bar_colors = []
    this.border_colors = []

    this.loads['node_colors'].forEach(
      value => {
        if (value == 'warning') {
          this.bar_colors.push(NbColorHelper.hexToRgbA(this.colors.warning, 0.8))
          this.border_colors.push(NbColorHelper.hexToRgbA(this.colors.warning, 1))
        } else if (value == 'danger') {
          this.bar_colors.push(NbColorHelper.hexToRgbA(this.colors.danger, 0.8))
          this.border_colors.push(NbColorHelper.hexToRgbA(this.colors.danger, 1))
        } else if (value == 'success') {
          this.bar_colors.push(NbColorHelper.hexToRgbA(this.colors.success, 0.8))
          this.border_colors.push(NbColorHelper.hexToRgbA(this.colors.success, 1))
        } else if (value == 'offline') {
          this.bar_colors.push('grey')
          this.border_colors.push(NbColorHelper.hexToRgbA(this.colors.danger, 1))
        }
      },
    )


    this.data = {
      labels: this.loads['node_names'],
      datasets: [
        {
          data: this.loads['node_loads'],
          label: 'Load %',
          backgroundColor: this.bar_colors,
          borderColor: this.border_colors,
          borderWidth: 2
        },
      ]
    };

  }

}

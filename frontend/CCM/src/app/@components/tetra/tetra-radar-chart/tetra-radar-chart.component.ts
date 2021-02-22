import { Component, OnDestroy, Input, OnInit } from '@angular/core';
import { NbThemeService, NbColorHelper } from '@nebular/theme';
import { TetraService } from '../../../@core/data/tetra.service'

@Component({
  selector: 'ngx-tetra-radar-chart',
  templateUrl: './tetra-radar-chart.component.html',
  styleUrls: ['./tetra-radar-chart.component.scss'],
})
export class TetraRadarChartComponent implements OnInit, OnDestroy {
  @Input() label_title: string;

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
            borderColor: this.colors.primary,
            backgroundColor: NbColorHelper.hexToRgbA(this.colors.primaryLight, 0.8),
          }
        ]
      };

      this.options = {
        animation: {
          duration: 0
        },
        responsive: true,
        maintainAspectRatio: false,
        scaleFontColor: 'white',
        legend: {
          labels: {
            fontColor: chartjs.textColor,
          },
        },
        scale: {
          pointLabels: {
            fontSize: 14,
            fontColor: chartjs.textColor,
          },
          gridLines: {
            color: "grey",
          },
          angleLines: {
            color: "grey",
          },
        },
      };
    });
  }

  refreshData() {
    this.tetra.getTetraTSLoad().subscribe(
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

    this.loads['ts_colors'].forEach(
      value => {
        if (value == 'warning') {
          this.bar_colors.push(NbColorHelper.hexToRgbA(this.colors.warning, 0.8))
          this.border_colors.push(NbColorHelper.hexToRgbA(this.colors.warning, 1))
        } else if (value == 'danger') {
          this.bar_colors.push(NbColorHelper.hexToRgbA(this.colors.danger, 0.8))
          this.border_colors.push(NbColorHelper.hexToRgbA(this.colors.danger, 1))
        } else if (value == 'success') {
          this.bar_colors.push(NbColorHelper.hexToRgbA(this.colors.success, 0.8))
          this.border_colors.push(NbColorHelper.hexToRgbA(this.colors.success, 0.8))
        } else if (value == 'info') {
          this.bar_colors.push(NbColorHelper.hexToRgbA(this.colors.info, 0.8))
          this.border_colors.push(NbColorHelper.hexToRgbA(this.colors.info, 0.8))
        } else if (value == 'primary') {
          this.bar_colors.push(NbColorHelper.hexToRgbA(this.colors.primary, 0.8))
          this.border_colors.push(NbColorHelper.hexToRgbA(this.colors.primary, 0.8))
        }

      },

    )

    this.data = {
      labels: this.loads['ts_type'],
      datasets: [
        {
          data: this.loads['ts_load'],
          label: this.label_title,
          backgroundColor: this.bar_colors,
          borderColor: this.border_colors
        }
      ]
    };

  }

}

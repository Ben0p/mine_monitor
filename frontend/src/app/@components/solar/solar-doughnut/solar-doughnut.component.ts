import { delay } from 'rxjs/operators';
import { AfterViewInit, Component, Input, OnDestroy } from '@angular/core';
import { NbThemeService, NbColorHelper } from '@nebular/theme';

declare const echarts: any;

@Component({
  selector: 'ngx-solar-doughnut',
  styleUrls: ['./solar-doughnut.component.scss'],
  templateUrl: './solar-doughnut.component.html',
})

export class SolarDoughnutComponent implements AfterViewInit, OnDestroy {

  colors: any;
  colorValue: any;
  percentage: number;
  remainder: number;

  @Input() data: any;

  option: any = {};
  themeSubscription: any;

  constructor(
    private theme: NbThemeService
  ) { }

  getColor(color) {
    if (color == "success") {
      return (NbColorHelper.hexToRgbA(this.colors.success, 0.8))
    } else if (color == "warning") {
      return (this.colorValue = NbColorHelper.hexToRgbA(this.colors.warning, 0.8))
    } else if (color == "danger") {
      return (this.colorValue = NbColorHelper.hexToRgbA(this.colors.danger, 0.8))
    } else if (color == "info") {
      return (this.colorValue = NbColorHelper.hexToRgbA(this.colors.info, 0.8))
    }
  }

  ngAfterViewInit() {
    this.themeSubscription = this.theme.getJsTheme().pipe(delay(1)).subscribe(config => {

      this.colors = config.variables;
      const solarTheme: any = config.variables.solar;

      this.option = Object.assign({}, {
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b}: {c} ({d}%)'
        },
        animation: false,
        series: [
          {
            name: 'Array',
            type: 'pie',
            selectedMode: 'single',
            hoverAnimation: true,
            avoidLabelOverlap: true,
            selectedOffset: 0,
            radius: ['85%', '100%'],
            right: '20%',
            data: [
              {
                value: this.data.live.solar.volts,
                name: 'Array',
                label: {
                  normal: {
                    position: 'outer',
                    formatter: '{a}\n{c}v',
                    textStyle: {
                      fontSize: '14',
                      fontFamily: config.variables.fontSecondary,
                      fontWeight: '600',
                      align: 'center',
                      color: config.variables.fgHeading,
                    },
                  },
                },
                itemStyle: {
                  normal: {
                    color: this.getColor(this.data.live.solar.color),
                    shadowColor: solarTheme.shadowColor,
                    shadowBlur: 0,
                    shadowOffsetX: 0,
                    shadowOffsetY: 3,
                  },
                }
              },
              {
                value: this.data.live.solar.max - this.data.live.solar.volts,
                name: '',
                label: {
                  normal: {
                    show: 'false',
                  }
                },
                labelLine: {
                  show: 'false',
                },
                itemStyle: {
                  normal: {
                    color: solarTheme.secondSeriesFill,
                  },
                }
              },
            ]
          },
          {
            name: 'Battery',
            type: 'pie',
            selectedMode: 'single',
            hoverAnimation: true,
            avoidLabelOverlap: true,
            selectedOffset: 0,
            radius: ['65%', '80%'],
            right: '20%',
            data: [
              {
                value: this.data.live.batt.volts,
                name: 'Battery',
                label: {
                  normal: {
                    position: 'center',
                    formatter: '{a}\n{c}v',
                    textStyle: {
                      fontSize: '14',
                      fontFamily: config.variables.fontSecondary,
                      fontWeight: '600',
                      align: 'center',
                      color: config.variables.fgHeading,
                    },
                  },
                },
                itemStyle: {
                  normal: {
                    color: this.getColor(this.data.live.batt.color),
                    shadowColor: solarTheme.shadowColor,
                    shadowBlur: 0,
                    shadowOffsetX: 0,
                    shadowOffsetY: 3,
                  },
                }
              },
              {
                value: (this.data.live.batt.volts / this.data.live.batt.soc) * (100 - this.data.live.batt.soc),
                name: '',
                label: {
                  show: 'false',
                },
                labelLine: {
                  show: 'false',
                },
                itemStyle: {
                  normal: {
                    color: solarTheme.secondSeriesFill,
                  },
                }
              },
            ]
          },
        ]
      });
    })
  }
  ngOnDestroy() {
    this.themeSubscription.unsubscribe();
  }
}




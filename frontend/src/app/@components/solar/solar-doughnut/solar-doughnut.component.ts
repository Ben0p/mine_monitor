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

  private value = 0;
  colors: any;
  colorValue: any;
  percentage: number;

  @Input() targetVoltage: number;
  @Input() pieColor: any;

  @Input('chartValue')
  set chartValue(value: number) {
    this.value = value;

    if (this.option.series) {
      this.option.series[0].data[0].value = value;
    }

  }

  option: any = {};
  themeSubscription: any;

  constructor(
    private theme: NbThemeService
  ) {}

  ngAfterViewInit() {
    this.themeSubscription = this.theme.getJsTheme().pipe(delay(1)).subscribe(config => {

      this.colors = config.variables;
      const solarTheme: any = config.variables.solar;

      this.percentage = (this.value / this.targetVoltage)*100

      if (this.pieColor == "success" ) {
        this.colorValue = NbColorHelper.hexToRgbA(this.colors.success, 0.8)
      } else if (this.pieColor == "warning" ) {
        this.colorValue = NbColorHelper.hexToRgbA(this.colors.warning, 0.8)
      } else if (this.pieColor == "danger" ) {
        this.colorValue = NbColorHelper.hexToRgbA(this.colors.danger, 0.8)
      } else if (this.pieColor == "info" ) {
        this.colorValue = NbColorHelper.hexToRgbA(this.colors.info, 0.8)
      } 

      this.option = Object.assign({}, {
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b} : {c} ({d}%)',
        },
        animation: false,
        series: [
          {
            name: ' ',
            clockWise: true,
            hoverAnimation: false,
            type: 'pie',
            center: ['45%', '50%'],
            radius: solarTheme.radius,
            data: [
              {
                value: this.value,
                name: ' ',
                label: {
                  normal: {
                    position: 'center',
                    formatter: '{c} v',
                    textStyle: {
                      fontSize: '22',
                      fontFamily: config.variables.fontSecondary,
                      fontWeight: '600',
                      color: config.variables.fgHeading,
                    },
                  },
                },
                tooltip: {
                  show: false,
                },
                itemStyle: {
                  normal: {
                    color: this.colorValue,
                    shadowColor: solarTheme.shadowColor,
                    shadowBlur: 0,
                    shadowOffsetX: 0,
                    shadowOffsetY: 3,
                  },
                },
                hoverAnimation: false,
              },
              {
                value: this.targetVoltage - this.value,
                name: ' ',
                tooltip: {
                  show: false,
                },
                label: {
                  normal: {
                    position: 'inner',
                  },
                },
                itemStyle: {
                  normal: {
                    color: solarTheme.secondSeriesFill,
                  },
                },
              },
            ],
          },
        ],
      });
    });
  }

  ngOnDestroy() {
    this.themeSubscription.unsubscribe();
  }
}
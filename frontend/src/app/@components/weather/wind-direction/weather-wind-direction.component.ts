import { delay } from 'rxjs/operators';
import { AfterViewInit, Component, Input, OnDestroy } from '@angular/core';
import { NbThemeService, NbColorHelper } from '@nebular/theme';

declare const echarts: any;

@Component({
  selector: 'ngx-weather-wind-direction',
  styleUrls: ['./weather-wind-direction.component.scss'],
  templateUrl: './weather-wind-direction.component.html',
})

export class WeatherWindDirectionComponent implements AfterViewInit, OnDestroy {

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

      const labeltext = {
        fontSize: '14',
        fontFamily: config.variables.fontSecondary,
        fontWeight: '600',
        align: 'center',
        color: config.variables.fgHeading,
      }

      this.option = Object.assign({},
        {
          angleAxis: {
            type: 'category',
            startAngle: 101,
            animation: false,
            axisLine: {
              lineStyle: {
                color: config.variables.fgHeading,
              }
            },
            data: [
              {
                value: 'N',
                textStyle: labeltext
              },
              {
                value: 'NNE',
                textStyle: labeltext
              },
              {
                value: 'NE',
                textStyle: labeltext
              },
              {
                value: 'ENE',
                textStyle: labeltext
              },
              {
                value: 'E',
                textStyle: labeltext
              },
              {
                value: 'ESE',
                textStyle: labeltext
              },
              {
                value: 'SE',
                textStyle: labeltext
              },
              {
                value: 'SSE',
                textStyle: labeltext
              },
              {
                value: 'S',
                textStyle: labeltext
              },
              {
                value: 'SSW',
                textStyle: labeltext
              },
              {
                value: 'SW',
                textStyle: labeltext
              },
              {
                value: 'WSW',
                textStyle: labeltext
              },
              {
                value: 'W',
                textStyle: labeltext
              },
              {
                value: 'WNW',
                textStyle: labeltext
              },
              {
                value: 'NW',
                textStyle: labeltext
              },
              {
                value: 'NNW',
                textStyle: labeltext
              }
            ]
          },
          radiusAxis: {
            axisLine: {
              lineStyle: {
                color: config.variables.fgHeading,
              }
            },
          },
          polar: {
          },
          series: [
            {
              type: 'bar',
              animation: false,
              barGap: '-100%', 
              data: this.data.speeds.min,
              coordinateSystem: 'polar',
              itemStyle: {
                color: this.getColor('success')
              },
              name: 'Minimum',
              stack: 'a'
            },
            {
              type: 'bar',
              animation: false,
              data: this.data.speeds.avg,
              coordinateSystem: 'polar',
              itemStyle: {
                color: this.getColor('info')
              },
              name: 'Average',
              stack: 'a'
            },
            {
              type: 'bar',
              animation: false,
              data: this.data.speeds.max,
              coordinateSystem: 'polar',
              itemStyle: {
                color: this.getColor('danger')
              },
              label: {
                color: NbColorHelper.hexToRgbA(this.colors.success, 0.8)
              },
              name: 'Maximum',
              stack: 'a'
            }
          ],
          legend: {
            show: true,
            left: 5,
            orient: 'vertical',
            data: ['Minimum', 'Average', 'Maximum'],
            textStyle: labeltext
          }
        }
      )
    })
  }


  ngOnDestroy() {
    this.themeSubscription.unsubscribe();
  }
}




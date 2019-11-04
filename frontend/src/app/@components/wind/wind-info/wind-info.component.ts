import { Component, OnDestroy, Input, OnInit } from '@angular/core';
import { NbThemeService, NbColorHelper } from '@nebular/theme';
import { WindService } from '../../../@core/data/wind.service';
import { trigger, state, style } from '@angular/animations';

@Component({
  selector: 'ngx-wind-info',
  templateUrl: './wind-info.component.html',
  styleUrls: ['./wind-info.component.scss'],
  animations: [
    trigger('rotatedState', [
      state('N', style({ transform: 'rotate(0)' })),
      state('NNE', style({ transform: 'rotate(22.5deg)' })),
      state('NE', style({ transform: 'rotate(45deg)' })),
      state('ENE', style({ transform: 'rotate(67.50deg)' })),
      state('E', style({ transform: 'rotate(90deg)' })),
      state('ESE', style({ transform: 'rotate(112.5deg)' })),
      state('SE', style({ transform: 'rotate(135deg)' })),
      state('SSE', style({ transform: 'rotate(157.5deg)' })),
      state('S', style({ transform: 'rotate(180deg)' })),
      state('SSW', style({ transform: 'rotate(202.5deg)' })),
      state('SW', style({ transform: 'rotate(225deg)' })),
      state('WSW', style({ transform: 'rotate(247.5deg)' })),
      state('W', style({ transform: 'rotate(270deg)' })),
      state('WNW', style({ transform: 'rotate(292.5deg)' })),
      state('NW', style({ transform: 'rotate(315deg)' })),
      state('NNW', style({ transform: 'rotate(337.5deg)' })),
    ])
  ]
})

export class WindInfoComponent implements OnInit, OnDestroy {

  @Input() name: string;
  icon: string = 'arrow-circle-up-outline';
  windInfo: Object;
  interval: any;
  direction: string = 'N';
  dataAvailable: boolean = false

  constructor(
    private wind: WindService,
  ) { }

  ngOnInit() {
    this.refreshData();
    this.interval = setInterval(() => {
      this.refreshData();
    }, 60000);
  }

  ngOnDestroy() {
    clearInterval(this.interval);
  }

  refreshData() {
    this.wind.getWindInfo(this.name).subscribe(
      (data: {}) => {
        this.windInfo = data;
        this.dataAvailable = true;
      }
    );
  }
}

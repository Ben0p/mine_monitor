import { Component, Input } from '@angular/core';
import { trigger, state, style, animate, transition } from '@angular/animations';

@Component({
  selector: 'ngx-wind-status-card',
  styleUrls: ['./wind-status-card.component.scss'],
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
  ],
  template: `
    <nb-card [ngClass]="{'off': !on}">
      <div class="icon-container">
        <div class="icon status-{{ status }}">
        <nb-icon [@rotatedState]="direction" icon="{{ icon }}" style="font-size: 50px"></nb-icon>
        </div>
      </div>
      <div class="details">
        <div class="title h5">{{ title }}</div>
        <div class="status paragraph-2">{{ on ? info + ' km/h - ' + direction : 'Offline' }}</div>
      </div>
    </nb-card>
  `,
})
export class WindStatusCardComponent {

  @Input() title: string;
  @Input() status: string;
  @Input() on = true;
  @Input() icon: string = 'arrow-circle-up-outline';
  @Input() info: string;
  @Input() direction: string = 'N';
  
}
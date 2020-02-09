import { Component, Input } from '@angular/core';

@Component({
  selector: 'ngx-tetra-radio-count-card',
  styleUrls: ['./tetra-radio-count-card.component.scss'],
  template: `
    <nb-card [ngClass]="{'off': !on}">
      <div class="icon-container">
        <div class="icon status-{{ type }}">
        <div class="count">{{count}}</div>
        </div>
      </div>
      <div class="details">
        <div class="title h5">{{ title }}</div>
        <div class="status paragraph-2">{{ on ? description : 'Offline' }}</div>
      </div>
    </nb-card>
`
})
export class TetraRadioCountCardComponent  {

  @Input() title: string;
  @Input() type: string;
  @Input() on = true;
  @Input() count: string;
  @Input() description: string;


}

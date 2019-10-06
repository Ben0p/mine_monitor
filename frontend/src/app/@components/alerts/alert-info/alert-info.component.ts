import { Component, Input, EventEmitter, Output } from '@angular/core';

@Component({
  selector: 'ngx-alert-info',
  templateUrl: './alert-info.component.html',
  styleUrls: ['./alert-info.component.scss']
})

export class AlertInfoComponent{
  @Input() uid: string;
  @Input() alert: any;

}

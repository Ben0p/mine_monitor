import { Component, Input } from '@angular/core';

@Component({
  selector: 'ngx-alert-sign',
  styleUrls: ['./alert-sign.component.scss'],
  templateUrl: './alert-sign.component.html',
})
export class AlertSignComponent {

  @Input() online: boolean;
  @Input() name: string;
  @Input() all_clear: boolean;
  @Input() emergency: boolean;
  @Input() lightning: boolean;
  @Input() a: boolean;
  @Input() b: boolean;
  @Input() c: boolean;

}
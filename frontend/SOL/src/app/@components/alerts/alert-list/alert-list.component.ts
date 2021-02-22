import { Component, Input } from '@angular/core';

@Component({
  selector: 'ngx-alert-list',
  templateUrl: './alert-list.component.html',
  styleUrls: ['./alert-list.component.scss']
})

export class AlertListComponent {
  @Input() alerts: any;

}

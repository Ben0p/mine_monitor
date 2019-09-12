import { Component, Input} from '@angular/core';

@Component({
  selector: 'ngx-alert-beacon',
  templateUrl: './alert-beacon.component.html',
  styleUrls: ['./alert-beacon.component.scss']
})
export class AlertBeaconComponent {

  @Input() online: boolean;
  @Input() name: string;
  @Input() c: boolean;

}

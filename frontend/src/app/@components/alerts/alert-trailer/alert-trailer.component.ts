import { Component, Input } from '@angular/core';

@Component({
  selector: 'ngx-alert-trailer',
  templateUrl: './alert-trailer.component.html',
  styleUrls: ['./alert-trailer.component.scss']
})
export class AlertTrailerComponent {
  @Input() online: boolean;
  @Input() name: string;
  @Input() modules: [];

}

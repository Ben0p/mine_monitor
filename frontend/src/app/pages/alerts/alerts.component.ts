import { Component } from '@angular/core';

@Component({
  selector: 'ngx-alerts',
  template: `
    <router-outlet *nbIsGranted="['view', 'alerts']"></router-outlet>
  `,
})

export class AlertsComponent {

}
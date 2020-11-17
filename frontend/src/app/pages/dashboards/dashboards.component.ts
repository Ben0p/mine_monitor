import { Component } from '@angular/core';

@Component({
  selector: 'ngx-dashboards',
  template: `
    <router-outlet *nbIsGranted="['view', 'dashboards']"></router-outlet>
  `,
})

export class DashboardsComponent {

}
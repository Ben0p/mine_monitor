import { Component } from '@angular/core';

@Component({
  selector: 'ngx-solar',
  template: `
    <router-outlet *nbIsGranted="['view', 'solar']"></router-outlet>
  `,
})

export class SolarComponent {

}
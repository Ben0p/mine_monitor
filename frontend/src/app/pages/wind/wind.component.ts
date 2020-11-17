import { Component } from '@angular/core';

@Component({
  selector: 'ngx-wind',
  template: `
    <router-outlet *nbIsGranted="['view', 'wind']"></router-outlet>
  `,
})

export class WindComponent {

}
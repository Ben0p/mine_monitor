import { Component } from '@angular/core';

@Component({
  selector: 'ngx-weather',
  template: `
    <router-outlet *nbIsGranted="['view', 'weather']"></router-outlet>
  `,
})

export class WeatherComponent {

}
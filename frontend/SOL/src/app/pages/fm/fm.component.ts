import { Component } from '@angular/core';

@Component({
  selector: 'ngx-fm',
  template: `
    <router-outlet *nbIsGranted="['view', 'fm']"></router-outlet>
  `,
})

export class FmComponent {

}
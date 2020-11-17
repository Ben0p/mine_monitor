import { Component } from '@angular/core';

@Component({
  selector: 'ngx-gen',
  template: `
    <router-outlet *nbIsGranted="['view', 'gen']"></router-outlet>
  `,
})

export class GenComponent {

}
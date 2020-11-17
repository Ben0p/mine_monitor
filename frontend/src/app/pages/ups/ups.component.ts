import { Component } from '@angular/core';

@Component({
  selector: 'ngx-ups',
  template: `
    <router-outlet *nbIsGranted="['view', 'ups']"></router-outlet>
  `,
})

export class UpsComponent {

}
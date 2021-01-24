import { Component } from '@angular/core';

@Component({
  selector: 'ngx-inspections',
  template: `
    <router-outlet *nbIsGranted="['view', 'inspections']"></router-outlet>
  `,
})

export class InspectionsComponent {

}
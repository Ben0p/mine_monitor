import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { UpsComponent } from './ups.component';
import { UpsStatusComponent } from './ups-status/ups-status.component';


const routes: Routes = [{
  path: '',
  component: UpsComponent,
  children: [
    {
      path: 'status',
      component: UpsStatusComponent,
    },
  ],
}];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class UpsRoutingModule { }
export const routedComponents = [
  UpsComponent,
  UpsStatusComponent,
];
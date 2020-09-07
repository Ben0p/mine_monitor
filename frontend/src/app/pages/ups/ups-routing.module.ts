import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { UpsComponent } from './ups.component';
import { UpsStatusComponent } from './ups-status/ups-status.component';
import { UpsEditComponent } from './ups-edit/ups-edit.component';


const routes: Routes = [{
  path: '',
  component: UpsComponent,
  children: [
    {
      path: 'status',
      component: UpsStatusComponent,
    },
    {
      path: 'edit',
      component: UpsEditComponent,
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
  UpsEditComponent
];
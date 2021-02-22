import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { GenComponent } from './gen.component';
import { GenStatusComponent } from './gen-status/gen-status.component';


const routes: Routes = [{
  path: '',
  component: GenComponent,
  children: [
    {
      path: 'status',
      component: GenStatusComponent,
    },
  ],
}];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class GenRoutingModule { }
export const routedComponents = [
  GenComponent,
  GenStatusComponent,
];
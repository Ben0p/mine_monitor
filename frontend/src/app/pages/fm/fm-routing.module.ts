import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { FmComponent } from './fm.component';
import { FmStatusComponent } from './fm-status/fm-status.component';


const routes: Routes = [{
  path: '',
  component: FmComponent,
  children: [
    {
      path: 'status',
      component: FmStatusComponent,
    },
  ],
}];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class FmRoutingModule { }
export const routedComponents = [
  FmComponent,
  FmStatusComponent,
];
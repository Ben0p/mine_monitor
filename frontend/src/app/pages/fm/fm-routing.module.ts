import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { FmComponent } from './fm.component';
import { FmStatusComponent } from './fm-status/fm-status.component';
import { FmEditComponent } from './fm-edit/fm-edit.component';

const routes: Routes = [{
  path: '',
  component: FmComponent,
  children: [
    {
      path: 'status',
      component: FmStatusComponent,
    },
    {
      path: 'edit',
      component: FmEditComponent,
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
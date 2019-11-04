import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { WindComponent } from './wind.component';
import { AllComponent } from './all/all.component';
import { DetailComponent } from './detail/detail.component';

const routes: Routes = [{
  path: '',
  component: WindComponent,
  children: [
    {
      path: 'all',
      component: AllComponent,
    },
    {
      path: ':name',
      component: DetailComponent,
    },
  ],
}];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class WindRoutingModule { }
export const routedComponents = [
  WindComponent,
  AllComponent
];
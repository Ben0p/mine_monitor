import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { WindComponent } from './wind.component';
import { AllComponent } from './all/all.component';

const routes: Routes = [{
  path: '',
  component: WindComponent,
  children: [
    {
      path: 'all',
      component: AllComponent,
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
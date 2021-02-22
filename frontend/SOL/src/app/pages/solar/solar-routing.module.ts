import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { SolarComponent } from './solar.component';
import { SolarControllersComponent } from './solar-controllers/solar-controllers.component';
import { SolarEditComponent } from './solar-edit/solar-edit.component';

const routes: Routes = [{
  path: '',
  component: SolarComponent,
  children: [
    {
      path: 'controllers',
      component: SolarControllersComponent,
    },
    {
      path: 'edit',
      component: SolarEditComponent,
    },
  ],
}];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class SolarRoutingModule { }
export const routedComponents = [
  SolarComponent,
  SolarControllersComponent,
  SolarEditComponent
];
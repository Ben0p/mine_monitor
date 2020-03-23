import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { DashboardsComponent } from './dashboards.component';
import { DashAlertsTetraComponent } from './dash-alerts-tetra/dash-alerts-tetra.component'



const routes: Routes = [{
  path: '',
  component: DashboardsComponent,
  children: [
    {
      path: 'alerts-tetra',
      component: DashAlertsTetraComponent,
    },
  ],
}];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class DashboardsRoutingModule { }
export const routedComponents = [
  DashboardsComponent,
  DashAlertsTetraComponent
];
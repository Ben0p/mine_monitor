import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { DashboardsComponent } from './dashboards.component';
import { DashAlertsTetraComponent } from './dash-alerts-tetra/dash-alerts-tetra.component'
import { DashPowerComponent } from './dash-power/dash-power.component'



const routes: Routes = [{
  path: '',
  component: DashboardsComponent,
  children: [
    {
      path: 'alerts-tetra',
      component: DashAlertsTetraComponent,
    },
    {
      path: 'power',
      component: DashPowerComponent,
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
  DashAlertsTetraComponent,
  DashPowerComponent
];
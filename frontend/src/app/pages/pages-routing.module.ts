import { RouterModule, Routes } from '@angular/router';
import { NgModule } from '@angular/core';

import { PagesComponent } from './pages.component';


const routes: Routes = [{
  path: '',
  component: PagesComponent,
  children: [
    {
      path: 'dashboards',
      loadChildren: () => import('./dashboards/dashboards.module')
        .then(m => m.DashboardsModule),
    },
    {
      path: 'settings',
      loadChildren: () => import('./settings/settings.module')
        .then(m => m.SettingsModule),
    },
    {
      path: 'alerts',
      loadChildren: () => import('./alerts/alerts.module')
        .then(m => m.AlertsModule),
    },
    {
      path: 'wind',
      loadChildren: () => import('./wind/wind.module')
        .then(m => m.WindModule),
    },
    {
      path: 'tetra',
      loadChildren: () => import('./tetra/tetra.module')
        .then(m => m.TetraModule),
    },
    {
      path: 'solar',
      loadChildren: () => import('./solar/solar.module')
        .then(m => m.SolarModule),
    },
    {
      path: 'gen',
      loadChildren: () => import('./gen/gen.module')
        .then(m => m.GenModule),
    },
    {
      path: 'fm',
      loadChildren: () => import('./fm/fm.module')
        .then(m => m.FmModule),
    },
    {
      path: '',
      redirectTo: 'dashboards/alerts-tetra',
      pathMatch: 'full',
    },
  ],
}];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class PagesRoutingModule {
}

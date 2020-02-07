import { RouterModule, Routes } from '@angular/router';
import { NgModule } from '@angular/core';

import { PagesComponent } from './pages.component';
import { DashboardComponent } from './dashboard/dashboard.component';

const routes: Routes = [{
  path: '',
  component: PagesComponent,
  children: [
    {
      path: 'dashboard',
      component: DashboardComponent,
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
      path: '',
      redirectTo: 'dashboard',
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

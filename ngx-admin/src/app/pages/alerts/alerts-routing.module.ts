import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { AlertsComponent } from './alerts.component';
import { OverviewComponent } from './overview/overview.component';
import { ListComponent } from './list/list.component';
import { AllComponent } from './all/all.component';
import { DisplayComponent } from './display/display.component';

const routes: Routes = [{
  path: '',
  component: AlertsComponent,
  children: [
    {
      path: 'overview',
      component: OverviewComponent,
    },
    {
      path: 'all',
      component: AllComponent,
    },
    {
      path: 'display',
      component: DisplayComponent,
    },
    {
      path: 'list',
      component: ListComponent,
    },
  ],
}];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AlertsRoutingModule { }
export const routedComponents = [
  OverviewComponent,
  ListComponent
];
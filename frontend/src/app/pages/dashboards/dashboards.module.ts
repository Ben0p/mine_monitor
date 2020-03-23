import { NgModule } from '@angular/core';
import {
  NbActionsModule,
  NbButtonModule,
  NbCardModule,
  NbTabsetModule,
  NbUserModule,
  NbRadioModule,
  NbSelectModule,
  NbListModule,
  NbIconModule,
  NbAlertModule,
} from '@nebular/theme';

import { RouterModule } from '@angular/router';
import { DashboardsRoutingModule, routedComponents } from './dashboards-routing.module';

import { ThemeModule } from '../../@theme/theme.module';
import { DashboardsComponent } from './dashboards.component';
import { ComponentsModule } from '../../@components/components.module';
import { DashAlertsTetraComponent } from './dash-alerts-tetra/dash-alerts-tetra.component'


@NgModule({
  declarations: [
    ...routedComponents,
    DashboardsComponent,
    DashAlertsTetraComponent,
  ],
  imports: [
    DashboardsRoutingModule,
    NbCardModule,
    ThemeModule,
    NbListModule,
    NbTabsetModule,
    NbAlertModule,
    ComponentsModule,
    RouterModule
  ],
})
export class DashboardsModule { }


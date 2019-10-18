import { NgModule } from '@angular/core';
import {
  NbCardModule,
  NbSelectModule,
  NbButtonModule,
  NbIconModule,
  NbTabsetModule,
  NbListModule
} from '@nebular/theme';

import { NbSecurityModule } from '@nebular/security';

import { ThemeModule } from '../../@theme/theme.module';
import { NgxEchartsModule } from 'ngx-echarts';
import { NgxChartsModule } from '@swimlane/ngx-charts';
import { RouterModule } from '@angular/router';

import { AlertsRoutingModule, routedComponents } from './alerts-routing.module';

import { ComponentsModule } from '../../@components/components.module';

import { OverviewComponent } from './overview/overview.component';
import { AlertsD3AdvancedPieComponent } from './overview/alerts-d3-advanced-pie.component'
import { AlertsComponent } from './alerts.component';
import { ListComponent } from './list/list.component';
import { AllComponent } from './all/all.component'
import { DisplayComponent } from './display/display.component';
import { DetailComponent } from './detail/detail.component';
import { EditComponent } from './edit/edit.component'





@NgModule({
  declarations: [
    ...routedComponents,
    AlertsComponent,
    OverviewComponent,
    AlertsD3AdvancedPieComponent,
    ListComponent,
    AllComponent,
    DisplayComponent,
    DetailComponent,
    EditComponent,
  ],
  imports: [
    AlertsRoutingModule,
    ThemeModule,
    NbCardModule,
    NbSelectModule,
    NbButtonModule,
    NgxEchartsModule,
    NgxChartsModule,
    NbIconModule,
    RouterModule,
    ComponentsModule,
    NbSecurityModule,
    NbTabsetModule,
    NbListModule,
  ]
})
export class AlertsModule { }

import { NgModule } from '@angular/core';
import { NbMenuModule } from '@nebular/theme';
import { NbSecurityModule } from '@nebular/security';


import { ThemeModule } from '../@theme/theme.module';
import { PagesRoutingModule } from './pages-routing.module';
import { AlertsModule } from './alerts/alerts.module';
import { DashboardModule } from './dashboard/dashboard.module';
import { ComponentsModule } from '../@components/components.module';

import { PagesComponent } from './pages.component';




@NgModule({
  imports: [
    PagesRoutingModule,
    ThemeModule,
    NbMenuModule,
    DashboardModule,
    AlertsModule,
    ComponentsModule,
    NbSecurityModule,
  ],
  declarations: [
    PagesComponent,
  ],
})
export class PagesModule {
  
}

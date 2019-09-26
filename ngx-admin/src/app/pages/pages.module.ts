import { NgModule } from '@angular/core';
import { NbMenuModule } from '@nebular/theme';


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
  ],
  declarations: [
    PagesComponent,
  ],
})
export class PagesModule {
  
}

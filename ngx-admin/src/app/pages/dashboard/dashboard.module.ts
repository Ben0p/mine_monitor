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

import { ThemeModule } from '../../@theme/theme.module';
import { DashboardComponent } from './dashboard.component';


@NgModule({
  imports: [
    NbCardModule,
    ThemeModule,
    NbListModule,
    NbTabsetModule,
    NbAlertModule,
  ],
  declarations: [
    DashboardComponent,
  ],
})
export class DashboardModule { }


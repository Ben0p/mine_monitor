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
} from '@nebular/theme';

import { ThemeModule } from '../../@theme/theme.module';
import { DashboardComponent } from './dashboard.component';


@NgModule({
  imports: [
    NbCardModule,
    ThemeModule,
    NbListModule,
    NbTabsetModule,
  ],
  declarations: [
    DashboardComponent,
  ],
})
export class DashboardModule { }


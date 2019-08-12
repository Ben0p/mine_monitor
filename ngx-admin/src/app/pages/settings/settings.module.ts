import { NgModule } from '@angular/core';
import {
  NbCardModule,
  NbSelectModule,
  NbButtonModule,
} from '@nebular/theme';

import { ThemeModule } from '../../@theme/theme.module';

import { StyleComponent } from './style/style.component';
import { SettingsComponent } from './settings.component'

import { SettingsRoutingModule, routedComponents } from './settings-routing.module';


@NgModule({
  declarations: [
    ...routedComponents,
    SettingsComponent,
    StyleComponent,
  ],
  imports: [
    SettingsRoutingModule,
    ThemeModule,
    NbCardModule,
    NbSelectModule,
    NbButtonModule,
  ]
})
export class SettingsModule { }

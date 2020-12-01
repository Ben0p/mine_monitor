import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import {
  NbCardModule
} from '@nebular/theme';
import { NbSecurityModule } from '@nebular/security';

import { ComponentsModule } from '../../@components/components.module';

import { WeatherComponent } from './weather.component';
import { WindRoutingModule, routedComponents } from './weather-routing.module';


@NgModule({
  declarations: [
    ...routedComponents,
    WeatherComponent,
  ],
  imports: [
    WindRoutingModule,
    CommonModule,
    ComponentsModule,
    NbCardModule,
    NbSecurityModule
  ]
})
export class WeatherModule { }

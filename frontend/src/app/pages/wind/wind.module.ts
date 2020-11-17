import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import {
  NbCardModule
} from '@nebular/theme';
import { NbSecurityModule } from '@nebular/security';

import { ComponentsModule } from '../../@components/components.module';

import { WindComponent } from './wind.component';
import { AllComponent } from './all/all.component';
import { WindRoutingModule, routedComponents } from './wind-routing.module';
import { DetailComponent } from './detail/detail.component';

@NgModule({
  declarations: [
    ...routedComponents,
    AllComponent,
    WindComponent,
    DetailComponent,

  ],
  imports: [
    WindRoutingModule,
    CommonModule,
    ComponentsModule,
    NbCardModule,
    NbSecurityModule
  ]
})
export class WindModule { }

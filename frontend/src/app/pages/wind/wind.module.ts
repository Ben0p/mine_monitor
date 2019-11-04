import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import {
  NbCardModule,
  NbSelectModule,
  NbButtonModule,
  NbIconModule,
  NbTabsetModule,
  NbListModule
} from '@nebular/theme';

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
  ]
})
export class WindModule { }

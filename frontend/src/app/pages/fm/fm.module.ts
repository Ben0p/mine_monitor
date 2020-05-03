import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FmRoutingModule, routedComponents } from './fm-routing.module';

import {
  NbCardModule,
  NbButtonModule,
  NbIconModule,
} from '@nebular/theme';

import { ComponentsModule } from '../../@components/components.module';

import { FmComponent } from './fm.component';
import { FmStatusComponent } from './fm-status/fm-status.component';

@NgModule({
  declarations: [
    ...routedComponents,
    FmComponent,
    FmStatusComponent,
  ],
  imports: [
    CommonModule,
    ComponentsModule,
    FmRoutingModule,
    NbCardModule,
    NbButtonModule,
    NbIconModule,
  ]
})
export class FmModule { }

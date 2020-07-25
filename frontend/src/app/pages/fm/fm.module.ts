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
import { FmEditComponent } from './fm-edit/fm-edit.component';

@NgModule({
  declarations: [
    ...routedComponents,
    FmComponent,
    FmStatusComponent,
    FmEditComponent,
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

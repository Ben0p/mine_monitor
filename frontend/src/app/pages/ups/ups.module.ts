import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { UpsRoutingModule, routedComponents } from './ups-routing.module';
import { Ng2SmartTableModule } from 'ng2-smart-table';

import {
  NbCardModule,
  NbButtonModule,
  NbIconModule,
} from '@nebular/theme';

import { ComponentsModule } from '../../@components/components.module';

import { UpsComponent } from './ups.component';
import { UpsStatusComponent } from './ups-status/ups-status.component';
import { UpsEditComponent } from './ups-edit/ups-edit.component';


@NgModule({
  declarations: [
    ...routedComponents,
    UpsComponent,
    UpsStatusComponent,
    UpsEditComponent
  ],
  imports: [
    CommonModule,
    UpsRoutingModule,
    ComponentsModule,
    NbCardModule,
    NbButtonModule,
    NbIconModule,
    Ng2SmartTableModule
  ]
})
export class UpsModule { }

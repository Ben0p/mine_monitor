import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { GenRoutingModule, routedComponents } from './gen-routing.module';
import { Ng2SmartTableModule } from 'ng2-smart-table';

import {
  NbCardModule,
  NbButtonModule,
  NbIconModule,
} from '@nebular/theme';

import { ComponentsModule } from '../../@components/components.module';

import { GenComponent } from './gen.component';
import { GenStatusComponent } from './gen-status/gen-status.component';


@NgModule({
  declarations: [
    ...routedComponents,
    GenComponent,
    GenStatusComponent
  ],
  imports: [
    CommonModule,
    GenRoutingModule,
    ComponentsModule,
    NbCardModule,
    NbButtonModule,
    NbIconModule,
    Ng2SmartTableModule
  ]
})
export class GenModule { }

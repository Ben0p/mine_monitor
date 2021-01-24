import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Ng2SmartTableModule } from 'ng2-smart-table';
import { NbSecurityModule } from '@nebular/security';

import { ComponentsModule } from '../../@components/components.module';

import {
  NbCardModule,
  NbButtonModule,
  NbIconModule,
  NbInputModule,
  NbFormFieldModule
} from '@nebular/theme';

import { InspectionsRoutingModule, routedComponents } from './inspections-routing.module';
import { InspectionsComponent } from './inspections.component';
import { InspectionsListComponent } from './inspections-list/inspections-list.component';
import { InspectionsUploadComponent } from './inspections-upload/inspections-upload.component';



@NgModule({
  declarations: [
    ...routedComponents,
    InspectionsComponent,
    InspectionsListComponent,
    InspectionsUploadComponent
  ],
  imports: [
    CommonModule,
    InspectionsRoutingModule,
    ComponentsModule,
    Ng2SmartTableModule,
    NbSecurityModule,
    NbCardModule,
    NbButtonModule,
    NbIconModule,
    NbInputModule,
    NbFormFieldModule
  ]
})

export class InspectionsModule { }

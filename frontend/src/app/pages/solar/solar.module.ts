import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SolarRoutingModule, routedComponents } from './solar-routing.module';
import { Ng2SmartTableModule } from 'ng2-smart-table';

import {
  NbCardModule,
  NbButtonModule,
  NbIconModule,
} from '@nebular/theme';

import { ComponentsModule } from '../../@components/components.module';

import { SolarComponent } from './solar.component';
import { SolarControllersComponent } from './solar-controllers/solar-controllers.component';
import { SolarEditComponent } from './solar-edit/solar-edit.component';



@NgModule({
  declarations: [
    ...routedComponents,
    SolarComponent,
    SolarControllersComponent,
    SolarEditComponent,
  ],
  imports: [
    CommonModule,
    SolarRoutingModule,
    ComponentsModule,
    NbCardModule,
    NbButtonModule,
    NbIconModule,
    Ng2SmartTableModule
  ]
})
export class SolarModule { }

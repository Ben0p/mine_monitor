import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TetraRoutingModule, routedComponents } from './tetra-routing.module';

import { ComponentsModule } from '../../@components/components.module';

import { TetraComponent } from './tetra.component';
import { NodesComponent } from './nodes/nodes.component';

@NgModule({
  declarations: [
    ...routedComponents,
    TetraComponent,
    NodesComponent
  ],
  imports: [
    TetraRoutingModule,
    CommonModule,
    ComponentsModule,
  ]
})
export class TetraModule { }

import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { GenRoutingModule, routedComponents } from './map-routing.module';

import { MapComponent } from './map.component';
import { MapBaseComponent } from './map-base/map-base.component';

@NgModule({
  declarations: [
    ...routedComponents,
    MapComponent,
    MapBaseComponent
  ],
  imports: [
    CommonModule,
    GenRoutingModule
  ]
})
export class MapModule { }

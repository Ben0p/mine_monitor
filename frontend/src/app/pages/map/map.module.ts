import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MapRoutingModule, routedComponents } from './map-routing.module';

import { MapComponent } from './map.component';
import { AngularCesiumModule, AngularCesiumWidgetsModule } from 'angular-cesium';

@NgModule({
  declarations: [
    ...routedComponents,
    MapComponent,
  ],
  imports: [
    CommonModule,
    MapRoutingModule,
    AngularCesiumWidgetsModule,
    AngularCesiumModule.forRoot(
      {
        fixEntitiesShadows: false,
        customPipes: []
      }
    ),
  ]
})
export class MapModule { }

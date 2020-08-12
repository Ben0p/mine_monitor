import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MapRoutingModule, routedComponents } from './map-routing.module';

import { ComponentsModule } from '../../@components/components.module';

import {
  NbButtonModule,
  NbIconModule,
  NbPopoverModule,
  NbCardModule,
  NbCheckboxModule,
} from '@nebular/theme';

import { MapComponent } from './map.component';
import { AngularCesiumModule, AngularCesiumWidgetsModule } from 'angular-cesium';
import { MapSdsComponent } from './map-sds/map-sds.component';
import { MapOptionsComponent } from './map-options/map-options.component';

@NgModule({
  declarations: [
    ...routedComponents,
    MapComponent,
    MapSdsComponent,
    MapOptionsComponent,
  ],
  imports: [
    CommonModule,
    MapRoutingModule,
    AngularCesiumWidgetsModule,
    ComponentsModule,
    NbButtonModule,
    NbIconModule,
    NbPopoverModule,
    NbCardModule,
    NbCheckboxModule,
    AngularCesiumModule.forRoot(
      {
        fixEntitiesShadows: false,
        customPipes: []
      }
    ),
  ]
})
export class MapModule { }

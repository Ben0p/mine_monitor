
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {
    NbCardModule,
    NbSelectModule,
    NbButtonModule,
    NbIconModule
  } from '@nebular/theme';

import { StatusCardComponent } from './status-card/status-card.component'
import { AlertSignComponent } from './alert-sign/alert-sign.component';
import { AlertBeaconComponent } from './alert-beacon/alert-beacon.component';
import { AlertTrailerComponent } from './alert-trailer/alert-trailer.component'
 

@NgModule({
    declarations: [
        StatusCardComponent,
        AlertSignComponent,
        AlertBeaconComponent,
        AlertTrailerComponent,
    ],
    imports: [
        CommonModule,
        NbCardModule,
        NbSelectModule,
        NbButtonModule,
        NbIconModule,
    ],
    exports: [
        StatusCardComponent,
        AlertSignComponent,
        AlertBeaconComponent,
        AlertTrailerComponent
    ]
})

export class ComponentsModule { }
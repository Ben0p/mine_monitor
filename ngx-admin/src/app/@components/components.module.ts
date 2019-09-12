
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {
    NbCardModule,
    NbSelectModule,
    NbButtonModule,
    NbIconModule
  } from '@nebular/theme';

import { StatusCardComponent } from './status-card/status-card.component'
import { AlertSignComponent } from './alerts/alert-sign/alert-sign.component';
import { AlertBeaconComponent } from './alerts/alert-beacon/alert-beacon.component';
import { AlertTrailerComponent } from './alerts/alert-trailer/alert-trailer.component';
import { AlertControlsComponent } from './alerts/alert-controls/alert-controls.component'
 

@NgModule({
    declarations: [
        StatusCardComponent,
        AlertSignComponent,
        AlertBeaconComponent,
        AlertTrailerComponent,
        AlertControlsComponent,
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
        AlertTrailerComponent,
        AlertControlsComponent,
    ]
})

export class ComponentsModule { }

import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {
    NbCardModule,
    NbSelectModule,
    NbButtonModule,
    NbIconModule,
    NbListModule,
    NbUserModule,
  } from '@nebular/theme';

import { StatusCardComponent } from './status-card/status-card.component'
import { AlertSignComponent } from './alerts/alert-sign/alert-sign.component';
import { AlertBeaconComponent } from './alerts/alert-beacon/alert-beacon.component';
import { AlertTrailerComponent } from './alerts/alert-trailer/alert-trailer.component';
import { AlertControlsComponent } from './alerts/alert-controls/alert-controls.component';
import { AlertInfoComponent } from './alerts/alert-info/alert-info.component';


@NgModule({
    declarations: [
        StatusCardComponent,
        AlertSignComponent,
        AlertBeaconComponent,
        AlertTrailerComponent,
        AlertControlsComponent,
        AlertInfoComponent,
    ],
    imports: [
        CommonModule,
        NbCardModule,
        NbSelectModule,
        NbButtonModule,
        NbIconModule,
        NbListModule,
        NbUserModule,
    ],
    exports: [
        StatusCardComponent,
        AlertSignComponent,
        AlertBeaconComponent,
        AlertTrailerComponent,
        AlertControlsComponent,
        AlertInfoComponent,
    ]
})

export class ComponentsModule { }
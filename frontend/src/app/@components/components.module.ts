
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
import { Ng2SmartTableModule } from 'ng2-smart-table';

import { ThemeModule } from '../@theme/theme.module';

import { StatusCardComponent } from './status-card/status-card.component'
import { AlertSignComponent } from './alerts/alert-sign/alert-sign.component';
import { AlertBeaconComponent } from './alerts/alert-beacon/alert-beacon.component';
import { AlertTrailerComponent } from './alerts/alert-trailer/alert-trailer.component';
import { AlertControlsComponent } from './alerts/alert-controls/alert-controls.component';
import { AlertInfoComponent } from './alerts/alert-info/alert-info.component';
import { AlertTableModulesComponent } from './alerts/alert-table-modules/alert-table-modules.component';
import { AlertTableZonesComponent } from './alerts/alert-table-zones/alert-table-zones.component';



@NgModule({
    declarations: [
        StatusCardComponent,
        AlertSignComponent,
        AlertBeaconComponent,
        AlertTrailerComponent,
        AlertControlsComponent,
        AlertInfoComponent,
        AlertTableModulesComponent,
        AlertTableZonesComponent,
    ],
    imports: [
        CommonModule,
        ThemeModule,
        NbCardModule,
        NbSelectModule,
        NbButtonModule,
        NbIconModule,
        NbListModule,
        NbUserModule,
        Ng2SmartTableModule
    ],
    exports: [
        StatusCardComponent,
        AlertSignComponent,
        AlertBeaconComponent,
        AlertTrailerComponent,
        AlertControlsComponent,
        AlertInfoComponent,
        AlertTableModulesComponent,
        AlertTableZonesComponent,
    ]
})

export class ComponentsModule { }
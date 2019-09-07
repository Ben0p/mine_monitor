
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {
    NbCardModule,
    NbSelectModule,
    NbButtonModule,
    NbIconModule
  } from '@nebular/theme';

import { StatusCardComponent } from './status-card/status-card.component'
import { AlertSignComponent } from './alert-sign/alert-sign.component'
 

@NgModule({
    declarations: [
        StatusCardComponent,
        AlertSignComponent,
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
        AlertSignComponent
    ]
})

export class ComponentsModule { }

import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { StatusCardComponent } from './status-card/status-card.component'
import {
    NbCardModule,
    NbSelectModule,
    NbButtonModule,
    NbIconModule
  } from '@nebular/theme';
 

@NgModule({
    declarations: [
        StatusCardComponent
    ],
    imports: [
        CommonModule,
        NbCardModule,
        NbSelectModule,
        NbButtonModule,
        NbIconModule,
    ],
    exports: [
        StatusCardComponent
    ]
})

export class ComponentsModule { }
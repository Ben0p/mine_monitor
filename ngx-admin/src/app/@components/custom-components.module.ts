
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AlertsD3AdvancedPieComponent } from './alerts/alerts-d3-advanced-pie.component'


@NgModule({
    declarations: [
        AlertsD3AdvancedPieComponent,
    ],
    imports: [
        CommonModule
    ],
    exports: [
        AlertsD3AdvancedPieComponent,
    ]
})

export class CustomComponentsModule { }
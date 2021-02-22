
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {
    NbCardModule,
    NbSelectModule,
    NbButtonModule,
    NbIconModule,
    NbListModule,
    NbUserModule,
    NbRadioModule,
    NbTabsetModule,
    NbProgressBarModule,
  } from '@nebular/theme';
import { Ng2SmartTableModule } from 'ng2-smart-table';
import { ChartModule } from 'angular2-chartjs';
import { NgxEchartsModule } from 'ngx-echarts';

import { ThemeModule } from '../@theme/theme.module';

import { StatusCardComponent } from './status-card/status-card.component'

import { AlertSignComponent } from './alerts/alert-sign/alert-sign.component';
import { AlertBeaconComponent } from './alerts/alert-beacon/alert-beacon.component';
import { AlertTrailerComponent } from './alerts/alert-trailer/alert-trailer.component';
import { AlertControlsComponent } from './alerts/alert-controls/alert-controls.component';
import { AlertInfoComponent } from './alerts/alert-info/alert-info.component';
import { AlertTableModulesComponent } from './alerts/alert-table-modules/alert-table-modules.component';
import { AlertTableZonesComponent } from './alerts/alert-table-zones/alert-table-zones.component';
import { AlertListInfiniteComponent } from './alerts/alert-list-infinite/alert-list-infinite.component';
import { AlertListComponent } from './alerts/alert-list/alert-list.component';

import { WindLineChartComponent } from './wind/wind-line-chart/wind-line-chart.component';
import { WindStatusCardComponent } from './wind/wind-status-card/wind-status-card.component';
import { WindInfoComponent } from './wind/wind-info/wind-info.component';
import { WindSpeedCardComponent } from './wind/wind-speed-card/wind-speed-card.component';

import { TetraBarChartComponent } from './tetra/tetra-bar-chart/tetra-bar-chart.component';
import { TetraSubsChartComponent } from './tetra/tetra-subs-chart/tetra-subs-chart.component';
import { TetraRadarChartComponent } from './tetra/tetra-radar-chart/tetra-radar-chart.component';
import { TetraRadioCountCardComponent } from './tetra/tetra-radio-count-card/tetra-radio-count-card.component';
import { TetraSubscriberTableComponent } from './tetra/tetra-subscriber-table/tetra-subscriber-table.component';
import { TetraCallsLineChartComponent } from './tetra/tetra-calls-line-chart/tetra-calls-line-chart.component';

import { SolarDoughnutComponent } from './solar/solar-doughnut/solar-doughnut.component';

import { GenStatusComponent } from './gen/gen-status/gen-status.component';

import { FmLiveComponent } from './fm/fm-live/fm-live.component';

import { WeatherWindDirectionComponent } from './weather/wind-direction/weather-wind-direction.component';



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
        AlertListInfiniteComponent,
        AlertListComponent,
        WindLineChartComponent,
        WindStatusCardComponent,
        WindInfoComponent,
        WindSpeedCardComponent,
        TetraBarChartComponent,
        TetraSubsChartComponent,
        TetraRadarChartComponent,
        TetraRadioCountCardComponent,
        TetraSubscriberTableComponent,
        TetraCallsLineChartComponent,
        SolarDoughnutComponent,
        GenStatusComponent,
        FmLiveComponent,
        WeatherWindDirectionComponent,
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
        Ng2SmartTableModule,
        ChartModule,
        NgxEchartsModule,
        NbRadioModule,
        NbTabsetModule,
        NbProgressBarModule,
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
        AlertListInfiniteComponent,
        AlertListComponent,
        WindLineChartComponent,
        WindStatusCardComponent,
        WindInfoComponent,
        WindSpeedCardComponent,
        TetraBarChartComponent,
        TetraSubsChartComponent,
        TetraRadarChartComponent,
        TetraRadioCountCardComponent,
        TetraSubscriberTableComponent,
        TetraCallsLineChartComponent,
        SolarDoughnutComponent,
        GenStatusComponent,
        FmLiveComponent,
        WeatherWindDirectionComponent,
    ]
})

export class ComponentsModule { }
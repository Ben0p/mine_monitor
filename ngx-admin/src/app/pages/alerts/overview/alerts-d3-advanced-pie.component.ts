import { Component, OnInit, OnDestroy } from '@angular/core';
import { NbThemeService } from '@nebular/theme';

import { AlertService } from '../../../@core/data/alerts'


@Component({
    selector: 'ngx-alerts-d3-advanced-pie',
    template: `
    <ngx-charts-advanced-pie-chart
      [scheme]="colorScheme"
      [results]="single">
    </ngx-charts-advanced-pie-chart>
  `,
})
export class AlertsD3AdvancedPieComponent implements OnDestroy, OnInit {
    alerts$: Object;
    interval: any;

    single: Object

    colorScheme: any;
    themeSubscription: any;

    constructor(
        private theme: NbThemeService,
        private alerts: AlertService,
    ) {

        this.themeSubscription = this.theme.getJsTheme().subscribe(config => {
            const colors: any = config.variables;
            this.colorScheme = {
                domain: [colors.successLight, colors.dangerLight, colors.infoLight, colors.warningLight, colors.dangerLight, '#d9d9d9'],
            };
        });
    }

    ngOnDestroy(): void {
        this.themeSubscription.unsubscribe();
        clearInterval(this.interval);
    }

    ngOnInit() {
        this.refreshData();
        this.interval = setInterval(() => {
            this.refreshData();
        }, 1000);
    }

    refreshData() {
        this.alerts.getAlertsOverview().subscribe(
            (
                data: {}) => {
                this.alerts$ = data;
                this.single = [
                    {
                        name: 'All Clear',
                        value: this.alerts$['all_clear'],
                    },
                    {
                        name: 'Emergency',
                        value: this.alerts$['emergency'],
                    },
                    {
                        name: 'A Alert',
                        value: this.alerts$['a'],
                    },
                    {
                        name: 'B Alert',
                        value: this.alerts$['b'],
                    },
                    {
                        name: 'C Alert',
                        value: this.alerts$['c'],
                    },
                    {
                        name: 'Offline',
                        value: this.alerts$['offline'],
                    },
                ]
            }
        );
    }

}
import { Component, OnInit} from '@angular/core';
import { AlertService } from '../../../@core/data/alerts.service'


@Component({
  selector: 'ngx-list',
  templateUrl: './list.component.html',
  styleUrls: ['./list.component.scss'],
})

export class ListComponent implements OnInit {
  alert$: {};

  constructor(
    private alerts: AlertService,
  ) { }

  ngOnInit() {
    this.refreshData();
  }

  refreshData() {
    this.alerts.getAlerts().subscribe(
      (data: {}) => {
        this.alert$ = data;
      }
    );
  }

}
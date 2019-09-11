import { Component, OnInit, OnDestroy } from '@angular/core';
import { AlertService } from '../../../@core/data/alerts.service'
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'detail',
  templateUrl: './detail.component.html',
  styleUrls: ['./detail.component.scss']
})
export class DetailComponent implements OnInit, OnDestroy {
  alert: {};
  interval: any;

  constructor(
    private alerts: AlertService,
    private route: ActivatedRoute,
  ) { }

  ngOnInit() {
    this.refreshData();
    this.interval = setInterval(() => {
      this.refreshData();
    }, 5000);
  }

  ngOnDestroy() {
    clearInterval(this.interval);
  }

  uid = this.route.snapshot.paramMap.get('uid');

  refreshData() {
    this.alerts.getAlertDetail(this.uid).subscribe(
      (data: {}) => {
        this.alert = data;
      }
    );
  }

}

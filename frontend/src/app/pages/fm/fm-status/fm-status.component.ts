import { Component, OnInit, OnDestroy } from '@angular/core';
import { FmService } from '../../../@core/data/fm.service'


@Component({
  selector: 'fm-status',
  templateUrl: './fm-status.component.html',
  styleUrls: ['./fm-status.component.scss']
})


export class FmStatusComponent implements OnInit, OnDestroy{
  fm_statuses: Object;
  interval: any;

  constructor(
    private fm: FmService,
  ) {}

  ngOnInit() {
    this.refreshData();
    this.interval = setInterval(() => {
      this.refreshData();
    }, 10000);
  }

  ngOnDestroy() {
    clearInterval(this.interval);
  }
  
  refreshData() {
    this.fm.getFmLive().subscribe(
      (data: {}) => {
        this.fm_statuses = data;
      }
    );
  }

}

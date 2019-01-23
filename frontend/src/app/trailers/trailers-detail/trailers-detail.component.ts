import { Component, OnInit, OnDestroy } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';

import { DataService } from '../../data.service';

@Component({
  selector: 'app-trailers-detail',
  templateUrl: './trailers-detail.component.html',
  styleUrls: ['./trailers-detail.component.scss']
})
export class TrailersDetailComponent implements OnInit, OnDestroy {

  trailer$: Object;
  interval: any;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private data: DataService
  ) { }

  ngOnInit() {
    this.refreshData();
    this.interval = setInterval(() => {
      this.refreshData();
    }, 1000);
  }

  name = this.route.snapshot.paramMap.get('name');

  refreshData() {
    this.data.trailerDetail(this.name)
      .subscribe((data: {}) => {
        this.trailer$ = data;
      })
  }

  ngOnDestroy() {
    clearInterval(this.interval);
  }


}

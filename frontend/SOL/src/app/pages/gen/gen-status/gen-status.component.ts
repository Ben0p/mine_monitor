import { Component, OnInit, OnDestroy } from '@angular/core';
import { GenService } from '../../../@core/data/gen.service'

@Component({
  selector: 'gen-status',
  templateUrl: './gen-status.component.html',
  styleUrls: ['./gen-status.component.scss']
})

export class GenStatusComponent implements OnInit, OnDestroy{
  gen$: Object;
  interval: any;

  constructor(
    private gen: GenService,
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
    this.gen.getGenStatus().subscribe(
      (data: {}) => {
        this.gen$ = data;
      }
    );
  }

}

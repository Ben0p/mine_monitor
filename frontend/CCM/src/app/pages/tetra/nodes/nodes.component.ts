import { Component, OnInit, OnDestroy } from '@angular/core';
import { TetraService } from '../../../@core/data/tetra.service'

@Component({
  selector: 'nodes',
  templateUrl: './nodes.component.html',
  styleUrls: ['./nodes.component.scss']
})
export class NodesComponent implements OnInit, OnDestroy {
  nodes: Object;
  load: Object;
  interval: any;

  constructor(
    private tetra: TetraService,
  ) { }

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

  }
}

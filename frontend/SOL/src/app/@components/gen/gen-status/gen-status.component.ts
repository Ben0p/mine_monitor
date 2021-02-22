import { Component, Input, OnDestroy } from '@angular/core';

@Component({
  selector: 'ngx-gen-status',
  templateUrl: './gen-status.component.html',
  styleUrls: ['./gen-status.component.scss']
})
export class GenStatusComponent {

  @Input() online: boolean;
  @Input() name: any;
  @Input() oil: any;
  @Input() flex: any;
  @Input() fuel: any;
  @Input() level: any;
  @Input() color: any;
  @Input() temps: any;


  constructor() { 
  }
    

}

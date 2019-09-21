import { Component, Input, EventEmitter, Output, } from '@angular/core';

@Component({
  selector: 'ngx-alert-controls',
  templateUrl: './alert-controls.component.html',
  styleUrls: ['./alert-controls.component.scss']
})

export class AlertControlsComponent{
  @Input() type: string;
  @Input() all_clear: boolean;
  @Input() emergency: boolean;
  @Input() lightning: boolean;
  @Input() a: boolean;
  @Input() b: boolean;
  @Input() c: boolean;
  @Output() stateChange = new EventEmitter();


  toggle(type, state){
    this.stateChange.emit(
      {
        'type' : type,
        'state' : state
      }
    )
  }


}
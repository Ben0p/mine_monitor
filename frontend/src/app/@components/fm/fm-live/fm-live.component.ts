import { Component, Input } from '@angular/core';

@Component({
  selector: 'ngx-fm-live',
  templateUrl: './fm-live.component.html',
  styleUrls: ['./fm-live.component.scss']
})

export class FmLiveComponent {

  @Input() station: string = 'Station';
  @Input() state: string = 'State';
  @Input() artist: string = 'Artist';
  @Input() song: string = 'Song';

}

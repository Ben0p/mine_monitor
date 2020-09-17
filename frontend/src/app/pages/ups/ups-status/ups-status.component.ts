import { Component, ChangeDetectionStrategy } from '@angular/core';
import { catchError, map, tap, shareReplay } from 'rxjs/operators';
import { Subject, combineLatest, EMPTY } from 'rxjs';

import { UpsStatusService } from './ups-status.service';


@Component({
  selector: 'ups-status',
  templateUrl: './ups-status.component.html',
  styleUrls: ['./ups-status.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class UpsStatusComponent {
  private errorMessageSubject = new Subject<string>();
  errorMessage$ = this.errorMessageSubject.asObservable();

  constructor(
    private upsStatusService: UpsStatusService,
  ) { }

  ups$ = this.upsStatusService.ups$
  .pipe(
    catchError(err => {
      this.errorMessageSubject.next(err);
      return EMPTY
    })
  );


}



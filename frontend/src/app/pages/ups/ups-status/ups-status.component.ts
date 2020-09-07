import { Component, ChangeDetectionStrategy } from '@angular/core';
import { catchError, map, tap, shareReplay } from 'rxjs/operators';
import { Subject, EMPTY, combineLatest } from 'rxjs';

import { UpsStatusService } from './ups-status.service';
import { UpsModuleService } from '../ups-modules/ups-modules.service';


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
    private upsModuleService: UpsModuleService,
  ) { }

  mergeById = ([t, s]) => t.map(p => Object.assign({}, p, s.find(q => p._id.$oid === q._id.$oid)));

  ups$ = combineLatest([
    this.upsModuleService.ups$,
    this.upsStatusService.ups$
  ])
    .pipe(
      map(this.mergeById),
      shareReplay(1)
    );
}



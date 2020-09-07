import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Observable, throwError, interval } from 'rxjs';
import { catchError, tap, shareReplay, map, flatMap, startWith } from 'rxjs/operators';

import { Ups } from './ups-status';

@Injectable({
  providedIn: 'root'
})
export class UpsStatusService {
  private upsUrl = 'http://localhost:5000/api/ups/status';

  getUpsStatus() {
    return this.http.get<Ups[]>(this.upsUrl)
 }

 ups$ = interval(10000)
          .pipe(
            startWith(0),
            flatMap(() => this.getUpsStatus()),
            shareReplay(1),
            catchError(this.handleError)
          )

  constructor(
    private http: HttpClient,
  ) { }

  private handleError(err: any): Observable<never> {
    // in a real world app, we may send the server to some remote logging infrastructure
    // instead of just logging it to the console
    let errorMessage: string;
    if (err.error instanceof ErrorEvent) {
      // A client-side or network error occurred. Handle it accordingly.
      errorMessage = `An error occurred: ${err.error.message}`;
    } else {
      // The backend returned an unsuccessful response code.
      // The response body may contain clues as to what went wrong,
      errorMessage = `Backend returned code ${err.status}: ${err.body.error}`;
    }
    console.error(err);
    return throwError(errorMessage);
  }

}

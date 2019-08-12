import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { map, catchError, tap } from 'rxjs/operators';

import { AlertModules } from './alert-modules.model'

const httpOptions = {
  headers: new HttpHeaders({
    'Content-Type': 'application/json',
  }),
};

const APIurl: String = 'http://localhost:5000/';

@Injectable({
  providedIn: 'root',
})
export class AlertService {
  constructor(private http: HttpClient) {}

  private extractData(res: Response) {
    const body = res;
    return body || {};
  }

  private handleError<T>(operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {
      console.error(error); // log to console

      // TODO: better job of transforming error for user consumption
      // console.log(`${operation} failed: ${error.message}`);

      // Let the app keep running by returning an empty result.
      return of(result as T);
    };
  }

  private returnFalse<T>(operation = 'operation', result?: T) {
    const status = {'online' : result};
    return of(result as T);
  }

  getAlerts(): Observable<any> {
    return this.http.get(APIurl + "alert").pipe(
      map(this.extractData),
      catchError(this.handleError<any>("failed"))
    );
  }

  getAlertsOverview(): Observable<any> {
    return this.http.get(APIurl + "alert_overview").pipe(
      map(this.extractData),
      catchError(this.handleError<any>("failed"))
    );
  }

  getAlertModules(): Observable<any> {
    return this.http.get(APIurl + "alert_modules").pipe(
      map(this.extractData),
      catchError(this.handleError<any>("failed"))
    );
  }
}
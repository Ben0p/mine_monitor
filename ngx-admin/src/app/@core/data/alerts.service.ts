import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { map, catchError, tap } from 'rxjs/operators';
import { NbToastrService } from '@nebular/theme';


const httpOptions = {
  headers: new HttpHeaders({
    'Content-Type': 'application/json',
  }),
};

const APIurl: String = 'http://localhost:5000/alerts/';

@Injectable({
  providedIn: 'root',
})
export class AlertService {
  constructor(
    private http: HttpClient,
    private toastrService: NbToastrService,
    ) {}

  private extractData(res: Response) {
    const body = res;
    return body || {};
  }

  private handleError<T>(operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {
      console.error(error); // log to console
      this.dangerToast('top-right', 'danger', error.statusText, error.status)

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
    return this.http.get(APIurl + "all").pipe(
      map(this.extractData),
      catchError(this.handleError<any>("failed"))
    );
  }

  getAlertsOverview(): Observable<any> {
    return this.http.get(APIurl + "overview").pipe(
      map(this.extractData),
      catchError(this.handleError<any>("failed"))
    );
  }

  getAlertModules(): Observable<any> {
    return this.http.get(APIurl + "modules").pipe(
      map(this.extractData),
      catchError(this.handleError<any>("failed"))
    );
  }

  getAlertZones(): Observable<any> {
    return this.http.get(APIurl + "zones").pipe(
      map(this.extractData),
      catchError(this.handleError<any>("failed"))
    );
  }

  getAlertTypes(): Observable<any> {
    return this.http.get(APIurl + "types").pipe(
      map(this.extractData),
      catchError(this.handleError<any>("failed"))
    );
  }

  getAlertStatus(): Observable<any> {
    return this.http.get(APIurl + "status").pipe(
      map(this.extractData),
      catchError(this.handleError<any>("failed"))
    );
  }

  deleteAlertModules(module): Observable<any> {
    return this.http.get(APIurl + "delete/"+module).pipe(
      map(
        this.extractData,
        (response: Response) => {
          console.log(response);
          this.successToast('top-right', 'success', response.statusText, response.status)
        }
      ),
      catchError(this.handleError<any>("failed"))
    );
  }


  dangerToast(position, status, message, code) {
      this.toastrService.show(
        'API call error - '+code+': '+message,
        `Failed`,
        { position, status });
  }

  successToast(position, status, message, code) {
    this.toastrService.show(
      'API call error - '+code+': '+message,
      `Failed`,
      { position, status });
}


}

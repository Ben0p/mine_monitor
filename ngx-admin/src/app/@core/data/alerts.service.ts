import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { map, catchError, tap } from 'rxjs/operators';
import { NbToastrService, NbToastRef } from '@nebular/theme';


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
  ) { }

  toastRef: NbToastRef
  tempToast: NbToastRef

  private extractData(res: Response) {
    const body = res;
    return body || {};
  }

  private handleError<T>(operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {
      this.dangerToast('top-right', 'danger', error.statusText, error.status)
      return of(result as T);
    };
  }

  private returnFalse<T>(operation = 'operation', result?: T) {
    const status = { 'online': result };
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

  getAlertAll(): Observable<any> {
    return this.http.get(APIurl + "all").pipe(
      map(this.extractData),
      catchError(this.handleError<any>("failed"))
    );
  }

  getAlertStatus(): Observable<any> {
    var data = this.http.get(APIurl + "status").pipe(
      map(
        this.extractData,
      ),
      catchError(
        this.handleError<any>("failed")
      )
    );
    data.subscribe(
      val => {
        if (this.tempToast && val){
          this.tempToast.close()
        }
      }
    )
    return(data)
  }

  deleteAlertModules(module): Observable<any> {
    return this.http.get(APIurl + "delete/" + module).pipe(
      map(
        this.extractData,
        (response: Response) => {
          this.successToast('top-right', 'success', response.statusText, response.status)
        }
      ),
      catchError(this.handleError<any>("failed"))
    );
  }

  
 dangerToast(position, status, message, code) {
    var preventDuplicates = true
    var duration = 0

    this.toastRef = this.toastrService.show(
      'API call error - ' + code + ': ' + message,
      `Failed`,
      { position, status, preventDuplicates, duration });
    
    if (this.toastRef){
      this.tempToast = this.toastRef
    }
  }


  successToast(position, status, message, code) {
    var preventDuplicates = true
    this.toastrService.show(
      'API call error - ' + code + ': ' + message,
      `Failed`,
      { position, status, preventDuplicates });
  }


}

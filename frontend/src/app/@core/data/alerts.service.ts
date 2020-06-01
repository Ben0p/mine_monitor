import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { map, catchError, tap, delay } from 'rxjs/operators';
import { NbToastrService, NbToastRef } from '@nebular/theme';


const httpOptions = {
  headers: new HttpHeaders({
    'Content-Type': 'application/json',
  }),
};

const APIurl: String = 'https://solmm01.fmg.local/api/alerts/';

@Injectable({
  providedIn: 'root',
})
export class AlertService {

  delay: any;

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
      this.dangerToast('top-right', 'danger', error.statusText, error.status);
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

  getAlertZonesList(): Observable<any> {
    return this.http.get(APIurl + "zones/list").pipe(
      map(this.extractData),
      catchError(this.handleError<any>("failed"))
    );
  }

  createAlertZone(payload): Observable<any> {
    return this.http
      .post<any>(APIurl + "zones/create", JSON.stringify(payload), httpOptions)
      .pipe(
        map(this.extractData),
        catchError(this.handleError<any>("error"))
      );
  }

  getAlertWZ(): Observable<any> {
    return this.http.get(APIurl + "wz").pipe(
      map(this.extractData),
      catchError(this.handleError<any>("failed"))
    );
  }

  updateAlertZone(module): Observable<any> {
    return this.http
      .post<any>(APIurl + "zones/update", JSON.stringify(module), httpOptions)
      .pipe(
        map(this.extractData),
        catchError(this.handleError<any>("error"))
      );
  }

  deleteAlertZone(zone): Observable<any> {
    return this.http
      .post<any>(APIurl + "zones/delete", JSON.stringify(zone), httpOptions)
      .pipe(
        map(this.extractData),
        catchError(this.handleError<any>("error"))
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

  loadAlertList(page: number, pageSize: number): Observable<any> {
    const TOTAL_PAGES = 7;
    const startIndex = ((page - 1) % TOTAL_PAGES) * pageSize;

    return this.http
      .get<any>(APIurl + "all")
      .pipe(
        map(data => data.splice(startIndex, pageSize)),
        delay(1500),
      );
  }

  getAlertDisplay(): Observable<any> {
    return this.http.get(APIurl + "display").pipe(
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

  getAlertDetail(uid): Observable<any> {
    return this.http.get(APIurl + uid).pipe(
      map(this.extractData),
      catchError(this.handleError<any>("failed"))
    );
  }

  postAlertDetail(uid, payload): Observable<any> {
    return this.http
      .post<any>(APIurl + uid, JSON.stringify(payload), httpOptions)
      .pipe(
        map(this.extractData),
        catchError(this.handleError<any>("error"))
      );
  }

  deleteAlertModule(name): Observable<any> {
    return this.http.delete(APIurl + "delete/" + name).pipe(
      map(this.extractData),
      catchError(this.handleError<any>("failed"))
    );
  }

  updateAlertModule(module): Observable<any> {
    return this.http
      .post<any>(APIurl + "update", JSON.stringify(module), httpOptions)
      .pipe(
        map(this.extractData),
        catchError(this.handleError<any>("error"))
      );
  }

  createAlertModule(module): Observable<any> {
    return this.http
      .post<any>(APIurl + "create", JSON.stringify(module), httpOptions)
      .pipe(
        map(this.extractData),
        catchError(this.handleError<any>("error"))
      );
  }

  dangerToast(position, status, message, code) {
    var preventDuplicates = true
    var duration = 0

    this.toastRef = this.toastrService.show(
      'API call error - ' + code + ': ' + message,
      `Failed`,
      { position, status, preventDuplicates, duration });

    if (this.toastRef) {
      this.tempToast = this.toastRef
    }

    if (this.delay){
      clearTimeout(this.delay)
    }
    this.delay = setTimeout(() => {
      this.clearToast(this.tempToast);
    }, 5500);
  }

  successToast(position, status, message, code) {
    var preventDuplicates = true
    this.toastrService.show(
      'API call error - ' + code + ': ' + message,
      `Failed`,
      { position, status, preventDuplicates });
  }

  clearToast(toast) {
    if (toast) {
      toast.close()
    }
  }


}

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

const APIurl: String = 'http://10.58.10.31:5000/api/tetra/';

@Injectable({
  providedIn: 'root',
})
export class TetraService {

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

  getTetraNodes(): Observable<any> {
    return this.http.get(APIurl + "node/all").pipe(
      map(this.extractData),
      catchError(this.handleError<any>("failed"))
    );
  }

  getTetraNodeLoad(): Observable<any> {
    return this.http.get(APIurl + "node/load").pipe(
      map(this.extractData),
      catchError(this.handleError<any>("failed"))
    );
  }

  getTetraTSLoad(): Observable<any> {
    return this.http.get(APIurl + "ts/load").pipe(
      map(this.extractData),
      catchError(this.handleError<any>("failed"))
    );
  }

  getTetraRadioCount(node): Observable<any> {
    return this.http.get(APIurl + "radio/count/" + node).pipe(
      map(this.extractData),
      catchError(this.handleError<any>("failed"))
    );
  }

  getTetraSubscribers(): Observable<any> {
    return this.http.get(APIurl + "subscribers").pipe(
      map(this.extractData),
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

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

const APIurl: String = 'https://solmm01/api/gen/';

@Injectable({
  providedIn: 'root',
})
export class GenService {

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

  createGenModule(module): Observable<any> {
    return this.http
      .post<any>(APIurl + "create", JSON.stringify(module), httpOptions)
      .pipe(
        map(this.extractData),
        catchError(this.handleError<any>("error"))
      );
  }

  updateGenModule(module): Observable<any> {
    return this.http
      .post<any>(APIurl + "update", JSON.stringify(module), httpOptions)
      .pipe(
        map(this.extractData),
        catchError(this.handleError<any>("error"))
      );
  }

  deleteGenModule(oid): Observable<any> {
    return this.http.delete(APIurl + "delete/" + oid).pipe(
      map(this.extractData),
      catchError(this.handleError<any>("failed"))
    );
  }

  getGenModules(): Observable<any> {
    return this.http.get(APIurl + "modules").pipe(
      map(this.extractData),
      catchError(this.handleError<any>("failed"))
    );
  }

  getGenStatus(): Observable<any> {
    return this.http.get(APIurl + "status").pipe(
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

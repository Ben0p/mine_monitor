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

const APIurl: String = 'https://solmm01.fmg.local/api/weather/';

@Injectable({
  providedIn: 'root',
})
export class WeatherService {

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

  getWeatherWind(): Observable<any> {
    return this.http.get(APIurl + "wind").pipe(
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

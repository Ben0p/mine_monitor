import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { map, catchError, tap } from 'rxjs/operators';


const httpOptions = {
    headers: new HttpHeaders({
      'Content-Type':  'application/json'
    })
  };


@Injectable({
    providedIn: 'root'
})


export class DataService {

    constructor(private http: HttpClient) { }

    private extractData(res: Response) {
        let body = res;
        return body || { };
      }

      private handleError<T> (operation = 'operation', result?: T) {
        return (error: any): Observable<T> => {
      
          // TODO: send the error to remote logging infrastructure
          console.error(error); // log to console instead
      
          // TODO: better job of transforming error for user consumption
          console.log(`${operation} failed: ${error.message}`);
      
          // Let the app keep running by returning an empty result.
          return of(result as T);
        };
      }

    getSigns() {
        return this.http.get('/assets/json/signs.json');
    }

    getSignDetail(ip): Observable<any> {
        return this.http.get('http://10.20.64.253:5000/sign/' + ip).pipe(
            map(this.extractData)
        )
    }

    getTrucks(): Observable<any> {
      return this.http.get('http://localhost:5000/fleet').pipe(
          map(this.extractData)
      )
  }

    setOutputs (ip, outputs): Observable<any> {
        console.log(outputs);
        return this.http.post<any>('http://10.20.64.253:5000/sign/' + ip, JSON.stringify(outputs), httpOptions).pipe(
          tap((outputs) => console.log('Changed outputs on '+ip)),
          catchError(this.handleError<any>('setOutputs'))
        );
      }
}
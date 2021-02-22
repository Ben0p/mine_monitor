import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { from, interval } from 'rxjs';
import { flatMap, map, startWith } from 'rxjs/operators';



const APIurl: String = 'https://solmm01.fmg.local/api/map/';


@Injectable({
  providedIn: 'root'
})

export class MapSdsService {

  constructor(
    private http: HttpClient,
  ) { }


  private extractData(res: Response) {
    const body = res;
    return body || {};
  }

  getSdsCzml(): Observable<any> {
    return this.http.get(APIurl + "sds").pipe(
      map(this.extractData)
    );
  }

  getSdsRange(start, end): Observable<any> {
    var params = "get?start=" + start + "&end=" + end
    return this.http.get(APIurl + "sds/range/" + params).pipe(
      map(
        this.extractData
      )
    );
  }


  getSdsRange$(start, end) {

    const staticEntities = this.getSdsRange(start, end);
    console.log(staticEntities)

    return interval(99999999999).pipe(
      startWith(0),
      map(intervalValue => {
        return staticEntities
      }),
      flatMap(entity => entity));
  }


  getDataSteam$(intervalms) {
    const staticEntities = this.getSdsCzml();

    return interval(intervalms).pipe(
      startWith(0),
      map(intervalValue => {
        return staticEntities
      }),
      flatMap(entity => entity));
  }

}

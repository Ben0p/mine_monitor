import { Component, OnInit, ɵsetCurrentInjector } from '@angular/core';
import { from, Observable, interval, fromEvent, Subject } from 'rxjs';
import { map, timeInterval, distinctUntilChanged, windowTime, concatMap } from 'rxjs/operators';

import { AcNotification, ActionType, MapsManagerService } from 'angular-cesium';
import { MapSdsService } from './map-sds.service';
import { ɵHttpInterceptingHandler } from '@angular/common/http';

@Component({
  selector: 'map-sds',
  templateUrl: './map-sds.component.html',
  styleUrls: ['./map-sds.component.scss']
})


export class MapSdsComponent implements OnInit {

  entities$: Observable<AcNotification>;
  Cesium = Cesium;

  constructor(
    private sdsData: MapSdsService,
    private mapsManagerService: MapsManagerService
  ) { }


  ngOnInit() {
    var end = Date.now() / 1000
    var start = end - 1800

    const viewer = this.mapsManagerService.getMap().getCesiumViewer();
    const clockStream = Cesium.knockout.getObservable(viewer.clockViewModel, 'currentTime')

    const source = viewer.clockViewModel.currentTime

    const ticks = interval(1000)
    /** 
    ticks.pipe(
      timeInterval()
      )
      .subscribe(
        value => console.log(viewer.clockViewModel.currentTime)
      )
      */


      const subject = new Subject();

      subject
        .pipe(
          windowTime(1000),
          concatMap(obs => obs.pipe(distinctUntilChanged())),
        )
        .subscribe(val => console.log(viewer.clockViewModel.currentTime));
      



    /** 
    Cesium.knockout.getObservable(viewer.clockViewModel,
      'shouldAnimate').subscribe(function (isAnimating) {
        if (isAnimating) {
          console.log('Cesium clock is animating.');
        } else {
          console.log('Cesium clock is paused.');
        }
      });
    */
    
    /** 
    viewer.clock.onTick.addEventListener(function (clock) {
      console.log(clock)
    })
    */








    //var currentJulianTime = clock.currentTime
    //var end = Cesium.JulianDate.toDate(currentJulianTime)
    //var start = new Date(end.getTime() + -5*60000);

    //this.entities$ = this.sdsData.getSdsRange$(start, end)



    this.entities$ = this.sdsData.getDataSteam$(60000)
      .pipe(
        map(
          entity => (
            {
              id: 'Subscribers',
              actionType: ActionType.ADD_UPDATE,
              entity: entity,
            }
          )
        )
      );


  }


}

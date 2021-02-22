import { Component, OnInit, OnDestroy, ViewChild } from '@angular/core';
import {
  ViewerConfiguration,
  MapLayerProviderOptions
} from 'angular-cesium'
import { MapService } from '../../@core/data/map.service'


@Component({
  selector: 'ngx-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.scss'],
  providers: [
    ViewerConfiguration
  ],
})

export class MapComponent implements OnInit, OnDestroy {

  layers$: Object;
  interval: any;
  MapLayerProviderOptions = MapLayerProviderOptions
  dataLoaded: Boolean = false

  constructor(
    private viewerConf: ViewerConfiguration,
    private map: MapService,
  ) {

    const extent = Cesium.Rectangle.fromDegrees(117.702242, -22.260914, 117.981473, -22.089772);
    Cesium.Camera.DEFAULT_VIEW_RECTANGLE = extent;
    Cesium.Camera.DEFAULT_VIEW_FACTOR = 0;
    Cesium.Ion.defaultAccessToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiIyZWZjZjk2OS03MTY4LTQzNTUtODE4Yy1lMGI0MWVjYmFjNDgiLCJpZCI6Mzc3ODYsImlhdCI6MTYwNTU4NTYxN30.KFh3DgwvUdP1v8O6q4SPJ92uz3G-4kvSm6EK3E-YBqQ'

    // viewerOptions will be passed the Cesium.Viewer contstuctor 
    viewerConf.viewerOptions = {
      selectionIndicator: true,
      timeline: true,
      infoBox: true,
      fullscreenButton: true,
      baseLayerPicker: true,
      animation: true,
      shouldAnimate: true,
      homeButton: true,
      geocoder: true,
      navigationHelpButton: true,
      navigationInstructionsInitiallyVisible: false,
      mapMode2D: Cesium.MapMode2D.ROTATE,
      automaticallyTrackDataSourceClocks: true,
      vrButton: true,
    };

  }

  blocks: boolean

  ngOnInit() {
    this.map.getMapLayers().subscribe(
      (data: {}) => {
        this.layers$ = data;
        this.dataLoaded = true
      }
    );
  }

  ngOnDestroy() {
    clearInterval(this.interval);
  }

  refreshData() {

  }
}
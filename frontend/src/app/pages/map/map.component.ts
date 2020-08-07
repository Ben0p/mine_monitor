import { Component } from '@angular/core';
import { ViewerConfiguration, MapLayerProviderOptions } from 'angular-cesium'

@Component({
  selector: 'ngx-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.scss'],
  providers: [
    ViewerConfiguration
  ],
})

export class MapComponent {

  MapLayerProviderOptions = MapLayerProviderOptions

  constructor(
    private viewerConf: ViewerConfiguration,
  ) {

    const extent = Cesium.Rectangle.fromDegrees(117.702242, -22.260914, 117.981473, -22.089772);
    Cesium.Camera.DEFAULT_VIEW_RECTANGLE = extent;
    Cesium.Camera.DEFAULT_VIEW_FACTOR = 0;

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
      automaticallyTrackDataSourceClocks: false,
      vrButton: true,
    };

  }
}
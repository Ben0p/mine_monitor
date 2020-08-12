import { Component, OnInit } from '@angular/core';
import { MapsManagerService } from 'angular-cesium';

@Component({
  selector: 'map-options',
  templateUrl: './map-options.component.html',
  styleUrls: ['./map-options.component.scss']
})
export class MapOptionsComponent implements OnInit {

  constructor(
    private mapsManagerService: MapsManagerService
  ) { }

  tetra: boolean = true;
  nams: boolean = true;
  lanes: boolean = true;
  zones: boolean = true;
  blocks: boolean = true;
  viewer: any;
  layers: any;
  billboards: any;
  tetraCzml: any;

  ngOnInit(): void {

    this.viewer = this.mapsManagerService.getMap().getCesiumViewer();
    this.layers = this.viewer.imageryLayers;
  }

  toggle(layer, checked: boolean) {
    console.log(layer + " " + checked)
    if (layer == 'tetra') {
      this.tetra = checked;
      this.viewer.dataSources.getByName('Tetra CZML data')[0].show = checked
    }
    if (layer == 'nams') {
      this.nams = checked;
      this.layers._layers[5].show = checked
    }
    if (layer == 'lanes') {
      this.lanes = checked;
      this.layers._layers[3].show = checked
    }
    if (layer == 'zones') {
      this.zones = checked;
      this.layers._layers[4].show = checked
    }
    if (layer == 'blocks') {
      this.blocks = checked;
      this.layers._layers[2].show = checked
    }
  }

}

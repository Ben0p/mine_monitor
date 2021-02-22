import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { InspectionsComponent } from './inspections.component';
import { InspectionsListComponent } from './inspections-list/inspections-list.component';
import { InspectionsUploadComponent } from './inspections-upload/inspections-upload.component';


const routes: Routes = [{
  path: '',
  component: InspectionsComponent,
  children: [
    {
      path: 'upload',
      component: InspectionsUploadComponent,
    },
    {
      path: 'list',
      component: InspectionsListComponent,
    },
  ],
}];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class InspectionsRoutingModule { }
export const routedComponents = [
  InspectionsComponent,
  InspectionsUploadComponent,
  InspectionsListComponent,
];
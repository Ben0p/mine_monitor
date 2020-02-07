import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { TetraComponent } from './tetra.component';
import { NodesComponent } from './nodes/nodes.component';

const routes: Routes = [{
  path: '',
  component: TetraComponent,
  children: [
    {
      path: 'nodes',
      component: NodesComponent,
    },
  ],
}];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class TetraRoutingModule { }
export const routedComponents = [
  TetraComponent,
  NodesComponent
];
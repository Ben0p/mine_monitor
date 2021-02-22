import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { TetraComponent } from './tetra.component';
import { NodesComponent } from './nodes/nodes.component';
import { SubscribersComponent } from './subscribers/subscribers.component';

const routes: Routes = [{
  path: '',
  component: TetraComponent,
  children: [
    {
      path: 'nodes',
      component: NodesComponent,
    },
    {
      path: 'subscribers',
      component: SubscribersComponent,
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
  NodesComponent,
  SubscribersComponent
];
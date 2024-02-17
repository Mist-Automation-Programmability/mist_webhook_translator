import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';


import { LoginComponent } from './login/login.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { OrgComponent } from './org/org.component';


const routes: Routes = [
  { path: 'login', component: LoginComponent },
  { path: 'select', component: OrgComponent },
  { path: 'config/:org_id', component: DashboardComponent },
  { path: '',   redirectTo: '/login', pathMatch: 'full' }, // redirect to `first-component`
  { path: '**',   redirectTo: '/login' }, // redirect to `first-component`
];

@NgModule({
  imports: [RouterModule.forRoot(routes, {})],
  exports: [RouterModule]
})
export class AppRoutingModule { }

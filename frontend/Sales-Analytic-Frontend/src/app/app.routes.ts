import { Routes } from '@angular/router';
import { LandingPageComponent } from './landing-page/landing-page/landing-page.component';
import { LoginComponent } from './login/login.component';
import { ClientsPageComponent } from './clients-page/clients-page/clients-page.component';
import { AccountExecPageComponent } from './account-exec-page/account-exec-page/account-exec-page.component';
import { WinsPageComponent } from './wins-page/wins-page/wins-page.component';
// import { AuthGuard } from './auth/auth.guard'; 
import { RevenuePageComponent } from './revenue-page/revenue-page/revenue-page.component';
import { SigningsDashboardComponent } from './signings-page/signings-dashboard/signings-dashboard.component';
import { PipelineDashboardComponent } from './pipeline-page/pipeline-dashboard/pipeline-dashboard.component';

export const appRoutes: Routes = [
  { path: 'login', component: LoginComponent },
  { path: '', redirectTo: '/login', pathMatch: 'full' },
  {
    path: 'landing-page',
    component: LandingPageComponent,
    // canActivate: [AuthGuard],
  },
  {
    path: 'revenue-page',
    component: RevenuePageComponent,
    // canActivate: [AuthGuard],
  },
  {
    path: 'clients-page',
    component: ClientsPageComponent,
    // canActivate: [AuthGuard],
  },
  {
    path: 'signings',
    component: SigningsDashboardComponent,
    // canActivate: [AuthGuard],
  },
  {
    path: 'pipeline',
    component: PipelineDashboardComponent,
    // canActivate: [AuthGuard],
  },
  {
    path: 'count-to-wins',
    component: WinsPageComponent,
    // canActivate: [AuthGuard],
  },
  {
    path: 'account-executives',
    component: AccountExecPageComponent,
  },
];

import { Routes } from '@angular/router';
import { LandingPageComponent } from './landing-page/landing-page/landing-page.component';
import { RevenuePageFullComponent } from './revenue-page/revenue-page-full/revenue-page-full.component';
import { LoginComponent } from './login/login.component';
import { ClientsPageComponent } from './clients-page/clients-page/clients-page.component';
import { SigningsPageComponent } from './signings-page/signings-page/signings-page.component';
import { PipelinePageComponent } from './pipeline-page/pipeline-page/pipeline-page.component';
import { WinsPageComponent } from './wins-page/wins-page/wins-page.component';
import { AuthGuard } from './auth/auth.guard'; // Import the AuthGuard

export const appRoutes: Routes = [
  { path: 'login', component: LoginComponent },
  { path: '', redirectTo: '/login', pathMatch: 'full' },
  {
    path: 'landing-page',
    component: LandingPageComponent,
    canActivate: [AuthGuard],
  },
  {
    path: 'revenue-page',
    component: RevenuePageFullComponent,
    canActivate: [AuthGuard],
  },
  {
    path: 'clients-page',
    component: ClientsPageComponent,
    canActivate: [AuthGuard],
  },
  {
    path: 'signings',
    component: SigningsPageComponent,
    canActivate: [AuthGuard],
  },
  {
    path: 'pipeline',
    component: PipelinePageComponent,
    canActivate: [AuthGuard],
  },
  {
    path: 'count-to-wins',
    component: WinsPageComponent,
    canActivate: [AuthGuard],
  },
];

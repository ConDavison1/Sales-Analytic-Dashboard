import { Component } from '@angular/core';
import { SidebarComponent } from '../../sidebar/sidebar.component';
import { HeaderComponent } from '../../header/header.component';
import { SigningsDashboardComponent } from '../signings-dashboard/signings-dashboard.component';

@Component({
  selector: 'app-signings-page',
  imports: [SidebarComponent, HeaderComponent, SigningsDashboardComponent],
  templateUrl: './signings-page.component.html',
  styleUrl: './signings-page.component.css'
})
export class SigningsPageComponent {

}

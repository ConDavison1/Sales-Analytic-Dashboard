import { Component } from '@angular/core';
import { SidebarComponent } from '../../sidebar/sidebar.component';
import { HeaderComponent } from '../../header/header.component';
import { AccountExecDashboardComponent } from '../account-exec-dashboard/account-exec-dashboard.component';

@Component({
  selector: 'app-account-exec-page',
  imports: [SidebarComponent, HeaderComponent, AccountExecDashboardComponent],
  templateUrl: './account-exec-page.component.html',
  styleUrl: './account-exec-page.component.css'
})
export class AccountExecPageComponent {

}

import { Component, OnInit, ViewEncapsulation } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DashboardService } from '../../services/dashboard-services/dashboard.service';
import { AccountExecService } from '../../services/account-exec-services/account-exec.service';
import { first } from 'rxjs';

@Component({
  selector: 'app-account-exec-dashboard',
  imports: [CommonModule],
  standalone: true,
  templateUrl: './account-exec-dashboard.component.html',
  styleUrl: './account-exec-dashboard.component.css',
  encapsulation: ViewEncapsulation.Emulated
})
export class AccountExecDashboardComponent {

  pipelineCount: number = 0;
  revenueCount: number = 0;
  signingsCount: number = 0;
  winsCount: number = 0;

  accountExecData: any[] = [];

  isDataLoaded: boolean = false;

  constructor(
    private dashboardService: DashboardService,
    private accountExecService: AccountExecService
  ) {}

  ngOnInit(): void {
    this.fetchDashboardData();
    this.fetchAccountExecData();

    this.accountExecData = [
      {
        executive_id: 1,
        first_name: 'John',
        last_name: 'Doe',
        email: 'john.doe@example.com'
      }
    ]
  }

  fetchDashboardData(): void {
    this.dashboardService
      .getPipelineCount()
      .subscribe((response: { pipeline_count: number }) => {
        this.pipelineCount = response.pipeline_count;
      });
    
    this.dashboardService
      .getRevenueSum()
      .subscribe((response: { revenue_sum: number }) => {
        this.revenueCount = response.revenue_sum;
      });
    
    this.dashboardService
      .getSigningsCount()
      .subscribe((response: { signings_count: number }) => {
        this.signingsCount = response.signings_count;
      });
    
    this.dashboardService
      .getWinsCount()
      .subscribe((response: { wins_count: number }) => {
        this.winsCount = response.wins_count;
      });
  }

  fetchAccountExecData(): void {
    this.accountExecService
      .getAccountExecData()
  }

  get cards() {
    return [
      {
        title: 'Pipeline',
        value: `$${this.pipelineCount}`,
        percentage: '+55%',
      },
      {
        title: 'Revenue',
        value: `$${this.revenueCount}`,
        percentage: '+5%',
      },
      {
        title: 'Signings',
        value: `$${this.signingsCount}`,
        percentage: '+8%',
      },
      {
        title: 'Count To Wins',
        value: `$${this.winsCount}`,
        percentage: '-14%',
      }
    ]
  }
}

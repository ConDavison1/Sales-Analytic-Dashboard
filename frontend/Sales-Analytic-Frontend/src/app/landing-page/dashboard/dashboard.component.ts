import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DashboardService } from "../../services/dashboard-services/dashboard.service";

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {
  pipelineCount: number = 0;
  revenueCount: number = 0;
  signingsCount: number = 0;
  winsCount: number = 0;

  accountExecutives: any[] = [];
  isLoadingAccountExecutives: boolean = true;

  constructor(private dashboardService: DashboardService) { }

  ngOnInit(): void {
    this.fetchCardData();
    this.fetchAccountExecutives();
  }

  fetchCardData(): void {
    this.dashboardService.getPipelineCount().subscribe((response: { pipeline_count: number }) => {
      this.pipelineCount = response.pipeline_count;
    });

    this.dashboardService.getRevenueSum().subscribe((response: { revenue_sum: number }) => {
      this.revenueCount = response.revenue_sum;
    });

    this.dashboardService.getSigningsCount().subscribe((response: { signings_count: number }) => {
      this.signingsCount = response.signings_count;
    });

    this.dashboardService.getWinsCount().subscribe((response: { wins_count: number }) => {
      this.winsCount = response.wins_count;
    });
  }

  fetchAccountExecutives(): void {
    this.dashboardService.getAccountExecutives().subscribe(
      (response) => {
        this.accountExecutives = response;
        this.isLoadingAccountExecutives = false;
      },
      (error) => {
        console.error('Error fetching account executives:', error);
        this.isLoadingAccountExecutives = false;
      }
    );
  }

  get cards() {
    return [
      { title: 'Pipeline', value: `$${this.pipelineCount}`, percentage: '+55%' },
      { title: 'Revenue', value: `$${this.revenueCount}`, percentage: '+5%' },
      { title: 'Count To Wins', value: `${this.winsCount}`, percentage: '-14%' },
      { title: 'Signings', value: `$${this.signingsCount}`, percentage: '+89%' },
    ];
  }

  product_sale = [
    { title: 'Account Executive' },
    { title: 'Clients' },
    { title: 'Status' },
    { title: 'Targets' },
  ];
}

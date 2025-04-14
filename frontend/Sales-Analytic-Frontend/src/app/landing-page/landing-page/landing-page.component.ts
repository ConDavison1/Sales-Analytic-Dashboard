import { Component, OnInit, AfterViewInit, ViewChild } from '@angular/core';
import { HeaderComponent } from '../../header/header.component';
import { SidebarComponent } from '../../sidebar/sidebar.component';
import { DashboardService } from '../../services/dashboard-services/dashboard.service';
import { Title } from '@angular/platform-browser';
import {
  NgApexchartsModule,
  ApexResponsive,
  ChartComponent,
} from 'ng-apexcharts';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';

export type ChartOptions = {
  series: any[];
  chart: any;
  plotOptions: any;
  dataLabels: any;
  stroke: any;
  xaxis: any;
  yaxis: any;
  fill: any;
  tooltip: any;
  legend: any;
  colors: any;
  responsive: ApexResponsive[];
  theme: any;
};

@Component({
  standalone: true,
  selector: 'app-landing-page',
  templateUrl: './landing-page.component.html',
  styleUrls: ['./landing-page.component.css'],
  imports: [
    CommonModule,
    NgApexchartsModule,
    HeaderComponent,
    SidebarComponent,
  ],
})
export class LandingPageComponent implements OnInit {
  username: string = '';
  year: number = 2024;

  isLoadingChartData = true;

  cards: any[] = [];
  chartOptionsOne: any = {};
  chartOptionsTwo: any = {};
  chartOptionsThree: any = {};
  chartOptionsFour: any = {};

  constructor(
    private dashboardService: DashboardService,
    private route: ActivatedRoute,
    private router: Router,
    private titleService: Title
  ) {}

  ngOnInit(): void {
    this.titleService.setTitle('Dashboard | Sales Analytics');
    const userData = localStorage.getItem('user');
    if (userData) {
      const user = JSON.parse(userData);
      this.username = user.username;
      console.log('Logged in as:', this.username);

      this.loadKpiCards();
      this.loadRevenueChart();
      this.loadWinChart();
      this.loadPipelineChart();
      this.loadSigningsChart();
    } else {
      console.error('No user found in localStorage. Redirecting to login.');

      this.router.navigate(['/login']);
    }
  }

  loadKpiCards(): void {
    this.dashboardService
      .getKpiCards(this.username, this.year)
      .subscribe((data) => {
        this.cards = [
          { title: 'Pipeline', value: `$${data.pipeline}`, percentage: '' },
          { title: 'Revenue', value: `$${data.revenue}`, percentage: '' },
          { title: 'Signings', value: `$${data.signings}`, percentage: '' },
          { title: 'Wins', value: `${data.wins}`, percentage: '' },
        ];
      });
  }

  loadRevenueChart(): void {
    this.dashboardService
      .getRevenueChartData(this.username, this.year)
      .subscribe((data) => {
        this.chartOptionsOne = {
          series: [
            {
              name: 'Revenue',
              data: data.revenue_chart_data.map((d: any) => d.revenue),
            },
          ],
          chart: { type: 'bar', height: 350 },
          xaxis: {
            categories: data.revenue_chart_data.map(
              (d: any) => `Month ${d.month}`
            ),
          },
        };
        this.isLoadingChartData = false;
      });
  }

  loadWinChart(): void {
    this.dashboardService
      .getWinChartData(this.username, this.year)
      .subscribe((data) => {
        this.chartOptionsTwo = {
          series: [
            {
              name: 'Wins',
              data: data.win_chart_data.map((d: any) => d.win_count),
            },
          ],
          chart: { type: 'bar', height: 350 },
          xaxis: {
            categories: data.win_chart_data.map((d: any) => `Q${d.quarter}`),
          },
        };
      });
  }

  loadPipelineChart(): void {
    this.dashboardService
      .getPipelineChartData(this.username, this.year)
      .subscribe((data) => {
        this.chartOptionsThree = {
          series: data.pipeline_chart_data.map((d: any) => d.count),
          chart: { type: 'pie' },
          labels: data.pipeline_chart_data.map((d: any) => d.forecast_category),
        };
      });
  }

  loadSigningsChart(): void {
    this.dashboardService
      .getSigningsChartData(this.username, this.year)
      .subscribe((data) => {
        this.chartOptionsFour = {
          series: data.signings_chart_data.map((d: any) => d.count),
          chart: { type: 'pie' },
          labels: data.signings_chart_data.map((d: any) => d.product_category),
        };
      });
  }
}

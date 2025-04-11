import {
  Component,
  OnInit,
  AfterViewInit,
  ViewEncapsulation,
} from '@angular/core';
import { CommonModule } from '@angular/common';
import { SidebarComponent } from '../../sidebar/sidebar.component';
import { NgApexchartsModule } from 'ng-apexcharts';
import { ApexChart } from 'ng-apexcharts';
import { HeaderComponent } from '../../header/header.component';
import { RevenueService } from '../../services/revenue-services/revenue.service';
import { DashboardService } from '../../services/dashboard-services/dashboard.service';

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
};

@Component({
  selector: 'app-revenue-page',
  imports: [NgApexchartsModule, CommonModule, SidebarComponent, HeaderComponent],
  standalone: true,
  templateUrl: './revenue-page.component.html',
  styleUrls: ['./revenue-page.component.css'],
})
export class RevenuePageComponent implements OnInit {
  pipelineCount: number = 0;
  revenueCount: number = 0;
  signingsCount: number = 0;
  winsCount: number = 0;

  revenueData: any[] = [];
  revenueChartData: any[] = [];
  isDataLoaded: boolean = false;

  constructor(
    private dashboardService: DashboardService,
    private revenueService: RevenueService
  ) {}

  ngOnInit(): void {
    // this.fetchDashboardData();
    this.fetchRevenueClients();
    this.fetchRevenueChart();
  }

  // fetchDashboardData(): void {
  //   this.dashboardService
  //     .getPipelineCount()
  //     .subscribe((response: { pipeline_count: number }) => {
  //       this.pipelineCount = response.pipeline_count;
  //     });

  //   this.dashboardService
  //     .getRevenueSum()
  //     .subscribe((response: { revenue_sum: number }) => {
  //       this.revenueCount = response.revenue_sum;
  //     });

  //   this.dashboardService
  //     .getSigningsCount()
  //     .subscribe((response: { signings_count: number }) => {
  //       this.signingsCount = response.signings_count;
  //     });

  //   this.dashboardService
  //     .getWinsCount()
  //     .subscribe((response: { wins_count: number }) => {
  //       this.winsCount = response.wins_count;
  //     });
  // }

  fetchRevenueClients(): void {
    this.revenueService.getRevenueClients().subscribe((data) => {
      this.revenueData = data;
    });
  }

  fetchRevenueChart(): void {
    this.revenueService.getRevenueChart().subscribe((data) => {
      this.revenueChartData = data;
      this.isDataLoaded = true;
      this.updateBarChartData();
    });
  }

  updateBarChartData(): void {
    // Check if data exists before updating
    if (this.revenueChartData.length > 0) {
      this.barChart.series[0].data = this.revenueChartData.map(
        (item) => item.count
      );
      this.barChart.xaxis.categories = this.revenueChartData.map(
        (item) => item.category
      );
    }
  }

  get cards() {
    return [
      {
        title: 'Pipeline',
        value: `$${this.pipelineCount}`,
        percentage: '+55%',
      },
      { title: 'Revenue', value: `$${this.revenueCount}`, percentage: '+5%' },
      { title: 'Signings', value: `$${this.signingsCount}`, percentage: '+8%' },
      {
        title: 'Count To Wins',
        value: `${this.winsCount}`,
        percentage: '-14%',
      },
    ];
  }

  // Define types for the bar chart
  barChart = {
    chart: { type: 'bar' as ApexChart['type'], height: 350 },
    series: [{ name: 'Clients', data: [] as number[] }],
    xaxis: { categories: [] as string[] },
    plotOptions: {
      bar: { horizontal: false, columnWidth: '50%', distributed: true },
    },
    dataLabels: { enabled: true },
    colors: ['#008FFB', '#00E396', '#FEB019', '#FF4560'],
    tooltip: {
      enabled: true,
      y: { formatter: (val: number) => `${val} Clients` },
    },
  };

  gaugeChart = {
    series: [81],
    chart: { type: 'radialBar' as ApexChart['type'], height: 350 },
    plotOptions: {
      radialBar: {
        startAngle: -90,
        endAngle: 90,
        track: { background: '#e7e7e7', strokeWidth: '97%' },
        dataLabels: {
          name: {
            show: true,
            fontSize: '16px',
            offsetY: 20,
            color: '#333',
            formatter: () => 'Revenue Target Score',
          },
          value: {
            fontSize: '24px',
            show: true,
            offsetY: -10,
            formatter: (val: number) => `${Math.round((val / 100) * 60)}M`,
          },
        },
      },
    },
    fill: { colors: ['#4CAF50'] },
    yaxis: { min: 0, max: 60 },
  };
}

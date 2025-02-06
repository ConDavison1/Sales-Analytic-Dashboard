import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DashboardService } from '../../services/dashboard-services/dashboard.service';
import { NgApexchartsModule } from 'ng-apexcharts';

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
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, NgApexchartsModule],
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css'],
})
export class DashboardComponent implements OnInit {
  pipelineCount: number = 0;
  revenueCount: number = 0;
  signingsCount: number = 0;
  winsCount: number = 0;
  
  accountExecutives: any[] = [];
  isLoadingAccountExecutives: boolean = true;
  isLoadingChartData: boolean = true;

  chartOptions!: Partial<ChartOptions>;

  constructor(private dashboardService: DashboardService) {
    this.chartOptions = {
      series: [
        { name: 'Pipeline', data: [] },
        { name: 'Revenue', data: [] },
        { name: 'Count To Wins', data: [] },
        { name: 'Signings', data: [] },
      ],
      chart: {
        type: 'bar',
        height: 350,
      },
      plotOptions: {
        bar: {
          horizontal: false,
          columnWidth: '55%',
          borderRadius: 8,
        },
      },
      dataLabels: { enabled: false },
      stroke: {
        show: true,
        width: 2,
        colors: ['transparent'],
      },
      xaxis: {
        categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
      },
      yaxis: {
        title: {
          text: '$ Thousands',
          style: {
            color: '#5f6368',
            fontFamily: 'Arial, Helvetica, sans-serif',
          },
        },
      },
      fill: { opacity: 1 },
      tooltip: {
        y: {
          formatter: function (val: number) {
            return '$ ' + val + ' thousands';
          },
        },
      },
      legend: { show: true },
    };
  }

  ngOnInit(): void {
    this.fetchCardData();
    this.fetchAccountExecutives();
    this.fetchChartData();
  }

  fetchCardData(): void {
    this.dashboardService.getPipelineCount().subscribe((response) => {
      this.pipelineCount = response.pipeline_count;
    });

    this.dashboardService.getRevenueSum().subscribe((response) => {
      this.revenueCount = response.revenue_sum;
    });

    this.dashboardService.getSigningsCount().subscribe((response) => {
      this.signingsCount = response.signings_count;
    });

    this.dashboardService.getWinsCount().subscribe((response) => {
      this.winsCount = response.wins_count;
    });
  }

  fetchAccountExecutives(): void {
    this.dashboardService.getAccountExecutives().subscribe(
      (response) => {
        console.log('API Response:', response);  // Log the response here to see how the data is formatted
        this.accountExecutives = response;  // Assign the response to accountExecutives
        this.isLoadingAccountExecutives = false;  // Set loading flag to false after data is fetched
      },
      (error) => {
        console.error('Error fetching account executives:', error);  // Log any error to the console
        this.isLoadingAccountExecutives = false;  // Set loading flag to false even if there is an error
      }
    );
  }
  

  fetchChartData(): void {
    this.dashboardService.getChartData().subscribe(
      (response) => {
        this.chartOptions = Object.assign({}, this.chartOptions, {
          series: [
            { name: 'Pipeline', data: response.pipeline },
            { name: 'Revenue', data: response.revenue },
            { name: 'Count To Wins', data: response.wins },
            { name: 'Signings', data: response.signings },
          ],
        });
        this.isLoadingChartData = false;
      },
      (error) => {
        console.error('Error fetching chart data:', error);
        this.isLoadingChartData = false;
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
}

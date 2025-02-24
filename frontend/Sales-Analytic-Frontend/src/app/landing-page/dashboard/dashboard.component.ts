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
  colors: any;
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

  chartOptionsOne!: Partial<ChartOptions>;
  chartOptionsTwo!: Partial<ChartOptions>;
  chartOptionsThree!: Partial<ChartOptions>;
  chartOptionsFour!: Partial<ChartOptions>;

  constructor(private dashboardService: DashboardService) {
    this.chartOptionsOne = {
      series: [{ name: 'Pipeline', data: [] }],
      chart: { type: 'bar', height: 350 },
      colors: ['#1E88E5'], // Blue
      plotOptions: {
        bar: { horizontal: false, columnWidth: '55%', borderRadius: 8 },
      },
      fill: {
        opacity: 1,
        colors: ['#1E88E5'], // Blue, added explicitly in fill
      },
      dataLabels: { enabled: false },
      stroke: { show: true, width: 2, colors: ['transparent'] },
      xaxis: {
        categories: [
          'J',
          'F',
          'M',
          'A',
          'M',
          'J',
          'J',
          'A',
          'S',
          'O',
          'N',
          'D',
        ],
      },
      yaxis: {
        title: {
          text: 'Amount ($)',
          style: {
            color: '#5f6368',
            fontFamily: 'Arial, Helvetica, sans-serif',
          },
        },
      },
      tooltip: { y: { formatter: (val: number) => '$ ' + val } },
      legend: { show: true },
    };

    this.chartOptionsTwo = {
      series: [{ name: 'Revenue', data: [] }],
      chart: { type: 'bar', height: 350 },
      colors: ['#F4511E'], // Red
      fill: {
        opacity: 1,
        colors: ['#F4511E'], // Red, added explicitly in fill
      },
      plotOptions: {
        bar: { horizontal: false, columnWidth: '55%', borderRadius: 8 },
      },
      dataLabels: { enabled: false },
      stroke: { show: true, width: 2, colors: ['transparent'] },
      xaxis: {
        categories: [
          'J',
          'F',
          'M',
          'A',
          'M',
          'J',
          'J',
          'A',
          'S',
          'O',
          'N',
          'D',
        ],
      },
      yaxis: {
        title: {
          text: 'Amount ($)',
          style: {
            color: '#5f6368',
            fontFamily: 'Arial, Helvetica, sans-serif',
          },
        },
      },
      tooltip: { y: { formatter: (val: number) => '$ ' + val } },
      legend: { show: true },
    };

    this.chartOptionsThree = {
      series: [{ name: 'Signings', data: [] }],
      chart: { type: 'bar', height: 350 },
      colors: ['#43A047'], // Green
      fill: {
        opacity: 1,
        colors: ['#43A047'], // Green, added explicitly in fill
      },
      plotOptions: {
        bar: { horizontal: false, columnWidth: '55%', borderRadius: 8 },
      },
      dataLabels: { enabled: false },
      stroke: { show: true, width: 2, colors: ['transparent'] },
      xaxis: {
        categories: [
          'J',
          'F',
          'M',
          'A',
          'M',
          'J',
          'J',
          'A',
          'S',
          'O',
          'N',
          'D',
        ],
      },
      yaxis: {
        title: {
          text: 'Amount ($)',
          style: {
            color: '#5f6368',
            fontFamily: 'Arial, Helvetica, sans-serif',
          },
        },
      },
      tooltip: { y: { formatter: (val: number) => '$ ' + val } },
      legend: { show: true },
    };

    this.chartOptionsFour = {
      series: [{ name: 'Wins', data: [] }],
      chart: { type: 'bar', height: 350 },
      colors: ['#FDD835'], // Yellow
      fill: {
        opacity: 1,
        colors: ['#FDD835'], // Yellow, added explicitly in fill
      },
      plotOptions: {
        bar: { horizontal: false, columnWidth: '55%', borderRadius: 8 },
      },
      dataLabels: { enabled: false },
      stroke: { show: true, width: 2, colors: ['transparent'] },
      xaxis: {
        categories: [
          'J',
          'F',
          'M',
          'A',
          'M',
          'J',
          'J',
          'A',
          'S',
          'O',
          'N',
          'D',
        ],
      },
      yaxis: {
        title: {
          text: 'Amount',
          style: {
            color: '#5f6368',
            fontFamily: 'Arial, Helvetica, sans-serif',
          },
        },
      },
      tooltip: { y: { formatter: (val: number) => val } },
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
        console.log('API Response:', response); // Log the response here to see how the data is formatted
        this.accountExecutives = response; // Assign the response to accountExecutives
        this.isLoadingAccountExecutives = false; // Set loading flag to false after data is fetched
      },
      (error) => {
        console.error('Error fetching account executives:', error); // Log any error to the console
        this.isLoadingAccountExecutives = false; // Set loading flag to false even if there is an error
      }
    );
  }

  fetchChartData(): void {
    this.dashboardService.getChartData().subscribe(
      (response) => {
        this.chartOptionsOne.series = [
          { name: 'Pipeline', data: response.pipeline },
        ];
        this.chartOptionsTwo.series = [
          { name: 'Revenue', data: response.revenue },
        ];
        this.chartOptionsThree.series = [
          { name: 'Signings', data: response.signings },
        ];
        this.chartOptionsFour.series = [{ name: 'Wins', data: response.wins }];
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
      {
        title: 'Pipeline',
        value: `$${this.pipelineCount}`,
        percentage: '+55%',
      },
      { title: 'Revenue', value: `$${this.revenueCount}`, percentage: '+5%' },
      {
        title: 'Signings',
        value: `$${this.signingsCount}`,
        percentage: '+89%',
      },
      {
        title: 'Count To Wins',
        value: `${this.winsCount}`,
        percentage: '-14%',
      },
    ];
  }
}

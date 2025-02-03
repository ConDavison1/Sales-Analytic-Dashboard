import { Component, ViewChild, OnInit } from '@angular/core';
import { DashboardService } from '../../services/dashboard-services/dashboard.service';
import { CommonModule } from '@angular/common';
import { NgApexchartsModule } from 'ng-apexcharts';
import {
  ApexAxisChartSeries,
  ApexChart,
  ChartComponent,
  ApexDataLabels,
  ApexPlotOptions,
  ApexYAxis,
  ApexLegend,
  ApexStroke,
  ApexXAxis,
  ApexFill,
  ApexTooltip,
  ApexTitleSubtitle,
  ApexMarkers,
} from 'ng-apexcharts';

// Define the ChartOptions type
export type ChartOptions = {
  series: ApexAxisChartSeries;
  chart: ApexChart;
  dataLabels: ApexDataLabels;
  plotOptions: ApexPlotOptions;
  yaxis: ApexYAxis;
  xaxis: ApexXAxis;
  fill: ApexFill;
  tooltip: ApexTooltip;
  stroke: ApexStroke;
  legend: ApexLegend;
};

export type TerritoryChartOptions = {
  series: ApexAxisChartSeries;
  chart: ApexChart;
  title: ApexTitleSubtitle;
  stroke: ApexStroke;
  dataLabels: ApexDataLabels;
  tooltip: any;
  plotOptions: ApexPlotOptions;
  fill: ApexFill;
  colors: string[];
  yaxis: ApexYAxis;
  markers: ApexMarkers;
  xaxis: ApexXAxis;
};

interface ProgressBarItem {
  value: string;
  color: string;
  percentage: number;
}

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, NgApexchartsModule], // Import required modules
  templateUrl: './dashboard.component.html', // Link to the HTML file
  styleUrls: ['./dashboard.component.css'], // Link to the CSS file
})
export class DashboardComponent implements OnInit {
  @ViewChild('chart', { static: true }) chart!: ChartComponent; // Use definite assignment assertion
  public chartOptions: ChartOptions; // Chart configuration (no Partial)
  public territoryChartOptions: TerritoryChartOptions; // Chart configuration (no Partial)

  // Cards Data
  pipelineCount: number = 0;
  revenueCount: number = 0;
  signingsCount: number = 0;
  winsCount: number = 0;

  get cards() {
    return [
      { title: 'Pipeline', value: `$${this.pipelineCount}`, percentage: '+55%' },
      { title: 'Revenue', value: `$${this.revenueCount}`, percentage: '+5%' },
      { title: 'Count To Wins', value: `${this.winsCount}`, percentage: '-14%' },
      { title: 'Signings', value: `$${this.signingsCount}`, percentage: '+8%' },
    ];
  }

  // Account Executives Data
  product_sale = [
    { title: 'Account Executive' },
    { title: 'Clients' },
    { title: 'Status' },
    { title: 'Targets' },
  ];

  progressBar: ProgressBarItem[] = [
    { value: '4', color: 'green', percentage: 40 },
    { value: 'Online', color: 'green', percentage: 100 },
    { value: '70%', color: 'green', percentage: 70 },
  ];

  progressBar2: ProgressBarItem[] = [
    { value: '8', color: 'red', percentage: 80 },
    { value: 'Offline', color: 'red', percentage: 100 },
    { value: '49%', color: '#ffc107', percentage: 49 },
  ];

  progressBar3: ProgressBarItem[] = [
    { value: '2', color: 'green', percentage: 20 },
    { value: 'Offline', color: 'red', percentage: 100 },
    { value: '76%', color: 'green', percentage: 76 },
  ];

  progressBar4: ProgressBarItem[] = [
    { value: '9', color: 'red', percentage: 90 },
    { value: 'Online', color: 'green', percentage: 100 },
    { value: '91%', color: 'green', percentage: 91 },
  ];

  progressBar5: ProgressBarItem[] = [
    { value: '1', color: 'green', percentage: 10 },
    { value: 'Online', color: 'green', percentage: 100 },
    { value: '89%', color: 'green', percentage: 89 },
  ];

  progressBar6: ProgressBarItem[] = [
    { value: '5', color: '#ffc107', percentage: 50 },
    { value: 'Online', color: 'green', percentage: 100 },
    { value: '32%', color: 'red', percentage: 32 },
  ];

  progressBar7: ProgressBarItem[] = [
    { value: '8', color: 'red', percentage: 80 },
    { value: 'Offline', color: 'red', percentage: 100 },
    { value: '24%', color: 'red', percentage: 24 },
  ];

  progressBar8: ProgressBarItem[] = [
    { value: '1', color: 'green', percentage: 10 },
    { value: 'Online', color: 'green', percentage: 100 },
    { value: '100%', color: 'green', percentage: 100 },
  ];

  progressBar9: ProgressBarItem[] = [
    { value: '5', color: '#ffc107', percentage: 50 },
    { value: 'Online', color: 'green', percentage: 100 },
    { value: '78%', color: 'green', percentage: 78 },
  ];

  progressBar10: ProgressBarItem[] = [
    { value: '7', color: 'red', percentage: 70 },
    { value: 'Online', color: 'green', percentage: 100 },
    { value: '44%', color: '#ffc107', percentage: 44 },
  ];


  constructor(private dashboardService: DashboardService) {
    // Initialize chart options with all required properties
    this.chartOptions = {
      series: [
        {
          name: 'Pipeline',
          data: [44, 55, 57, 56, 61, 58, 63, 60, 66],
        },
        {
          name: 'Revenue',
          data: [76, 85, 101, 98, 87, 105, 91, 114, 94],
        },
        {
          name: 'Count To Wins',
          data: [35, 41, 36, 26, 45, 48, 52, 53, 41],
        },
        {
          name: 'Signings',
          data: [35, 41, 36, 26, 45, 48, 52, 53, 41],
        },
      ],
      chart: {
        type: 'bar',
        height: 350,
      },
      plotOptions: {
        bar: {
          horizontal: false,
          columnWidth: '55%',
          borderRadius: 8, // Use borderRadius instead of endingShape
        },
      },
      dataLabels: {
        enabled: false,
      },
      stroke: {
        show: true,
        width: 2,
        colors: ['transparent'],
      },
      xaxis: {
        categories: [
          'Feb',
          'Mar',
          'Apr',
          'May',
          'Jun',
          'Jul',
          'Aug',
          'Sep',
          'Oct',
        ],
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
      fill: {
        opacity: 1,
      },
      tooltip: {
        y: {
          formatter: function (val) {
            return '$ ' + val + ' thousands';
          },
        },
      },
      legend: {
        show: true, // Ensure legend is defined
      },
    };

    // Initialize territory chart options
    this.territoryChartOptions = {
      series: [
        {
          name: 'Series 1',
          data: [20, 100, 40, 30, 50, 80, 33],
        },
      ],
      chart: {
        height: 350,
        type: 'radar',
      },
      dataLabels: {
        enabled: true,
      },
      plotOptions: {
        radar: {
          size: 140,
          polygons: {
            strokeColors: '#e9e9e9',
            fill: {
              colors: ['#f8f8f8', '#fff'],
            },
          },
        },
      },
      title: {
        text: 'Territories',
        style: {
          color: '#5f6368',
          fontFamily: 'Arial, Helvetica, sans-serif',
        },
      },
      colors: ['#FF4560'],
      markers: {
        size: 4,
        colors: ['#fff'],
        strokeColors: ['#FF4560'],
        strokeWidth: 2,
      },
      tooltip: {
        y: {
          formatter: function (val: number) {
            return val.toString();
          },
        },
      },
      xaxis: {
        categories: [
          '1',
          '2',
          '3',
          '4',
          '5',
          '6',
          '7',
        ],
      },
      yaxis: {
        tickAmount: 7,
        labels: {
          formatter: function (val:number, i: number) {
            if (i % 2 === 0) {
              return val.toString();
            } else {
              return '';
            }
          },
        },
      },
      stroke: {
        show: true,
        width: 2,
        colors: ['#FF4560'],
      },
      fill: {
        opacity: 0.9,
      },
    };
  }

  ngOnInit(): void {
    this.fetchDashboardData();
  }

  fetchDashboardData(): void {

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
}

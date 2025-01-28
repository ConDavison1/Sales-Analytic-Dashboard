// dashboard.component.ts
import { Component, ViewChild } from '@angular/core';
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
export class DashboardComponent {
  @ViewChild('chart', { static: true }) chart!: ChartComponent; // Use definite assignment assertion
  public chartOptions: ChartOptions; // Chart configuration (no Partial)

  // Cards Data
  cards = [
    { title: 'Revenue', value: '$53,000,000', percentage: '+55%' },
    { title: 'Pipeline', value: '$80,300,000', percentage: '+5%' },
    { title: 'Count To Wins', value: '200', percentage: '-14%' },
    { title: 'Signings', value: '$53,000,000', percentage: '+8%' },
  ];

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

  constructor() {
    // Initialize chart options with all required properties
    this.chartOptions = {
      series: [
        {
          name: 'Revenue',
          data: [44, 55, 57, 56, 61, 58, 63, 60, 66],
        },
        {
          name: 'Pipeline',
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
          text: '$ (thousands)',
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
  }
}
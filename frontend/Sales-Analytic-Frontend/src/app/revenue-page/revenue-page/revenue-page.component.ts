import { Component, ViewChild, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NgApexchartsModule } from 'ng-apexcharts';
import { RevenueService } from '../../services/revenue-services/revenue.service';
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

export type RevenueGoalOptions = {
  series: ApexAxisChartSeries;
  chart: ApexChart;
  plotOptions: ApexPlotOptions;
  fill: ApexFill;
  stroke: ApexStroke;
  yaxis: ApexYAxis;
}

@Component({
  selector: 'app-revenue-page',
  imports: [NgApexchartsModule, CommonModule],
  standalone: true,
  templateUrl: './revenue-page.component.html',
  styleUrl: './revenue-page.component.css'
})
export class RevenuePageComponent implements OnInit {
  @ViewChild('chart', { static: true }) chart!: ChartComponent;
  public chartOptions: ChartOptions;

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

  

  // revenueData = [
  //   { accountName: "Client 7", revenueType: "GCP", totalRevenue: 1200000, arr: 480000, timePeriod: 2024 },
  //   { accountName: "Client 40", revenueType: "Workplace", totalRevenue: 3200000, arr: 1200000, timePeriod: 2024 },
  //   { accountName: "Client 32", revenueType: "GCP", totalRevenue: 480000, arr: 100000, timePeriod: 2024 },
  //   { accountName: "Client 3", revenueType: "DA", totalRevenue: 600000, arr: 230000, timePeriod: 2024 },
  //   { accountName: "Client 12", revenueType: "GCP", totalRevenue: 980000, arr: 120000, timePeriod: 2024 },
  //   { accountName: "Client 70", revenueType: "GCP", totalRevenue: 880000, arr: 220000, timePeriod: 2024 },
  // ];

  barChart = {
    chart: { 
      type: 'bar' as ApexChart["type"], 
      height: 350 
    },
    series: [
      { 
        name: "Clients", 
        data: [50, 120, 75]
      }
    ],
    xaxis: { 
      categories: ["GCP", "Workplace", "DA"]
    },
    plotOptions: {
      bar: {
        horizontal: false,
        columnWidth: "50%",
        distributed: true
      }
    },
    dataLabels: { enabled: true },
    colors: ["#008FFB", "#00E396", "#FEB019", "#FF4560"],
    tooltip: {
      enabled: true,
      y: {
        formatter: (val: number) => `${val} Clients`
      }
    }
  };

  gaugeChart = {
    series: [81],
    chart: { 
      type: 'radialBar' as ApexChart["type"], 
      height: 350 
    },
    plotOptions: {
      radialBar: {
        startAngle: -90,
        endAngle: 90,
        track: {
          background: '#e7e7e7',
          strokeWidth: '97%'
        },
        dataLabels: {
          name: { 
            show: true,
            fontSize: '16px',
            offsetY: 20,
            color: '#333',
            formatter: () => "Revenue Target Score" 
          }, 
          value: { 
            fontSize: '24px', 
            show: true,
            offsetY: -10,
            formatter: (val: number) => `${Math.round((val / 100) * 60)}M`
          }
        }
      }
    },
    fill: { colors: ['#4CAF50'] },
    stroke: { lineCap: 'round' as ApexStroke["lineCap"] },
    yaxis: {
      min: 0,
      max: 60
    }
  }
  
  constructor(private revenueService: RevenueService) {
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
          borderRadius: 8,
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
        show: true,
      },
    };
  }

  ngOnInit(): void {
    this.fetchRevenueData();
  }
  
  fetchRevenueData(): void {

    this.revenueService.getPipelineCount().subscribe((response) => {
      this.pipelineCount = response.pipeline_count;
    });

    this.revenueService.getRevenueSum().subscribe((response) => {
      this.revenueCount = response.revenue_sum;
    });

    this.revenueService.getSigningsCount().subscribe((response) => {
      this.signingsCount = response.signings_count;
    });

    this.revenueService.getWinsCount().subscribe((response) => {
      this.winsCount = response.wins_count;
    });
  }

}

import { Component, OnInit, ViewEncapsulation } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NgApexchartsModule } from 'ng-apexcharts';
import { ApexChart } from 'ng-apexcharts';
import { HeaderComponent } from '../../header/header.component';
import { SidebarComponent } from '../../sidebar/sidebar.component';
import { DashboardService } from '../../services/dashboard-services/dashboard.service';
import { PipelineService } from '../../services/pipeline-services/pipeline.service';
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
  selector: 'app-pipeline-dashboard',
  imports: [NgApexchartsModule, CommonModule, SidebarComponent, HeaderComponent],
  standalone: true,
  templateUrl: './pipeline-dashboard.component.html',
  styleUrl: './pipeline-dashboard.component.css',
  encapsulation: ViewEncapsulation.Emulated
})
export class PipelineDashboardComponent implements OnInit {

  pipelineCount: number = 0;
  revenueCount: number = 0;
  signingsCount: number = 0;
  winsCount: number = 0;

  pipelineData: any[] = [];

  pipelineChartData: any[] = [];
  isDataLoaded: boolean = false;

  constructor(private dashboardService: DashboardService, private pipelineService: PipelineService) { }

  ngOnInit() {
    // this.fetchDashboardData();
    this.fetchPipelineTable();
    this.fetchPipelineChart();

  }

  // fetchDashboardData(): void {
  //   this.dashboardService.getPipelineCount().subscribe((response: { pipeline_count: number; }) => {
  //     this.pipelineCount = response.pipeline_count;
  //   });

  //   this.dashboardService.getRevenueSum().subscribe((response: { revenue_sum: number; }) => {
  //     this.revenueCount = response.revenue_sum;
  //   });

  //   this.dashboardService.getSigningsCount().subscribe((response: { signings_count: number; }) => {
  //     this.signingsCount = response.signings_count;
  //   });

  //   this.dashboardService.getWinsCount().subscribe((response: { wins_count: number; }) => {
  //     this.winsCount = response.wins_count;
  //   });
  // }

  fetchPipelineTable(): void {
    this.pipelineService.getPipelineTable().subscribe((data) => {
      this.pipelineData = data;
    });
  }



  fetchPipelineChart(): void {
    this.pipelineService.getPipelineChart().subscribe((data) => {
      this.pipelineChartData = data;
      this.isDataLoaded = true;
      this.updateBarChartData();
    });
  }

  updateBarChartData(): void {
    this.pipelineService.getPipelineChart().subscribe((data) => {
      console.log('Fetched data:', data);
      data.sort((a: any, b: any) => a.probability - b.probability);
      this.barChart.series = [{
        name: 'Accounts',
        data: data.map((item: any) => item.count)
      }];
      this.barChart.xaxis.categories = data.map((item: any) => item.probability.toString());
    });
  }








  get cards() {
    return [
      { title: 'Pipeline', value: `$${this.pipelineCount}`, percentage: '+55%' },
      { title: 'Revenue', value: `$${this.revenueCount}`, percentage: '+5%' },
      { title: 'Count To Wins', value: `${this.winsCount}`, percentage: '-14%' },
      { title: 'Signings', value: `$${this.signingsCount}`, percentage: '+8%' },
    ];
  }

  barChart = {
    chart: { type: 'bar' as ApexChart['type'], height: 350 },
    series: [{ name: 'Clients', data: [] as number[] }],
    xaxis: { categories: ['10%', '33%', '66%', '95%'] as string[] },
    yaxis: {
      title: {
        text: 'Accounts #', style: {
          fontFamily: 'Arial, Helvetica, sans-serif',
        }
      }
    },
    plotOptions: {
      bar: { horizontal: false, columnWidth: '50%', distributed: true }
    },
    dataLabels: { enabled: true },
    colors: ['#008FFB', '#00E396', '#FEB019', '#FF4560'],
    tooltip: {
      enabled: true,
      y: { formatter: (val: number) => `${val} Clients` }
    }
  };

  gaugeChart = {
    series: [46],
    chart: { type: 'radialBar' as ApexChart['type'], height: 350 },
    plotOptions: {
      radialBar: {
        startAngle: -90,
        endAngle: 90,
        track: { background: '#e7e7e7', strokeWidth: '97%' },
        dataLabels: {
          name: { show: true, fontSize: '16px', offsetY: 20, color: '#333', formatter: () => 'Pipeline Target Score' },
          value: { fontSize: '24px', show: true, offsetY: -10, formatter: (val: number) => `${Math.round((val / 100) * 60)}M` }
        }
      }
    },
    fill: { colors: ['#4CAF50'] },
    yaxis: { min: 0, max: 60 }
  };
}

import {
  Component,
  OnInit,
  ViewEncapsulation,
  ViewChild,
  AfterViewInit,
  AfterViewChecked,
} from '@angular/core';
import { CommonModule } from '@angular/common';
import { NgApexchartsModule, ChartComponent, ApexChart } from 'ng-apexcharts';
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
  imports: [
    NgApexchartsModule,
    CommonModule,
    SidebarComponent,
    HeaderComponent,
  ],
  standalone: true,
  templateUrl: './pipeline-dashboard.component.html',
  styleUrl: './pipeline-dashboard.component.css',
  encapsulation: ViewEncapsulation.Emulated,
})
export class PipelineDashboardComponent
  implements OnInit, AfterViewInit, AfterViewChecked
{
  @ViewChild('barChartRef') barChartRef!: ChartComponent;
  @ViewChild('gaugeChartRef') gaugeChartRef!: ChartComponent;

  pipelineCount = 0;
  revenueCount = 0;
  signingsCount = 0;
  winsCount = 0;

  pipelineData: any[] = [];
  pipelineChartData: any[] = [];
  isDataLoaded = false;

  constructor(
    private dashboardService: DashboardService,
    private pipelineService: PipelineService
  ) {}

  ngOnInit() {
    this.fetchDashboardData();
    this.fetchPipelineTable();
    this.fetchPipelineChart();
  }

  ngAfterViewInit(): void {
    this.toggleChartTheme();
  }

  ngAfterViewChecked(): void {
    this.toggleChartTheme();
  }

  toggleChartTheme(): void {
    const isDark = document.body.classList.contains('dark-mode');
    const labelColor = isDark ? '#ffffff' : '#333333';

    this.barChartRef?.updateOptions(
      {
        theme: {
          mode: isDark ? 'dark' : 'light',
        },
        chart: {
          foreColor: 'var(--text-color)',
        },
        grid: {
          borderColor: isDark ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)',
        },
        tooltip: {
          theme: isDark ? 'dark' : 'light',
        },
      },
      false,
      true
    );

    this.gaugeChartRef?.updateOptions(
      {
        theme: {
          mode: isDark ? 'dark' : 'light',
        },
        chart: {
          foreColor: 'var(--text-color)',
        },
        plotOptions: {
          radialBar: {
            dataLabels: {
              name: {
                color: labelColor,
              },
              value: {
                color: labelColor,
              },
            },
          },
        },
        tooltip: {
          theme: isDark ? 'dark' : 'light',
        },
      },
      false,
      true
    );
  }

  fetchDashboardData(): void {
    this.dashboardService.getPipelineCount().subscribe((res) => {
      this.pipelineCount = res.pipeline_count;
    });
    this.dashboardService.getRevenueSum().subscribe((res) => {
      this.revenueCount = res.revenue_sum;
    });
    this.dashboardService.getSigningsCount().subscribe((res) => {
      this.signingsCount = res.signings_count;
    });
    this.dashboardService.getWinsCount().subscribe((res) => {
      this.winsCount = res.wins_count;
    });
  }

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
      data.sort((a: any, b: any) => a.probability - b.probability);
      this.barChart.series = [
        {
          name: 'Accounts',
          data: data.map((item: any) => item.count),
        },
      ];
      this.barChart.xaxis.categories = data.map((item: any) =>
        item.probability.toString()
      );
    });
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
        title: 'Count To Wins',
        value: `${this.winsCount}`,
        percentage: '-14%',
      },
      {
        title: 'Signings',
        value: `$${this.signingsCount}`,
        percentage: '+8%',
      },
    ];
  }

  barChart = {
    chart: {
      type: 'bar' as ApexChart['type'],
      height: 350,
      background: 'transparent',
      foreColor: 'var(--text-color)',
    },
    series: [{ name: 'Clients', data: [] as number[] }],
    xaxis: { categories: ['10%', '33%', '66%', '95%'] as string[] },
    yaxis: {
      title: {
        text: 'Accounts #',
        style: { fontFamily: 'Arial, Helvetica, sans-serif' },
      },
    },
    plotOptions: {
      bar: { horizontal: false, columnWidth: '50%', distributed: true },
    },
    dataLabels: { enabled: true },
    colors: ['#008FFB', '#00E396', '#FEB019', '#FF4560'],
    tooltip: {
      enabled: true,
      theme: document.body.classList.contains('dark-mode') ? 'dark' : 'light',
      y: { formatter: (val: number) => `${val} Clients` },
    },
    theme: {
      mode: document.body.classList.contains('dark-mode') ? 'dark' : 'light',
    },
  };

  gaugeChart = {
    series: [46],
    chart: {
      type: 'radialBar' as ApexChart['type'],
      height: 350,
      background: 'transparent',
    },
    plotOptions: {
      radialBar: {
        startAngle: -90,
        endAngle: 90,
        track: {
          background: '#e7e7e7',
          strokeWidth: '97%',
        },
        dataLabels: {
          name: {
            show: true,
            fontSize: '16px',
            offsetY: 20,
            color: '#333',
            formatter: () => 'Pipeline Target Score',
          },
          value: {
            fontSize: '24px',
            show: true,
            offsetY: -10,
            color: '#333',
            formatter: (val: number) => `${Math.round((val / 100) * 60)}M`,
          },
        },
      },
    },
    fill: {
      colors: ['#4CAF50'],
    },
    yaxis: {
      min: 0,
      max: 60,
    },
    tooltip: {
      enabled: true,
      theme: document.body.classList.contains('dark-mode') ? 'dark' : 'light',
    },
    theme: {
      mode: document.body.classList.contains('dark-mode') ? 'dark' : 'light',
    },
  };
}

import {
  Component,
  OnInit,
  AfterViewInit,
  AfterViewChecked,
  ViewChild,
  ViewEncapsulation,
} from '@angular/core';
import { CommonModule } from '@angular/common';
import { SidebarComponent } from '../../sidebar/sidebar.component';
import { NgApexchartsModule, ChartComponent, ApexChart } from 'ng-apexcharts';
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
  imports: [
    NgApexchartsModule,
    CommonModule,
    SidebarComponent,
    HeaderComponent,
  ],
  standalone: true,
  templateUrl: './revenue-page.component.html',
  styleUrls: ['./revenue-page.component.css'],
  encapsulation: ViewEncapsulation.Emulated,
})
export class RevenuePageComponent
  implements OnInit, AfterViewInit, AfterViewChecked
{
  @ViewChild('barChartRef') barChartRef!: ChartComponent;
  @ViewChild('gaugeChartRef') gaugeChartRef!: ChartComponent;

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
    this.fetchDashboardData();
    this.fetchRevenueClients();
    this.fetchRevenueChart();
  }

  ngAfterViewInit(): void {
    this.toggleChartTheme(); // Initial check
  }

  ngAfterViewChecked(): void {
    this.toggleChartTheme(); // Re-check on return to page
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
    this.dashboardService
      .getPipelineCount()
      .subscribe((response: { pipeline_count: number }) => {
        this.pipelineCount = response.pipeline_count;
      });

    this.dashboardService
      .getRevenueSum()
      .subscribe((response: { revenue_sum: number }) => {
        this.revenueCount = response.revenue_sum;
      });

    this.dashboardService
      .getSigningsCount()
      .subscribe((response: { signings_count: number }) => {
        this.signingsCount = response.signings_count;
      });

    this.dashboardService
      .getWinsCount()
      .subscribe((response: { wins_count: number }) => {
        this.winsCount = response.wins_count;
      });
  }

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

  barChart = {
    chart: {
      type: 'bar' as ApexChart['type'],
      height: 350,
      background: 'transparent',
      foreColor: 'var(--text-color)',
    },
    series: [{ name: 'Clients', data: [] as number[] }],
    xaxis: { categories: [] as string[] },
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
    series: [81],
    chart: {
      type: 'radialBar' as ApexChart['type'],
      height: 350,
      background: 'transparent',
      foreColor: 'var(--text-color)',
    },
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
            color: '#333',
            formatter: (val: number) => `${Math.round((val / 100) * 60)}M`,
          },
        },
      },
    },
    fill: { colors: ['#4CAF50'] },
    yaxis: { min: 0, max: 60 },
    tooltip: {
      enabled: true,
      theme: document.body.classList.contains('dark-mode') ? 'dark' : 'light',
    },
    theme: {
      mode: document.body.classList.contains('dark-mode') ? 'dark' : 'light',
    },
  };
}

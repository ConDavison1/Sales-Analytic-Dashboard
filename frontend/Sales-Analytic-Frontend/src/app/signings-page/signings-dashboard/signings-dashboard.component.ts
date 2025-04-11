import { Component, OnInit, ViewEncapsulation } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NgApexchartsModule } from 'ng-apexcharts';
import { ApexChart } from 'ng-apexcharts';
import { HeaderComponent } from '../../header/header.component';
import { SidebarComponent } from '../../sidebar/sidebar.component';
import { SigningsService } from '../../services/signings-page/signings.service';
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
interface ChartData {
  category: string;
  count: number;
}
@Component({
  selector: 'app-signings-dashboard',
  imports: [NgApexchartsModule, CommonModule, SidebarComponent, HeaderComponent],
  standalone: true,
  templateUrl: './signings-dashboard.component.html',
  styleUrls: ['./signings-dashboard.component.css'],
  encapsulation: ViewEncapsulation.Emulated,
})
export class SigningsDashboardComponent implements OnInit {
  pipelineCount: number = 0;
  revenueCount: number = 0;
  signingsCount: number = 0;
  winsCount: number = 0;

  signingsData: any[] = [];

  signingsChartData: ChartData[] = [];

  showFilterOverlay: boolean = false;

  selectedFilters: {
    product_category: Set<string>;
    quarter: Set<string>;
  } = {
    product_category: new Set(),
    quarter: new Set(),
  };

  uniqueProductCategories: string[] = [];
  uniqueQuarters: string[] = [];

  isDataLoaded: boolean = false;

  constructor(
    private dashboardService: DashboardService,
    private signingsService: SigningsService
  ) {}

  ngOnInit(): void {
    this.fetchDashboardData();
    this.fetchSigningsData();
    this.fetchSigningsChart();
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

  fetchSigningsData(): void {
    this.signingsService.getSigningsData().subscribe((data) => {
      this.signingsData = data;
      this.signingsData = [...data];
  
      this.uniqueProductCategories = [...new Set(data.map(row => row.category))];
      this.uniqueQuarters = [...new Set(data.map(row => row.quarter))];
    });
  }

  toggleFilter(category: keyof typeof this.selectedFilters, value: string, event: Event): void {
    const checked = (event.target as HTMLInputElement).checked;
    if (checked) {
      this.selectedFilters[category].add(value);
    } else {
      this.selectedFilters[category].delete(value);
    }
  }

  applyMultiFilters(): void {
    this.signingsData = this.signingsData.filter(row =>
      (!this.selectedFilters.product_category.size || this.selectedFilters.product_category.has(row.stage)) &&
      (!this.selectedFilters.quarter.size || this.selectedFilters.quarter.has(row.forecast_category))
    );
    this.showFilterOverlay = false;
  }

  clearFilters(): void {
    this.selectedFilters.product_category.clear();
    this.selectedFilters.quarter.clear();
    this.signingsData= [...this.signingsData];
  }

  onOverlayClick(event: MouseEvent): void {
    this.showFilterOverlay = false;
  }

  fetchSigningsCount(): void {
    this.signingsService.getSigningsCount().subscribe((data) => {
      this.signingsData = data;
    });
  }

  fetchSigningsChart(): void {
    this.signingsService.getSigningsChart().subscribe((data) => {
      this.signingsChartData = data;
      this.isDataLoaded = true;
      this.updateBarChartData();
    });
  }

  updateBarChartData(): void {
    if (this.signingsChartData.length > 0) {
      this.barChart = {
        ...this.barChart,
        series: [
          {
            data: this.signingsChartData.map((item) => item.count),
            name: '',
          },
        ],
        xaxis: {
          categories: this.signingsChartData.map((item) =>
            String(item.category)
          ),
        },
      };
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
    },
    series: [
      {
        name: 'Forecast Categories',
        data: [] as number[],
      },
    ],
    xaxis: {
      categories: [] as string[],
    },
    plotOptions: {
      bar: {
        horizontal: false,
        columnWidth: '50%',
        distributed: true,
      },
    },
    dataLabels: { enabled: true },
    colors: ['#008FFB', '#00E396', '#FEB019', '#FF4560'],
    tooltip: {
      enabled: true,
      y: { formatter: (val: number) => `${val} Clients` },
    },
    legend: {
      show: false,
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
            formatter: () => 'Signings Target Score',
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

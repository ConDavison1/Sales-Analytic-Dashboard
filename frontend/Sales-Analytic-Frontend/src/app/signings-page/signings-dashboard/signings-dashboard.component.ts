import { Component, OnInit, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ChartComponent, NgApexchartsModule } from 'ng-apexcharts';
import {
  ApexAxisChartSeries,
  ApexChart,
  ApexXAxis,
  ApexYAxis,
  ApexDataLabels,
  ApexPlotOptions,
  ApexTooltip,
  ApexFill,
  ApexNonAxisChartSeries,
  ApexResponsive,
  ApexChart as ApexNonAxisChart
} from 'ng-apexcharts';
import { HeaderComponent } from '../../header/header.component';
import { SidebarComponent } from '../../sidebar/sidebar.component';
import { SigningsService } from '../../services/signings-page/signings.service';
import { FormsModule } from '@angular/forms';

export type BarChartOptions = {
  series: ApexAxisChartSeries;
  chart: ApexChart;
  xaxis: ApexXAxis;
  yaxis: ApexYAxis;
  dataLabels: ApexDataLabels;
  plotOptions: ApexPlotOptions;
  tooltip: ApexTooltip;
  colors: string[];
};

export type PolarChartOptions = {
  series: ApexNonAxisChartSeries;
  chart: ApexNonAxisChart;
  labels: string[];
  colors: string[];
  responsive: ApexResponsive[];
};

@Component({
  selector: 'app-signings-dashboard',
  standalone: true,
  templateUrl: './signings-dashboard.component.html',
  styleUrls: ['./signings-dashboard.component.css'],
  imports: [
    CommonModule,
    NgApexchartsModule,
    HeaderComponent,
    SidebarComponent,
    FormsModule
  ]
})
export class SigningsDashboardComponent implements OnInit {
  @ViewChild('barChartRef') barChartRef!: ChartComponent;
  @ViewChild('gaugeChartRef') gaugeChartRef!: ChartComponent;

  username = localStorage.getItem('username') || '';
  year = 2024;

  signingsData: any[] = [];
  signingsDataUnfiltered: any[] = [];
  quarterlyCards: any[] = [];

  showFilterOverlay: boolean = false;
  searchTerm: string = '';

  selectedFilters: {
    product_category: Set<string>;
    fiscal_quarter: Set<string>;
  } = {
    product_category: new Set<string>(),
    fiscal_quarter: new Set<string>()
  };

  uniqueProductCategories: string[] = [];
  uniqueQuarters: string[] = [];

  barChart: BarChartOptions = {
    series: [{ name: 'iACV', data: [] }],
    chart: {
      type: 'bar',
      height: 350,
      background: 'transparent'
    },
    xaxis: {
      categories: [],
      title: {
        text: 'Industry'
      }
    },
    yaxis: {
      title: {
        text: 'Incremental ACV ($)'
      },
      labels: {
        formatter: (val: number) => `$${val.toLocaleString()}`
      }
    },
    dataLabels: {
      enabled: true,
      formatter: (val: number) => `$${val.toLocaleString()}`
    },
    plotOptions: {
      bar: {
        columnWidth: '60%',
        distributed: false
      }
    },
    tooltip: {
      enabled: true,
      y: {
        formatter: (val: number) => `$${val.toLocaleString()}`
      }
    },
    colors: ['#3f51b5']
  };

  polarChart: PolarChartOptions = {
    series: [],
    chart: {
      type: 'polarArea',
      height: 350
    },
    labels: [],
    colors: [
      '#1E90FF', '#FF8C00', '#32CD32', '#FF69B4',
      '#8A2BE2', '#00CED1', '#FFD700', '#FF6347',
      '#40E0D0', '#DA70D6'
    ],
    responsive: [
      {
        breakpoint: 480,
        options: {
          chart: {
            height: 300
          },
          legend: {
            position: 'bottom'
          }
        }
      }
    ]
  };

  gaugeChart = {
    series: [0],
    chart: {
      type: 'radialBar' as const,
      height: 350,
      background: 'transparent'
    },
    plotOptions: {
      radialBar: {
        startAngle: -90,
        endAngle: 90,
        dataLabels: {
          name: {
            show: true,
            fontSize: '16px',
            offsetY: 20,
            formatter: () => 'Signings Target Score'
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
    fill: { colors: ['#4CAF50'] } as ApexFill
  };

  constructor(private signingsService: SigningsService) {}

  ngOnInit(): void {
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    this.username = user.username || '';

    if (!this.username) {
      console.warn('[SigningsDashboard] No username found in localStorage.');
      return;
    }

    console.log('[SigningsDashboard] Username:', this.username);
    this.loadSignings();
    this.loadIndustryChart();
    this.loadQuarterlyTargets();
    this.loadProvincialDistributionChart();
  }

  loadSignings(): void {
    this.signingsService.getSignings(this.username, this.year).subscribe({
      next: res => {
        const formattedData = res.signings.map((s: any) => ({
          client_name: s.client_name,
          product_name: s.product_name,
          product_category: s.product_category,
          total_contract_value: s.total_contract_value,
          incremental_acv: s.incremental_acv,
          start_date: s.start_date,
          end_date: s.end_date,
          signing_date: s.signing_date,
          fiscal_year: s.fiscal_year,
          fiscal_quarter: s.fiscal_quarter
        }));
        this.signingsDataUnfiltered = formattedData;
        this.signingsData = [...formattedData];

        this.uniqueProductCategories = [...new Set<string>(
          formattedData.map((row: any) => row.product_category as string)
        )];
        this.uniqueQuarters = [...new Set<string>(
          formattedData.map((row: any) => row.fiscal_quarter as string)
        )];
      },
      error: err => console.error('Signings error:', err)
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

  applyFilters(): void {
    this.signingsData = this.signingsDataUnfiltered.filter(row =>
    (!this.selectedFilters.product_category.size || this.selectedFilters.product_category.has(row.product_category)) &&
    (!this.selectedFilters.fiscal_quarter.size || this.selectedFilters.fiscal_quarter.has(row.fiscal_quarter)) &&
    (!this.searchTerm || row.client_name.toLowerCase().includes(this.searchTerm.toLowerCase()))
    );
    this.showFilterOverlay = false;
  }

  clearFilters(): void {
    this.selectedFilters.product_category.clear();
    this.selectedFilters.fiscal_quarter.clear();
    this.searchTerm = '';
    this.signingsData = [...this.signingsDataUnfiltered];
    this.showFilterOverlay = false;
  }

  onOverlayClick(event: MouseEvent): void {
    this.showFilterOverlay = false;
  }

  loadIndustryChart(): void {
    console.log('[SigningsDashboard] Loading Industry ACV Histogram...');
    this.signingsService.getIndustryACV(this.username, this.year).subscribe({
      next: res => {
        const chartData = res.industry_acv_data;
        const industries = chartData.map((item: any) => item.industry);
        const values = chartData.map((item: any) => item.incremental_acv);

        this.barChart.series = [{ name: 'iACV', data: values }];
        this.barChart = {
          ...this.barChart,
          series: [{ name: 'iACV', data: values }],
          xaxis: {
            ...this.barChart.xaxis,
            categories: industries,
            title: { text: 'Industry' }
          }
        };
      },
      error: err => console.error('Industry ACV error:', err)
    });
  }

  loadProvincialDistributionChart(): void {
    console.log('[SigningsDashboard] Loading Provincial Distribution...');
    this.signingsService.getProvincialDistribution(this.username, this.year).subscribe({
      next: (res) => {
        const data = res.provincial_data;
        this.polarChart.series = data.map((item: any) => item.count);
        this.polarChart.labels = data.map((item: any) => `${item.province} - $${item.avg_value.toLocaleString()}`);
      },
      error: (err) => console.error('Provincial Distribution error:', err)
    });
  }

  loadQuarterlyTargets(): void {
    this.signingsService.getQuarterlyTargets(this.username, this.year).subscribe({
      next: res => {
        this.quarterlyCards = res.quarterly_targets.map((q: any) => ({
          title: `Q${q.quarter} Target`,
          value: `$${q.accumulated_value.toLocaleString()}`,
          percentage: `${q.achievement_percentage.toFixed(1)}% Achieved`
        }));
        const latest = res.quarterly_targets[res.quarterly_targets.length - 1];
        this.gaugeChart.series = [latest.achievement_percentage];
      },
      error: err => console.error('Quarterly targets error:', err)
    });
  }
}
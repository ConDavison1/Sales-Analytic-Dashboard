import {
  Component,
  OnInit,
  ViewChild,
  AfterViewInit,
  AfterViewChecked,
  ViewEncapsulation,
} from '@angular/core';
import { CommonModule } from '@angular/common';
import { DashboardService } from '../../services/dashboard-services/dashboard.service';
import { AccountExecService } from '../../services/account-exec-services/account-exec.service';
import { first } from 'rxjs';
import { ChartComponent, NgApexchartsModule, ApexChart } from 'ng-apexcharts';
import {
  FormGroup,
  FormBuilder,
  Validators,
  ReactiveFormsModule,
} from '@angular/forms';

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
  selector: 'app-account-exec-dashboard',
  imports: [CommonModule, NgApexchartsModule, ReactiveFormsModule],
  standalone: true,
  templateUrl: './account-exec-dashboard.component.html',
  styleUrl: './account-exec-dashboard.component.css',
  encapsulation: ViewEncapsulation.Emulated,
})
export class AccountExecDashboardComponent
  implements OnInit, AfterViewInit, AfterViewChecked
{
  @ViewChild('barChartRef') chartComponent!: ChartComponent;

  pipelineCount = 0;
  revenueCount = 0;
  signingsCount = 0;
  winsCount = 0;
  addExecutiveForm: FormGroup;

  accountExecData: any[] = [];
  selectedExecutive: any = null;
  topExecutivesChartData: ChartData[] = [];

  isDataLoaded = false;

  constructor(
    private dashboardService: DashboardService,
    private accountExecService: AccountExecService,
    private fb: FormBuilder
  ) {
    this.addExecutiveForm = this.fb.group({
      first_name: ['', Validators.required],
      last_name: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
    });
  }

  ngOnInit(): void {
    this.fetchDashboardData();
    this.fetchAccountExecData();
    this.fetchTopExecutivesChart();

    this.accountExecData = [
      {
        executive_id: 1,
        first_name: 'John',
        last_name: 'Doe',
        email: 'john.doe@example.com',
        location: 'Calgary',
        performance: '$50000',
        status: 'Active',
        assigned_accounts: [
          'Sigma Strategies',
          'Beta Biotech',
          'Alpha Agencies',
        ],
      },
      {
        executive_id: 2,
        first_name: 'Jane',
        last_name: 'Doe',
        email: 'jane.doe@example.com',
        location: 'Toronto',
        performance: '$70000',
        status: 'Active',
        assigned_accounts: [1, 2, 17, 67, 68, 71],
      },
    ];

    this.topExecutivesChartData = [
      { category: 'John Doe', count: 50000 },
      { category: 'Jane Doe', count: 70000 },
      { category: 'Emily Johnson', count: 80000 },
      { category: 'Michael Brown', count: 75000 },
      { category: 'Steven White', count: 100 },
      { category: 'Sarah Black', count: 90000 },
    ];

    this.updateBarChartData();
  }

  ngAfterViewInit(): void {
    this.toggleChartTheme();
  }

  ngAfterViewChecked(): void {
    this.toggleChartTheme();
  }

  toggleChartTheme(): void {
    const isDark = document.body.classList.contains('dark-mode');

    this.chartComponent?.updateOptions(
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

  fetchAccountExecData(): void {
    this.accountExecService
      .getAccountExecData()
      .pipe(first())
      .subscribe((data: any[]) => {
        this.accountExecData = data;
        this.isDataLoaded = true;
      });
  }

  fetchTopExecutivesChart(): void {
    this.accountExecService.getTopExecutivesChart().subscribe((data) => {
      this.topExecutivesChartData = data;
      this.isDataLoaded = true;
      this.updateBarChartData();
    });
  }

  toggleExecutive(executive: any): void {
    this.selectedExecutive =
      this.selectedExecutive === executive ? null : executive;
  }

  updateBarChartData(): void {
    if (this.topExecutivesChartData.length > 0) {
      const top5Executives = this.topExecutivesChartData
        .sort((a, b) => b.count - a.count)
        .slice(0, 5);

      this.barChart = {
        ...this.barChart,
        series: [
          {
            data: top5Executives.map((item) => item.count),
            name: '',
          },
        ],
        xaxis: {
          categories: top5Executives.map((item) => item.category),
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
        value: `$${this.winsCount}`,
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
    series: [
      {
        name: 'Top Executives by Sales',
        data: [] as number[],
      },
    ],
    plotOptions: {
      bar: {
        horizontal: true,
        columnWidth: '50%',
        distributed: true,
      },
    },
    dataLabels: { enabled: true },
    colors: ['#008FFB', '#00E396', '#FEB019', '#FF4560'],
    tooltip: {
      enabled: true,
      theme: document.body.classList.contains('dark-mode') ? 'dark' : 'light',
      y: { formatter: (val: number) => `${val} Sales` },
    },
    legend: {
      show: false,
    },
    xaxis: {
      categories: [] as string[],
    },
    theme: {
      mode: document.body.classList.contains('dark-mode') ? 'dark' : 'light',
    },
  };

  addExecutive(): void {
    if (this.addExecutiveForm.valid) {
      const newExecutive = {
        executive_id: this.accountExecData.length + 1,
        ...this.addExecutiveForm.value,
      };

      this.accountExecData.push(newExecutive);
      alert('New Executive Added');
      console.log('Updated Executives:', this.accountExecData);
      this.addExecutiveForm.reset();
    } else {
      alert('Please fill in all required fields');
    }
  }

  removeExecutive(executiveId: number): void {
    if (confirm('Are you sure you want to delete this executive?')) {
      this.accountExecData = this.accountExecData.filter(
        (executive) => executive.executive_id !== executiveId
      );
      console.log('Updated Executives:', this.accountExecData);
    }
  }
}

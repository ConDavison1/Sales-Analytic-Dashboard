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
  topExecutivesChartData: any[] = [];

  isDataLoaded = false;
  username = 'shogg';
  year = 2024;

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
    this.fetchAccountExecData();
    this.fetchTopExecutivesChart();
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
        theme: { mode: isDark ? 'dark' : 'light' },
        chart: { foreColor: 'var(--text-color)' },
        grid: {
          borderColor: isDark ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)',
        },
        tooltip: { theme: isDark ? 'dark' : 'light' },
      },
      false,
      true
    );
  }

  fetchAccountExecData(): void {
    this.accountExecService
      .getAccountExecData()
      .pipe(first())
      .subscribe({
        next: (res) => {
          console.log('Account Executives:', res.account_executives);
          this.accountExecData = res.account_executives || [];
        },
        error: (err) => {
          console.error('Error loading account executives:', err);
        },
      });
  }
  

  fetchTopExecutivesChart(): void {
    this.accountExecService
      .getAEPerformance(this.username, this.year)
      .pipe(first())
      .subscribe((res) => {
        const data = res.ae_performance || [];
        this.topExecutivesChartData = data.map((ae: any) => ({
          category: ae.account_executive_name,
          count: ae.wins_revenue,
        }));
        this.updateBarChartData();
        this.isDataLoaded = true;
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
    colors: ['#4285F4', '#DB4437', '#F4B400', '#0F9D58'],
    tooltip: {
      enabled: true,
      theme: document.body.classList.contains('dark-mode') ? 'dark' : 'light',
      y: { formatter: (val: number) => `$${val.toLocaleString()}` },
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
        user_id: this.accountExecData.length + 100, 
        ...this.addExecutiveForm.value,
        role: 'account-executive',
        location: 'N/A',
        performance: 'N/A',
      };
  
      this.accountExecData.push(newExecutive);
      alert('New Executive Added');
      this.addExecutiveForm.reset();
    } else {
      alert('Please fill in all required fields');
    }
  }
  

  removeExecutive(executiveId: number): void {
    if (confirm('Are you sure you want to delete this executive?')) {
      this.accountExecData = this.accountExecData.filter(
        (executive) => executive.user_id !== executiveId
      );
      console.log('Updated Executives:', this.accountExecData);
    }
  }
}

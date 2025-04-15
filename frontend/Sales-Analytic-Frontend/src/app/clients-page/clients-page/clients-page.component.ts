import {
  Component,
  OnInit,
  AfterViewInit,
  ViewChild,
  OnDestroy,
} from '@angular/core';
import { Router } from '@angular/router';
import { ClientService } from './../../services/client-services/client.service';
import { HeaderComponent } from '../../header/header.component';
import { SidebarComponent } from '../../sidebar/sidebar.component';
import { CommonModule } from '@angular/common';
import { ChartComponent, NgApexchartsModule } from 'ng-apexcharts';
import { Title } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';

import {
  FormGroup,
  FormBuilder,
  Validators,
  ReactiveFormsModule,
} from '@angular/forms';

@Component({
  selector: 'app-clients-page',
  standalone: true,
  imports: [
    HeaderComponent,
    SidebarComponent,
    CommonModule,
    NgApexchartsModule,
    ReactiveFormsModule,
    FormsModule,
  ],
  templateUrl: './clients-page.component.html',
  styleUrls: ['./clients-page.component.css'],
})
export class ClientsPageComponent implements OnInit, AfterViewInit, OnDestroy {
  @ViewChild('industryChartRef') industryChartRef?: ChartComponent;
  @ViewChild('provinceChartRef') provinceChartRef?: ChartComponent;

  username = '';
  isDataLoaded = false;
  loadCount = 0;
  totalLoads = 2;

  industryTreemap: any = {};
  provincePieChart: any = {};
  clients: any[] = [];
  clientsUnfiltered: any[] = [];

  showFilterOverlay: boolean = false;
  searchTerm: string = '';

  selectedFilters: {
    industry: Set<string>;
    account_executive: Set<string>;
  } = {
    industry: new Set<string>(),
    account_executive: new Set<string>()
  }

  uniqueIndustries: string[] = [];
  uniqueExecutives: string[] = [];

  private themeObserver!: MutationObserver;

  constructor(
    private clientService: ClientService,
    private fb: FormBuilder,
    private router: Router,
    private titleService: Title
  ) {}

  ngOnInit(): void {
    this.titleService.setTitle('Clients | Sales Analytics');


    const user = JSON.parse(localStorage.getItem('user') || '{}');
    const token = localStorage.getItem('token');
    this.username = user.username || '';

    if (this.username && token) {
      this.loadIndustryTreemap();
      this.loadProvincePieChart();
      this.clientService.getClients(this.username).subscribe({
        next: (res) => {
          const formattedData = res.clients.map((c: any) => ({
            client_id: c.client_id,
            client_name: c.client_name,
            industry: c.industry,
            city: c.city,
            province: c.province,
            account_executive: c.account_executive,
            created_date: c.created_date,
          }));

          this.clientsUnfiltered = formattedData;
          this.clients = [...formattedData];

          this.uniqueIndustries = [
            ...new Set<string>(
              formattedData.map((row: any) => row.industry as string)
            ),
          ];

          this.uniqueExecutives = [
            ...new Set<string>(
              formattedData.map((row: any) => row.account_executive as string)
            ),
          ];

        },
        error: (err) => {
          console.error('Client fetch error:', err);
        },
      });
    } else {
      console.warn(
        '[ClientsPage] No token or username available yet. Retrying...'
      );
    }

    this.themeObserver = new MutationObserver(() => {
      this.toggleChartTheme();
    });

    this.themeObserver.observe(document.body, {
      attributes: true,
      attributeFilter: ['class'],
    });
  }

  ngAfterViewInit(): void {
    // Ensure charts get correct theme styling after they render
    setTimeout(() => this.toggleChartTheme(), 800);
  }

  ngOnDestroy(): void {
    if (this.themeObserver) {
      this.themeObserver.disconnect();
    }
  }

  private markLoaded(): void {
    this.loadCount++;
    if (this.loadCount >= this.totalLoads) {
      this.isDataLoaded = true;
      // Charts are ready, apply theme one last time
      setTimeout(() => this.toggleChartTheme(), 200);
    }
  }

  applyFilters(): void {
    this.clients = this.clientsUnfiltered.filter(
      (row) =>
        (!this.selectedFilters.industry.size ||
          this.selectedFilters.industry.has(row.industry)) &&
        (!this.selectedFilters.account_executive.size ||
          this.selectedFilters.account_executive.has(row.account_executive)) &&
        (!this.searchTerm ||
          row.client_name.toLowerCase().includes(this.searchTerm.toLowerCase()))
    );
    this.showFilterOverlay = false;
  }

  toggleFilter(
    industry: keyof typeof this.selectedFilters,
    value: string,
    event: Event
  ): void {
    const checked = (event.target as HTMLInputElement).checked;
    if (checked) {
      this.selectedFilters[industry].add(value);
    } else {
      this.selectedFilters[industry].delete(value);
    }
  }

  clearFilters(): void {
    this.selectedFilters.industry.clear();
    this.selectedFilters.account_executive.clear();
    this.searchTerm = '';
    this.clients = [...this.clientsUnfiltered];
    this.showFilterOverlay = false;
  }

  onOverlayClick(event: MouseEvent): void {
    this.showFilterOverlay = false;
  }

  toggleChartTheme(): void {
    const isDark = document.body.classList.contains('dark-mode');
    const foreColor = isDark ? '#fff' : '#000';

    this.industryChartRef?.updateOptions(
      {
        chart: {
          foreColor,
          theme: { mode: isDark ? 'dark' : 'light' },
        },
        tooltip: { theme: isDark ? 'dark' : 'light' },
      },
      false,
      true
    );

    this.provinceChartRef?.updateOptions(
      {
        chart: {
          foreColor,
          theme: { mode: isDark ? 'dark' : 'light' },
        },
        legend: {
          labels: {
            colors: [foreColor],
          },
        },
        tooltip: { theme: isDark ? 'dark' : 'light' },
      },
      false,
      true
    );
  }

  loadIndustryTreemap(): void {
    const isDark = document.body.classList.contains('dark-mode');
    const foreColor = isDark ? '#fff' : '#000';

    this.clientService.getIndustryTreemap(this.username).subscribe({
      next: (treemapData) => {
        this.industryTreemap = {
          chart: {
            type: 'treemap',
            height: 350,
            foreColor,
            theme: { mode: isDark ? 'dark' : 'light' },
          },
          series: [
            {
              data: treemapData.map((item: any) => ({
                x: item.x,
                y: item.y,
              })),
            },
          ],
          tooltip: {
            theme: isDark ? 'dark' : 'light',
          },
        };
        this.markLoaded();
      },
      error: (err) => {
        console.error('Industry Treemap Error:', err);
        this.markLoaded();
      },
    });
  }

  loadProvincePieChart(): void {
    const isDark = document.body.classList.contains('dark-mode');
    const foreColor = isDark ? '#fff' : '#000';

    this.clientService.getProvincePieChart(this.username).subscribe({
      next: (res) => {
        this.provincePieChart = {
          chart: {
            type: 'pie',
            height: 350,
            foreColor,
            theme: { mode: isDark ? 'dark' : 'light' },
          },
          labels: res.labels,
          series: res.series,
          legend: {
            position: 'bottom',
            labels: {
              colors: [foreColor],
            },
          },
          tooltip: {
            theme: isDark ? 'dark' : 'light',
          },
        };
        this.markLoaded();
      },
      error: (err) => {
        console.error('Province Pie Chart Error:', err);
        this.markLoaded();
      },
    });
  }
}

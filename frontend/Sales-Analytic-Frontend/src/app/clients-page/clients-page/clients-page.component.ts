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

  private themeObserver!: MutationObserver;

  constructor(
    private clientService: ClientService,
    private fb: FormBuilder,
    private router: Router
  ) {}

  ngOnInit(): void {
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    this.username = user.username || '';

    if (this.username) {
      this.loadIndustryTreemap();
      this.loadProvincePieChart();
      this.clientService.getClients(this.username).subscribe({
        next: (res) => {
          this.clients = res.clients;
        },
        error: (err) => {
          console.error('Client fetch error:', err);
        },
      });
    }

    // Watch for theme changes
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

import { Component, OnInit, AfterViewInit, ViewChild } from '@angular/core';
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
export class ClientsPageComponent implements OnInit, AfterViewInit {
  @ViewChild('industryChartRef') industryChartRef?: ChartComponent;
  @ViewChild('provinceChartRef') provinceChartRef?: ChartComponent;

  username = '';
  isDataLoaded = false;
  loadCount = 0;
  totalLoads = 2;

  industryTreemap: any = {};
  provincePieChart: any = {};
  clients: any[] = [];


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
          console.log('Clients loaded:', this.clients);
        },
        error: (err) => {
          console.error('Client fetch error:', err);
        },
      });
      
    }
  }

  ngAfterViewInit(): void {
    const observer = new MutationObserver(() => {
      this.toggleChartTheme();
    });

    observer.observe(document.body, {
      attributes: true,
      attributeFilter: ['class'],
    });
  }

  private markLoaded(): void {
    this.loadCount++;
    if (this.loadCount >= this.totalLoads) {
      this.isDataLoaded = true;
    }
  }

  toggleChartTheme(): void {
    const isDark = document.body.classList.contains('dark-mode');

    this.industryChartRef?.updateOptions(
      {
        theme: {
          mode: isDark ? 'dark' : 'light',
        },
        chart: {
          foreColor: 'var(--text-color)',
        },
      },
      false,
      true
    );

    this.provinceChartRef?.updateOptions(
      {
        theme: {
          mode: isDark ? 'dark' : 'light',
        },
        chart: {
          foreColor: 'var(--text-color)',
        },
      },
      false,
      true
    );
  }
  loadClients(): void {
    this.clientService.getClients(this.username).subscribe({
      next: (res) => {
        this.clients = res.clients;  
      },
      error: (err) => {
        console.error('Client fetch error:', err);
      }
    });
  }
  
  loadIndustryTreemap(): void {
    this.clientService.getIndustryTreemap(this.username).subscribe({
      next: (treemapData) => {
        this.industryTreemap = {
          chart: { type: 'treemap', height: 350 },
          series: [
            {
              data: treemapData.map((item: any) => ({
                x: item.x,
                y: item.y,
              })),
            },
          ],        
          tooltip: {
            custom: ({ series, seriesIndex, dataPointIndex, w }: any) => {
              const data = treemapData[dataPointIndex];
              return `<div class="tooltip">
                <strong>${data.x}</strong><br>
                Clients: ${data.client_count}<br>
                Revenue: $${data.revenue.toLocaleString()}
              </div>`;
            },
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
    this.clientService.getProvincePieChart(this.username).subscribe({
      next: (res) => {
        this.provincePieChart = {
          chart: { type: 'pie', height: 350 },
          labels: res.labels,
          series: res.series,
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

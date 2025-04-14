import {
  Component,
  OnInit,
  AfterViewInit,
  OnDestroy,
  ViewChild,
} from '@angular/core';
import { CommonModule } from '@angular/common';
import { NgApexchartsModule, ChartComponent } from 'ng-apexcharts';
import { HeaderComponent } from '../../header/header.component';
import { SidebarComponent } from '../../sidebar/sidebar.component';
import { PipelineService } from '../../services/pipeline-services/pipeline.service';
import { FormsModule } from '@angular/forms';
import { Title } from '@angular/platform-browser';

@Component({
  standalone: true,
  selector: 'app-pipeline-dashboard',
  templateUrl: './pipeline-dashboard.component.html',
  styleUrls: ['./pipeline-dashboard.component.css'],
  imports: [
    CommonModule,
    NgApexchartsModule,
    SidebarComponent,
    HeaderComponent,
    FormsModule,
  ],
})
export class PipelineDashboardComponent
  implements OnInit, AfterViewInit, OnDestroy
{
  username = '';
  year = 2024;

  cards: any[] = [];
  pipelineData: any[] = [];
  pipelineDataUnfiltered: any[] = [];

  showFilterOverlay: boolean = false;
  searchTerm: string = '';

  selectedFilters: {
    stage: Set<string>;
    forecast_category: Set<string>;
  } = {
    stage: new Set<string>(),
    forecast_category: new Set<string>(),
  };

  uniqueStages: string[] = [];
  uniqueForecastCategories: string[] = [];
  funnelChart: any = {};
  heatmapChart: any = {};

  // ViewChild references for the ApexCharts components.
  @ViewChild('funnelChartRef') funnelChartRef!: ChartComponent;
  @ViewChild('heatmapChartRef') heatmapChartRef!: ChartComponent;

  // MutationObserver to detect theme changes.
  private themeObserver!: MutationObserver;

  constructor(private pipelineService: PipelineService, private titleService: Title) {}

  ngOnInit(): void {
    this.titleService.setTitle('Pipeline | Sales Analytics');
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    this.username = user.username || '';

    if (this.username) {
      this.loadOpportunities();
      this.loadStageFunnel();
      this.loadHeatmapChart();
      this.loadQuarterlyCards();
    }

    // Set up MutationObserver to watch for changes in the body's class attribute.
    this.themeObserver = new MutationObserver((mutations) => {
      mutations.forEach((mutation) => {
        if (
          mutation.type === 'attributes' &&
          mutation.attributeName === 'class'
        ) {
          console.log('Pipeline Dashboard: Theme change detected.');
          this.toggleChartTheme();
        }
      });
    });
    this.themeObserver.observe(document.body, {
      attributes: true,
      attributeFilter: ['class'],
    });
  }

  ngAfterViewInit(): void {
    // Immediately update the charts with the current theme.
    this.toggleChartTheme();

    // Use multiple delays to ensure that dark mode is applied before the charts update.
    setTimeout(() => {
      this.toggleChartTheme();
    }, 500);
    setTimeout(() => {
      this.toggleChartTheme();
    }, 1000);
  }

  ngOnDestroy(): void {
    if (this.themeObserver) {
      this.themeObserver.disconnect();
    }
  }

  /**
   * Updates the chart options for the Funnel and Heatmap charts based on the active theme.
   * When dark mode is active (i.e. body contains "dark-mode"), foreColor is set to white.
   */
  toggleChartTheme(): void {
    const isDark = document.body.classList.contains('dark-mode');
    const foreColor = isDark ? '#fff' : '#000';

    // Update the Funnel Chart
    if (this.funnelChartRef) {
      this.funnelChartRef.updateOptions(
        {
          chart: {
            foreColor: foreColor,
            theme: { mode: isDark ? 'dark' : 'light' },
          },
          xaxis: {
            labels: { style: { colors: [foreColor] } },
          },
          tooltip: { theme: isDark ? 'dark' : 'light' },
        },
        false,
        true
      );
    }

    // Update the Heatmap Chart
    if (this.heatmapChartRef) {
      this.heatmapChartRef.updateOptions(
        {
          chart: {
            foreColor: foreColor,
            theme: { mode: isDark ? 'dark' : 'light' },
          },
          xaxis: {
            labels: { style: { colors: [foreColor] } },
          },
          tooltip: { theme: isDark ? 'dark' : 'light' },
        },
        false,
        true
      );
    }
  }

  loadQuarterlyCards(): void {
    this.pipelineService
      .getQuarterlyTargets(this.username, this.year)
      .subscribe((res) => {
        const quarters = res.quarterly_targets;
        if (!quarters || quarters.length === 0) {
          console.warn('No quarterly targets available');
          return;
        }
        this.cards = quarters.map((q: any) => ({
          title: `Q${q.quarter} Target`,
          value: `$${q.accumulated_value.toLocaleString()}`,
          percentage: `${q.achievement_percentage.toFixed(1)}% Achieved`,
        }));
      });
  }

  loadOpportunities(): void {
    this.pipelineService.getOpportunities(this.username).subscribe((res) => {
      const formattedData = res.opportunities.map((opp: any) => ({
        account_name: opp.client_name,
        opportunity_id: opp.opportunity_id,
        stage: opp.sales_stage,
        forecast_category: opp.forecast_category,
        probability: `${opp.probability}%`,
        opportunity_value: `$${opp.amount.toLocaleString()}`,
        time_period: opp.close_date,
      }));

      this.pipelineDataUnfiltered = formattedData;
      this.pipelineData = [...formattedData];

      this.uniqueForecastCategories = [
        ...new Set<string>(
          formattedData.map((row: any) => row.forecast_category as string)
        ),
      ];
      this.uniqueStages = Array.from(
        new Set<string>(formattedData.map((row: any) => row.stage))
      );
    });
  }

  toggleFilter(
    stage: keyof typeof this.selectedFilters,
    value: string,
    event: Event
  ): void {
    const checked = (event.target as HTMLInputElement).checked;
    if (checked) {
      this.selectedFilters[stage].add(value);
    } else {
      this.selectedFilters[stage].delete(value);
    }
  }

  applyFilters(): void {
    this.pipelineData = this.pipelineData.filter(
      (row) =>
        (!this.selectedFilters.stage.size ||
          this.selectedFilters.stage.has(row.stage)) &&
        (!this.selectedFilters.forecast_category.size ||
          this.selectedFilters.forecast_category.has(row.forecast_category)) &&
        (!this.searchTerm ||
          row.account_name
            .toLowerCase()
            .includes(this.searchTerm.toLowerCase()))
    );
    this.showFilterOverlay = false;
  }

  clearFilters(): void {
    this.selectedFilters.stage.clear();
    this.selectedFilters.forecast_category.clear();
    this.searchTerm = '';
    this.pipelineData = [...this.pipelineDataUnfiltered];
    this.showFilterOverlay = false;
  }

  onOverlayClick(event: MouseEvent): void {
    this.showFilterOverlay = false;
  }

  loadStageFunnel(): void {
    this.pipelineService
      .getStageFunnelData(this.username, this.year)
      .subscribe((res) => {
        const sortedData = res.stage_funnel_data.sort(
          (a: any, b: any) => b.count - a.count
        );
        const funnelStages = sortedData.map((d: any) => d.stage);
        const funnelCounts = sortedData.map((d: any) => d.count);
        const isDark = document.body.classList.contains('dark-mode');
        const foreColor = isDark ? '#fff' : '#000';

        this.funnelChart = {
          series: [
            {
              name: 'Funnel Series',
              data: funnelCounts,
            },
          ],
          chart: {
            type: 'bar',
            height: 400,
            foreColor: foreColor,
            theme: { mode: isDark ? 'dark' : 'light' },
          },
          plotOptions: {
            bar: {
              horizontal: true,
              barHeight: '80%',
              borderRadius: 0,
              distributed: true,
              isFunnel: true,
            },
          },
          dataLabels: {
            enabled: true,
            formatter: function (val: any, opt: any) {
              return funnelStages[opt.dataPointIndex] + ': ' + val;
            },
          },
          xaxis: {
            categories: funnelStages,
            labels: { style: { colors: [foreColor] } },
          },
          colors: [
            '#4285F4', // Google Blue
            '#34A853', // Google Green
            '#FBBC05', // Google Yellow
            '#EA4335', // Google Red
            '#A142F4', // Google Purple
            '#00ACC1', // Google Teal
          ],
        };
      });
  }

  loadHeatmapChart(): void {
    this.pipelineService.getHeatmapData(this.username, this.year).subscribe({
      next: (res: any) => {
        if (!res || !Array.isArray(res.heatmap_data)) {
          console.warn('Invalid or missing heatmap data:', res);
          return;
        }
        const data = res.heatmap_data;
        const productCategories = [
          ...new Set(data.map((d: any) => d.product_category)),
        ];
        const forecastCategories = [
          ...new Set(data.map((d: any) => d.forecast_category)),
        ];
        const series = productCategories.map((product) => ({
          name: product,
          data: forecastCategories.map((forecast) => {
            const match = data.find(
              (d: any) =>
                d.product_category === product &&
                d.forecast_category === forecast
            );
            return match ? match.value : 0;
          }),
        }));
        const isDark = document.body.classList.contains('dark-mode');
        const foreColor = isDark ? '#fff' : '#000';

        this.heatmapChart = {
          series,
          chart: {
            height: 350,
            type: 'heatmap',
            foreColor: foreColor,
            theme: { mode: isDark ? 'dark' : 'light' },
          },
          dataLabels: { enabled: true },
          xaxis: {
            categories: forecastCategories,
            labels: { style: { colors: [foreColor] } },
          },
          legend: {
            position: 'bottom',
          },
          plotOptions: {
            heatmap: {
              enableShades: false,
              colorScale: {
                ranges: [
                  {
                    from: 0,
                    to: 500000,
                    name: 'Low',
                    color: '#4285F4',
                  },
                  {
                    from: 500001,
                    to: 1000000,
                    name: 'Below Average',
                    color: '#DB4437',
                  },
                  {
                    from: 1000001,
                    to: 15000000,
                    name: 'Above Average',
                    color: '#F4B400',
                  },
                  {
                    from: 15000001,
                    to: 17000000,
                    name: 'High',
                    color: '#0F9D58',
                  },
                ],
              },
            },
          },
          fill: { opacity: 1 },
        };
      },
      error: (err) => {
        console.error('Error fetching heatmap data:', err);
      },
    });
  }
}

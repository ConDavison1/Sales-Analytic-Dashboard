import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NgApexchartsModule } from 'ng-apexcharts';
import { HeaderComponent } from '../../header/header.component';
import { SidebarComponent } from '../../sidebar/sidebar.component';
import { PipelineService } from '../../services/pipeline-services/pipeline.service';
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
  ],
})
export class PipelineDashboardComponent implements OnInit {
  username = '';
  year = 2024;

  cards: any[] = [];
  pipelineData: any[] = [];

  funnelChart: any = {};
  heatmapChart: any = {};

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
      this.pipelineData = res.opportunities.map((opp: any) => ({
        account_name: opp.client_name,
        opportunity_id: opp.opportunity_id,
        stage: opp.sales_stage,
        forecast_category: opp.forecast_category,
        probability: `${opp.probability}%`,
        opportunity_value: `$${opp.amount.toLocaleString()}`,
        //close_date: opp.close_date,
      }));
    });
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

        this.heatmapChart = {
          series,
          chart: { height: 350, type: 'heatmap', toolbar: { show: false } },
          fill: {
            type: 'gradient',
            gradient: {
              shadeIntensity: 1,
              opacityFrom: 0.8, // increased from 0.4
              opacityTo: 0.4,   // increased from 0.1
            },
          },
          
          dataLabels: {
            enabled: true,
            formatter: function (val: number) {
              return `$${val.toLocaleString()}`;
            },
          xaxis: { categories: forecastCategories },
          colors: ['#008FFB'],
          }
        };
      },
      error: (err) => {
        console.error('Error fetching heatmap data:', err);
      },
    });
  }
}

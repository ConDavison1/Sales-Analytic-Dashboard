import { Component, Pipe } from '@angular/core';
import { PipelineDashboardComponent } from '../pipeline-dashboard/pipeline-dashboard.component';
import { SidebarComponent } from '../../sidebar/sidebar.component';
import { HeaderComponent } from '../../header/header.component';

@Component({
  selector: 'app-pipeline-page',
  imports: [PipelineDashboardComponent, SidebarComponent, HeaderComponent],
  templateUrl: './pipeline-page.component.html',
  styleUrl: './pipeline-page.component.css'
})
export class PipelinePageComponent {

}

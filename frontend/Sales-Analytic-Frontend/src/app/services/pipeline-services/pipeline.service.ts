import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class PipelineService {
  private apiUrl = 'https://sales-analytics-backend-jcggzuuyxq-uc.a.run.app';
  constructor(private http: HttpClient) { }

  getOpportunities(username: string, filters: any = {}): Observable<any> {
    const params = new HttpParams({ fromObject: { username, ...filters } });
    return this.http.get(`${this.baseUrl}/opportunities`, { params });
  }

  getStageFunnelData(username: string, year: number = 2024): Observable<any> {
    const params = new HttpParams().set('username', username).set('year', year);
    return this.http.get(`${this.baseUrl}/stage-funnel-chart-data`, { params });
  }

  getQuarterlyTargets(username: string, year: number = 2024): Observable<any> {
    const params = new HttpParams().set('username', username).set('year', year);
    return this.http.get(`${this.baseUrl}/pipeline-quarterly-targets`, { params });
  }
  getHeatmapData(username: string, year: number = 2024) {
    const params = new HttpParams().set('username', username).set('year', year);
    return this.http.get(`${this.baseUrl}/product-forecast-heatmap-chart-data`, { params });
  }
  
}

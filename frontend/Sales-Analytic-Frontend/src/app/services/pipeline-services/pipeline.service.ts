import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';


@Injectable({
  providedIn: 'root'
})
export class PipelineService {
  private apiUrl = 'https://sales-analytics-backend-jcggzuuyxq-uc.a.run.app';
  constructor(private http: HttpClient) { }

  getPipelineTable(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/pipeline-table-data`);
  }
  getPipelineChart(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/pipeline-chart-data`);
  }
}

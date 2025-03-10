import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';


@Injectable({
  providedIn: 'root'
})
export class PipelineService {
  private apiUrl = 'http://localhost:5000';
  constructor(private http: HttpClient) { }

  getPipelineTable(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/pipeline-table-data`);
  }
  getPipelineChart(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/pipeline-chart-data`);
  }
}

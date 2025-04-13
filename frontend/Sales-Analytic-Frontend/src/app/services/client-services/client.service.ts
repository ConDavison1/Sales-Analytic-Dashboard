import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root',
})
export class ClientService {
  private baseUrl = 'http://localhost:5000/api/clients';

  constructor(private http: HttpClient) {}

  getClients(username: string): Observable<any> {
    return this.http.get(`${this.baseUrl}/clients?username=${username}`)
      .pipe(catchError(this.handleError));
  }
  

  getIndustryTreemap(username: string): Observable<any> {
    return this.http
      .get<{ treemap_data: any[] }>(
        `${this.baseUrl}/industry-treemap-chart?username=${username}`
      )
      .pipe(
        map((res) => res.treemap_data),
        catchError(this.handleError)
      );
  }

  getProvincePieChart(username: string): Observable<any> {
    return this.http
      .get<{ labels: string[]; series: number[]; additional_data: any[] }>(
        `${this.baseUrl}/province-pie-chart?username=${username}`
      )
      .pipe(catchError(this.handleError));
  }

  private handleError(error: any): Observable<never> {
    console.error('API Error:', error);
    return throwError(error);
  }
}

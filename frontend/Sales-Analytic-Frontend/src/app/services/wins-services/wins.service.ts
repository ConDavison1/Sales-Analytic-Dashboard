import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root',
})
export class WinsService {
  baseUrl = `${environment.apiUrl}/api/wins`;

  constructor(private http: HttpClient) {}

  getWins(username: string, year = 2024): Observable<any> {
    const params = new HttpParams().set('username', username).set('year', year);
    return this.http.get(`${this.baseUrl}/wins`, { params });
  }

  getWinsQuarterlyTargets(username: string, year = 2024): Observable<any> {
    const params = new HttpParams().set('username', username).set('year', year);
    return this.http.get(`${this.baseUrl}/wins-quarterly-targets`, { params });
  }

  getWinsCategoryDistribution(username: string, year = 2024): Observable<any> {
    const params = new HttpParams().set('username', username).set('year', year);
    return this.http.get(`${this.baseUrl}/win-category-quarterly-chart`, { params });
  }

  getWinsOverTime(username: string, year = 2024): Observable<any> {
    const params = new HttpParams().set('username', username).set('year', year);
    return this.http.get(`${this.baseUrl}/win-quarterly-evolution-chart`, { params });
  }
}

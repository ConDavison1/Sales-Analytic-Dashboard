import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class WinsService {
  baseUrl = 'http://localhost:5000/api/wins';

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
    return this.http.get(`${this.baseUrl}/win-category-quarterly-chart`, { params }); // 🔁 correct endpoint
  }

  getWinsOverTime(username: string, year = 2024): Observable<any> {
    const params = new HttpParams().set('username', username).set('year', year);
    return this.http.get(`${this.baseUrl}/win-quarterly-evolution-chart`, { params }); // 🔁 correct endpoint
  }
}

import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class SigningsService {
  private baseUrl = 'http://localhost:5000/api/signings';

  constructor(private http: HttpClient) {}

  getSignings(username: string, year = 2024, quarters?: number[], productCategories?: string[]): Observable<any> {
    let params = new HttpParams().set('username', username).set('year', year.toString());
    if (quarters?.length) params = params.set('quarters', quarters.join(','));
    if (productCategories?.length) params = params.set('product_categories', productCategories.join(','));

    return this.http.get(`${this.baseUrl}/signings`, { params });
  }

  getIndustryACV(username: string, year = 2024): Observable<any> {
    const params = new HttpParams().set('username', username).set('year', year.toString());
    return this.http.get(`${this.baseUrl}/industry-acv-chart-data`, { params });
  }

  getProvincialDistribution(username: string, year = 2024): Observable<any> {
    const params = new HttpParams().set('username', username).set('year', year.toString());
    return this.http.get(`${this.baseUrl}/provincial-distribution-chart`, { params });
  }

  getQuarterlyTargets(username: string, year = 2024): Observable<any> {
    const params = new HttpParams().set('username', username).set('year', year.toString());
    return this.http.get(`${this.baseUrl}/signings-quarterly-targets`, { params });
  }
}

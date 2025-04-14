import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root',
})
export class RevenueService {
  private baseUrl = `${environment.apiUrl}/api/revenue`;

  constructor(private http: HttpClient) {}

  getRevenue(username: string, year = 2024, quarters?: number[], productCategories?: string[]): Observable<any> {
    let params = new HttpParams().set('username', username).set('year', year.toString());

    if (quarters && quarters.length) {
      params = params.set('quarters', quarters.join(','));
    }

    if (productCategories && productCategories.length) {
      params = params.set('product_categories', productCategories.join(','));
    }

    return this.http.get(`${this.baseUrl}/revenue`, { params });
  }

  getRevenueProductDistribution(username: string, year = 2024): Observable<any> {
    const params = new HttpParams().set('username', username).set('year', year.toString());
    return this.http.get(`${this.baseUrl}/revenue-product-distribution-chart`, { params });
  }

  getIndustryRevenueAreaChart(username: string, year = 2024): Observable<any> {
    const params = new HttpParams().set('username', username).set('year', year.toString());
    return this.http.get(`${this.baseUrl}/industry-revenue-area-chart`, { params });
  }

  getRevenueQuarterlyTargets(username: string, year = 2024): Observable<any> {
    const params = new HttpParams().set('username', username).set('year', year.toString());
    return this.http.get(`${this.baseUrl}/revenue-quarterly-targets`, { params });
  }
}

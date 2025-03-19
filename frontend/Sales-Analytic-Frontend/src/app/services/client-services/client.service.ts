import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { Router } from '@angular/router';

interface RevenueSumResponse {
  revenue_sum: number;
}

interface PipelineCountResponse {
  pipeline_count: number;
}

interface SigningsCountResponse {
  signings_count: number;
}

interface WinsCountResponse {
  wins_count: number;
}

interface Clients {
  client_id: number;
  executive_id: number;
  company_name: string;
  industry: string;
  location: string;
  email: string;
}

@Injectable({
  providedIn: 'root',
})
export class ClientService {
  private baseUrl = 'https://sales-analytics-backend-jcggzuuyxq-uc.a.run.app';

  constructor(private http: HttpClient, private router: Router) {} 

  private getAuthHeaders(): HttpHeaders {
    const token = localStorage.getItem('token');
    if (!token) {
      console.warn("No JWT token found Redirecting to login.");
      this.router.navigate(['/login']); 
      return new HttpHeaders();
    }
    return new HttpHeaders({
      'Authorization': `Bearer ${token}`,  
      'Content-Type': 'application/json'
    });
  }

  // Revenue API Calls
  getRevenueSum(): Observable<RevenueSumResponse> {
    return this.http.get<RevenueSumResponse>(`${this.baseUrl}/revenue-sum`, { headers: this.getAuthHeaders() })
      .pipe(catchError(this.handleError));
  }

  getPipelineCount(): Observable<PipelineCountResponse> {
    return this.http.get<PipelineCountResponse>(`${this.baseUrl}/pipeline-count`, { headers: this.getAuthHeaders() })
      .pipe(catchError(this.handleError));
  }

  getSigningsCount(): Observable<SigningsCountResponse> {
    return this.http.get<SigningsCountResponse>(`${this.baseUrl}/signings-count`, { headers: this.getAuthHeaders() })
      .pipe(catchError(this.handleError));
  }

  getWinsCount(): Observable<WinsCountResponse> {
    return this.http.get<WinsCountResponse>(`${this.baseUrl}/wins-count`, { headers: this.getAuthHeaders() })
      .pipe(catchError(this.handleError));
  }

  getClients(): Observable<any> {
    let token = localStorage.getItem('token');
  
    if (!token) {
      console.warn("No JWT token found Redirecting to login.");
      this.router.navigate(['/login']);
      return new Observable(observer => observer.error({ message: "No authentication token found" }));
    }
  
    if (!token.startsWith("Bearer ")) {
      token = `Bearer ${token}`;
      localStorage.setItem('token', token); 
    }
  
    console.log("JWT Token Sent:", token);
  
    const headers = new HttpHeaders({
      'Authorization': token,
      'Content-Type': 'application/json'
    });
  
    console.log("Fetching clients with headers:", headers.keys());
  
    return this.http.get(`${this.baseUrl}/clients`, { headers }).pipe(
      catchError(error => {
        console.error("API Error:", error);
        return throwError(error);
      })
    );
  }
  
  

  deleteClient(clientId: number): Observable<void> {
    return this.http.delete<void>(`${this.baseUrl}/clients/${clientId}`, { headers: this.getAuthHeaders() })
      .pipe(catchError(this.handleError));
  }

  addClient(client: Clients): Observable<Clients> {
    return this.http.post<Clients>(`${this.baseUrl}/clients`, client, { headers: this.getAuthHeaders() })
      .pipe(catchError(this.handleError));
  }

  private handleError(error: any): Observable<never> {
    console.error("API Error:", error);
    return throwError(error);
  }
}

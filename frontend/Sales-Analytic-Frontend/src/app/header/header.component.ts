import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [CommonModule, FormsModule, HttpClientModule],
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css'],
})
export class HeaderComponent {
  aiQuery = '';
  aiInsight: string | null = null;

  constructor(private http: HttpClient) {}

  submitAIQuery() {
    const query = this.aiQuery.trim();
    if (!query) return;

    this.http.post<any>('http://localhost:5000/ai-insight', { query }).subscribe({
      next: (res) => {
        this.aiInsight = res.insight || 'No insight returned.';
      },
      error: (err) => {
        console.error(err);
        this.aiInsight = 'Something went wrong. Please try again.';
      },
    });
  }
}

import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { environment } from '../../environments/environment';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [
    FormsModule,
    CommonModule
  ],
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit {
  query: string = '';
  aiInsights: { query: string; response: string }[] = [];
  showInsight: boolean = false;
  isDarkMode: boolean = false;

  @ViewChild('insightPanel') insightPanel!: ElementRef;

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    const savedMode = localStorage.getItem('dark-mode');
    this.isDarkMode = savedMode === 'true';
    document.body.classList.toggle('dark-mode', this.isDarkMode);
  }

  toggleDarkMode(): void {
    this.isDarkMode = !this.isDarkMode;
    document.body.classList.toggle('dark-mode', this.isDarkMode);
    localStorage.setItem('dark-mode', this.isDarkMode.toString());
  }

  onSearchKeydown(event: KeyboardEvent): void {
    if (event.key === 'Enter' && this.query.trim()) {
      const userQuery = this.query;
      this.query = '';

      this.http
        .post<any>(`${environment.apiUrl}/ai-insight`, { query: userQuery })
        .subscribe({
          next: (res) => {
            console.log('AI Response:', res);
            this.aiInsights.push({
              query: userQuery,
              response: res.insight?.trim() || 'No insight could be generated.'
            });
            this.showInsight = true;

            setTimeout(() => {
              if (this.insightPanel) {
                this.insightPanel.nativeElement.scrollTop = this.insightPanel.nativeElement.scrollHeight;
              }
            }, 100);
          },
          error: (err) => {
            console.error('Search error:', err);
            this.aiInsights.push({
              query: userQuery,
              response: 'Something went wrong. Please try again.'
            });
            this.showInsight = true;
          }
        });
    }
  }

  closeInsightPopup(): void {
    this.showInsight = false;
  }

  clearInsights(): void {
    this.aiInsights = [];
  }
}

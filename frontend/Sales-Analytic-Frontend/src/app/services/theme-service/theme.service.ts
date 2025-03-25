import { Injectable, Signal, signal } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ThemeService {
  private readonly THEME_KEY = 'theme';
  private theme = signal<'light' | 'dark'>('light');

  constructor() {
    const storedTheme = localStorage.getItem(this.THEME_KEY) as 'light' | 'dark' | null;
    if (storedTheme) {
      this.theme.set(storedTheme);
    }
  }

  getTheme(): Signal<'light' | 'dark'> {
    return this.theme;
  }

  toggleTheme() {
    const newTheme = this.theme() === 'light' ? 'dark' : 'light';
    this.theme.set(newTheme);
  }

  private setTheme(theme: 'light' | 'dark') {
    this.theme.set(theme);
    localStorage.setItem(this.THEME_KEY, theme);

    if (theme === 'dark') {
      document.body.classList.add('dark-theme');
    } else {
      document.body.classList.remove('dark-theme');
    }
  }
}

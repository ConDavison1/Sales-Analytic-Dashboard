import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { CommonModule, NgIf } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { MatDialog } from '@angular/material/dialog';
import { MatDialogModule } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { ForgotPasswordModalComponent } from '../forgot-password-modal/forgot-password-modal.component';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [
    CommonModule, 
    FormsModule,
    HttpClientModule,
    MatDialogModule,
    MatButtonModule,
    MatInputModule,
    MatFormFieldModule,
    NgIf,
  ],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'],
})
export class LoginComponent {
  username: string = '';
  password: string = '';
  message: string = '';

  constructor(private http: HttpClient, private router: Router, private dialog: MatDialog) {}

  openForgotPasswordModal(): void {
    this.dialog.open(ForgotPasswordModalComponent, {
      width: '60%'
    });
  }

  showPassword = false;

  togglePasswordVisibility() {
    this.showPassword = !this.showPassword;
  }

  onLogin() {
    const payload = { username: this.username, password: this.password };
  
    this.http.post('http://localhost:5000/login', payload).subscribe({
      next: (response: any) => {
        if (!response.token) {
          this.message = "Login failed: No token received!";
          return;
        }
  
        const token = `Bearer ${response.token}`;
        localStorage.setItem('token', token);
        
        console.log('JWT Token:', token);
  
        try {
          const payloadBase64 = token.split('.')[1];  
          const decodedPayload = JSON.parse(atob(payloadBase64));
          console.log('Decoded JWT Payload:', decodedPayload);
        } catch (error) {
          console.error("Failed to decode JWT token:", error);
        }
  
        this.router.navigate(['/landing-page']);
      },
      error: (error) => {
        console.error("Login Error:", error);
        this.message = error.error.message || 'Login failed!';
      }
    });
  }
  
}

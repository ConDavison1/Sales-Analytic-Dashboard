import { appRoutes } from './app/app.routes';
import { bootstrapApplication } from '@angular/platform-browser';
import {
  provideHttpClient,
  withInterceptors
} from '@angular/common/http';
import { provideRouter } from '@angular/router';
import { AppComponent } from './app/app.component';
import { AuthInterceptor } from './app/auth/auth.interceptor'; // ✅ Make sure this path is correct

bootstrapApplication(AppComponent, {
  providers: [
    provideHttpClient(
      withInterceptors([AuthInterceptor]) // ✅ Register the interceptor here
    ),
    provideRouter(appRoutes)
  ]
}).catch(err => console.error(err));

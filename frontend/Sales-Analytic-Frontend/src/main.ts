import { appRoutes } from './app/app.routes';
import { bootstrapApplication } from '@angular/platform-browser';
import { provideHttpClient } from '@angular/common/http';
import { provideRouter } from '@angular/router'; // Import provideRouter
import { AppComponent } from './app/app.component'; // Import your root component

bootstrapApplication(AppComponent, {
  providers: [
    provideHttpClient(), // Provide HttpClient if necessary
    provideRouter(appRoutes) // Provide the router with your appRoutes
  ]
}).catch(err => console.error(err));

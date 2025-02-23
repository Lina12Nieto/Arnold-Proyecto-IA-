import { Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { ChatbotComponent } from './chatbot/chatbot.component';


export const routes: Routes = [
    {
      path: 'home',
      component: HomeComponent,
      data: { public: true }
    },
    {
      path: '',
      redirectTo: 'home',
      pathMatch: 'full',
      data: { public: true }
    },
    {
      path: '*',
      redirectTo: 'home',
      pathMatch: 'full',
      data: { public: true }
    },
    {
      path: 'chatbot',
      component: ChatbotComponent,
      data: { public: true }
    },
    {
      path: 'sobre-nosotros',
      component: ChatbotComponent,
      data: { public: true }
    },
  ];

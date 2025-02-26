import { Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { ChatBoxpComponent } from './chat-boxp/chat-boxp.component';


export const routes: Routes = [
    {
      path: 'home',
      component: HomeComponent,
      /* data: { public: true } */
    },
/*     {
      path: '',
      redirectTo: 'home',
      pathMatch: 'full',
      data: { public: true }
    } */
    {
      path: 'chat',
      component: ChatBoxpComponent,
      /* data: { public: true } */
    }
  ];

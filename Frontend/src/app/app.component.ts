import { Component, OnInit } from '@angular/core';
import { ApiService } from './services/api.service';
import { NavigationEnd, RouterOutlet } from '@angular/router';
import { MatToolbarModule } from '@angular/material/toolbar';
import {MatTabsModule} from '@angular/material/tabs';
import { Router } from '@angular/router';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    RouterOutlet, 
    MatToolbarModule, 
    MatTabsModule
  ],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  message = '';
  title = '💓';
  rutas = ['/', '/chatbot', '/sobre-nosotros', '*']
  selectedIndex = 0;

  constructor(private apiService: ApiService, private router: Router) { 
    console.log("Angular se está ejecutando correctamente");

    this.router.events.subscribe(event => {
      if (event instanceof NavigationEnd) {
        this.selectedIndex = this.rutas.indexOf(event.url); // Ajustar índice según la ruta actual
      }
    });
  }

  ngOnInit() {
    this.apiService.getMessage().subscribe(response => {
      this.message = response.message;
    });
  }

  cambiarRuta(index: number) {
    this.router.navigate([this.rutas[index]]);
  }
}

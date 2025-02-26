import { Component, OnInit } from '@angular/core';
import { ApiService } from './services/api.service';
import { RouterOutlet } from '@angular/router';
import { MatToolbarModule } from '@angular/material/toolbar';
import {MatButtonModule} from '@angular/material/button';
import { Router } from '@angular/router';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    RouterOutlet, 
    MatToolbarModule, 
    MatButtonModule
  ],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  message = '';
  title = '💓';

  constructor(private apiService: ApiService, private router: Router) { 
    console.log("Angular se está ejecutando correctamente");
  }

  ngOnInit() {
    this.apiService.getMessage().subscribe(response => {
      this.message = response.message;
    });
  }

  goTo(route: string) {
    this.router.navigate([route]);
  }

}

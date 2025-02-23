import { Component, OnInit } from '@angular/core';
import { ApiService } from './services/api.service';
import { RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  message = '';
  title = '💓';

  constructor(private apiService: ApiService) { 
    console.log("Angular se está ejecutando correctamente");
  }

  ngOnInit() {
    this.apiService.getMessage().subscribe(response => {
      this.message = response.message;
    });
  }
}

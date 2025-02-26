import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { CarouselModule } from 'primeng/carousel';
import { Router } from '@angular/router';

interface Ruta {
  url: string;
}

@Component({
  selector: 'app-home',
  imports: [CommonModule, CarouselModule],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css',
  standalone: true
})
export class HomeComponent implements OnInit {

  constructor(private router: Router) {
    console.log("HomeComponent cargado");
  }
  images: Ruta [] = [];

  ngOnInit(): void {
    this.images = [
      { url: 'assets/carrusel1.jpg' },
      { url: 'assets/carrusel2.jpg' },
      { url: 'assets/carrusel3.jpg' },
      { url: 'assets/carrusel4.jpg' },
      { url: 'assets/carrusel5.jpg' },
    ];
  }

  irAChatbot() {
    this.router.navigate(['/chat']);
  }
}

import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { MatIconModule } from '@angular/material/icon';


@Component({
  selector: 'app-chat-boxp',
  imports: [FormsModule, CommonModule, MatIconModule],
  templateUrl: './chat-boxp.component.html',
  styleUrls: ['./chat-boxp.component.css']
})
export class ChatBoxpComponent implements OnInit {
  @ViewChild('messagesContainer') private messagesContainer!: ElementRef;

  messages: { text: string, sender: string }[] = [];
  userInput: string = '';
  apiUrl = 'http://127.0.0.1:8000';
  questionId: number = 0;

  awaitingDietConfirmation: boolean = false; 
  awaitingDietType: boolean = false; 
  constructor(private http: HttpClient) {} 
  nombre_Dieta: string = '';

  ngOnInit() {
    this.messages.push({ 
      text: '👋 ¡Bienvenido, soy Arnold, tu asesor de nutrición! Responde las siguientes preguntas para calcular tu plan nutricional.', 
      sender: 'bot' 
    });

    this.http.get<{ message: string, question: string, question_id: number }>(`${this.apiUrl}/`)
      .subscribe(response => {
        this.messages.push({ text: response.question, sender: 'bot' });
        this.questionId = response.question_id;
      });
  }

  scrollToBottom() {
    setTimeout(() => {
      if (this.messagesContainer) {
        this.messagesContainer.nativeElement.scrollTop = this.messagesContainer.nativeElement.scrollHeight;
      }
    }, 100);
  }
  
  sendMessage() {
    if (this.userInput.trim() === '') return;
  
    // Agregar mensaje del usuario
    this.messages.push({ text: this.userInput, sender: 'user' });
    this.scrollToBottom();

    // Verificar si el usuario dijo "gracias"
    if (this.userInput.toLowerCase().includes("gracias")) {
      setTimeout(() => {
        this.messages.push({ text: "¡De nada❤️! Recuerda que estoy aquí para ayudarte. ¡Sigue adelante con tus metas! 💪😊", sender: 'bot' });
        this.scrollToBottom();
      }, 500);
      this.userInput = '';
      return;
    }
     // Si el chatbot está preguntando por la dieta
    if (this.awaitingDietConfirmation) {
      if (this.userInput.toLowerCase() === 'si') {
        this.messages.push({ text: '¿Qué tipo de dieta te gustaría?', sender: 'bot' });
        this.awaitingDietType = true;
      } else {
        this.messages.push({ text: '¡Entendido! Si necesitas algo más, avísame. 😊', sender: 'bot' });
      }
      this.awaitingDietConfirmation = false;
      this.userInput = '';
      return;
    }
    // Si el usuario está escribiendo el tipo de dieta que quiere
    if (this.awaitingDietType) {
      
      this.messages.push({ text: 'Estoy trabajando para ofrecerte la mejor dieta, dame un momento...', sender: 'bot' });
      this.nombre_Dieta =  this.userInput;
      setTimeout(() => {
        this.http.get<{ respuesta: string, dietas?: any[] }>(
          `${this.apiUrl}/Chatbot/?query=${this.nombre_Dieta}`
          
        ).subscribe(res => {
          this.messages.push({ text: res.respuesta, sender: 'bot' });
          if (res.dietas) {
            if (res.dietas && res.dietas.length > 0) {
              let mensajeDieta = ''
            
              res.dietas.forEach((dieta, index) => {
                mensajeDieta += `\n───────────────────────\n\n`;
                mensajeDieta += `🍽️ ${dieta.Recipe_name} (Tipo: ${dieta.Diet_type})\n`;
                mensajeDieta += `💪 Proteína: ${dieta.Protein}\n`;
                mensajeDieta += `🍞 Carbohidratos: ${dieta.Carbs}\n`;
                mensajeDieta += `🥑 Grasas: ${dieta.Fat}\n`;

                mensajeDieta += `\n───────────────────────\n\n`;
              });
            
              this.messages.push({ text: mensajeDieta, sender: 'bot' });
            } else {
              this.messages.push({ text: "Lo siento, no encontré dietas con ese tipo de cocina.", sender: 'bot' });
            }
          }
        });
        
      }, 3000);

      this.awaitingDietType = false;
      this.userInput = '';
      return;
    }
    
    // Enviar respuesta al backend
    this.http.post<{ message: string, question?: string, question_id?: number, TMB?: number, GET?: number, 'Calorías diarias recomendadas'?: number, Macronutrientes?: any }>(
      `${this.apiUrl}/answer`,
      { question_id: this.questionId, answer: this.userInput }
    ).subscribe(
      (res) => {
        if (res.question) {
          this.messages.push({ text: res.question, sender: 'bot' });
          this.scrollToBottom();
          this.questionId = res.question_id!;
        } else {
          this.messages.push({ text: 'Resultados:', sender: 'bot' });
          this.messages.push({ text: `TMB: ${res.TMB}`, sender: 'bot' });
          this.messages.push({ text: `GET: ${res.GET}`, sender: 'bot' });
          this.messages.push({ text: `Calorías diarias: ${res['Calorías diarias recomendadas']}`, sender: 'bot' });
          this.messages.push({ text: `Proteínas: ${res.Macronutrientes['Proteínas (g)']} g`, sender: 'bot' });
          this.messages.push({ text: `Grasas: ${res.Macronutrientes['Grasas (g)']} g`, sender: 'bot' });
          this.messages.push({ text: `Carbohidratos: ${res.Macronutrientes['Carbohidratos (g)']} g`, sender: 'bot' });
          
          // Preguntar si desea recomendaciones de dietas
          this.messages.push({ text: '¿Deseas que te de algunas sugerencias de dietas? (Sí / No)', sender: 'bot' });
          this.awaitingDietConfirmation = true;

        }
      },
      (error) => {
        this.messages.push({ text: 'Ha ocurrido un error 😞', sender: 'bot' });
      }
    );
    
    this.userInput = '';
  }
  
}

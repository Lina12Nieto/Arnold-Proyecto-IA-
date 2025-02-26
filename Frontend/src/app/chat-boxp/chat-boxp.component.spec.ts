import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ChatBoxpComponent } from './chat-boxp.component';

describe('ChatBoxpComponent', () => {
  let component: ChatBoxpComponent;
  let fixture: ComponentFixture<ChatBoxpComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ChatBoxpComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ChatBoxpComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

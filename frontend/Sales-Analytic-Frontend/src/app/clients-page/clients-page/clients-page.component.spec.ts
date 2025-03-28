import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ClientsPageComponent } from './clients-page.component';

describe('ClientsPageComponent', () => {
  let component: ClientsPageComponent;
  let fixture: ComponentFixture<ClientsPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ClientsPageComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(ClientsPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

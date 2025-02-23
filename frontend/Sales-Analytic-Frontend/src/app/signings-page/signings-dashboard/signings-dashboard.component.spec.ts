import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SigningsDashboardComponent } from './signings-dashboard.component';

describe('SigningsDashboardComponent', () => {
  let component: SigningsDashboardComponent;
  let fixture: ComponentFixture<SigningsDashboardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SigningsDashboardComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SigningsDashboardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

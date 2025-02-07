import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SigningsPageComponent } from './signings-page.component';

describe('SigningsPageComponent', () => {
  let component: SigningsPageComponent;
  let fixture: ComponentFixture<SigningsPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SigningsPageComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SigningsPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

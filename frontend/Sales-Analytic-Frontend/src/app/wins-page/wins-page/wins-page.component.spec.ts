import { ComponentFixture, TestBed } from '@angular/core/testing';

import { WinsPageComponent } from './wins-page.component';

describe('WinsPageComponent', () => {
  let component: WinsPageComponent;
  let fixture: ComponentFixture<WinsPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [WinsPageComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(WinsPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

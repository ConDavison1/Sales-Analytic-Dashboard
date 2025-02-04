import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RevenuePageFullComponent } from './revenue-page-full.component';

describe('RevenuePageFullComponent', () => {
  let component: RevenuePageFullComponent;
  let fixture: ComponentFixture<RevenuePageFullComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RevenuePageFullComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(RevenuePageFullComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

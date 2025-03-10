import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PipelineDashboardComponent } from './pipeline-dashboard.component';

describe('PipelineDashboardComponent', () => {
  let component: PipelineDashboardComponent;
  let fixture: ComponentFixture<PipelineDashboardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PipelineDashboardComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PipelineDashboardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

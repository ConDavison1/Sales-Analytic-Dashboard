import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AccountExecDashboardComponent } from './account-exec-dashboard.component';

describe('AccountExecDashboardComponent', () => {
  let component: AccountExecDashboardComponent;
  let fixture: ComponentFixture<AccountExecDashboardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AccountExecDashboardComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AccountExecDashboardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

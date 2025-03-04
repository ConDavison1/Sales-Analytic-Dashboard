import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AccountExecPageComponent } from './account-exec-page.component';

describe('AccountExecPageComponent', () => {
  let component: AccountExecPageComponent;
  let fixture: ComponentFixture<AccountExecPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AccountExecPageComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AccountExecPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

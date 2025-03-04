import { TestBed } from '@angular/core/testing';

import { AccountExecService } from './account-exec.service';

describe('AccountExecService', () => {
  let service: AccountExecService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(AccountExecService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});

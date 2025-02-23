import { TestBed } from '@angular/core/testing';

import { SigningsService } from './signings.service';

describe('SigningsService', () => {
  let service: SigningsService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(SigningsService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});

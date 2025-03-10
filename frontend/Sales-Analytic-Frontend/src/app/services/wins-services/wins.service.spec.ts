import { TestBed } from '@angular/core/testing';

import { WinsService } from './wins.service';

describe('WinsService', () => {
  let service: WinsService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(WinsService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});

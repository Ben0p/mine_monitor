import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SignDetailComponent } from './sign-detail.component';

describe('SignDetailComponent', () => {
  let component: SignDetailComponent;
  let fixture: ComponentFixture<SignDetailComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SignDetailComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SignDetailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

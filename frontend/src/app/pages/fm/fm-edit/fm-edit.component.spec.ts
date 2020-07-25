import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { FmEditComponent } from './fm-edit.component';

describe('FmEditComponent', () => {
  let component: FmEditComponent;
  let fixture: ComponentFixture<FmEditComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ FmEditComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(FmEditComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

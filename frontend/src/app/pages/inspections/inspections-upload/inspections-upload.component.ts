import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { of } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import { HttpEventType, HttpErrorResponse, HttpClient } from '@angular/common/http';
import { FormGroup, FormControl, Validators } from '@angular/forms';

import { InspectionsService } from '../../../@core/data/inspections.service'

@Component({
  selector: 'inspections-upload',
  templateUrl: './inspections-upload.component.html',
  styleUrls: ['./inspections-upload.component.scss']
})
export class InspectionsUploadComponent implements OnInit {

  fileToUpload: File = null;

  constructor(
    private inspectionsService: InspectionsService,
    private http: HttpClient
  ) { }

  handleFileInput(files: FileList) {
    this.fileToUpload = files.item(0);
  }

  submit() {
    const formData = new FormData();
    formData.append('file', this.fileToUpload);

    this.http.post('http://localhost:5000/api/inspections/upload', formData)
      .subscribe(res => {
        console.log(res);
        alert('Uploaded Successfully.');
      })
  }


  ngOnInit(): void {
  }

}

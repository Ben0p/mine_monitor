import { Component, OnInit, ViewChild, ElementRef, HostListener } from '@angular/core';
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
  @ViewChild("fileDropRef", { static: false }) fileDropEl: ElementRef;
  files: any[] = [];

  fileToUpload: File = null;

  constructor(
    private inspectionsService: InspectionsService,
    private http: HttpClient
  ) { }

  /**
 * on file drop handler
 */
  onFileDropped($event) {
    this.prepareFilesList($event);
  }

  /**
   * handle file from browsing
   */
  fileBrowseHandler(files) {
    this.prepareFilesList(files);
  }

  /**
   * Delete file from files list
   * @param index (File index)
   */
  deleteFile(index: number) {
    if (this.files[index].progress < 100) {
      console.log("Upload in progress.");
      return;
    }
    this.files.splice(index, 1);
  }

  /**
   * Simulate the upload process
   */
  uploadFilesSimulator(index: number) {
    setTimeout(() => {
      if (index === this.files.length) {
        return;
      } else {
        const progressInterval = setInterval(() => {
          if (this.files[index].progress === 100) {
            clearInterval(progressInterval);
            this.uploadFilesSimulator(index + 1);
          } else {
            this.files[index].progress += 5;
          }
        }, 200);
      }
    }, 1000);
  }

  /**
   * Convert Files list to normal array list
   * @param files (Files List)
   */
  prepareFilesList(files: Array<any>) {
    for (const item of files) {
      item.progress = 0;
      var fileIndex = this.files.push(item) -1;
      this.submit(item, fileIndex)
    }
    this.fileDropEl.nativeElement.value = "";

    this.uploadFilesSimulator(0);
  }

  /**
   * format bytes
   * @param bytes (File size in bytes)
   * @param decimals (Decimals point)
   */
  formatBytes(bytes, decimals = 2) {
    if (bytes === 0) {
      return "0 Bytes";
    }
    const k = 1024;
    const dm = decimals <= 0 ? 0 : decimals;
    const sizes = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + " " + sizes[i];
  }


  submit(file: File, fileIndex: number) {
    const formData = new FormData();
    formData.append('file', file);

    this.http.post('https://solmm01.fmg.local/api/inspections/upload', formData)
      .subscribe(res => {
        this.files[fileIndex].response = res
        console.log(this.files)
      })

  }


  ngOnInit(): void {
  }

}

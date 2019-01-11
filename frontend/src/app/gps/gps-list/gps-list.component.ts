import { Component, OnInit, ViewChild, AfterViewInit } from '@angular/core';
import { DataService } from "../../data.service";
import { MatPaginator, MatSort, MatTableDataSource } from '@angular/material';

export interface UserData {
  parent: string;
  ip: string;
}

@Component({
  selector: 'app-gps-list',
  templateUrl: './gps-list.component.html',
  styleUrls: ['./gps-list.component.scss']
})

export class GpsListComponent implements OnInit, AfterViewInit {

  displayedColumns: string[] = ['parent', 'ip'];
  dataSource: MatTableDataSource<UserData>;

  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatSort) sort: MatSort;

  constructor(private data: DataService) { 
  }
  

  ngOnInit() {
    this.data.getGpsList().subscribe((data) => {
      this.dataSource = new MatTableDataSource(data)
      this.dataSource.sort = this.sort;
      this.dataSource.paginator = this.paginator;
    });
  }

  ngAfterViewInit() {
  }

  applyFilter(filterValue: string) {
    this.dataSource.filter = filterValue.trim().toLowerCase();

    if (this.dataSource.paginator) {
      this.dataSource.paginator.firstPage();
    }
  }

}
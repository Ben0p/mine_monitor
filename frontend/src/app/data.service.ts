import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
    providedIn: 'root'
})

export class DataService {
    
    constructor(private http: HttpClient) { }

    getSigns() {
        return this.http.get('/assets/json/signs.json');
    }
}
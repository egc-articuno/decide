import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Voting } from './voting.model';

@Injectable({
  providedIn: 'root'
})
export class DataService {

  baseurl = 'http://127.0.0.1:8000/voting';

  constructor(private http: HttpClient) { }

  getVotings() {
    return this.http.get<Voting[]>(this.baseurl);
  }

  logUser() {
    return this.http.post
  }
}

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Voting } from './voting.model';
import { Token } from '@angular/compiler/src/ml_parser/lexer';

@Injectable({
  providedIn: 'root'
})
export class DataService {

  baseurl = 'http://127.0.0.1:8000/';

  constructor(private http: HttpClient) { }

  getVotings() {
    return this.http.get<Voting[]>(this.baseurl + 'voting');
  }

  logUser(user: String, pass: String) {
    return this.http.post<Token>(this.baseurl + 'authentication/login/',
      {
        username: user,
        password: pass
      }
    );
  }

  getUserId(jsonToken: String) {
    return this.http.post<Number>(this.baseurl + 'authentication/getuser/', jsonToken);
  }
}

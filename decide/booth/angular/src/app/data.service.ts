import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Voting, Token } from './voting.model';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class DataService {

  baseurl = 'http://127.0.0.1:8000/';

  constructor(private http: HttpClient) { }

  getVotings() {
    return this.http.get<Voting[]>(this.baseurl + 'voting');
  }

  logUser(user: string, pass: string): Observable<Token> {

    return this.http.post<Token>(this.baseurl + 'authentication/login/',
      {
        username: user,
        password: pass
      }
    );
  }

  getUserId(jsonToken: Token) {
    return this.http.post(this.baseurl + 'authentication/getuser/', jsonToken);
  }
}

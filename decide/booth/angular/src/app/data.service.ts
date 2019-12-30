import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Voting, Token, User } from './voting.model';
import { Observable } from 'rxjs';
import { promise } from 'protractor';

@Injectable({
  providedIn: 'root'
})
export class DataService {

  baseurl = 'http://127.0.0.1:8000/';

  constructor(private http: HttpClient) { }

  getVotings(): Observable<Voting[]> {
    return this.http.get<Voting[]>(this.baseurl + 'voting');
  }

  async logUser(user: string, pass: string): Promise<Token> {

    const token: Token = await this.http.post<Token>(this.baseurl + 'authentication/login/',
      {
        username: user,
        password: pass
      }
    ).toPromise();

    return token;
  }

  async getUserId(jsonToken: Token): Promise<User> {
    const user: User = await this.http.post<User>(this.baseurl + 'authentication/getuser/', jsonToken).toPromise();
    return user;
  }
}

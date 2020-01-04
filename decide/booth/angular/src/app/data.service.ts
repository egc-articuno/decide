import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Voting, Token, User } from './voting.model';
import { Observable, BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class DataService {

  constructor(private http: HttpClient) { }


  // gamalito(voting: Voting, option: number) {

  //   let p: bigint = BigInt.fromInt(voting.pub_key.p);
  //   let g = BigInt(voting.pub_key.g);
  //   let y = BigInt(voting.pub_key.y);

  //   let bigmsg = BigInt(option);

  //   // const bigmsg = BigInt.fromJSONObject("1");
  //   var cipher = ElGamal.encrypt({p, g, y}, bigmsg);

  // }

  private tokenSource = new BehaviorSubject<string>('Not ready token');
  private userIdSource = new BehaviorSubject<number>(null);
  currentToken = this.tokenSource.asObservable();
  currentUserId = this.userIdSource.asObservable();


  baseurl = 'http://127.0.0.1:8000/';

  changeToken(token: string) {
    this.tokenSource.next(token);
  }

  changeUserId(id: number) {
    this.userIdSource.next(id);
  }


  getVotingById(id: number): Observable<Voting> {
    return this.http.get<Voting>(this.baseurl + 'voting/' + id );
  }

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

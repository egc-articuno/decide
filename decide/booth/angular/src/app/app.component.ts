import { Component, OnInit } from '@angular/core';
import { Voting } from './voting.model';
import { DataService } from './data.service';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  votings: Voting[];

  // constructor(private api: ApiService) {
  //   this.getVoting();
  // }


  // (res: any) => {
  //   console.log(res);
  // }

  constructor(private dataService: DataService) {}

  ngOnInit() {
    return this.dataService.getVotings()
    .subscribe(data => this.votings = data);

  }

  // getVoting = () => {
  //   this.api.getVotings().subscribe(
  //     data => {
  //       this.votings = data;
  //     },
  //     error => {
  //       console.log(error);
  //     }
  //   );
  // };

}

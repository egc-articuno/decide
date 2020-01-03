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
  showVoting = false;


  constructor(private dataService: DataService) {}

  ngOnInit() {
    return this.dataService.getVotings()
    .subscribe(data => this.votings = data);

  }

}

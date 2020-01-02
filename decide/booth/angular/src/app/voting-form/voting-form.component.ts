import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { DataService } from '../data.service';
import { Voting, Option } from '../voting.model';

@Component({
  selector: 'app-voting-form',
  templateUrl: './voting-form.component.html',
  styleUrls: ['./voting-form.component.css']
})
export class VotingFormComponent implements OnInit {
  votingForm: FormGroup;
  voting: Voting;
  options: Option[] = [];
  isSubmitted = false;

  constructor(private formBuilder: FormBuilder, public dataService: DataService) {

    this.dataService.getVotings()
    .subscribe(data => {this.voting = data[0];
                        for (const op of this.voting.question.options) {
        console.log(op.option);
        this.options.push(op);
      }
    } );

    this.votingForm = this.formBuilder.group({
      demoArray: this.formBuilder.array([])
    });
  }

  ngOnInit() {
  }

  onSubmit(){
    this.isSubmitted = true;
    if(!this.votingForm.valid) {
      return false;
    } else {
      alert(JSON.stringify(this.votingForm.value));
    }
  }

}

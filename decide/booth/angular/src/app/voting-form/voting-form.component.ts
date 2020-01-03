import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, FormArray, FormControl } from '@angular/forms';
import { DataService } from '../data.service';
import { Voting, Option } from '../voting.model';

@Component({
  selector: 'app-voting-form',
  templateUrl: './voting-form.component.html',
  styleUrls: ['./voting-form.component.css']
})
export class VotingFormComponent {
  votingForm: FormGroup;
  voting: Voting;
  optionsData: Option[] = [];
  isSubmitted = false;

  constructor(private formBuilder: FormBuilder, public dataService: DataService) {
    this.votingForm = this.formBuilder.group({
      options: new FormArray([])
    });

    this.dataService.getVotings()
    .subscribe(data => {this.voting = data[0];
                        for (const op of this.voting.question.options) {
        this.optionsData.push(op);
      }
                        this.addCheckboxes();
    } );
  }

  private addCheckboxes() {
    this.optionsData.forEach((o, i) => {
    const control = new FormControl(); // if first item set to true, else false
    (this.votingForm.controls.options as FormArray).push(control);
    });
    }

  onSubmit() {
    const selectedOptions = this.votingForm.value.options
  .map((v, i) => v ? this.optionsData[i].number : null)
  .filter(v => v !== null);
    console.log(selectedOptions);
  }

}

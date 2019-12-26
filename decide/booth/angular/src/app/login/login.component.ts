import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { DataService } from '../data.service';
import { Observable } from 'rxjs';
import { Token } from '../voting.model';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  registerForm: FormGroup;
  username = '';
  password = '';
  buttonDisabled: boolean;
  submitted = false;
  token: Token;
  userId: any;



  constructor(private formBuilder: FormBuilder, public dataService: DataService) {
  }

  ngOnInit() {
    this.buttonDisabled = false;
    this.registerForm = this.formBuilder.group({
      username: ['', [Validators.required]],
      password: ['', [Validators.required]]
    });
  }




  onSubmit() {
    this.submitted = true;

    if (this.registerForm.invalid) {
      return;
    }

    console.log(this.registerForm.get('username').value);
    console.log(this.registerForm.get('password').value);

    this.dataService.logUser(this.registerForm.get('username').value,
      this.registerForm.get('password').value)
      .subscribe(data => {
        this.token = data; }
      );

    console.log('my token:' + this.token.token);

    this.dataService.getUserId(this.token)
    .subscribe(data => {
      this.userId = data;
    });

    console.log('my user id: ' + this.userId.id);
  }





}



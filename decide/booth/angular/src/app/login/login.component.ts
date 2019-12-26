import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { DataService } from '../data.service';
import { Token } from '@angular/compiler/src/ml_parser/lexer';
import { Observable } from 'rxjs';

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
  jsonToken: String;
  userId: Number;



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
        this.token = data;
        this.jsonToken = JSON.stringify(this.token);
      })
    console.log(this.jsonToken);

    this.dataService.getUserId(this.jsonToken)
    .subscribe(data => {
      this.userId = data;
      console.log(this.userId);
    })
  }





}



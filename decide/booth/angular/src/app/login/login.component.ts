import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { DataService } from '../data.service';
import { Observable } from 'rxjs';
import { Token, User } from '../voting.model';

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




  constructor(private formBuilder: FormBuilder, public dataService: DataService) {
  }

  ngOnInit() {
    this.buttonDisabled = false;
    this.registerForm = this.formBuilder.group({
      username: ['', [Validators.required]],
      password: ['', [Validators.required]]
    });
  }




  async onSubmit() {
    this.submitted = true;

    if (this.registerForm.invalid) {
      return;
    }

    const token = await this.dataService.logUser(this.registerForm.get('username').value, this.registerForm.get('password').value);
    const user = await this.dataService.getUserId(token);


    console.log('the username: ' + this.registerForm.get('username').value);
    console.log('the password: ' + this.registerForm.get('password').value);
    console.log('the token: ' + token.token);
    console.log('my user id: ' + user.id );
  }





}



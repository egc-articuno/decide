import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { DataService } from '../data.service';

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

    const tokenR = await this.dataService.logUser(this.registerForm.get('username').value, this.registerForm.get('password').value);
    const userR = await this.dataService.getUserId(tokenR);

    this.dataService.changeToken(tokenR.token);
    this.dataService.changeUserId(userR.id);

    console.log('the username: ' + this.registerForm.get('username').value);
    console.log('the password: ' + this.registerForm.get('password').value);
    console.log('the token: ' + tokenR.token);
    console.log('my user id: ' + userR.id );
  }

}



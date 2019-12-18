import { Component, OnInit } from '@angular/core';
import { FormGroup,  FormBuilder, Validators } from '@angular/forms';

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

  constructor(private formBuilder: FormBuilder) { }

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
  }


}



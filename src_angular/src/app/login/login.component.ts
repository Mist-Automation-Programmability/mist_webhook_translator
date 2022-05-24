import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { FormBuilder } from '@angular/forms';
import { ConnectorService } from '../connector.service';
import {PlatformLocation} from '@angular/common';
import { TwoFactorDialog } from './login-2FA';

export interface TwoFactorData {
  twoFactor: string;
}

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})


export class LoginComponent implements OnInit {

  constructor(private _formBuilder: FormBuilder, private _http: HttpClient, private _router: Router, private _appService: ConnectorService, public _dialog: MatDialog, private _platformLocation: PlatformLocation
    ) { }


  github_url: string;
  docker_url: string;
  disclaimer: string;
  host = null;
  headers = {};
  cookies = {};
  self = {};
  loading: boolean;
  hosts = [
    { value: 'api.mist.com', viewValue: 'US - manage.mist.com' },
    { value: 'api.eu.mist.com', viewValue: 'EU - manage.eu.mist.com' },
    { value: 'api.gc1.mist.com', viewValue: 'GCP - manage.gc1.mist.com' }
  ];

  // LOGIN FORM
  frmStepLogin = this._formBuilder.group({
    host: [''],
    credentials: this._formBuilder.group({
      email: [''],
      password: [''],
    }),
    token: [''],
  });
  error_mess = {
    "credentials": "",
    "token": ""
  }


  //// INIT ////
  ngOnInit(): void {
    this.frmStepLogin = this._formBuilder.group({
      host: ['api.mist.com'],
      credentials: this._formBuilder.group({
        email: [''],
        password: [''],
      }),
      token: [""],
    });
    this._http.get<any>('/api/gap').subscribe({
      next: data => this._appService.googleApiKeySet(data.gap),
      error: error => console.error("Unable to load the Google API Key... Maps won't be available...")      
    })
    this._http.get<any>("/api/disclaimer").subscribe({
      next: data => {
        if (data.disclaimer) this.disclaimer = data.disclaimer;
        if (data.github_url) this.github_url = data.github_url;
        if (data.docker_url) this.docker_url = data.docker_url;
      }
    })
  }

  //// COMMON ////
  check_host(): boolean {
    if (this.frmStepLogin.value.host != '') {
      return true;
    } else {
      return false;
    }
  }

  // RESET AUTHENTICATION FORM
  reset_response(): void {
    this.host = null;
    this._appService.headersSet({});
    this._appService.cookiesSet({});
    this._appService.selfSet({});
    this._appService.hostSet(this.host);
    this.reset_error_mess();
  }
  reset_error_mess(): void{
    this.error_mess = {
      "credentials": "",
      "token": ""
    }
  }

  // PARSE AUTHENTICATION RESPONSE FROM SERVER
  parse_response(data): void {
    if ("error" in data) {
      this.loading = false;
      this.error_mess["username"] = data.error;
    } else if ("data" in data) {
      if ("detail" in data.data) {
        this.error_message(data["method"], data.data.detail);
      } else if ("two_factor_required" in data.data && "two_factor_passed" in data.data) {
        if (data.data["two_factor_required"] == false) {
          this.authenticated(data)
        } else if (data.data["two_factor_passed"] == true) {
          this.authenticated(data)
        } else {
          this.open2FA()
        }
      } else {
        this.authenticated(data)
      }
    }
  }

  // WHEN AUTHENTICATION IS NOT OK
  error_message(method, message): void {
    this.loading = false;
    this.error_mess[method] = message;
  }


  // WHEN AUTHENTICATION IS OK
  authenticated(data): void {
    this._appService.headersSet(data.headers);
    this._appService.cookiesSet(data.cookies);
    this._appService.hostSet(data.host);
    this._appService.selfSet(data.data)
    this.loading = false; 
    this._router.navigate(['/select']);
  }

  //// AUTHENTICATION ////
  submitCredentials(): void {
    this.reset_response();
    if (this.check_host()) {
      this.loading = true;
      this._http.post<any>('/api/login/', { host: this.frmStepLogin.value.host, email: this.frmStepLogin.value.credentials.email, password: this.frmStepLogin.value.credentials.password }).subscribe({
        next: data => this.parse_response(data),
        error: error => this.error_message("credentials", error.error.message)      
      })
    }
  }
  submitToken(): void {
    this.reset_response();
    if (this.check_host()) {
      this.loading = true;
      this._http.post<any>('/api/login/', { host: this.frmStepLogin.value.host, token: this.frmStepLogin.value.token }).subscribe({
        next: data => this.parse_response(data),
        error: error => this.error_message("credentials", error.error.message)
      })
    }
  }
  submit2FA(twoFactor: number): void {
    if (this.check_host()) {
      this.loading = true;
      this._http.post<any>('/api/login/', { host: this.frmStepLogin.value.host, email: this.frmStepLogin.value.credentials.email, password: this.frmStepLogin.value.credentials.password, two_factor: twoFactor }).subscribe({
        next: data => this.parse_response(data),
        error: error => this.error_message("credentials", error.error.message)      
      })
    }
  }

  //// DIALOG BOX ////
  open2FA(): void {
    const dialogRef = this._dialog.open(TwoFactorDialog, {});
    dialogRef.afterClosed().subscribe(result => {
      this.submit2FA(result)
    });
  }
}
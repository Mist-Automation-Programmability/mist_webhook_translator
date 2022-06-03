import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { FormBuilder } from '@angular/forms';
import { SessionService } from '../services/session.service'

export interface Org {
  id: string;
  name: string;
  //role: string;
}

@Component({
  selector: 'app-org',
  templateUrl: './org.component.html',
  styleUrls: ['./org.component.css']
})
export class OrgComponent implements OnInit {

  constructor(
    private _http: HttpClient,
    private _router: Router,
    private _sessionService: SessionService
  ) { }

  self;
  org_id: string = "";
  orgs: Org[] = [];
  loading: boolean = false;
  error_mess: string = "";

  ngOnInit(): void {
    this.loadOrgs()
  }



  //// LOAD ORGS ////
  loadOrgs(): void {
    this.orgs = []
    this.loading = true;
    this._http.get<any>('/api/orgs').subscribe({
      next: data => {
        this.orgs = data;
        this.loading = false;
      },
      error: error => this.error_message(error)
    })
  }

  submitOrg(): void {
    this._router.navigate(['/config/'+this.org_id]);
  }


  // WHEN AUTHENTICATION IS NOT OK
  error_message(data): void {
    this.loading = false;
    if (data.status == "401") {
      this._router.navigate(["/"])
    }
    this.error_mess = data.error;
  }



  //////////////////////////////////////////////////////////////////////////////
  /////           Logout
  //////////////////////////////////////////////////////////////////////////////
  // WHEN AUTHENTICATION IS NOT OK
  parseError(message: any): void {
    this.loading = false;
    this.error_message = message.detail;
  }
  logout(): void {
    this._http.post<any>("/api/logout", {}).subscribe({
      next: data => {
        this._router.navigate(["/"])
          .catch(console.error)
          .then(() => window.location.reload());
      },
      error: error => this.parseError(error)
    })
  }
}



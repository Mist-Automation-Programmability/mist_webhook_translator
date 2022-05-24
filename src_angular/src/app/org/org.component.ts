import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { ConnectorService } from '../connector.service';
import { MatDialog } from '@angular/material/dialog';
import { ErrorDialog } from './../common/common-error';
import { Router } from '@angular/router';

@Component({
  selector: 'app-org',
  templateUrl: './org.component.html',
  styleUrls: ['./org.component.css']
})
export class OrgComponent implements OnInit {

  headers = {};
  cookies = {};
  host = '';
  self = {};
  search = "";
  orgs = [];
  sites = [];
  orgMode: boolean = false;
  selected_org_obj = {
    id: "",
    name: ""
  };
  org_id: string = "";
  site_id: string = "";
  me: string = "";
  adminMode: boolean = false;
  map = {
    options: {
      scrollwheel: false,
      disableDefaultUI: true,
      draggable: false,
      draggableCursor: "pointer",
      clickableIcons: false
    },
    zoom: 12
  }

  apiLoaded: Observable<boolean>;
  claimDisabled: boolean = true;
  topBarLoading = false;
  noSiteToDisplay = false;
  constructor(private _http: HttpClient, private _appService: ConnectorService, public _dialog: MatDialog, private _router: Router) { }


  ngOnInit() {
    this._appService.headers.subscribe(headers => this.headers = headers)
    this._appService.cookies.subscribe(cookies => this.cookies = cookies)
    this._appService.host.subscribe(host => this.host = host)
    this._appService.self.subscribe(self => this.self = self || {})
    this._appService.org_id.subscribe(org_id => this.org_id = org_id)
    this.me = this.self["email"] || null

    var tmp_orgs: string[] = []

    // parsing all the orgs/sites from the privileges
    // only orgs with admin/write/installer roles are used
    if (this.self != {} && this.self["privileges"]) {
      this.self["privileges"].forEach(element => {
        if (element["role"] == "admin" || element["role"] == "write") {
          if (element["scope"] == "org") {
            if (tmp_orgs.indexOf(element["org_id"]) < 0) {
              this.orgs.push({ id: element["org_id"], name: element["name"], role: element["role"] })
              tmp_orgs.push(element["org_id"])
            }
          } else if (element["scope"] == "site") {
            if (tmp_orgs.indexOf(element["org_id"]) < 0) {
              this.orgs.push({ id: element["org_id"], name: element["org_name"], role: element["role"] })
              tmp_orgs.push(element["org_id"])
            }
          }
        }
      });
      this.orgs = this.sortList(this.orgs, "name");
    }

    // if only one, using it by default
    if (!this.org_id && this.orgs.length == 1) {
      this.org_id = this.orgs[1]["id"]
    }
    // if back button used, retrieving previously selected org
    // or if only one org, loading it automatically
    if (this.org_id) {
      this.orgs.forEach(element => {
        if (element.id == this.org_id) {
          this.selected_org_obj = element;
          this.changeOrg();
        }
      })
    }
  }

  // when the user selects a new org
  // disabling the admin mode
  // and loading the sites
  changeOrg() {
    this.loadSites();
  }

  // loads the org sites
  loadSites() {
    this.org_id = this.selected_org_obj.id
    this.topBarLoading = true;
    this.claimDisabled = true;
    this.sites = [];
    this._http.post<any>('/api/sites/', { host: this.host, cookies: this.cookies, headers: this.headers, org_id: this.org_id}).subscribe({
      next: data => this.parseSites(data),
      error: error => {
        var message: string = "There was an error... "
        if ("error" in error) {
          message += error["error"]["message"]
        }
        this.topBarLoading = false;
        this.openError(message)
      }
    })
  }

  // parse the org sites from HTTP response
  parseSites(data) {
    if (data.sites.length > 0) {
      this.noSiteToDisplay = false;
      this.sites = this.sortList(data.sites, "name");
      this.claimDisabled = false;
    } else {
      this.noSiteToDisplay = true;
    }
    this.topBarLoading = false;
  }




  // ROUTING FUNCTION
  // used when user wants to claim devices to org
  setOrg(): void {
    this.orgMode = true;
    this.gotoDash();    
  }
  // used when user wants to claim devices to site
  setSite(site): void {
    if (site != null) {
      this.site_id = site.id;
    } else {
      this.site_id = "";
    }
    this.orgMode = true;
    this._appService.siteIdSet(this.site_id);
    this.gotoDash();
  }
  // publish variables and go to the dashboard
  gotoDash(): void {    
    this._appService.orgModeSet(this.orgMode)
    this._appService.orgIdSet(this.org_id);
    this._router.navigate(["/dashboard"]);
  }


  // COMMON
  sortList(data, attribute) {
    return data.sort(function (a, b) {
      var nameA = a[attribute].toUpperCase(); // ignore upper and lowercase
      var nameB = b[attribute].toUpperCase(); // ignore upper and lowercase
      if (nameA < nameB) {
        return -1;
      }
      if (nameA > nameB) {
        return 1;
      }
      return 0;
    })
  }

  // DIALOG BOXES
  // ERROR
  openError(message: string): void {
    const dialogRef = this._dialog.open(ErrorDialog, {
      data: message
    });
  }
}

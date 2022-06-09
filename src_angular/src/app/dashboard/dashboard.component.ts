import { Component, OnInit, ViewChild } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { HttpClient } from '@angular/common/http';
import { Router, ActivatedRoute } from "@angular/router";
import { MatPaginator } from '@angular/material/paginator';
import { MatTableDataSource } from '@angular/material/table';
import { MatChipInputEvent } from '@angular/material/chips';
import { C, COMMA, ENTER, SEMICOLON } from '@angular/cdk/keycodes';
import { FormControl } from '@angular/forms';

import { MatSnackBar } from '@angular/material/snack-bar';


import { ErrorDialog } from '../common/common-error';
import { SessionService } from '../services/session.service';
import { WarningDialog } from '../common/common-warning';

export interface TopicElement {
  topic: string,
  sub_topic: string,
  name: string,
  channel: string
}

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})


export class DashboardComponent implements OnInit {
  @ViewChild(MatPaginator) paginator: MatPaginator;

  separatorKeysCodes: number[] = [ENTER, COMMA, SEMICOLON];
  approvedAdminsCtrl = new FormControl();

  displayedColumns: string[] = ['sub_topic', 'name', 'channel'];
  dataSource = new MatTableDataSource<TopicElement>();

  headers = {};
  cookies = {};
  url = '';
  self = {};

  org_id: string = "";
  org_name: string = "__any__";
  me: string = "";

  mist_configured: boolean = false;
  mist_updated: boolean = false;
  mist_enabled: boolean = false;
  slack_configured: boolean = false;
  slack_updated: boolean = false;
  teams_configured: boolean = false;
  teams_updated: boolean = false;
  topics_configured: boolean = false;
  topics_updated: boolean = false;

  selected_topic: string = ""
  topics: string[] = [];
  channels: string[] = [];

  default_topics: TopicElement[] = [];
  custom_settings = {
    channels: [],
    topics_status: {},
    topics: [],
    slack_settings: {
      enabled: false,
      url: {}
    },
    teams_settings: {
      enabled: false,
      url: {}
    },
    mist_settings: {
      approved_admins: []
    }
  }


  // LOADINBG INDICATORS
  mist_in_progress: boolean = true;
  topics_in_progress: boolean = true;
  notif_in_progress: boolean = true;
  loading_in_progress: boolean = false;



  constructor(
    private _http: HttpClient,
    private _sessionService: SessionService,
    public _dialog: MatDialog,
    private _snackBar: MatSnackBar,
    private _router: Router,
    private _activatedRoute: ActivatedRoute
  ) { }

  //////////////////////////////////////////////////////////////////////////////
  /////           INIT
  //////////////////////////////////////////////////////////////////////////////

  ngOnInit() {
    this._sessionService.self.subscribe(self => this.self = self || {})
    this._activatedRoute.params.forEach(p => this.org_id = p["org_id"])

    if (!this.self) this._router.navigate(["/login"]);
    else if (!this.org_id) this._router.navigate(["/select"]);
    else {
      this.getOrgSettings();
      this.getOrgWebhook();
    }
  }


  //////////////////////////////////////////////////////////////////////////////
  /////           COMMON
  //////////////////////////////////////////////////////////////////////////////
  parseError(error: any): void {
    if (error.status == "401") this.notAuthenticated()
    else if (error.status == "403") this._router.navigate(["/select"])
    else {
      var message: string = "Unable to contact the server... Please try again later... "
      if (error.error && error.error.message) message = error.error.message
      else if (error.error) message = error.error
      this.openSnackBar(message, "OK")
    }
  }

  //////////////////////////////////////////////////////////////////////////////
  /////           MIST WEBHOOK CONFIGURATION
  //////////////////////////////////////////////////////////////////////////////
  parseOrgWebhook(data: {}): void {
    this.mist_in_progress = false;
    if (data && data['url'] == this.url) {
      this.mist_configured = true;
      this.mist_updated = false;
      this.mist_enabled = data["enabled"];
      this.topics.forEach(topic => {
        if (!data["topics"].includes(topic)) this.mist_updated = true;
      })
    }
  }

  getOrgWebhook(): void {
    this._http.get("/api/orgs/webhook/" + this.org_id).subscribe({
      next: data => this.parseOrgWebhook(data),
      error: error => this.parseError(error)
    })
  }

  configureOrgWebhook(): void {
    var data: string[] = []
    for (const topic in this.custom_settings.topics_status) {
      if (this.custom_settings.topics_status[topic]) data.push(topic)
    }
    this._http.post("/api/orgs/webhook/" + this.org_id, { topics: data }).subscribe({
      next: data => this.parseOrgWebhook(data),
      error: error => {
        this.mist_in_progress = false;
        this.parseError(error)
      }
    })
  }
  //////////////////////////////////////////////////////////////////////////////
  /////           GET SETTINGS
  //////////////////////////////////////////////////////////////////////////////

  parseOrgSettings(data: {}): void {
    if (this.org_id == data["org_id"]) {
      this.notif_in_progress = false;
      this.topics_in_progress = false;

      this.org_name = data["org_name"];
      this.default_topics = data["default_topics"];
      this.custom_settings = data["settings"];
      this.url = data["url"];

      if (Object.keys(this.custom_settings.slack_settings).length) this.slack_configured = true;
      else this.custom_settings.slack_settings = { enabled: false, url: {} }
      if (Object.keys(this.custom_settings.teams_settings).length) this.teams_configured = true;
      else this.custom_settings.teams_settings = { enabled: false, url: {} }
      if (Object.keys(this.custom_settings.topics).length) this.topics_configured = true;

      this.custom_settings["topics"] = this.parseTopics(this.default_topics, this.custom_settings["topics"]);

    } else { this.openError("Issue when getting the settings from the server...") }
  }

  getOrgSettings(): void {
    this._http.get("/api/orgs/settings/" + this.org_id).subscribe({
      next: data => this.parseOrgSettings(data),
      error: error => this.parseError(error)
    })
  }

  //////////////////////////////////////////////////////////////////////////////
  /////           ORG SETTINGS
  //////////////////////////////////////////////////////////////////////////////
  saveOrgSettings(): void {
    this.notif_in_progress = true;
    this.topics_in_progress = true;
    this.mist_in_progress = true;
    this._http.post('/api/orgs/settings/' + this.org_id, this.custom_settings).subscribe({
      next: data => {
        this.topics_updated = false;
        this.slack_updated = false;
        this.teams_updated = false;
        this.notif_in_progress = false;
        this.topics_in_progress = false;
        this.configureOrgWebhook();
      },
      error: error => {
        this.notif_in_progress = false;
        this.topics_in_progress = false;
        this.parseError(error)
      }
    })
  }

  deleteOrgSettings(): void {
    this._http.delete("/api/orgs/settings/" + this.org_id).subscribe({
      next: data => this._router.navigate(["/select"]),
      error: error => this.parseError(error)
    })
  }

  //////////////////////////////////////////////////////////////////////////////
  /////           NOTIFICATIONS
  //////////////////////////////////////////////////////////////////////////////
  toggleNotif(notif: string, new_status: boolean): void {
    switch (notif) {
      case "slack":
        this.custom_settings.slack_settings.enabled = new_status;
        this.slack_configured = true;
        this.slack_updated = true;
        break;
      case "teams":
        this.custom_settings.teams_settings.enabled = new_status;
        this.teams_configured = true;
        this.teams_updated = true;
        break;
    }
  }

  updateNotifUrl(notif: string, channel: string, e: any): void {
    const names = {
      "slack": { "settings": "slack_settings", "update": "slack_updated" },
      "teams": { "settings": "teams_settings", "update": "teams_updated" }
    }

    const notif_settings = this.custom_settings[names[notif]["settings"]];
    if (notif_settings.url[channel] != e.target.value) {
      notif_settings.url[channel] = e.target.value;
      this[names[notif]["update"]] = true;

      if (channel == "default") {
        for (const chan in notif_settings.url) {
          if (!notif_settings.url[chan]) notif_settings.url[chan] = e.target.value
        }
      }
    }

  }
  //////////////////////////////////////////////////////////////////////////////
  /////           PROCESS TOPICS
  //////////////////////////////////////////////////////////////////////////////

  parseTopics(default_topics: TopicElement[], configured_topics: {}): any[] {
    var custom_topics = [];
    if (Object.keys(configured_topics).length) {
      // reformat the topic list
      for (const topic in configured_topics) {
        for (const event in configured_topics[topic]) {
          const tmp = default_topics.filter(t => t.name == event && t.topic == topic)[0];
          var sub_topic = "";
          if (tmp) sub_topic = tmp["sub_topic"]
          const data = custom_topics.push({
            "topic": topic,
            "sub_topic": sub_topic,
            "name": event,
            "channel": configured_topics[topic][event]
          })
        }
      }
      // compare the default topics and the customer topics to find missing ones
      const missing_topics = default_topics.filter(({ name: id1 }) => !custom_topics.some(({ name: id2 }) => id2 === id1));
      missing_topics.forEach(topic => {
        topic["new"] = true;
        custom_topics.push(topic);
      })
    } else {
      custom_topics = default_topics;
    }
    // extract the list of channels from custom topics
    this.channels = ["default", "critical", "warning", "info", "debug"];
    this.channels.forEach(channel => {
      if (!this.custom_settings.teams_settings.url[channel]) this.custom_settings.teams_settings.url[channel] = "";
      if (!this.custom_settings.slack_settings.url[channel]) this.custom_settings.slack_settings.url[channel] = "";
    })
    custom_topics.forEach(topic => {
      if (topic.channel && !this.channels.includes(topic.channel)) {
        this.channels.push(topic.channel);
        if (!this.custom_settings.teams_settings.url[topic.channel]) this.custom_settings.teams_settings.url[topic.channel] = "";
        if (!this.custom_settings.slack_settings.url[topic.channel]) this.custom_settings.slack_settings.url[topic.channel] = "";
      }
    })

    // extract the list of topicvs
    this.topics = [];
    default_topics.forEach(topic => {
      if (!this.topics.includes(topic.topic) && this.custom_settings.topics_status[topic.topic]) this.topics.push(topic.topic);
    })

    return custom_topics;
  }

  changeTopic(): void {
    this.dataSource = new MatTableDataSource<TopicElement>(this.custom_settings.topics.filter(t => t.topic == this.selected_topic));
    setTimeout(() => this.dataSource.paginator = this.paginator);
    console.log(this.dataSource.paginator)
  }

  toggleTopic(topic: string, new_status: boolean): void {
    this.custom_settings.topics_status[topic] = new_status;
    this.topics_configured = true;
    this.topics_updated = true;
    if (new_status) {
      this.topics.push(topic)
      this.selected_topic = topic;
    } else {
      this.topics.splice(this.topics.indexOf(topic), 1);
      this.selected_topic = undefined;
    }
    this.mist_updated = true;
    this.changeTopic();
  }

  topicsUpdated(): void {
    this.topics_configured = true;
    this.topics_updated = true;
  }

  //////////////////////////////////////////////////////////////////////////////
  /////           APPROVED ADMINS
  //////////////////////////////////////////////////////////////////////////////
  add(event: MatChipInputEvent): void {
    const value = (event.value || '').trim();
    console.log(this.custom_settings)
    if (value) {
      this.custom_settings.mist_settings.approved_admins.push(value);
    }
    // Clear the input value
    event.chipInput!.clear();
    this.approvedAdminsCtrl.setValue(null);

    this.topics_updated = true;
  }

  remove(fruit: string): void {
    const index = this.custom_settings.mist_settings.approved_admins.indexOf(fruit);

    if (index >= 0) {
      this.custom_settings.mist_settings.approved_admins.splice(index, 1);
    }
    
    this.topics_updated = true;
  }
  //////////////////////////////////////////////////////////////////////////////
  /////           NAV
  //////////////////////////////////////////////////////////////////////////////
  backToOrgs(): void {
    this._router.navigate(["/select"]);
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

  //////////////////////////////////////////////////////////////////////////////
  /////           DIALOG BOXES
  //////////////////////////////////////////////////////////////////////////////

  openNewTab(url: string): void {
    window.open(url, "_blank");
  }
  // ERROR
  openError(message: string): void {
    const dialogRef = this._dialog.open(ErrorDialog, {
      data: message
    });
  }

  openWarning(message: string, cb): void {
    const dialogRef = this._dialog.open(WarningDialog, {
      data: message
    });
    dialogRef.afterClosed().subscribe(result => {
      cb(result);
    });
  }

  notAuthenticated(): void {
    this._router.navigate(["/"]);
  }

  // SNACK BAR
  openSnackBar(message: string, action: string) {
    this._snackBar.open(message, action, {
      duration: 5000,
      horizontalPosition: "center",
      verticalPosition: "top",
    });
  }
}



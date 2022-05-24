import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ConnectorService {
  private headersSource = new BehaviorSubject({});
  private cookiesSource = new BehaviorSubject({});
  private hostSource = new BehaviorSubject('');
  private selfSource = new BehaviorSubject({});
  private orgIdSource = new BehaviorSubject("");
  private siteIdSource = new BehaviorSubject("");
  private orgModeSource = new BehaviorSubject(false);
  private googleApiKey = new BehaviorSubject("");

  headers = this.headersSource.asObservable();
  host = this.hostSource.asObservable();
  cookies = this.cookiesSource.asObservable();
  self = this.selfSource.asObservable();
  org_id = this.orgIdSource.asObservable();
  site_id = this.siteIdSource.asObservable();
  orgMode = this.orgModeSource.asObservable();
  google_api_key = this.googleApiKey.asObservable();

  constructor() { }

  headersSet(data: {}) {
    this.headersSource.next(data)
  }
  cookiesSet(data: {}) {
    this.cookiesSource.next(data)
  }
  hostSet(data: string) {
    this.hostSource.next(data)
  }
  selfSet(data: {}) {
    this.selfSource.next(data)
  }
  orgIdSet(data: string){
    this.orgIdSource.next(data)
  }
  siteIdSet(data:string){
    this.siteIdSource.next(data)
  }
  orgModeSet(data:boolean){
    this.orgModeSource.next(data)
  }
  googleApiKeySet(data:string){
    this.googleApiKey.next(data)
  }
}

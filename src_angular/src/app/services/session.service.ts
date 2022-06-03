import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SessionService {
  private selfSource = new BehaviorSubject({});
  private orgIdSource = new BehaviorSubject("");
  private orgNameSource = new BehaviorSubject("");

  self = this.selfSource.asObservable();
  org_id = this.orgIdSource.asObservable();
  org_name = this.orgNameSource.asObservable();

  constructor() { }

  selfSet(data: {}) {
    this.selfSource.next(data)
  }
  orgIdSet(data: string) {
    this.orgIdSource.next(data)
  }
  orgNameSet(data: string) {
    this.orgNameSource.next(data)
  }
 
}

import { Component, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';

export interface DeviceElement {
    mac: string;
    model: string;
    serial: string;
    connected: boolean;
    type: string;  
    deviceprofile_name: string;
    height: Int16Array;
    map_id: string;
    name: string;
    orientation: Int16Array;
    site_id: string;
    site_name: string;
    x:Int16Array;
    y: Int16Array;
  }

@Component({
    selector: 'common-unclaim',
    templateUrl: 'common-unclaim.html',
})
export class UnclaimDialog {

    constructor(
        public dialogRef: MatDialogRef<UnclaimDialog>,
        @Inject(MAT_DIALOG_DATA) public data: DeviceElement
    ) { }

    confirm(device_mac) {
        this.dialogRef.close(device_mac)
    }
    cancel(): void {
        this.dialogRef.close();
    }

}
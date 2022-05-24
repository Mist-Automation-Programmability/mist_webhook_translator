import { Component, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';

export interface WarningData {
    text: string,
    vlan_check: [""],
    bigWarning: boolean
}

@Component({
    selector: 'common-warning',
    templateUrl: 'common-warning.html',
})
export class WarningDialog {

    constructor(
        public dialogRef: MatDialogRef<WarningDialog>,
        @Inject(MAT_DIALOG_DATA) public data: WarningData
    ) { }
    ok(): void {
        this.dialogRef.close(true);
    }
    cancel(): void {
        this.dialogRef.close();
    }

}
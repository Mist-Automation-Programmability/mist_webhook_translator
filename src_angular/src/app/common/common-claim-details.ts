import { Component, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';

@Component({
    selector: 'common-claim-details',
    templateUrl: 'common-claim-details.html',
})
export class ClaimDetailsDialog {
    constructor(
        public dialogRef: MatDialogRef<ClaimDetailsDialog>, @Inject(MAT_DIALOG_DATA) public data) { }
    details = this.data;
    
    ngOnInit(){
        console.log(this.details)
    }
    cancel(): void {
        this.dialogRef.close();
    }
}
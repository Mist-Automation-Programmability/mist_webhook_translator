import { Component, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';

interface DataElement {
    message: string[],
    color: string
}

@Component({
    selector: 'common-warning',
    templateUrl: 'common-warning.html',
})
export class WarningDialog {
    constructor(
        public dialogRef: MatDialogRef<WarningDialog>,
        @Inject(MAT_DIALOG_DATA) public data: DataElement
    ) { }

    
    ok(): void {
        this.dialogRef.close(true);
    }
    cancel(): void {
        this.dialogRef.close();
    }

}
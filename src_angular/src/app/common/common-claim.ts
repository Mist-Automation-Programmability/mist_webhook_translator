import { Component, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA, MatDialog } from '@angular/material/dialog';
import { HttpClient } from '@angular/common/http';
import { ErrorDialog } from './common-error';
import { ClaimDetailsDialog } from './common-claim-details'

export interface ClaimCodeElement {
    code: string;
    duplicated: boolean;
    valid: boolean;
    success: boolean;
    reason: string;
    processed: boolean;
}

@Component({
    selector: 'common-claim',
    templateUrl: 'common-claim.html',
})
export class ClaimDialog {
    constructor(
        public dialogRef: MatDialogRef<ClaimDialog>, private _http: HttpClient, public _dialog: MatDialog, @Inject(MAT_DIALOG_DATA) public data) { }
    claimCodes: ClaimCodeElement[] = [];
    claimButtonDisabled: boolean = true;
    inputClaimCodes: string = "";
    body = this.data.body;
    isDone = false;
    claimResult = {};
    isWorking = false;

    add(): void {
        var regex = /^[0-9a-zA-Z]{5}-?[0-9a-zA-Z]{5}-?[0-9a-zA-Z]{5}$/i;
        this.inputClaimCodes.split(/[\s,; ]+/).forEach(element => {
            var claim = element.replace(";", "").replace(",", "").trim().toUpperCase();
            if (claim.length > 0) {
                var newClaim = { code: claim, success: null, reason: null, duplicated: false, valid: false, processed: false };
                if (newClaim.code.match(regex)) {
                    newClaim.valid = true;
                }
                this.claimCodes.forEach(element => {
                    if (element.code == newClaim.code) {
                        element.duplicated = true;
                        newClaim.duplicated = true;
                    }
                })
                this.claimCodes.push(newClaim);
            }
        })
        this.check_issues();
        this.inputClaimCodes = "";
    }

    edit(claimCode: ClaimCodeElement): void {
        this.inputClaimCodes = claimCode.code;
        var index = this.claimCodes.indexOf(claimCode)
        this.claimCodes.splice(index, 1)
    }

    check_issues(): void {
        var issues = {
            invalid: [],
            duplicated: []
        };
        this.claimCodes.forEach(element => {
            if (element.valid == false) {
                issues.invalid.push(element.code);
            }
            if (element.duplicated == true) {
                issues.duplicated.push(element.code);
            }
        })
        if (this.claimCodes.length > 0 && issues.duplicated.length == 0 && issues.invalid.length == 0) {
            this.claimButtonDisabled = false;
        } else {
            this.claimButtonDisabled = true;
        }
    }

    remove(claimCode: ClaimCodeElement): void {
        var duplicated_codes = [];
        var index = -1;
        // remove the claim code
        index = this.claimCodes.indexOf(claimCode);
        if (index >= 0) {
            this.claimCodes.splice(index, 1);
        }
        // if the removed claim code has the duplicated flag
        if (claimCode.duplicated) {
            // find other same codes
            this.claimCodes.forEach(element => {
                if (element.code == claimCode.code) {
                    duplicated_codes.push(element);
                }
            })
            // if only one other same code, remove the duplicated flash
            if (duplicated_codes.length == 1) {
                index = this.claimCodes.indexOf(duplicated_codes[0]);
                this.claimCodes[index].duplicated = false;
            }
        }
        // check issues for "claim" button
        this.check_issues()
    }

    // CLAIM NEW CODES
    confirm(): void {
        this.isWorking = true;
        this.isDone = true;
        // Add claim codes to request body
        this.body.claim_codes = [];
        this.claimCodes.forEach(element => {
            this.body.claim_codes.push(element.code)
        })
        // Send request to server
        this._http.post<any>('/api/devices/claim/', this.body).subscribe({
            next: data => {
                // retrieve result data
                this.claimResult = data.results;
                this.claimCodes.forEach(element => {
                    element.processed = true;
                    var index = -1;
                    // if code added to account
                    if (this.claimResult["added"].indexOf(element.code) >= 0) {
                        element.success = true;
                        // if error when adding the code
                    } else if (this.claimResult["error"].indexOf(element.code) >= 0) {
                        index = this.claimResult["error"].indexOf(element.code);
                        element.success = false;
                        element.reason = this.claimResult["reason"][index]
                        // if code already claimed somewhere
                    } else if (this.claimResult["duplicated"].indexOf(element.code) >= 0) {
                        element.success = false;
                        element.reason = "Already Claimed"
                    }
                })
                this.isWorking = false;
            },
            error: error => {
                var message: string = "Unable to create claim the devices... "
                if ("error" in error) { message += error["error"]["message"] }
                this.openError(message)
                this.isWorking = false;
            }
        })
    }


    // EXIT
    cancel(): void {
        this.dialogRef.close();
    }
    // DIALOG BOXES
    // Restart Claim Process
    reset(): void {
        const dialogRef = this._dialog.open(ClaimDialog, {
            data: { body: this.body }
        })
        dialogRef.afterClosed().subscribe(result => {
            this.dialogRef.close();
        })
    }
    // DETAILS
    details(): void {
        console.log(this.claimResult);
        const dialogRef = this._dialog.open(ClaimDetailsDialog, {
            data: this.claimResult
        })

    }
    // ERROR
    openError(message: string): void {
        const dialogRef = this._dialog.open(ErrorDialog, {
            data: message
        });
    }


}




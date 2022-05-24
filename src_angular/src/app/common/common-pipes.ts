import { Pipe, PipeTransform } from '@angular/core';

@Pipe({ name: 'startsWith' })
export class StartsWithPipe implements PipeTransform {
    transform(fullText: string, textMatch: string): boolean {
        return fullText.startsWith(textMatch);
    }
}

@Pipe({ name: 'mapToArray' })
export class MapToArrayPipe implements PipeTransform {
    transform(value, args: string[]): any {
        let arr = [];
        for (let key in value) {
            arr.push({ key: key, value: value[key] });
        }
        return arr;
    }
}
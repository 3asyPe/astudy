import { Time } from '@angular/common';

export class CategoryCourse {
    constructor(
        public slug: string,
        public image: string,
        public title: string,
        public subtitle: string,
        public price: number,
        public lectures_count: number,
        public duration_time: Time,
    ) { }
}
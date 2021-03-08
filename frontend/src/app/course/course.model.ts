import { Time } from "@angular/common";

export class Course {
    constructor(
        public slug: string,
        public category: number,
        public image: string,
        public title: string,
        public subtitle: string,
        public price: number,
        public description: string,
        public students_count: number,
        public lectures_count: number,
        public duration_time: Time,
        public goals: {goal: string}[],
        public requirements: {requirement: string}[],
    ) { }
}
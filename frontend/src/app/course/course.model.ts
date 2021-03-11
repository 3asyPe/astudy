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
        public goals: {goal: string}[],
        public requirements: {requirement: string}[],
        public content: {
            sections_count: number,
            lectures_count: number,
            articles_count: number,
            resources_count: number,
            assignments_count: number,
            duration_time: Time,
            sections: {
                title: string,
                lectures_count: number,
                duration_time: Time,
                lectures: {
                    free_opened: boolean,
                    title: string,
                    description: string|null,
                    duration_time: {
                        hours: number,
                        minutes: number,
                        seconds: number
                    }
                }[]
            }[]
        }
    ) { }
}
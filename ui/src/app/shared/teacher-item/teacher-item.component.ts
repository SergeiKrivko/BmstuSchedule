import {Component, inject, Input} from '@angular/core';
import {Teacher} from "../../core/models/teacher";
import {NgIf} from "@angular/common";
import {Router, RouterLink} from "@angular/router";
import {ScheduleService} from "../../core/schedule.service";

@Component({
  selector: 'app-teacher-item',
  standalone: true,
  imports: [
    NgIf,
    RouterLink
  ],
  templateUrl: './teacher-item.component.html',
  styleUrl: './teacher-item.component.scss'
})
export class TeacherItemComponent {
  @Input() teacher: Teacher | undefined;

  private readonly scheduleService = inject(ScheduleService);
  private readonly router = inject(Router);

  onSelected() {
    if (this.teacher) {
      this.scheduleService.setTeacher(this.teacher);
      void this.router.navigate(['/pairs']);
    }
  }
}

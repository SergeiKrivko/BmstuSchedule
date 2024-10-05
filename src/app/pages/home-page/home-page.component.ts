import {ChangeDetectionStrategy, Component, inject} from '@angular/core';
import {InputTextModule} from "primeng/inputtext";
import {AsyncPipe} from "@angular/common";
import {CardModule} from "primeng/card";
import {DropdownModule} from "primeng/dropdown";
import {PaginatorModule} from "primeng/paginator";
import {PairItemComponent} from "../../shared/pair-item/pair-item.component";
import {FormControl, ReactiveFormsModule} from "@angular/forms";
import {ScheduleService} from "../../core/schedule.service";
import {TeacherItemComponent} from "../../shared/teacher-item/teacher-item.component";

@Component({
  selector: 'app-home-page',
  standalone: true,
  imports: [
    InputTextModule,
    AsyncPipe,
    CardModule,
    DropdownModule,
    PaginatorModule,
    PairItemComponent,
    ReactiveFormsModule,
    TeacherItemComponent
  ],
  templateUrl: './home-page.component.html',
  styleUrl: './home-page.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class HomePageComponent {
  private readonly scheduleService = inject(ScheduleService);
  protected readonly teachers$ = this.scheduleService.teachers$;

  protected readonly lastNameControl = new FormControl<string>('');

  onLastNameChanged() {
    console.log("Last name changed")
    if (this.lastNameControl.value) {
      this.scheduleService.loadTeachers(this.lastNameControl.value).subscribe()
    }
  }
}

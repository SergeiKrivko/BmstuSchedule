import {ChangeDetectionStrategy, Component, inject, OnInit} from '@angular/core';
import {DropdownModule} from "primeng/dropdown";
import {ScheduleService} from "../../core/schedule.service";
import {Teacher} from "../../core/models/teacher";
import {FormControl, FormGroup, ReactiveFormsModule} from "@angular/forms";
import {CardModule} from "primeng/card";
import {tap} from "rxjs";
import {AsyncPipe} from "@angular/common";
import {PairItemComponent} from "../../shared/pair-item/pair-item.component";
import {RouterLink} from "@angular/router";

@Component({
  selector: 'app-pairs-page',
  standalone: true,
  imports: [
    DropdownModule,
    ReactiveFormsModule,
    CardModule,
    AsyncPipe,
    PairItemComponent,
    RouterLink,
  ],
  templateUrl: './pairs-page.component.html',
  styleUrl: './pairs-page.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class PairsPageComponent implements OnInit {

  private readonly scheduleService = inject(ScheduleService);

  protected readonly formGroup = new FormGroup({
    teacher: new FormControl<Teacher | null>(null),
  })
  protected readonly pairs$ = this.scheduleService.pairs$;
  protected currentTeacher: Teacher | null = null;

  ngOnInit() {
    this.scheduleService.currentTeacher$.pipe(
      tap(currentTeacher => this.currentTeacher = currentTeacher)
    ).subscribe();
    // this.formGroup.get('teacher')?.valueChanges.pipe(
    //   tap(teacher => this.scheduleService.setTeacher(teacher?.id ?? null))
    // ).subscribe()
    // this.scheduleService.currentTeacher$.subscribe(teacher => console.log(`Current teacher ${teacher}`));
  }

}

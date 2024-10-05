import {Component, inject, OnInit} from '@angular/core';
import {DropdownModule} from "primeng/dropdown";
import {ScheduleService} from "../../core/schedule.service";
import {Teacher} from "../../core/models/teacher";
import {FormControl, FormGroup, ReactiveFormsModule} from "@angular/forms";
import {BrowserAnimationsModule} from "@angular/platform-browser/animations";
import {BrowserModule} from "@angular/platform-browser";
import {CardModule} from "primeng/card";
import {EMPTY, switchMap, tap} from "rxjs";
import {AsyncPipe} from "@angular/common";
import {PairItemComponent} from "../../shared/pair-item/pair-item.component";

@Component({
  selector: 'app-home-page',
  standalone: true,
  imports: [
    DropdownModule,
    ReactiveFormsModule,
    CardModule,
    AsyncPipe,
    PairItemComponent,
  ],
  templateUrl: './home-page.component.html',
  styleUrl: './home-page.component.scss'
})
export class HomePageComponent implements OnInit {

  private readonly scheduleService = inject(ScheduleService);

  protected teachers: Teacher[] = [];
  protected readonly formGroup = new FormGroup({
    teacher: new FormControl<Teacher | null>(null),
  })
  protected readonly pairs$ = this.scheduleService.pairs$;

  ngOnInit() {
    this.scheduleService.loadTeachers().subscribe(teachers => this.teachers = teachers);
    this.formGroup.get('teacher')?.valueChanges.pipe(
      tap(teacher => this.scheduleService.setTeacher(teacher?.id ?? null))
    ).subscribe()
    // this.scheduleService.currentTeacher$.subscribe(teacher => console.log(`Current teacher ${teacher}`));
  }

}

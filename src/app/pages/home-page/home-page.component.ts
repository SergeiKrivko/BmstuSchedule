import {ChangeDetectionStrategy, ChangeDetectorRef, Component, DestroyRef, inject, OnInit} from '@angular/core';
import {InputTextModule} from "primeng/inputtext";
import {AsyncPipe} from "@angular/common";
import {CardModule} from "primeng/card";
import {DropdownModule} from "primeng/dropdown";
import {PaginatorModule} from "primeng/paginator";
import {PairItemComponent} from "../../shared/pair-item/pair-item.component";
import {FormControl, ReactiveFormsModule} from "@angular/forms";
import {ScheduleService} from "../../core/schedule.service";
import {TeacherItemComponent} from "../../shared/teacher-item/teacher-item.component";
import {debounceTime, EMPTY, switchMap, tap} from "rxjs";
import {takeUntilDestroyed} from "@angular/core/rxjs-interop";
import {ProgressSpinnerModule} from "primeng/progressspinner";

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
    TeacherItemComponent,
    ProgressSpinnerModule
  ],
  templateUrl: './home-page.component.html',
  styleUrl: './home-page.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class HomePageComponent implements OnInit {
  private readonly scheduleService = inject(ScheduleService);
  protected readonly teachers$ = this.scheduleService.teachers$;

  protected readonly lastNameControl = new FormControl<string>('');
  private readonly destroyRef = inject(DestroyRef);
  private readonly changeDetectorRef = inject(ChangeDetectorRef);

  protected loading: boolean = false;

  ngOnInit() {
    this.lastNameControl.valueChanges.pipe(
      debounceTime(500),
      // tap(() => this.onLastNameChanged()),
      tap(() => {
        this.loading = true;
        this.changeDetectorRef.detectChanges();
      }),
      switchMap(value => {
        if (value)
          return this.scheduleService.loadTeachers(value)
        return EMPTY;
      }),
      tap(() => {
        this.loading = false;
        this.changeDetectorRef.detectChanges();
      }),
      takeUntilDestroyed(this.destroyRef),
    ).subscribe()
  }
}

import {inject, Injectable} from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Teacher} from "./models/teacher";
import {
  BehaviorSubject, catchError,
  distinctUntilChanged,
  EMPTY,
  map,
  merge,
  Observable,
  of,
  shareReplay,
  switchMap,
  tap
} from "rxjs";
import {PairsResponse} from "./models/pairs-response";
import {Pair} from "./models/pair";

@Injectable({
  providedIn: 'root'
})
export class ScheduleService {

  private readonly http = inject(HttpClient);

  private readonly currentTeacher$$ = new BehaviorSubject<string | null>(null);
  readonly currentTeacher$ = this.currentTeacher$$.pipe(
    distinctUntilChanged(),
    shareReplay(1),
  );

  private readonly pairs$$ = new BehaviorSubject<Pair[]>([]);
  public readonly pairs$: Observable<Pair[]> = merge(
    this.pairs$$.pipe(
      distinctUntilChanged(),
      shareReplay(1),
    ),
    this.currentTeacher$.pipe(
      tap(console.log),
      tap(() => console.log("12345678")),
      switchMap(teacher => {
        if (teacher)
          return this.loadPairs(teacher).pipe(
            catchError(err => {
              console.error(err);
              return of([]);
            }),
          );
        return of([]);
      }),
      switchMap(() => EMPTY),
    ),
  ).pipe(
    tap(console.log),
  );

  loadTeachers() {
    return this.http.get<Teacher[]>("https://bmstuschedule-aa498-default-rtdb.europe-west1.firebasedatabase.app/teachers.json").pipe(
      map((teachers: Teacher[]) => {
          teachers = teachers.map((teacher: Teacher) => {
            teacher.fullName = `${teacher.lastName} ${teacher.firstName} ${teacher.middleName}`;
            return teacher;
          });
          teachers.sort((a: Teacher, b: Teacher) => (a.fullName ?? '') < b.firstName ? -1 : 1);
          return teachers;
        }
      )
    );
  }

  loadPairs(id: string) {
    return this.http.get<PairsResponse>(`/api/v1/schedules/teacher/${id}`).pipe(
      tap(pairs => this.pairs$$.next(pairs.data.schedule))
    );
  }

  setTeacher(teacher: string | null) {
    this.currentTeacher$$.next(teacher);
  }
}

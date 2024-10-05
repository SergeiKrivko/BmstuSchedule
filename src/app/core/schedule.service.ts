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

  private readonly currentTeacher$$ = new BehaviorSubject<Teacher | null>(null);
  readonly currentTeacher$ = this.currentTeacher$$.pipe(
    distinctUntilChanged(),
    shareReplay(1),
  );

  private readonly teachers$$ = new BehaviorSubject<Teacher[]>([]);
  readonly teachers$ = this.teachers$$.pipe(
    distinctUntilChanged(),
    shareReplay(1),
  )

  private readonly pairs$$ = new BehaviorSubject<Pair[]>([]);
  public readonly pairs$: Observable<Pair[]> = merge(
    this.pairs$$.pipe(
      distinctUntilChanged(),
      shareReplay(1),
    ),
    this.currentTeacher$.pipe(
      switchMap(teacher => {
        if (teacher)
          return this.loadPairs(teacher.id).pipe(
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

  loadTeachers(lastName: string) {
    console.log(`Loading teachers: ${lastName}`);
    return this.http.get<any>(`https://bmstuschedule-aa498-default-rtdb.europe-west1.firebasedatabase.app/teachers.json?orderBy="lastName"&startAt="${lastName}"&endAt="${lastName}яяя"`).pipe(
      map((teachers: any) => {
          let lst = Object.values(teachers).map((teacher: any) => {
            teacher.fullName = `${teacher.lastName} ${teacher.firstName} ${teacher.middleName}`;
            return teacher as Teacher;
          });
          lst.sort((a: Teacher, b: Teacher) => (a.fullName ?? '') < b.firstName ? -1 : 1);
          return lst;
        }
      ),
      tap(teachers => this.teachers$$.next(teachers)),
    );
  }

  loadPairs(id: string) {
    return this.http.get<PairsResponse>(`/api/v1/schedules/teacher/${id}`).pipe(
      tap(pairs => this.pairs$$.next(pairs.data.schedule))
    );
  }

  setTeacher(teacher: Teacher | null) {
    this.currentTeacher$$.next(teacher);
  }
}

import {ChangeDetectionStrategy, Component, Input} from '@angular/core';
import {Teacher} from "../../core/models/teacher";
import {CardModule} from "primeng/card";
import {Pair} from "../../core/models/pair";
import {NgIf} from "@angular/common";

@Component({
  selector: 'app-pair-item',
  standalone: true,
  imports: [
    CardModule,
    NgIf
  ],
  templateUrl: './pair-item.component.html',
  styleUrl: './pair-item.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class PairItemComponent {
  @Input() pair: Pair | undefined;
  @Input() teacher: Teacher | undefined;

  getDay(day: number): string | undefined {
    return ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье'][day];
  }
}

export interface Audience {
  uuid: string;
  name: string;
}

interface Discipline {
  abbr: string;
  actType: string;
  fullName: string;
  shortName: string;
}

export interface Pair {
  day: number;
  time: number;
  week: 'all' | 'ch' | 'zn';
  startTime: string;
  endTime: string;
  stream: string;
  audiences: Audience[];
  discipline: Discipline;
}

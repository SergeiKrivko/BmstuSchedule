import {Pair} from "./pair";

export interface PairsResponse {
  data: {
    uuid: string;
    time: string;
    schedule: Pair[];
  }
}

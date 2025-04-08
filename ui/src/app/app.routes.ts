import { Routes } from '@angular/router';
import {PairsPageComponent} from "./pages/pairs-page/pairs-page.component";
import {HomePageComponent} from "./pages/home-page/home-page.component";

export const routes: Routes = [
  {path: '', pathMatch: 'full', redirectTo: 'home'},
  {path: 'home', component: HomePageComponent},
  {path: 'pairs', component: PairsPageComponent},
];

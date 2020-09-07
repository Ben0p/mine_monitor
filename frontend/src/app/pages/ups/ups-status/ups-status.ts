/* Defines the product entity */
export interface Ups {
  id: object;
  batt_icon: string;
  batt_remaining: number;
  batt_status: string;
  kw_out: number;
  load_icon: string;
  load_percent: number;
  load_status: string;
  phases: [];
  status: [];
  temp: number;
  temp_icon: string;
  temp_status: string;
  unix: number;
}

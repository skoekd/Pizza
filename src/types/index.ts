export type TempUnit = 'C' | 'F';
export type YeastType = 'fresh' | 'idy' | 'ady';
export type MixerType = 'hand' | 'fork' | 'spiral' | 'planetary' | 'planetary_long';
export type OvenType = 'wood' | 'gas_pizza' | 'home_steel' | 'home_no_steel';
export type Timeline = number;
export type BigaPct = 20 | 30 | 50 | 70 | 100;
export type PuntataType = number; // hours
export type AprettoType = number; // hours

export interface Flour {
  id: string;
  name: string;
  w: number;
  pl: number;
  protein: number;
  fn: number;
  stability: number;
  type: '00' | '0' | '1' | '2' | 'whole';
  notes: string;
  canUseInBiga: boolean;
  canUseInRefresh: boolean;
}

export interface FlourEntry {
  flourId: string;
  customFlour?: Flour;
  percentage: number; // 0-100, must sum to 100
}

export interface UserInputs {
  // Environment
  tempUnit: TempUnit;
  ambientTemp: number;
  flourTemp: number;
  fridgeTemp: number;

  // Process
  numPizzas: number;
  ballWeight: number;
  bigaPct: number;
  bigaHydration: number;
  totalHydration: number;
  timeline: Timeline;
  puntata: PuntataType;
  appretto: AprettoType;

  // Flour
  flourEntries: FlourEntry[];

  // Yeast
  yeastType: YeastType;
  bigaYeastOverrideEnabled: boolean;
  bigaYeastOverridePct: number;
  refreshYeastOverrideEnabled: boolean;
  refreshYeastOverridePct: number;

  // Additions
  saltPct: number;
  oilEnabled: boolean;
  oilPct: number;
  maltEnabled: boolean;
  maltPct: number;

  // Equipment
  mixerType: MixerType;

  // Baking
  ovenType: OvenType;
  floorTemp: number;
  domeTemp: number;
}

export interface BlendStats {
  w: number;
  pl: number;
  fn: number;
  stability: number;
  maxHydration: number;
}

export interface Weights {
  totalDough: number;
  totalFlour: number;
  bigaFlour: number;
  refreshFlour: number;
  totalWater: number;
  bigaWater: number;
  refreshWater: number;
  bassinage: number;
  mainRefreshWater: number;
  salt: number;
  oil: number;
  malt: number;
  bigaYeast: number;
  refreshYeast: number;
}

export interface Temperatures {
  bigaWater: number;
  finalDoughWater: number;
  frictionFactor: number;
  targetBigaExit: number;
  targetFDT: number;
  bigaYeastPct: number;
  refreshYeastPct: number;
  useIceForBiga: boolean;
  bigaIceFraction: number;
}

export type WarningSeverity = 'error' | 'warning' | 'note';
export interface Warning {
  id: string;
  severity: WarningSeverity;
  title: string;
  message: string;
}

export interface ScheduleStage {
  label: string;
  offset: string;
  action: string;
  temp: string;
  duration: string;
  lookFor: string;
}

export interface RecipeResult {
  inputs: UserInputs;
  blend: BlendStats;
  weights: Weights;
  temps: Temperatures;
  warnings: Warning[];
  schedule: ScheduleStage[];
  discDiameter: string;
  framework: string;
}

export interface BakeLogEntry {
  id: string;
  date: string;
  protocolNumber: string;
  method: string;
  fermentationTime: string;
  flours: string;
  yeastAmountType: string;
  hydration: number;
  salt: number;
  goal: string;
  roomTempMix: number;
  flourTempMix: number;
  waterTempCalc: number;
  waterTempActual: number;
  prefermentTemp: number;
  fdt: number;
  mixingMinutes: number;
  bulkRoomHours: number;
  bulkFridgeHours: number;
  ballRoomHours: number;
  ballFridgeHours: number;
  ballWeightUsed: number;
  finalProofTime: number;
  finalProofTemp: number;
  ovenType: string;
  bakingTemp: number;
  bakingMinutes: number;
  specialNotes: string;
  scoreCornicione: number;
  scoreCrumb: number;
  scoreFlavor: number;
  scoreHandling: number;
  scoreOvenSpring: number;
  scoreOverall: number;
  nextNotes: string;
}

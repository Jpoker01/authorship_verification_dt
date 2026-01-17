export type PredictionResult = {
    probability_same_author: number;
    model_version?: string;
    warnings?: string[];
}

import { API_BASE_URL } from './config';

export interface PredictionRequest {
  text1: string;
  text2: string;
}

export interface PredictionResponse {
  same_author_probability: number;
}

export async function checkHealth(): Promise<boolean> {
  try {
    const response = await fetch(`${API_BASE_URL}/health`);
    return response.ok;
  } catch {
    return false;
  }
}
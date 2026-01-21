/**
 * API service for communicating with the FastAPI backend
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export interface PredictionRequest {
  text1: string;
  text2: string;
}

export interface PredictionResponse {
  same_author_probability: number;
}

export class ApiError extends Error {
  statusCode?: number;
  details?: unknown;

  constructor(
    message: string,
    statusCode?: number,
    details?: unknown
  ) {
    super(message);
    this.name = 'ApiError';
    this.statusCode = statusCode;
    this.details = details;
  }
}

/**
 * Predicts whether two texts are written by the same author
 */
export async function predictAuthorship(
  text1: string,
  text2: string
): Promise<PredictionResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}/predict/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        text1,
        text2,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new ApiError(
        errorData.detail || `API request failed with status ${response.status}`,
        response.status,
        errorData
      );
    }

    const data: PredictionResponse = await response.json();
    return data;
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }
    
    // Network or other errors
    throw new ApiError(
      'Failed to connect to the API. Please ensure the backend is running.',
      undefined,
      error
    );
  }
}

/**
 * Check if the API is healthy
 */
export async function checkHealth(): Promise<boolean> {
  try {
    const response = await fetch(`${API_BASE_URL}/health`);
    return response.ok;
  } catch {
    return false;
  }
}

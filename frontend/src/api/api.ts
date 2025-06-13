import axios from 'axios';

// API client function to send a question to the backend /answer endpoint
// and receive the AI-generated answer along with source document excerpts.

type Source = {
  content: string;
  filename: string;
};

export type AnswerResponse = {
  answer: string;
  sources: Source[];
};

// const API_BASE_URL = 'http://localhost:8001';
const API_BASE_URL = 'https://ai-poswered-document-qa-app.onrender.com';

export const getAnswer = async (question: string): Promise<AnswerResponse> => {
  const response = await axios.get(`${API_BASE_URL}/answer`, {
    params: { question },
  });
  return response.data as AnswerResponse;
};
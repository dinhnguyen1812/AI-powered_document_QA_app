import axios from 'axios';

// export interface AnswerResponse {
//   answer: string;
//   sources: { content: string }[];
// }

type Source = {
  content: string;
  filename: string;
};

export type AnswerResponse = {
  answer: string;
  sources: Source[];
};

const API_BASE_URL = 'http://localhost:8001';

export const getAnswer = async (question: string): Promise<AnswerResponse> => {
  const response = await axios.get(`${API_BASE_URL}/answer`, {
    params: { question },
  });
  return response.data as AnswerResponse;
};
import React, { useState } from 'react';
import { getAnswer } from '../api/api';
import type { AnswerResponse } from '../api/api';
import { Button, Form, Spinner, Alert } from 'react-bootstrap';

const AnswerBox: React.FC = () => {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [sources, setSources] = useState<AnswerResponse['sources']>([]);
  const [loading, setLoading] = useState(false);

  const handleAsk = async () => {
    setLoading(true);
    try {
      const result = await getAnswer(question) as AnswerResponse;
      setAnswer(result.answer);
      setSources(result.sources);
    } catch (err) {
      setAnswer('エラーが発生しました。もう一度お試しください。');
      setSources([]);
    }
    setLoading(false);
  };

  return (
    <div>
      <Form.Group controlId="question">
        <Form.Label>質問を入力してください：</Form.Label>
        <Form.Control
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="例：このシステムはどんな目的で使われますか？"
        />
      </Form.Group>
      <Button variant="primary" className="mt-2" onClick={handleAsk} disabled={loading}>
        {loading ? <Spinner size="sm" animation="border" /> : '質問する'}
      </Button>

      {answer && (
        <Alert variant="success" className="mt-3">
          <h5>回答：</h5>
          <p>{answer}</p>
        </Alert>
      )}

      {sources.length > 0 && (
        <div className="mt-3">
          <h6>参照された文書抜粋：</h6>
          {Object.entries(
            sources.reduce((acc, src) => {
              const file = src.filename ?? '不明なファイル';
              if (!acc[file]) acc[file] = [];
              acc[file].push(src.content);
              return acc;
            }, {} as Record<string, string[]>)
          ).map(([filename, contents], idx) => (
            <div key={idx} className="mb-3">
              <h6 className="fw-bold">{filename}</h6>
              {contents.map((text, i) => (
                <Alert key={i} variant="light" className="mb-1">
                  <small>{text}</small>
                </Alert>
              ))}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default AnswerBox;

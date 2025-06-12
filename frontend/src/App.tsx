import 'bootstrap/dist/css/bootstrap.min.css';
import { Container } from 'react-bootstrap';
import AnswerBox from './components/AnswerBox';

function App() {
  return (
    <Container className="p-4">
      <h2 className="mb-4">ドキュメントQAアシスタント</h2>
      <AnswerBox />
    </Container>
  );
}

export default App;

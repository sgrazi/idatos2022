import './App.css';
import Main from './Main.js'

function App() {
  return (
    <div className="App">
      <header className="App-header">
       Disponibilidad en streaming
      </header>
      <div style={{
        margin: "auto",
        paddingRight: 80,
        paddingLeft: 80,
        height: "100%"
      }}>
        <Main/>
      </div>
    </div>
  );
}

export default App;

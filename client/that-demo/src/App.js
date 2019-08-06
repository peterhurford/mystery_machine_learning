import React, { useState } from "react";
import axios from "axios";
import * as url from "./mystery_machine.png";
import Shaggy from "./scooby-doo-characters/Shaggy_Rogers.png";
import Fred from "./scooby-doo-characters/Fred_Jones.png";
import Daphne from "./scooby-doo-characters/Daphne_Blake.png";
import Velma from "./scooby-doo-characters/Velma_Dinkley.png";
import Scooby from "./scooby-doo-characters/Scooby_Doo.png";
import "./App.css";

const images = {
  "Shaggy Rogers": Shaggy,
  "Velma Dinkley": Velma,
  "Fred Jones": Fred,
  "Daphne Blake": Daphne,
  "Scooby-Doo": Scooby
};

function App() {
  const [data, setData] = useState();
  const [textToPredict, setTextToPredict] = useState();

  function predictWhoSaidIt() {
    axios
      .post("https://mystery-machine-learning-api.herokuapp.com/predict", {
        text: textToPredict
      })
      .then(res => {
        setData(res.data);
        console.log(res);
      });
  }

  return (
    <div className="App">
      <header className="App-header">
        <div className="header">
          Mystery Machine Learning!
          <img src={url} className="App-logo" alt="logo" />
        </div>
        <div>Who said : "{textToPredict}" ?</div>
        <textarea onChange={e => setTextToPredict(e.target.value)} />

        <button onClick={predictWhoSaidIt}>Who said this?</button>
        {data && data.prediction && (
          <div className="winner">
            It was probably...
            <img
              className="winner-image"
              src={images[data.prediction]}
              alt={"winner"}
            />
            {data.prediction}!
          </div>
        )}

        <div className="data-table">
          <table>
            <tbody>
              {data &&
                Object.keys(data.probabilities)
                  .map(person => {
                    return {
                      name: person,
                      score: (data.probabilities[person] * 100).toFixed(2)
                    };
                  })
                  .sort((a, b) => b.score - a.score)
                  .map((person, i) => (
                    <tr key={`${person.name}-${i}`}>
                      <td className="person-name">{person.name}</td>
                      <td className="person-score">{person.score} %</td>
                    </tr>
                  ))}
            </tbody>
          </table>
        </div>
      </header>
    </div>
  );
}

export default App;
